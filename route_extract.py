from graph_tool.all import *


def search_route(now, N, f, num, flow):
    if num[now] > 0:
        for e in now.out_edges():
            if f[e] != 0:
                source = N.vertex(num[e.source()])
                target = N.vertex(num[e.target()])
                if source != target and target != 0:
                    e_n = N.edge(source, target)
                    flow[e_n] += f[e]

                search_route(e.target(), N, f, num, flow)
    else:
        return


def route_extract(inFile1, inFile2, outFile, departure):
    # load transit Network
    N = load_graph("xml/" + inFile1 + ".xml.gz")
    # load Omage Graph
    N_o = load_graph("xml/" + inFile2 + ".xml.gz")

    # read or delete vertex's properties
    color = N.vertex_properties["color"]    # color
    pos = N.vertex_properties["pos"]        # position
    size = N.vertex_properties["size"]      # size
    # read edges' properties
    cap = N.edge_properties["cap"]
    tm = N.edge_properties["tm"]

    # read properties from Omage Graph
    f = N_o.edge_properties["f"]
    num = N_o.vertex_properties["num"]

    # create new edges' properties
    flow = N.new_edge_property("int")

    # example begin from point No.(departure)
    search_route(N_o.vertex(departure+3), N, f, num, flow)

    # draw graph
    graph_draw(N, pos=pos, vertex_size=size, vertex_fill_color=color,
               edge_pen_width=prop_to_size(flow, mi=0, ma=4, power=1), output="result" + outFile + ".pdf")
