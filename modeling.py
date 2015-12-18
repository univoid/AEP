from graph_tool.all import *
# constants
# free velocity
V_F = 0         # m / s
# limited density
RHO_M = 4       # persons / m^2
# limited velocity
V_M = 0         # m / s
# optimal density
RHO_OPT = 2     # persons / m^2
# optimal velocity
V_OPT = 2       # m / s
# unit time
DELTA_T = 10    # s

# define slope influence function
def h(slope):
    pass
# define widening drop function
def f(phi):
    pass
# define widening drop function
def g(w):
    pass

# G: Original Graph
G = load_graph("OrignalGraph.xml.gz")
# N: Transit Network
# initialisation
N = G.copy()

# read vertex's properties
type = N.vertex_properties["type"]
phi = N.vertex_properties["phi"]
# read edges' properties
length = N.edge_properties["length"]
width = N.edge_properties["width"]
slope = N.edge_properties["slope"]
sat = N.edge_properties["sat"]
B = N.graph_properties["B"]
S = N.graph_properties["S"]
# create new property maps
cap = N.new_edge_property("int")
tm = N.new_edge_property("int")

# modify edges
for e in G.vertices():
    if sat[e]:
        cap[e] = width[e] * RHO_OPT * DELTA_T
        tm[e] = length[e] / (V_OPT * h(slope[e]) * DELTA_T)

        u = e.source()
        if type(u) == "widenning":
            cap[e] = f(phi[u]) * cap[e]
        elif type(u) == "bottleneck":
            cap[e] = g(u.all_edges()) * cap[e]
    else:
        cap[e] = width[e] * RHO_M * DELTA_T
        tm[e] = length[e] / (V_f * h(slope[e]) * DELTA_T)

# save new properties
N.edge_properties["cap"] = cap
N.edge_properties["tm"] = tm
# delete useless properties
del N.vertex_properties["type"]
del N.vertex_properties["phi"]
del N.edge_properties["length"]
del N.edge_properties["width"]
del N.edge_properties["slope"]
del N.edge_properties["sat"]

# save transit network
N.save("TransitNetwork.xml.gz")