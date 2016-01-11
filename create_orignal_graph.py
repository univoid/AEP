from graph_tool.all import *
from json import loads
rawList = []
## read raw data from json file
with open("raw.json", "r") as file:
    for line in file:
        data = loads(line)
        rawList.append(data);

# initialise Original Graph
G = Graph()

# create graph's properties
B = G.new_graph_property("object")      # list of departures
B[G] = []
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


# save Original Graph
G.save("OrignalGraph.xml.gz")

