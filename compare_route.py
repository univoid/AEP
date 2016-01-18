from route_extract import route_extract

des = 0
while des >= 0:
    des = raw_input("Enter Des:")
    route_extract(inFile1="TransitNetwork", inFile2="OmegaGraph", outFile="route", departure=int(des))
    route_extract(inFile1="TransitNetwork_c", inFile2="OmegaGraph_c", outFile="route_c", departure=int(des))

