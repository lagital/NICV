import statistics
class TextTracePair(object):

    def __init__(self, loadedText, loadedTrace, pathToText, pathToTrace):
        self.text = loadedText
        self.trace = [float(s) for s in loadedTrace.split()]
        self.nicv = 0
        self.variance = 0
        self.pathToText = pathToText
        self.pathToTrace = pathToTrace

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