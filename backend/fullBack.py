from itertools import combinations

import matplotlib
import networkx as nx

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import random
import os

"""
Graphs
1. cycle
2. star
3. tree
4. path
5. complete
6. bipartite
7. hypercubes
8. petersen
9. custom
10. Temporal

Algorithms
1. bfs
2. dfs
3. dijkstra
4. cycle det
5. foremost journey
"""

my_path = os.path.abspath(__file__)


def cycle(numNodes, exact_path):
    plt.clf()

    G = nx.cycle_graph(numNodes)

    # gathers all the nodes and edges created and draws them on a networkx canvas
    # with the labels starting from 1 to numNodes and all the nodes coloured
    # white
    # G.add_nodes_from(G.nodes(), colour='never coloured')
    positions = nx.spring_layout(G)
    nx.draw(G, pos=positions, node_color='white')
    nx.draw_networkx_labels(G, pos=positions, labels={n: n + 1 for n in G})

    # matplotlib function that saves the graph creates as a png
    if not os.path.exists('static/graph_images'):
        os.makedirs('static/graph_images')
    plt.savefig(os.path.join(exact_path, (str(numNodes) + "cycle")), dpi=300)

    # convert graph created into a list of lists, where each index represents
    # the node, and the list at that index contains the nodes it is connected to
    # by an edge
    adjlist = []
    x = nx.convert.to_dict_of_lists(G)
    for i in x.values():
        adjlist.append(i)

    # adjlist is returned in the case of the user wanting to see a search alg
    # implemented on the graph, the same graph can easily be used, the graph
    # itself is returned as well as thet positions of the nodes to aid with
    # consistency
    return adjlist, G, positions


def star(numNodes, exact_path):
    plt.clf()
    G = nx.Graph()
    if numNodes == 1:
        G.add_node(0)

    elif numNodes > 1:
        G.add_node(0)
        for i in range(1, numNodes):
            G.add_node(i)
            G.add_edge(0, i)

    G.add_nodes_from(G.nodes(), colour='never coloured')
    positions = nx.spring_layout(G)
    nx.draw(G, pos=positions, node_color='white')
    nx.draw_networkx_labels(G, pos=positions, labels={n: n + 1 for n in G})
    plt.savefig(os.path.join(exact_path, (str(numNodes) + "star")), dpi=300)
    adjlist = []
    x = nx.convert.to_dict_of_lists(G)
    for i in x.values():
        adjlist.append(i)
    return adjlist, G, positions


def tree(numNodes, exact_path):
    for trying in range(10):
        plt.clf()
        G = nx.Graph()
        if numNodes == 1:
            G.add_node(0)
            break
        elif numNodes > 1:
            G.add_node(0)
            for i in range(1, numNodes):
                G.add_node(i)
                prob = random.uniform(0, 1)
                print(prob)
                if prob > 0.5:
                    randy = random.randint(0, i - 1)
                    G.add_edge(randy, i)
                else:
                    G.add_edge(i, i - 1)
        if numNodes <= 3:
            break
        no3 = False
        save2 = []
        deg3 = []
        ones = []
        for i in G.nodes():  # range(0,numNodes):
            x = [n for n in G.neighbors(i)]
            print(x, 'nodes', i)
            if len(x) == 3:
                no3 = True
                deg3.append(i)
                break
            if len(x) == 2:
                save2.append(i)
            if len(x) == 1:
                ones.append(i)
        if no3 == True:
            break

    print(G.edges())
    G.add_nodes_from(G.nodes(), colour='never coloured')
    positions = nx.spring_layout(G)
    nx.draw(G, pos=positions, node_color='white')
    nx.draw_networkx_labels(G, pos=positions, labels={n: n + 1 for n in G})
    plt.savefig(os.path.join(exact_path, (str(numNodes) + "tree")), dpi=300)
    adjlist = []
    xx = nx.convert.to_dict_of_lists(G)
    for i in xx.values():
        adjlist.append(i)
    return adjlist, G, positions


def path(numNodes, exact_path):
    plt.clf()
    G = nx.Graph()
    if numNodes == 1:
        G.add_node(0)
    elif numNodes > 1:
        G.add_node(0)
        for i in range(0, numNodes - 1):
            G.add_node(i)
            G.add_edge(i, i + 1)

    G.add_nodes_from(G.nodes(), colour='never coloured')
    positions = nx.spring_layout(G)
    nx.draw(G, pos=positions, node_color='white')
    nx.draw_networkx_labels(G, pos=positions, labels={n: n + 1 for n in G})
    plt.savefig(os.path.join(exact_path, (str(numNodes) + "path")), dpi=300)
    adjlist = []
    x = nx.convert.to_dict_of_lists(G)
    for i in x.values():
        adjlist.append(i)
    return adjlist, G, positions


