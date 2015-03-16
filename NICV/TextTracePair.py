import statistics
import numpy
from numpy import array
from scipy.io.wavfile import read
class Trace_tmp(object):

    def __init__(self, pathToTrace):
        self.text = ''
        self.nicv = 0
        self.variance = 0
        self.pathToText = ''
        self.pathToTrace = pathToTrace

        tmp = read(pathToTrace)
        self.trace = numpy.array(tmp[1], dtype=float)
        print(self.trace)

    def setMean(self):
        self.mean = statistics.mean(self.trace)

    def getMean(self):
        return self.mean

    def getNicv(self):
        return self.nicv

    def setNicv(self, nicv):
        self.nicv = nicv

    def getText(self):
        return self.text

    def getTrace(self):
        return self.trace

    def getPathToText(self):
        return self.pathToText

    def getPathToTrace(self):
        return self.pathToTrace

    def getVariance(self):
        return self.variance

    def setVariance(self):
        self.variance = statistics.variance(self.trace)
