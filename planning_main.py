from graph_tool.all import *
from time_expand import time_expand
# CONSTANT
# sum of evacuees
SUM_EVACUEE = 46355     # person

# load transit Network
N = load_graph("TransitNetwork.xml.gz")
# load initial network from initialise_graph
N_s = load_graph("TimeExpandedNetwork0.xml.gz")

# read transitNetwork properties
cap0 = N.edge_properties["b"]        # traffic capacity
tm0 = N.edge_properties["tm"]        # transit time

# read TENetwork properties
B_s = N.graph_properties["B_s"]         # super source
S_s = N.graph_properties["S_s"]         # super sink
cap = N.edge_properties["cap"]        # edges capacity
res = N.edge_properties["res"]        # edges residual

# initialise list of vertices for time slide
vlist = N_s.new_graph_property("object")
vlist[N_s] = []
# get alias
vl = vlist[N_s]
# append vertices of time 0
vl[0] = []
for v in N_s.vertices():
    if (v != B_s) and (v != S_s):
        vl[0].append(v)

# iterate time to expand N_s and deal with max flow
time = 0
maxFlow = 0
while maxFlow < SUM_EVACUEE:
    time += 1
    # expand N_s with time slide
    time_expand(time, N_s, vl, N)
    # reread TENetwork0 properties
    # cap = N.vertex_properties["cap"]        # edges capacity
    res = N.vertex_properties["res"]        # edges residual
    # get new residual by max_flow
    res = boykov_kolmogorov_max_flow(N_s, B_s, S_s, cap, res)
    # get value of maxFlow
    maxFlow = sum((cap[e]-res[e]) for e in S_s.in_edges())
    print('time slide {}: max flow is {}'.format(time, maxFlow))
    # save new residual property map
    N_s.graph_properties["res"] = res

# print total time of Evacuation
print('total time of Evacuation is {}'.format(time))

# save new properties
N_s.graph_properties["vlist"] = vlist

# save Omage Graph
N_s.save("OmageGraph.xml.gz")
