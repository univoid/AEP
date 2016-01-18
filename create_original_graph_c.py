from graph_tool.all import *
from json import loads


def create_original_graph_c(outFile):
    rawEList = []
    rawVList = []
    # read raw data from json file
    # read edge
    with open("json/rawEdge.json", "r") as infile:
        for line in infile:
            data = loads(line)
            rawEList.append(data)
    # read vertex
    with open("json/rawVertex.json", "r") as infile:
        for line in infile:
            data = loads(line)
            rawVList.append(data)
    # the sum of evacuee
    sumb = 0
    # the sum of refuges' capacity
    sumr = 0
    for item in rawVList:
        sumb += item["b"]
        sumr += item["r"]

    print "The sum of evacuee is {}, and the sum of refuges' capacity is {}".format(sumb, sumr)


    # initialise Original Graph
    G = Graph()

    # create graph's properties
    # B = G.new_graph_property("object")      # list of departures
    S = G.new_graph_property("object")      # list of refuges
    # create vertex's properties
    b = G.new_vertex_property("int")        # supply
    r = G.new_vertex_property("int")        # receive
    color = G.new_vertex_property("string")         # color
    pos = G.new_vertex_property("vector<double>")   # position
    size = G.new_vertex_property("int")             # size
    # create edge's properties
    length = G.new_edge_property("float")       # length of road
    width = G.new_edge_property("float")        # width of road


    # input
    # edge properties
    for item in rawEList:
        e = G.add_edge(item["from"], item["to"])
        width[e] = item["width"]
        length[e] = item["length"]
        # duplex
        e2 = G.add_edge(item["to"], item["from"])
        width[e2], length[e2] = width[e], length[e]

    # vertex properties
    for item in rawVList:
        v = G.vertex(item["num"])
        b[v] = item["b"]
        r[v] = item["r"]
        color[v] = item["color"]
        pos[v] = item["pos"]
        if color[v] == "#4f8f00":
            size[v] = 10
        elif color[v] == "#919191":
            size[v] = 7
        else:
            size[v] = 5

    # graph properties
    S[G] = []
    S[G].extend(range(0, 8))
    # B[G] = G.vertices()

    # save properties
    # G.graph_properties["B"] = B
    G.graph_properties["S"] = S
    G.vertex_properties["b"] = b
    G.vertex_properties["r"] = r
    G.vertex_properties["color"] = color
    G.vertex_properties["pos"] = pos
    G.vertex_properties["size"] = size
    G.edge_properties["length"] = length
    G.edge_properties["width"] = width

    # draw graph
    graph_draw(G, pos=pos, vertex_size=size, vertex_fill_color=color, output="pdf/" + outFile + ".pdf")

    # save Original Graph
    G.save("xml/" + outFile + ".xml.gz")

