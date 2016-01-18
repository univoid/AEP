from __future__ import division
from math import floor
from graph_tool.all import *
# CONSTANT
# free velocity
V_F = 2         # m / s
# limited density
RHO_M = 4       # persons / m^2
# limited velocity
V_M = 0         # m / s
# optimal density
RHO_OPT = 2     # persons / m^2
# optimal velocity
V_OPT = 0.75       # m / s
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
def g(u, cap):
    return u.out_degree(cap) / u.in_degree(cap)


def modeling(inFile, outFile):
    # G: Original Graph
    G = load_graph(inFile + ".xml.gz")
    # N: Transit Network
    N = G.copy()

    # read vertex's properties
    type = N.vertex_properties["type"]      # 'widenning' or 'bottleneck' or 'normal'
    phi = N.vertex_properties["phi"]        # radians
    color = N.vertex_properties["color"]    # color
    pos = N.vertex_properties["pos"]        # position
    size = N.vertex_properties["size"]      # size
    # read edges' properties
    length = N.edge_properties["length"]    # m
    width = N.edge_properties["width"]      # m
    slope = N.edge_properties["slope"]      # degrees
    sat = N.edge_properties["sat"]          # boolean
    # read graph's properties
    # B = N.graph_properties["B"]             # list
    S = N.graph_properties["S"]             # list

    # create new property maps
    cap = N.new_edge_property("int")
    tm = N.new_edge_property("int")

    # modify edges
    for e in N.edges():
        if sat[e]:
            cap[e] = width[e] * RHO_OPT * DELTA_T
            tm[e] = length[e] // (V_OPT * h(slope[e]) * DELTA_T)

            u = e.source()
            if type[u] == "widenning":
                cap[e] = floor(f(phi[u]) * cap[e])
            elif type[u] == "bottleneck":
                cap[e] = floor(g(u, cap) * cap[e])
            else:
                pass
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

    # draw graph
    graph_draw(N, pos=pos, vertex_size=size, vertex_fill_color=color, edge_pen_width=prop_to_size(cap, mi=0, ma=3, power=1), output=outFile + ".pdf")

    # save transit network
    N.save(outFile + ".xml.gz")
