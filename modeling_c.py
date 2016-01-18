# Kamiyama, N., Takizawa, A., Katoh, N., & Kawabata, Y. (2009).
#  Evaluation of capacities of refuges in urban areas by using dynamic network flows.
#  Retrieved from http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.419.771&rep=rep1&type=pdf

from __future__ import division
from graph_tool.all import *

# unit time
DELTA_T = 10    # s


def modeling_c(inFile, outFile):
    # G: Original Graph
    G = load_graph(inFile + ".xml.gz")
    # N: Transit Network
    N = G.copy()

    # read vertex's properties
    color = N.vertex_properties["color"]    # color
    pos = N.vertex_properties["pos"]        # position
    size = N.vertex_properties["size"]      # size
    # read edges' properties
    length = N.edge_properties["length"]    # m
    width = N.edge_properties["width"]      # m
    # read graph's properties
    # B = N.graph_properties["B"]             # list
    S = N.graph_properties["S"]             # list

    # create new property maps
    cap = N.new_edge_property("int")
    tm = N.new_edge_property("int")

    # modify edges
    for e in N.edges():
        d = 0
        if width[e] > 13:
            d = 20
        elif width[e] >= 5.5:
            d = 9
        else:
            d = 4
        if d == 0:
            print e

        cap[e] = 6 * d * DELTA_T
        tm[e] = length[e] / DELTA_T

    # save new properties
    N.edge_properties["cap"] = cap
    N.edge_properties["tm"] = tm
    # delete useless properties
    del N.edge_properties["length"]
    del N.edge_properties["width"]

    # draw graph
    graph_draw(N, pos=pos, vertex_size=size, vertex_fill_color=color, edge_pen_width=prop_to_size(cap, mi=0.5, ma=3, power=1), output=outFile + ".pdf")

    # save transit network
    N.save(outFile + ".xml.gz")
