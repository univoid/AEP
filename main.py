from get_raw import get_raw
from create_original_graph import create_original_graph
from create_original_graph_c import create_original_graph_c
from modeling import modeling
from modeling_c import modeling_c

from initialise_graph import initialise_graph
from planning_main import planning_main
from plot import plot_figure
from route_extract import route_extract

get_raw()
# create test group
create_original_graph(outFile="OriginalGraph")
modeling(inFile="OriginalGraph", outFile="TransitNetwork")

# create control group
create_original_graph_c(outFile="OriginalGraph_c")
modeling_c(inFile="OriginalGraph_c", outFile="TransitNetwork_c")

# planning
# test group
initialise_graph(inFile="TransitNetwork", outFile="TimeExpandedNetwork0")
planning_main(inFile1="TransitNetwork", inFile2="TimeExpandedNetwork0", outFile="OmegaGraph")

# control group
initialise_graph(inFile="TransitNetwork_c", outFile="TimeExpandedNetwork0_c")
planning_main(inFile1="TransitNetwork_c", inFile2="TimeExpandedNetwork0_c", outFile="OmegaGraph_c")


# compare result
# output plot Figures
plot_figure(inFile="OmegaGraph", outFile="testGroup")
plot_figure(inFile="OmegaGraph_c", outFile="controlGroup")
