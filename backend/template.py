def searchAlgTemplate(adjlist,G,positions):
    #can clear the canvas 
    plt.clf()

    #more colours are welcome, as long as the path taken for progression is less than or equal
    #to the length of the colourList.
    colourList=['orange','blue','yellow','red','purple','grey','pink','green','grey']

    #initialise an all white list for the nodes that have not yet been coloured
    #will get coloured as the algorithm progresses. this can be modified within a loop
    #(if a loop exists) and can be redrawn and saved to keep up with the progression
    vColour=['#ffffff']*len(adjlist)

    #draw the graph with the colours at each index referring to the index
    #i.e index 0 refers to vertex 0
    nx.draw(G, pos=positions,node_color=vColour)

    #this is to aid saving each picture with a different name but keeps
    #track of progression. increment later (order+=1) if multiple images are to be used
    order=0
    plt.savefig((str(order)+"searchAlgTemplate.png"), dpi=300)


    #algorithm starts
    

def graphTemplate(numNodes):

    #this function will provide you with the necessary lines of code that will
    #be consistent and compatible with other functions of the program
    
    #clear the previously made graphs on the canvas (if one has been made before)
    #and create a new instance of a networkx graph
    plt.clf()
    G= nx.Graph()

    #adding your nodes in a certain way goes here, for example
    #the below adds the nodes to the graph. we start from i=0 since
    #it is a networkx default to start from zero. as a labelling issue this
    #is fixed when nx.draw_networkx_labels occurs
    for i in range(0,numNodes):
        G.add_node(i)
   
    #creating edges on the graph is what distinguishes each graph from the other
    #which vertices they join to is what your algorithm will do

        

    #adding edges may happen here

        

        
    #positions allows the vertices and edges to be laid out in a default
    #networkx layout. here, I use spring_layout, but there are many others
    #to choose from
    positions = nx.spring_layout(G)

    #the graph with the genereated positions for each node and edge is created
    #with the node colour defaulted as white, since the search algorithms will
    #change the colour when traversing the graph
    nx.draw(G, pos=positions,node_color='white')

    #adding labels to each node - labelled as 1 more than the current node number
    #so node 0 becomes node 1
    nx.draw_networkx_labels(G, pos=positions,labels={n: n+1 for n in G})


    #matplotlib function that saves the graph creates as a png
    plt.savefig((str(numNodes)+"graphTemplate.png"), dpi=300)


    #the below allows the created graph to be converted to an adjaceny list
    #this is because, if the user has selected a graph search algorithm, each
    #of the currently made graphs has been standardised to take in the same
    #parameters with the same layout of graph
    adjlist=[]
    x = nx.convert.to_dict_of_lists(G)
    for i in x.values():
        adjlist.append(i)

    #ensure the values below are returned in the same order as shown below
    return adjlist,G,positions