def complete(numNodes, exact_path):
    plt.clf()
    G = nx.Graph()
    if numNodes == 1:
        G.add_node(0)
    elif numNodes > 1:
        G.add_node(0)
        for i in range(1, numNodes):
            G.add_node(i)
            for j in range(0, i):
                G.add_edge(j, i)

    G.add_nodes_from(G.nodes(), colour='never coloured')
    positions = nx.spring_layout(G)
    nx.draw(G, pos=positions, node_color='white')
    nx.draw_networkx_labels(G, pos=positions, labels={n: n + 1 for n in G})
    plt.savefig(os.path.join(exact_path, (str(numNodes) + "complete")), dpi=300)
    adjlist = []
    x = nx.convert.to_dict_of_lists(G)
    for i in x.values():
        adjlist.append(i)
    return adjlist, G, positions


def bipartite(numNodes, exact_path):
    plt.clf()
    odds = []
    evens = []
    colours = []
    B = nx.Graph()
    for i in range(0, numNodes):
        if ((i % 2) == 0):
            evens.append(i)
            B.add_node(i)
            colours.append('red')
        else:
            odds.append(i)
            B.add_node(i)
            colours.append('blue')
    for i in range(0, numNodes - 1):
        B.add_edge(i, i + 1)

    # just adds a few more edges on
    if numNodes > 3:
        for j in range(0, numNodes - 1):
            x = random.uniform(0, 1)
            if x > 0.6:
                y = random.randint(0, len(evens) - 2)
                z = random.randint(0, len(odds) - 2)
                if z != y:
                    B.add_edge(odds[z], evens[y])
    lhs = nx.bipartite.sets(B)[0]
    positions = nx.bipartite_layout(B, lhs)
    nx.draw_networkx_labels(B, pos=positions, labels={n: n + 1 for n in B})
    nx.draw(B, pos=positions, node_color=colours)
    plt.savefig(os.path.join(exact_path, (str(numNodes) + "bipartite")), dpi=300)
    adjlist = []
    x = nx.convert.to_dict_of_lists(B)
    for i in x.values():
        adjlist.append(i)
    return adjlist, B, positions


def hypercube(n, exact_path):
    plt.clf()
    if n == 1:
        x = nx.Graph()
        x.add_node(0)

    elif n == 8:
        x = nx.Graph()
        for i in range(0, n):
            x.add_node(i)
        x.add_edge(0, 1)
        x.add_edge(0, 2)
        x.add_edge(0, 3)
        x.add_edge(1, 4)
        x.add_edge(1, 5)
        x.add_edge(2, 4)
        x.add_edge(2, 6)
        x.add_edge(3, 5)
        x.add_edge(3, 6)
        x.add_edge(4, 7)
        x.add_edge(5, 7)
        x.add_edge(6, 7)

    elif n == 4:
        x = nx.Graph()
        for i in range(0, n):
            x.add_node(i)
        x.add_edge(0, 1)
        x.add_edge(1, 2)
        x.add_edge(2, 3)
        x.add_edge(0, 3)

    elif n == 2:
        x = nx.Graph()
        for i in range(0, n):
            print(i)
            x.add_node(i)
        x.add_edge(0, 1)

    positions = nx.spring_layout(x, scale=0.8)
    nx.draw(x, pos=positions, node_color='white', width=1, edge_color="black", style="solid")
    nx.draw_networkx_labels(x, pos=positions, labels={u: u + 1 for u in x})

    # fits everything in
    plt.margins(0.15)
    plt.savefig(os.path.join(exact_path, (str(n) + "hypercube")), dpi=800)
    adjlist = []
    h = nx.convert.to_dict_of_lists(x)
    for i in h.values():
        adjlist.append(i)
    return adjlist, x, positions


