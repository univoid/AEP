import numpy as np
import matplotlib.pyplot as plt
import json


def plot_figure(inFile, outFile):
    with open("json/" + inFile + ".json", "r") as inFile:
        data = json.load(inFile)

    plt.figure(1)
    plt.subplot(211)
    plt.plot(data["time"], data["sumFlow"])
    plt.title("Sum of Evacuees arrived")
    plt.xlabel("time")
    plt.ylabel("arrived")

    plt.subplot(212)
    plt.bar(data["time"][1:], data["nowFlow"][1:])
    plt.title("Histogram of Evacuees arrived at each time slide(expect time 0)")
    plt.xlabel("time")
    plt.ylabel("arrived")

    # save and show
    plt.tight_layout()
    plt.savefig("result/" + outFile + ".pdf")
    # plt.show()
