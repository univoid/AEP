from graph_tool.all import *
from time_expand import time_expand
import json

# CONSTANT
# sum of evacuees
# SUM_EVACUEE = 46355     # person


def planning_main(inFile1, inFile2, outFile):
    # load transit Network
    N = load_graph(inFile1 + ".xml.gz")
    # load initial network from initialise_graph
    N_s = load_graph(inFile2 + ".xml.gz")

    # read transitNetwork properties
    # cap0 = N.edge_properties["b"]        # traffic capacity
    # tm0 = N.edge_properties["tm"]        # transit time

    # read TENetwork properties
    num = N_s.vertex_properties["num"]                    # index of vertex Mapping to transitNetwork
    cap = N_s.edge_properties["cap"]        # edges capacity
    res = N_s.edge_properties["res"]        # edges residual
    B_s = N_s.vertex(N_s.graph_properties["B_s"])         # super source
    S_s = N_s.vertex(N_s.graph_properties["S_s"])         # super sink

    # initialize json (save answer)
    data = dict()
    data["time"] = list()
    data["sumFlow"] = list()
    data["nowFlow"] = list()


    # list initial
    vl = list()                         # time slide supply list
    vl.append([])                       # append vertices of time 0
    stl = list()                        # time slide sink list
    S_t = N_s.vertex(2)                 # super sink of time 0
    stl.append(S_t)                     # append it to stl

    for v in N_s.vertices():
        if (v != B_s) and (v != S_s) and (v != S_t):
            vl[0].append(v)

    # iterate time to expand N_s and deal with max flow
    SUM_EVACUEE = sum(cap[e] for e in B_s.out_edges())
    print "Sum of Evacuees is {}".format(SUM_EVACUEE)
    time = 0                    # the time slide at this moment
    sumFlow = 0                 # the value of max flow
    while sumFlow < SUM_EVACUEE:
        # expand N_s with time slide
        if time > 0:
            time_expand(time, N_s, vl, stl, N)
        # reread TENetwork0 properties
        # cap = N.vertex_properties["cap"]        # edges capacity
        # res = N.vertex_properties["res"]        # edges residual
        # get new residual by max_flow
        res = boykov_kolmogorov_max_flow(N_s, B_s, S_s, cap, res)
        # get value of maxFlow
        nowCap = sum(cap[e] for e in stl[time].in_edges())
        nowRes = sum(res[e] for e in stl[time].in_edges())

        sumFlow = sum((cap[e]-res[e]) for e in S_s.in_edges())
        nowFlow = nowCap - nowRes
        print('time slide {}: sum flow {}, now flow {}, cap {}, residual {} '.
              format(time, sumFlow, nowFlow, nowCap, nowRes))

        # save to Answer
        data["time"].append(time)
        data["sumFlow"].append(sumFlow)
        data["nowFlow"].append(nowFlow)
        # # DEBUG
        # for e in S_s.in_edges():
        #     print "    {}".format(cap[e]-res[e])
        #
        # print
        # # DEBUG
        # # if time == 90:
        # #     print "residual evacuees"
        # #     for e in B_s.out_edges():
        # #         if res[e] > 0:
        # #             print num[e.target()], cap[e], res[e]
        # #
        # #     print "residual capacity of refuges"
        # #     for e in stl[time].in_edges():
        # #         fr = e.source()
        # #         if fr in vl[time]:
        # #             print num[fr], cap[e], res[e]
        # #
        # #     break
        # if time == 15:
        #     break

        time += 1


    # print total time of Evacuation
    print('total time of Evacuation is {}'.format(time))

    # save answer to json
    with open(outFile + ".json", "w") as outFile:
        json.dump(data, outFile)

    # save flow property
    f = N_s.new_edge_property("int")
    for e in N_s.edges():
        f[e] = cap[e] - res[e]
    N_s.edge_properties["f"] = f

    # save as Omage Graph
    N_s.save(outFile + ".xml.gz")
