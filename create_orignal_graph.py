from graph_tool.all import *
from json import loads

rawEList = []
rawVList = []
# read raw data from json file
# read edge
with open("rawEdge.json", "r") as infile:
    for line in infile:
        data = loads(line)
        rawEList.append(data)
# read vertex
with open("rawVertex.json", "r") as infile:
    for line in infile:
        data = loads(line)
        rawVList.append(data)


# initialise Original Graph
G = Graph()

# create graph's properties
# B = G.new_graph_property("object")      # list of departures
# B[G] = []
S = G.new_graph_property("object")      # list of refuges
S[G] = []
# create vertex's properties
type = G.new_vertex_property("string")  # type of point
phi = G.new_vertex_property("float")    # inner radian
b = G.new_vertex_property("int")        # supply
r = G.new_vertex_property("int")        # receive
# create edge's properties
length = G.new_edge_property("int")     # length of road
width = G.new_edge_property("int")      # width of road
slope = G.new_edge_property("int")      # slope of road
sat = G.new_edge_property("int")        # saturation flag


# input
# graph properties
S[G].extend(range(0, 8))

# edge properties
for item in rawEList:
    e = G.add_edge(item["from"], item["to"])
    sl = item["slope"]
    slope[e] = int(sl) if sl else None
    wi = item["width"]
    width[e] = int(wi) if wi else None
    le = item["length"]
    length[e] = int(le) if le else None
    sa = item["sat"]
    sat[e] = sa
    if item["duplex"] == "T":
        e2 = G.add_edge(item["to"], item["from"])
        slope[e2], width[e2], length[e2], sat[e2] =slope[e], width[e], length[e], sat[e]

# vertex properties
for item in rawVList:
    # TODO
    pass

# save properties
# G.graph_properties["B"] = B
G.graph_properties["S"] = S
G.vertex_properties["type"] = type
G.vertex_properties["phi"] = phi
G.vertex_properties["b"] = b
G.vertex_properties["r"] = r
G.edge_properties["length"] = length
G.edge_properties["width"] = width
G.edge_properties["slope"] = slope
G.edge_properties["sat"] = sat

# save Original Graph
G.save("OrignalGraph.xml.gz")
G.save("OrignalGraph.xml")