def petersen(exact_path):
    plt.clf()
    Graph = nx.petersen_graph()
    nx.draw_shell(Graph, nlist=[range(5, 10), range(5)], font_weight='bold', node_color='white')
    positions = nx.shell_layout(Graph, nlist=[range(5, 10), range(5)])
    nx.draw_networkx_labels(Graph, pos=positions, labels={n: n + 1 for n in Graph})
    plt.savefig(os.path.join(exact_path, "petersen"), dpi=800)
    adjlist = []
    x = nx.convert.to_dict_of_lists(Graph)
    for i in x.values():
        adjlist.append(i)
    return adjlist, Graph, positions


def custom(adj, exact_path):
    plt.clf()
    G = nx.Graph()
    for i in range(0, len(adj)):
        G.add_node(i)
    for i in range(0, len(adj)):
        for j in range(0, len(adj[i])):
            if (adj[i][j] == 1):
                G.add_edge(i, j)
    G.add_nodes_from(G.nodes(), colour='never coloured')
    positions = nx.spring_layout(G)
    nx.draw(G, pos=positions, node_color='white')
    nx.draw_networkx_labels(G, pos=positions, labels={n: n + 1 for n in G})
    plt.savefig(os.path.join(exact_path, (str(len(adj)) + "custom")), dpi=300)
    adjlist = []
    x = nx.convert.to_dict_of_lists(G)
    for i in x.values():
        adjlist.append(i)
    return adjlist, G, positions


def cycleDetection(adjlist, G, positions, direc):
    plt.clf()
    x = []
    try:
        x = list(nx.find_cycle(G, orientation="original"))
    except:
        pass

    G.add_nodes_from(G.nodes(), colour='never coloured')

    for e in G.edges():
        G[e[0]][e[1]]['color'] = 'black'
        for i in x:
            if (((e[0] == i[0]) and (e[1] == i[1])) or ((e[1] == i[0]) and (e[0] == i[1]))):
                G[e[0]][e[1]]['color'] = 'red'

    node_colour_list = ['white'] * len(adjlist)
    order = 0
    edge_colour_list = [G[e[0]][e[1]]['color'] for e in G.edges()]
    nx.draw(G, pos=positions, node_color=node_colour_list, edge_color=edge_colour_list)
    # nx.draw_networkx_labels(G, pos=positions)
    try:
        nx.draw_networkx_labels(G, pos=positions, labels={n: n + 1 for n in G})
    except:
        nx.draw_networkx_labels(G, pos=positions)
    plt.savefig(os.path.join(direc, (str(order) + "cycledetection.png")), dpi=300)
    # colour nodes that are in the cycle
    order += 1
    for e in G.nodes():
        coloured = False
        for i in x:
            if ((e == i[0])):
                node_colour_list[e] = 'pink'
                coloured = True
                break
        if (coloured == False):
            node_colour_list[e] = 'white'
        else:
            # positions = nx.spring_layout(G)
            edge_colour_list = [G[e[0]][e[1]]['color'] for e in G.edges()]
            nx.draw(G, pos=positions, node_color=node_colour_list, edge_color=edge_colour_list)
            # nx.draw_networkx_labels(G, pos=positions)
            try:
                nx.draw_networkx_labels(G, pos=positions, labels={n: n + 1 for n in G})
            except:
                nx.draw_networkx_labels(G, pos=positions)
            plt.savefig(os.path.join(direc, (str(order) + "cycledetection.png")), dpi=300)
            order += 1


