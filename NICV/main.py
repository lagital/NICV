import sys
import os
import statistics
from TextTracePair import TextTracePair

pairsList = []
meanList = []

for i in range(len(os.listdir(sys.argv[1]))):
    pathToTrace = sys.argv[1] + "\\" + os.listdir(sys.argv[1])[i]
    pathToText = sys.argv[2] + "\\" + os.listdir(sys.argv[2])[i]

    with open(pathToTrace, "r") as tmpTraceFile:
        tmpTrace = tmpTraceFile.read()

    with open(pathToText, "r") as tmpTextFile:
        tmpText = tmpTextFile.read()

    tmpTraceFile.close()
    tmpTextFile.close()

    pairsList.append(TextTracePair(tmpText, tmpTrace, pathToText, pathToTrace))

    pairsList[i].setMean()
    pairsList[i].setVariance()
    meanList.append(pairsList[i].getMean())

var = statistics.variance(meanList)

for i in range(len(os.listdir(sys.argv[1]))):

    tmpNicv = var / pairsList[i].getVariance()
    pairsList[i].setNicv(tmpNicv)

    print ((pairsList[i].getNicv()))