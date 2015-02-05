import sys
import os
from .TextTracePair import TextTracePair

pairsList = []

for i in range(len(os.listdir(sys.argv[1]))):
    pathToTrace = os.listdir[i](sys.argv[1])
    pathToText = os.listdir[i](sys.argv[0])
    tmpTrace = open(pathToTrace, 'r')
    tmpText = open(pathToText, 'r')
    pairsList[i] = TextTracePair(tmpText, tmpTrace, pathToText, pathToTrace)
    tmpTrace.close
    tmpText.close