def bfs(adjlist, G, positions, direc):
    # visited list- check if bfs already seen
    visited = [0] * len(adjlist)
    queue = []
    tour = [0]
    r = 0
    queue.extend(adjlist[0])  # =adjlist[0]

    # keeps track of which index of colourList we are allowed to colour the node in
    colourCount = 0
    colourList = ['#FFB6C1', '#836FFF', '#7FFFD4', '#7D9EC0', '#CAE1FF', '#458B00', '#FFFF00', '#FFA07A', '#F5DEB3',
                  '#FF3030', '#CDC9C9', '#EE7AE9', '#A0522D', '#00EE00', '#FF9912', '#E3CF57', '#B3EE3A', '#FF3E96',
                  '#00F5FF', '#BF3EFF', '#4876FF']
    # colourList=['orange','blue','yellow','red','purple','cyan','pink','green','grey','indigo']

    # initialise an all white list for the nodes that have not yet been coloured
    # will get coloured as we go on
    vColour = ['#ffffff'] * len(adjlist)

    # draws first stage and saves (non coloured graph)
    nx.draw(G, pos=positions, node_color=vColour)
    # nx.draw_networkx_labels(G, pos=positions)
    order = 0
    plt.savefig(os.path.join(direc, (str(order) + "bfs.png")), dpi=300)

    # adds orange to first node 0 (which is node 1 on networkx graph)
    vColour[0] = colourList[colourCount]
    colourCount += 1

    # draws first COLOURED stage and saves
    order = 1
    nx.draw(G, pos=positions, node_color=vColour)
    # nx.draw_networkx_labels(G, pos=positions)
    plt.savefig(os.path.join(direc, (str(order) + "bfs.png")), dpi=300)

    order = 2
    while (len(queue) != 0):
        a = len(queue)
        secondq = []
        for i in queue:
            secondq.append(i)
        visited[r] = 1

        # r keeps track of the first node in queue
        r = queue[0]
        tour.append(r)

        # everything thats in the queue at this moment in time must have come from the same node (if not already coloured)
        # therefore can be coloured the next colour in the list initialised at the top
        # save new drawn graph at each coloured node stage
        for i in queue:
            if vColour[i] == '#ffffff':
                vColour[i] = colourList[colourCount]
                nx.draw(G, pos=positions, node_color=vColour)
                plt.savefig(os.path.join(direc, (str(order) + "bfs.png")), dpi=300)
                order += 1

        colourCount += 1
        queue.remove(r)

        # add all unvisited nodes that are adjacent to the queue to repeat
        for x in secondq:
            for i in range(0, len(adjlist[x])):  # and (x not in tour)
                if (visited[adjlist[x][i]] == 0 and (adjlist[x][i] not in queue)):
                    queue.append(adjlist[x][i])


def dfs(adjlist, G, positions, direc):
    # keeps track of which index of colourList we are allowed to colour the node in
    colourCount = 0
    colourList = ['orange', 'blue', 'yellow', 'red', 'purple', 'grey', 'pink', 'green', 'grey']

    # initialise an all white list for the nodes that have not yet been coloured
    # will get coloured as we go on
    vColour = ['#ffffff'] * len(adjlist)

    # draws first stage and saves (non coloured graph)
    nx.draw(G, pos=positions, node_color=vColour)
    # nx.draw_networkx_labels(G, pos=positions)
    order = 0
    plt.savefig(os.path.join(direc, (str(order) + "dfs.png")), dpi=300)

    # adds orange to first node 0 (which is node 1 on networkx graph)
    vColour[0] = colourList[colourCount]

    order = 1
    visited = [False] * len(adjlist)
    s = 0
    stack = []
    stack.append(s)

    while (len(stack)):
        # Pop a vertex from stack and print it 
        s = stack[-1]
        stack.pop()

        # stack may contain same vertex twice, need to print the popped item only 
        # if not visited. 
        if (not visited[s]):
            vColour[s] = colourList[colourCount]
            nx.draw(G, pos=positions, node_color=vColour)
            plt.savefig(os.path.join(direc, (str(order) + "dfs.png")), dpi=300)
            order += 1
            visited[s] = True
        # Get all adjacent vertices of the popped vertex s 
        # If a adjacent has not been visited, then push it 
        # to the stack. 
        for node in adjlist[s]:
            if (not visited[node]):
                stack.append(node)


# used for dijkstra
def backtrace(parent, start, end):
    path = [end]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()
    return path


def dijkstra(adjlist, graph, positions, source, target, direc):
    source = source - 1
    target = target - 1
    queue = []
    visited = {}
    distance = {}
    shortest_distance = {}
    parent = {}

    colours = ['white'] * len(adjlist)
    for node in range(len(graph)):
        distance[node] = None
        visited[node] = False
        parent[node] = None
        shortest_distance[node] = float("inf")

    queue.append(source)
    distance[source] = 0
    while len(queue) != 0:
        current = queue.pop(0)
        visited[current] = True
        if current == target:
            shortpath = (backtrace(parent, source, target))
        for neighbor in graph[current]:
            if visited[neighbor] == False:
                distance[neighbor] = distance[current] + 1
                if distance[neighbor] < shortest_distance[neighbor]:
                    shortest_distance[neighbor] = distance[neighbor]
                    parent[neighbor] = current
                    queue.append(neighbor)

    nx.draw(graph, pos=positions, node_color='white', width=1, style="solid")
    try:
        nx.draw_networkx_labels(graph, pos=positions, labels={n: n + 1 for n in graph})
    except:
        nx.draw_networkx_labels(graph, pos=positions)
    order = 0
    plt.savefig(os.path.join(direc, (str(order) + "dijkstra.png")), dpi=300)

    for i in shortpath:
        colours[i] = 'orange'
        order += 1
        nx.draw(graph, pos=positions, node_color=colours)
        try:
            nx.draw_networkx_labels(graph, pos=positions, labels={n: n + 1 for n in graph})
        except:
            nx.draw_networkx_labels(graph, pos=positions)
        plt.savefig(os.path.join(direc, (str(order) + "dijkstra.png")), dpi=300)

