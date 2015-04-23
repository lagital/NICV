import statistics
import numpy
from numpy import array
import scipy
from numpy import array
from scipy.io.wavfile import read
import matplotlib.pyplot as plt
import pywt
from parse_binary import parse_binary
import Database
import time

class Kind(object):

    def __init__(self):
        self.text = ''
        self.variance = 0
        self.pathToText = ''
        self.fft = 0
        self.dwt = 0

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

    def nicv(self, db, idList):

        start_time = time.time()

        listLen = len(idList)
        nicvList = [(0, 0)]
        errList = []

        for i in range (listLen):

            meanList = []
            varList = []

            query = "SELECT data FROM trace WHERE id = "+str(idList[i])+";"
            db.cur.execute(query)
            raw_data = db.cur.fetchone()[0]

            try:
                parse_data = parse_binary(raw_data)

                mean = numpy.array(parse_data).mean()
                var = numpy.array(parse_data).var()
                meanList.append(mean)
                varList.append(var)

                if i%10000 == 0:
                    print 'Traces processed: ', i, ' / ', listLen
            except:
                errList.append(idList[i])
                print 'Error. Trace ID: ', idList[i]
                continue

        print 'All traces for the current kind are processed.'
        print 

        mVar = numpy.array(meanList).var()

        for j in range(len(idList)):

            nicv = mVar / varList[j]
            nicvList[j] = idList[j], nicv

            query = "INSERT INTO trace (nicv) VALUES (%s) WHERE id = "+str(idList[j])+";"
            content = (nicv)
            db.cur.execute(query, content)

        db.conn.commit()

        print('NICV is calculated for the current kind.')
        print 'Execution time: ', time.time() - start_time

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