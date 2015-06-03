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
        """
        1) We define all possible values of 6 bits for s-box #1.
        2) We divide all traces on groups according to the 6 bits value (64 classes, as you told before). Next steps (3-4) will be applied for the traces in each particular group.
        3) For each point in one trace within a group we compute the value of E(Y in that point in each trace). For example:

        group with 6 bits 010011:
        trace 1: 1.5 1.3 0.2 0.4 ...
        trace 2: 0.1 0.1 1.6 0.6 ...

        we will have the results: 0.8 0.7 0.9 0.5 ...

        4) We compute Var(results of step 3).
        5) We compute N points of the final NICV function: (Var computed on step 4)/Var(Y).

        Then we repeat those steps for the next s-boxes so new peaks may be added in 64 existing arrays (if a new value is greater than the old, we replace it).
        """
        start_time = time.time()
        iter_time = time.time()

        idListLen = len(idList)
        errList = []
        meanList = []
        varList = []

        top = int(top)

        cmd = "SELECT message, cipher, data FROM trace WHERE id = '" + str(idList[0]) + "'"
        db.cur.execute(cmd)
        one = db.cur.fetchone()
        tmsg, tcrypt, traw_data = one

        parse_data = parse_binary(str(traw_data))
        points = len(parse_data)
        lenTmsg = len(tmsg)/2
        traceList = []
        globVarList = []
        classList = [[] for i in range(lenTmsg)]
        tclassList = []
        nicvList = [[-1]*points for i in range(256)]
        #print 'Log0.1:', len(nicvList[0])
        #print 'Log0.2:', nicvList[0][0]

        for i in range (idListLen):
            err = 0

            cmd = "SELECT message, cipher, data FROM trace WHERE id = '" + str(idList[i]) + "'"
            db.cur.execute(cmd)
            one = db.cur.fetchone()
            msg, crypt, raw_data = one

            try:
                parse_data = parse_binary(str(raw_data))
            except:
                err = 1
                errList.append(idList[i])
                print 'Error. Trace ID: ', idList[i]

            if err == 0:
                if i%5000 == 0:
                    print 'Traces processed: ', i
                ttrace = (msg.strip(), parse_data)
                traceList.append(ttrace)

        tglobVar = []
        traceListLen = len(traceList)
        globDataList = [x[1] for x in traceList]
        print len(globDataList[0])

        for k in range(points):
            for i in range(traceListLen):
                #tglobVar = numpy.var(numpy.array(globDataList[k][0:traceListLen]))
                tglobVar.append(globDataList[i][k])
            globVarList.append(numpy.var(numpy.array(tglobVar)))
            #print 'Log lenglobVar:', len(globVarList)

        #TEST WARNING: for j in range(lenTmsg):
        for j in range(1):
            tVar = 0
            for i in range (256):
                for m in range(traceListLen):
                    tmsg, parse_data = traceList[m]
                    #TEST WARNING:
                    #if int(tmsg[j*2:j*2+2], 16) == i:
                    #    tclassList.append(parse_data)
                    tclassList.append(parse_data)
                tclassListLen = len(tclassList)

                while tVar == 0 or str(tVar) == 'nan':
                    tMeanList = []
                    tMean = []
                    for k in range(points):
                        for l in range(tclassListLen):
                            tMean.append(tclassList[l][k])
                        tMeanList.append(numpy.mean(numpy.array(tMean)))
                    tVar = numpy.var(numpy.array(tMeanList))
                for k in range(points):
                    t = tVar/globVarList[k]
                    if nicvList[i][k] < t:
                        nicvList[i][k] = t
            print 'Log nicvlist :', len(nicvList[0])
            print 'End log nicvlist'
            plt.plot(nicvList[i-1])
            plt.ylabel('nicv')
            plt.show()
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