def temporal_noalg(num, max_life, src, direc):
    print(num, max_life, src)
    src = src - 1

    vertices = []
    for i in range(num):
        vertices.append(i)
    print("vertices", vertices)

    check = src - 1

    edges_not_used = list(combinations((vertices), 2))  # getting all possible combinations of length 2
    print("combinations possible", edges_not_used)
    plt.clf()  # used to clear the current figure
    G = nx.Graph()
    order = 0

    for i in range(0, num):
        G.add_node(i)

    G.add_nodes_from(G.nodes(), colour='never coloured')
    positions = nx.spring_layout(G, scale=0.2)
    nx.draw(G, pos=positions, node_color='white')
    nx.draw_networkx_labels(G, pos=positions, labels={n: n + 1 for n in G})
    plt.savefig(os.path.join(direc, (str(order) + "temporal.png")), dpi=300)
    order += 1

    main = []

    for j in range(0, max_life, src + 1):
        lst1 = []
        G.remove_edges_from(list(G.edges()))
        for k in range(0, num):
            for q in range(0, num):
                probability = random.uniform(0, 1)
                if (k != q):  # edges created with random probability
                    if (probability < (1 / (num))):  # create random edges at diff times

                        if ((k, q) in edges_not_used) or ((q, k) in edges_not_used):
                            if j == 0:
                                k = src
                            vertices_traversed = (k, q)
                            lst1.append(vertices_traversed)
                            G.add_edge(k, q)
                            if (k, q) in edges_not_used:
                                edges_not_used.remove((k, q))
                            if (q, k) in edges_not_used:
                                edges_not_used.remove((q, k))

        plt.clf()
        main.append(lst1)
        nx.draw(G, pos=positions, node_color='pink')
        nx.draw_networkx_labels(G, pos=positions, labels={n: n + 1 for n in G})
        plt.savefig(os.path.join(direc, (str(order) + "temporal.png")), dpi=300)
        order += 1


