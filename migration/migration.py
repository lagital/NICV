import os
import sys

for i in range(len(os.listdir(sys.argv[1]))):
    pathToTrace = sys.argv[1] + "/" + os.listdir(sys.argv[1])[i]
    lines = open(pathToTrace, "r").read().splitlines()
    """
    with open(pathToTrace, "r") as tmpTraceFile:
        tmpArray = tmpTraceFile.readlines()
        tmpTrace = tmpTraceFile.read()
        #lines = (line.rstrip('\n') for line in open(pathToTrace, "r"))
        lines = open(tmpTraceFile).read().splitlines()
    tmpTraceFile.close()
    """
for i in range (24):
    print lines[i]