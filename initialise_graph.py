from graph_tool.all import *

# N: transit network
N = load_graph("TransitNetwork.xml.gz")
# N_s: time expanded network
N_s = Graph()

# read transitNetwork properties
B = N.graph_properties["B"]         # sources list
S = N.graph_properties["S"]         # sinks list
b = N.vertex_properties["b"]        # initial evacuees
r = N.vertex_properties["r"]        # capacity of refuges

# create new property maps
# capacity
cap = N_s.new_edge_property("int")
# residual
res = N_s.new_edge_property("int")
# original vertex
# ov = N_s.new_vertex_property("int")
# time slide
# ts = N_s.new_vertex_property("int")
# super source
B_s = N_s.new_graph_property("object")
# super sink
S_s = N_s.new_graph_property("object")

# add super source B_s and super sink S_s to N_s
B_s = N_s.add_vertex()
S_s = N_s.add_vertex()

# initialise distribution of spot
for v in N.vertices():
    # get index of v
    #num = N.vertex_index[v]
    # add new vertex to N_s as v_s
    v_s = N_s.add_vertex();
    # index pointing to original vertex
    #ov[v_s] = num
    # initial time 0
    #ts[v_s] = 0;

    # initialise Distribution of Evacuees
    if v in B:
        e_s = N_s.add_edge(B_s, v_s)  # add supply edge
        res[e_s] = cap[e_s] = b[v]

    # initialise Distribution of Refuges
    if v in S:
        e_s = N_s.add_edge(v_s, S_s)  # add sink edge
        res[e_s] = cap[e_s] = r[v]

# save new properties
N_s.edge_properties["cap"] = cap
N_s.edge_properties["res"] = res
# N_s.vertex_properties["ov"] = ov
# N_s.vertex_properties["ts"] = ts
N_s.graph_properties["B_s"] = B_s
N_s.graph_properties["S_s"] = S_s

N_s.save("TimeExpandedNetwork0.xml.gz")