def temporal(num, max_life, src, direc):
    src = src - 1

    vertices = []
    for i in range(num):
        vertices.append(i)

    edges_not_used = list(combinations(vertices, 2))  # getting all possible combinations of length 2
    plt.clf()  # used to clear the current figure
    G = nx.Graph()
    order = 0

    for i in range(0, num):
        G.add_node(i)

    G.add_nodes_from(G.nodes(), colour='never coloured')
    positions = nx.spring_layout(G, scale=0.2)
    nx.draw(G, pos=positions, node_color='white')
    nx.draw_networkx_labels(G, pos=positions, labels={n: n + 1 for n in G})
    plt.savefig(os.path.join(direc, (str(order) + "temporal.png")), dpi=300)
    order += 1

    main = []

    for j in range(0, max_life, src + 1):
        lst1 = []
        G.remove_edges_from(list(G.edges()))
        for k in range(0, num):
            for q in range(0, num):
                probability = random.uniform(0, 1)
                if k != q:  # edges created with random probability
                    if probability < (1 / num):  # create random edges at diff times

                        if ((k, q) in edges_not_used) or ((q, k) in edges_not_used):
                            if j == 0:
                                k = src
                            vertices_traversed = (k, q)
                            lst1.append(vertices_traversed)
                            G.add_edge(k, q)
                            if (k, q) in edges_not_used:
                                edges_not_used.remove((k, q))
                            if (q, k) in edges_not_used:
                                edges_not_used.remove((q, k))

        plt.clf()
        main.append(lst1)
        nx.draw(G, pos=positions, node_color='white')
        nx.draw_networkx_labels(G, pos=positions, labels={n: n + 1 for n in G})
        plt.savefig(os.path.join(direc, (str(order) + "temporal.png")), dpi=300)
        order += 1

    # If dest and source vertex found, we apply algorithm to find shortest path

    S = []  # creating a list called 'S' of (u,v) and (v,u) edges since our graph is undirectes
    for i in range(len(main)):
        new = []
        for each in main[i]:
            a = each[0]
            b = each[1]
            one = (a, b)
            swap = (b, a)
            new.append(one)
            new.append(swap)
        S.append(new)

    null = '-'

    vertices_traversed = [src]
    parents = {}
    arrival_time = {}
    parents[src] = null
    arrival_time[src] = 0

    # Part of the algorithm
    # finding time at which edges appear and adding it to the dict arrival_time
    # setting parents of all vertices to null

    for i in range(len(S)):
        for each in S[i]:
            if each[0] not in vertices_traversed:
                vertices_traversed.append(each[0])
                arrival_time[each[0]] = i + 1
                parents[each[0]] = null
            if each[1] not in vertices_traversed:
                vertices_traversed.append(each[1])
                arrival_time[each[1]] = i + 1
                parents[each[1]] = null

    # dst here is the vertex that appears latest
    dst = vertices_traversed[-1]

    R = [src]

    for l in range(len(S)):
        for each in S[l]:
            a = each[0]
            b = each[1]
            if a in R and b not in R:  # main algorithm of foremost jounrey
                if arrival_time[a] < l + 1:
                    parents[b] = a
                    arrival_time[b] = l + 1
                    R.append(b)
            elif b in R and a not in R:  # i have also taking reverse since our graph is undirected
                if arrival_time[b] < l + 1:
                    parents[a] = b
                    arrival_time[a] = l + 1
                    R.append(a)

    traverse = []  # to add all edges in the order they will be traversed
    for i in range(max_life):
        for each in arrival_time:
            if arrival_time[each] == i:
                lst2 = (parents[each], each)
                traverse.append(lst2)

    del traverse[0]

    final = 0  # to calculage total time taken
    if len(R) != len(vertices):
        exit()

    for i in vertices:
        final += arrival_time[i]

    G.remove_edges_from(list(G.edges()))  # to label edges with time at which they appear
    for each in traverse:
        G.add_edge(each[0], each[1])
        G[each[0]][each[1]]['time'] = arrival_time[each[1]]

    labels = {}  # to label nodes, source node also labelled
    for n in G.nodes:

        if n == src:
            labels[n] = str(n + 1) + '$: SOURCE$'

        else:
            labels[n] = n + 1

    plt.clf()  # Plotting edges from the list traversed
    main.append(lst1)
    nx.draw(G, pos=positions, node_color='white')
    nx.draw_networkx_labels(G, pos=positions, labels=labels)

    b = dict(((u, v), d) for u, v, d in G.edges(data=True))
    nx.draw_networkx_edge_labels(G, pos=positions, edge_labels=b, font_color='red')
    #final = str(max_life + 1)
    #name_of_final = final + "temporal.png"
    plt.savefig(os.path.join(direc, (str(order) + "temporal.png")), dpi=300)
    #plt.savefig((name_of_final), dpi=250)

    return G.edges


def select_graph(algorithm, graphtype, nodes, new_path, s, d):
    if graphtype == "Cycle":
        l, m, n = cycle(nodes, new_path)
    elif graphtype == "Star":
        l, m, n = star(nodes, new_path)
    elif graphtype == "Path":
        l, m, n = path(nodes, new_path)
    elif graphtype == "Tree":
        l, m, n = tree(nodes, new_path)
    elif graphtype == "Complete":
        l, m, n = complete(nodes, new_path)
    elif graphtype == "Bipartite":
        l, m, n = bipartite(nodes, new_path)
    elif graphtype == "Hypercubes":
        l, m, n = hypercube(nodes, new_path)
    elif graphtype == "Petersen":
        l, m, n = petersen(new_path)
    elif graphtype == "Temporal" and algorithm == "None":
        n = temporal_noalg(nodes, nodes*2, s, new_path)
        return n
    elif graphtype == "Temporal" and algorithm == "FJ":
        n = temporal(nodes, d, s, new_path)
        return n
    else:
        l, m, n = custom(graphtype, new_path)
    return l, m, n


def select_alg(algorithm, le, m, n, path, s, d):
    if algorithm == 'BFS':
        bfs(le, m, n, path)

    elif algorithm == 'DFS':
        dfs(le, m, n, path)

    elif algorithm == 'SP':
        dijkstra(le, m, n, s, d, path)

    elif algorithm == 'CD':
        cycleDetection(le, m, n, path)

    elif algorithm == 'None':
        print("None")
