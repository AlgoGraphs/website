import shutil

from flask import Flask, render_template, request, redirect, url_for, session, g, abort, send_file, jsonify, \
    make_response, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from backend import fullBack
from werkzeug import SharedDataMiddleware
from natsort import natsorted
import gunicorn
import natsort
import psycopg2
import uuid
import os
import fnmatch

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://qnohmjuedcpcyc' \
                                        ':584b459ad0c7fe32b2b9b191aa78604a25bbc7dbc8d59623202b3e3a68c5d261@ec2-34-240' \
                                        '-75-196.eu-west-1.compute.amazonaws.com:5432/d29t6n6itg14fl'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.wsgi_app = SharedDataMiddleware(
    app.wsgi_app,
    {'/static': os.path.join(os.path.dirname(__file__), 'static')},
    cache=False)
db = SQLAlchemy(app)

connection = psycopg2.connect(user="qnohmjuedcpcyc",
                              password="584b459ad0c7fe32b2b9b191aa78604a25bbc7dbc8d59623202b3e3a68c5d261",
                              host="ec2-34-240-75-196.eu-west-1.compute.amazonaws.com",
                              port="5432",
                              database="d29t6n6itg14fl")


def write_blob(part_id, path_to_file):
    """"" inserting a BLOB into image table """""
    try:

        # read image data
        image_chosen = open(path_to_file, 'rb').read()

        # Connect to database configuration (can be changed up according to needs)
        conn = connection

        # create new cursor object
        cur = conn.cursor()

        # INSERT statement into postgresql images database
        cur.execute("INSERT INTO images(id,file_extension,image) " +
                    "VALUES(%s,%s,%s)",
                    (str(part_id), "png", psycopg2.Binary(image_chosen)))

        # Commit the changes to the database (putting BLOB image data in images postgresql database)
        conn.commit()

        # close communication after process is completed
        # cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    #finally:
        #if conn is not None:
            #conn.close()


# Check if ID exist in data database

def checkInputDetails_Data(ID):
    global connection
    global num_nodes
    global value
    try:
        print("Using Python variable in PostgreSQL select Query")
        cursor = connection.cursor()
        postgreSQL_select_Query = " SELECT EXISTS(SELECT 1 FROM data WHERE id = %s); "

        cursor.execute(postgreSQL_select_Query, (ID,))
        value = cursor.fetchall()
        print(value)

    except (Exception, psycopg2.Error) as error:
        print("Error fetching data from PostgreSQL table", error)

    return value


# Check if input exist in the image database

def checkInputDetails(ID):
    global connection
    global num_nodes
    global value
    try:
        print("Using Python variable in PostgreSQL select Query")
        cursor = connection.cursor()
        postgreSQL_select_Query = " SELECT EXISTS(SELECT 1 FROM images WHERE id = %s); "

        cursor.execute(postgreSQL_select_Query, (str(ID),))
        value = cursor.fetchall()

    except (Exception, psycopg2.Error) as error:
        print("Error fetching data from PostgreSQL table", error)

    return value


def read_blob(data_id, path_to_dir):
    """ read BLOB data from a table """
    try:
        # connect to the PostgresQL database

        # create a new cursor object
        cur = connection.cursor()
        # execute the SELECT statement
        cur.execute(""" SELECT id, file_extension, image
                        FROM images
                        WHERE images.id = %s """,
                    (data_id,))

        blob = cur.fetchone()
        open(path_to_dir + str(blob[0]) + '.' + str(blob[1]), 'w+b').write(blob[2])
        # close the communication with the PostgresQL database
        # cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    #finally:
        #if connection is not None:
            #connection.close()


# def choose

def getDetails(ID):
    global bin_data
    try:
        print("Using Python variable in PostgreSQL select Query")
        cursor = connection.cursor()
        postgreSQL_select_Query = " select * from images WHERE id = %s "

        cursor.execute(postgreSQL_select_Query, (ID,))
        data_records = cursor.fetchall()
        print(data_records)
        if not data_records:
            return 0
        for row in data_records:
            print("Id = ", row[0], )
            print("Binary Data = ", row[2])
            bin_data = row[2]

    except (Exception, psycopg2.Error) as error:
        print("Error fetching data from PostgreSQL table", error)

    return bin_data


