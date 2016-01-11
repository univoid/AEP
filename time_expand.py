# CONSTANT
# infinition
INF = 500


def time_expand(time, N_s, vl, N):
    vl.append([])                           # new time slide for time

    # read transitNetwork properties
    cap0 = N.edge_properties["cap"]           # traffic capacity
    tm0 = N.edge_properties["tm"]           # transit time
    S = N.graph_properties["S"]             # sinks list

    # read TENetwork properties
    cap = N_s.edge_properties["cap"]        # edges capacity
    res = N_s.edge_properties["res"]        # edges residual
    S_s = N_s.graph_properties["S_s"]       # super sink

    # iterate original vertex
    for v in  N.vertices():
        # append new vertex to V_s(time)
        v_s = N_s.add_vertex()
        vl[time].append(v_s)

        target_index = N.vertex_index[v]    # index of the original of now vertex
        target = v_s                        # now vertex

        # add 'wait here' edges
        source = vl[time-1][target_index]   # now vertex when 1 time slide before in TENet
        e_s = N_s.add_edge(source, target)
        res[e_s] = cap[e_s] = INF

        # add 'go ahead' edges
        for e in v.in_edges():
            if time - tm0[e] >= 0:
                source_index = N.vertex_index[e.source()]   # index of source vertex of e
                source = vl[time-tm0[e]][source_index]      # source vertex in TENetwork
                e_s = N_s.add_edge(source, target)
                res[e_s] = cap[e_s] = cap0[e]

        # add escape accept edges
        if v in S:
            e_s = N_s.add_edge(v_s, S_s)                # new sink edge
            source = vl[time-1][target_index]           # now vertex when 1 time slide before in TENet
            res[e_s] = cap[e_s] = res[g.edge(source, S_s)]
