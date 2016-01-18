from graph_tool.all import *
# CONSTANT
INF = 23333

# N: transit network
N = load_graph("TransitNetwork_c.xml.gz")
# N_s: time expanded network
N_s = Graph()

# read transitNetwork properties
# B = N.graph_properties["B"]         # sources list
S = N.graph_properties["S"]         # sinks list
b = N.vertex_properties["b"]        # initial evacuees
r = N.vertex_properties["r"]        # capacity of refuges

# create new property maps
num = N_s.new_vertex_property("int")        # index of vertex mapping to transitNetwork
cap = N_s.new_edge_property("int")          # capacity
res = N_s.new_edge_property("int")          # residual
B_s = N_s.new_graph_property("int")         # super source index
S_s = N_s.new_graph_property("int")         # super sink index

# add super source B_s and super sink S_s to N_s
B_s[N_s] = N_s.vertex_index[N_s.add_vertex()]
S_s[N_s] = N_s.vertex_index[N_s.add_vertex()]


# initialise distribution of spot

S_t = N_s.add_vertex()                  # super sink of time 0

# print N_s.vertex_index[S_t]
for v in N.vertices():
    # add new vertex to N_s as v_s
    v_s = N_s.add_vertex()
    num[v_s] = N.vertex_index[v]

    if N.vertex_index[v] in S:
        # if v in S:
        # initialise Distribution of Refuges
        e_s = N_s.add_edge(v_s, S_t)  # add sink edge
        res[e_s] = r[v]
        cap[e_s] = r[v]
        # # initialise Distribution of Evacuees
        e_s = N_s.add_edge(B_s[N_s], v_s)  # add supply edge
        res[e_s] = b[v]
        cap[e_s] = b[v]
    else:
        # if v in B:
        # initialise Distribution of Evacuees
        e_s = N_s.add_edge(B_s[N_s], v_s)  # add supply edge
        res[e_s] = b[v]
        cap[e_s] = b[v]

# connect S_t to Super S_s
e_s = N_s.add_edge(S_t, S_s[N_s])
res[e_s] = INF
cap[e_s] = INF
# print S_t.out_degree()

# save new properties
N_s.vertex_properties["num"] = num
N_s.edge_properties["cap"] = cap
N_s.edge_properties["res"] = res
N_s.graph_properties["B_s"] = B_s
N_s.graph_properties["S_s"] = S_s

graph_draw(N_s, output="TimeExpandedNetwork0_c.pdf")
N_s.save("TimeExpandedNetwork0_c.xml.gz")
