import statistics
import numpy
import scipy
from numpy import array
from scipy.io.wavfile import read
import matplotlib.pyplot as plt
import pywt

class Trace_tmp(object):

    def __init__(self, pathToTrace):
        self.text = ''
        self.nicv = 0
        self.variance = 0
        self.pathToText = ''
        self.pathToTrace = pathToTrace
        self.fft = 0
        self.dwt = 0
"""
        tmp = read(pathToTrace)
        self.trace = numpy.array(tmp[1], dtype=float)
        print(self.trace)
"""
    def setFft(self):
        self.fft = scipy.fft(self.trace)

    def getFft(self):
        return self.fft

    def setDwt(self):
        cA, cD = pywt.dwt(self.trace, 'haar')
        self.dwt = cA

    def getDwt(self):
        return self.dwt

    def writeTrace(self, key):
        return 'pathToFftTrace'
        #TODO: writing traces using name from pathToTrace and choosing folder by key.
        #TODO: regexp!

    def setBandpass(self):
        #self.trace = 0
        return 0
        #TODO: bandpass

    def draw(self, trace):
        plt.plot(trace)
        plt.ylabel('some numbers')
        plt.show()
        #TODO: drawing

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