from random import *
from matplotlib import *
import matplotlib.pyplot as plt

"""
test = []
bins = []
for i in range(5002):
    test.append(uniform(0.0, 0.9))
    bins.append(i)
bins.append(5002)
"""
"""
plt.hist([0, 4, 6, 5, 7], bins=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
#plt.hist(test, bins=bins)
"""
test = []
for i in range(5001):
    test.append(uniform(0.0, 0.2)+uniform(0.0, 0.2)+uniform(0.0, 0.3))
test.append(1.0)

plt.bar(range(0, 5002), test, color='g')
plt.ylabel('NICV')
plt.xlabel('samples')
plt.colors()
plt.show()

"""
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
"""