class Data(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    type = db.Column(db.String(10))
    nodes = db.Column(db.Integer)
    source = db.Column(db.Integer)
    destination = db.Column(db.Integer)
    graph = db.Column(db.String(20))
    algorithm = db.Column(db.String(20))

    def __init__(self, id, type, nodes, source, destination, graph, algorithm):
        self.id = id
        self.type = type
        self.nodes = nodes
        self.source = source
        self.destination = destination
        self.graph = graph
        self.algorithm = algorithm

    def __repr__(self):
        return '<id: {self.id}>'  # f'<id: {self.id}>'


class Images(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    file_extension = db.Column(db.String(1020))
    image = db.Column(db.LargeBinary)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == "POST":
        req = request.get_json(force=True)
        print(req)
        print(req["type"])

        res = make_response(jsonify({"message": "JSON received"}), 200)

        # Cross referencing with data() db to see if input is similar

        nodes_be = int(req["nodes"])
        graph_be = req["graph"]
        algorithm_be = req["algorithm"]
        source_be = int(req["source"])
        destination_be = int(req["destination"])
        user_be = req["user"]
        # print(user_be)

        uuidone = uuid.uuid4()
        string_unique = str(uuidone)
        new_folder_path = os.path.join("static/graph_images/", string_unique)
        os.makedirs(new_folder_path)
        print(new_folder_path)
        print("DIRECTORY for user '% s' CREATED" % string_unique)

        # Deleting old images in file

        images_path = os.listdir(new_folder_path)
        print(images_path)

        custom_string = req["type"] + str(nodes_be) + str(graph_be) + str(source_be) + str(
            destination_be) + algorithm_be

        exist_image = checkInputDetails(custom_string + "1")

        if exist_image != [(False,)]:
            itera = 0
            while True:
                image_file_name = custom_string + str(itera)
                details = getDetails(image_file_name)
                if details == 0:
                    break
                else:
                    read_blob(image_file_name, "static/graph_images/" + string_unique + '/')
                    itera += 1

        else:

            if algorithm_be == 'None' or algorithm_be == 'Temporal':
                fullBack.select_graph(graph_be, nodes_be, new_folder_path, source_be, destination_be)
            else:
                n: int
                l, m, n = fullBack.select_graph(graph_be, nodes_be, new_folder_path, source_be, destination_be)
                fullBack.select_alg(algorithm_be, l, m, n, new_folder_path, source_be, destination_be)

        if len(os.listdir(new_folder_path)) == 0:
            return res
        else:
            images_path = os.listdir(new_folder_path)
            if algorithm_be != 'None':
                for filename in images_path:
                    if fnmatch.fnmatch(filename, '*cycle.png'):
                        os.remove(new_folder_path + '/' + filename)
                    elif fnmatch.fnmatch(filename, '*star.png'):
                        os.remove(new_folder_path + '/' + filename)
                    elif fnmatch.fnmatch(filename, '*tree.png'):
                        os.remove(new_folder_path + '/' + filename)
                    elif fnmatch.fnmatch(filename, '*path.png'):
                        os.remove(new_folder_path + '/' + filename)
                    elif fnmatch.fnmatch(filename, '*complete.png'):
                        os.remove(new_folder_path + '/' + filename)
                    elif fnmatch.fnmatch(filename, '*bipartite.png'):
                        os.remove(new_folder_path + '/' + filename)
                    elif fnmatch.fnmatch(filename, '*hypercube.png'):
                        os.remove(new_folder_path + '/' + filename)
                    elif fnmatch.fnmatch(filename, '*petersen.png'):
                        os.remove(new_folder_path + '/' + filename)
                    elif fnmatch.fnmatch(filename, '*custom.png'):
                        os.remove(new_folder_path + '/' + filename)
            exist_in_data = checkInputDetails(str(uuidone))
            if exist_in_data == [(False,)] and type(graph_be) != list:
                data = Data(id=uuidone, type=req["type"], nodes=req["nodes"], graph=req["graph"],
                            source=req["source"], destination=req["destination"], algorithm=req["algorithm"])
                db.session.add(data)
                db.session.commit()
            new_image_path = natsorted(os.listdir(new_folder_path))
            print(new_folder_path)
            print(new_image_path)
            n = 0
            for i in new_image_path:
                print(checkInputDetails(i))
                if type(graph_be) != list and checkInputDetails(i) != [(False,)]:
                    write_blob(custom_string + str(n), new_folder_path + '/' + i)
                    n += 1

            json_path = make_response(jsonify({"images": new_image_path, "user_id": string_unique}), 200)

            return json_path


@app.route('/graph_images/<user_id>/<filename>', methods=['GET', 'POST'])
def return_images(user_id, filename):
    if request.method == "GET":
        try:
            user_path = '../static/graph_images/' + user_id
            return send_from_directory(user_path, filename=filename, as_attachment=True)
        except FileNotFoundError:
            abort(404)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
