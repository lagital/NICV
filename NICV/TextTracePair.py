import statistics
class TextTracePair(object):

    def __init__(self, loadedText, loadedTrace, pathToText, pathToTrace):
        self.text = loadedText
        self.trace = loadedTrace
        self.nicv = 0
        self.pathToText = pathToText
        self.pathToTrace = pathToTrace

    def getNicv(self):
        return self.nicv

    def setNicv(self):
        var = statistics.variance(self.trace)
        self.nicv = statistics.variance(statistics.mean(self.trace)) / var

    def getText(self):
        return self.text

    def getTrace(self):
        return self.trace

    def getPathToText(self):
        return self.pathToText

    def getPathToTrace(self):
        return self.pathToTrace