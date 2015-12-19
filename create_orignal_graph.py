from graph_tool.all import *

# initialise Original Graph
G = Graph()

# create graph's properties
B = G.new_graph_property("Object")      # list of departures
B[G] = []
S = G.new_graph_property("Object")      # list of refuges
S[G] = []
# create vertex's properties
type = G.new_vertex_property("string")  # type of point
phi = G.new_vertex_property("float")    # inner radian
# create edge's properties
length = G.new_edge_property("int")     # length of road
width = G.new_edge_property("int")      # width of road
slope = G.new_edge_property("int")      # slope of road
sat = G.new_edge_property("int")        # saturation flag

# read table

# save Original Graph
G.save("OrignalGraph.xml.gz")

