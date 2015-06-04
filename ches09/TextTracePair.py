import matplotlib.pyplot as plt
import statistics
import numpy
from operator import itemgetter
import sys
from numpy import array
import scipy
import math
from dsp import *
from traces_database import *
from des_breaker import des_breaker
from des_block import des_block
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

    @staticmethod
    def getFromTuple(item):
        return item[0]

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

    def nicv(self, db, idList, top):

        start_time = time.time()
        iter_time = time.time()

        idListLen = len(idList)
        errList = []
        meanList = []
        varList = []

        top = int(top)

        for i in range (idListLen):
            err = 0

            query = "SELECT data FROM trace WHERE id = "+str(idList[i])+";"
            db.cur.execute(query)
            raw_data = db.cur.fetchone()[0]

            try:
                parse_data = parse_binary(raw_data)
            except:
                err = 1
                errList.append(idList[i])
                print 'Error. Trace ID: ', idList[i]

            if err == 0:
                mean = numpy.mean(numpy.array(parse_data))
                var = numpy.var(numpy.array(parse_data))

                meanList.append(mean)

                if math.isnan(var):
                    errList.append(idList[i])
                    print 'Error. Trace ID: ', idList[i]
                else:
                    varList.append(var)
                    if i%5000 == 0:
                        print 'Traces processed: ', i, ' / ', idListLen
                        print 'Execution time: ', time.time() - iter_time
                        iter_time = time.time()

        print 'All traces for the current kind are processed.'
        print 'Errors percent: ', len(errList) / idListLen * 100, '%'

        mMean = numpy.array(meanList)
        mVar = numpy.nanvar(mMean)

        for j in range(len(errList)):
            idList.remove(errList[j])

        idListLen = len(idList)

        nicvList = []

        for j in range(idListLen):

                nicv = math.sqrt(mVar / varList[j])
                print nicv
                nicvList.append((nicv, idList[j]))

                query = "UPDATE trace SET nicv = %s WHERE id = "+str(idList[j])+";"
                #content = ()
                db.cur.execute(query % nicv)

        db.conn.commit()
        print('NICV is calculated for the current kind...')

        nicvList.sort(key=itemgetter(0))

        nicvListLen = len(nicvList)

        for j in range(idListLen):

            if top - 1 - j >= 0:
                (nicv, id) = nicvList[nicvListLen - j - 1]
                query = "UPDATE trace SET is_top = '%s' WHERE id = "+str(id)+";"
                content = ('yes')
                db.cur.execute(query % content)
                #print str(nicv), content
            else:
                (nicv, id) = nicvList[nicvListLen - j - 1]
                query = "UPDATE trace SET is_top = '%s' WHERE id = "+str(id)+";"
                content = ('no')
                db.cur.execute(query % content)
                #print str(nicv), content

        db.conn.commit()
        print('NICV top is calculated for the current kind...')
        print 'Execution time: ', time.time() - start_time

    def nicv2(self, db, idList, top):

        idListLen = len(idList)
        errList = []
        meanList = []
        varList = []

        cmd = "SELECT message, cipher, data FROM trace WHERE id = '" + str(idList[0]) + "'"
        db.cur.execute(cmd)
        one = db.cur.fetchone()
        tmsg, tcrypt, traw_data = one

        parse_data = parse_binary(str(traw_data))
        points = len(parse_data)
        print "Points in trace:", points

        print "Calculating ..."

        #classList = [[0.0] * points]*256
        tclassList = [0.0] * points
        tMeanList = [0.0] * points
        tPowerMeanList = [0.0] * points
        parallels = 16
        tGlobalVarlist = [[]]*parallels
        classList = [[]]*256
        #globalVarlist = [0.0] * points
        globalVarlist = []
        byteList = []

        collected = 0
        classCalcCount = 0
        classCountNotIncluded = 0
        tracesInClass = 0

        #for i in range(points):
        for i in range(points//parallels):

            start_time = time.time()

            for j in range (idListLen):
                err = 0

                cmd = "SELECT message, data FROM trace WHERE id = '" + str(idList[j]) + "'"
                db.cur.execute(cmd)
                one = db.cur.fetchone()
                msg, raw_data = one

                try:
                    parse_data = parse_binary(str(raw_data))
                except:
                    err = 1
                    errList.append(idList[j])
                    #print 'Error. Trace ID: ', idList[j]

                if err == 0:
                    for k in range(parallels):
                        tGlobalVarlist[k].append(parse_data[i*parallels+k])

                    if classCalcCount < 256:
                        if int(msg[0:2], 16) == classCalcCount:
                            for d in range(points):
                                tMeanList[d] = tMeanList[d] + parse_data[d]
                                tPowerMeanList[d] = tPowerMeanList[d] + parse_data[d]**2
                                tracesInClass = tracesInClass + 1

                if j%20000 == 0:
                    print j, "traces was processed."
                    #if collected == 0:
                    #   byteList.append((int(msg[0:2], 16), idList[j]))
            #collected = 1

            for m in range(parallels):
                globalVarlist.append(numpy.var(numpy.array(tGlobalVarlist[m])))

            if tracesInClass > 0:
                for m in range(points):
                    #tMeanList[m] = tMeanList[m]/tracesInClass
                    tPowerMeanList[m] = tPowerMeanList[m]/tracesInClass - (tMeanList[m]/tracesInClass)**2
                print "Var[E(Y|X)] for class", classCalcCount, "was calculated"
                classList.append(tPowerMeanList)
            else:
                classCountNotIncluded = classCountNotIncluded + 1
                print "Class was empty!"

            classCalcCount = classCalcCount + 1
            tracesInClass = 0

            tGlobalVarlist = [[]]*parallels
            tMeanList = [0.0] * points
            tPowerMeanList = [0.0] * points

            if i%parallels == 0:
                print "Var(Y) was processed for", i*parallels + parallels, "points"

        lenn = len(idList) - (len(errList)/(points//parallels))

        for i in range(256 - classCountNotIncluded):
            for j in range(points):
                if i != 0:
                    classList[0][j] = classList[0][j] + classList[i][j]
        print "Total Var[E(Y|X)] for all classes was calculated!"

        for i in range(lenn):
            globalVarlist[i] = classList[0][i]/(globalVarlist[i]/lenn)
        print "NICV function was calculated!"

        print len(globalVarlist)
        return 0

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