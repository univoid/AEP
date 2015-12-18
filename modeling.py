from graph_tool.all import *
from __future__ import division
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
    if slope <= 5:
        return 1
    elif slope <= 10:
        return 0.885
    else:
        return 0.75

# define widening drop function
def f(phi):
    return -0.005581 * phi + 0.9367

# define widening drop function
def g(u, edges):
    w_in  = 0
    w_out = 0
    for e in edges:
        if e.source() == u:
            w_out += width[e]
        else:
            w_in += width[e]
    return w_in / w_out

# G: Original Graph
G = load_graph("OrignalGraph.xml.gz")
# N: Transit Network
# initialisation
N = G.copy()

# read vertex's properties
type = N.vertex_properties["type"]      # widenning or bottleneck
phi = N.vertex_properties["phi"]        # radians
# read edges' properties
length = N.edge_properties["length"]    # m
width = N.edge_properties["width"]      # m
slope = N.edge_properties["slope"]      # degrees
sat = N.edge_properties["sat"]          # boolean
B = N.graph_properties["B"]             # list
S = N.graph_properties["S"]             # list
# create new property maps
cap = N.new_edge_property("int")
tm = N.new_edge_property("int")

# modify edges
for e in G.vertices():
    if sat[e]:
        cap[e] = width[e] * RHO_OPT * DELTA_T
        tm[e] = length[e] // (V_OPT * h(slope[e]) * DELTA_T)

        u = e.source()
        if type(u) == "widenning":
            cap[e] = f(phi[u]) * cap[e]
        elif type(u) == "bottleneck":
            cap[e] = g(u, u.all_edges()) * cap[e]
    else:
        cap[e] = width[e] * RHO_M * DELTA_T
        tm[e] = length[e] // (V_F * h(slope[e]) * DELTA_T)

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