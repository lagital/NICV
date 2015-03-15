#!/usr/bin/python

import sys
import os
import statistics
from TextTracePair import TextTracePair

parameters = len(sys.argv)
code = None
top = 0

def print_help():
    print('')
    print('Available parameters for SCApack:')
    print('')
    print('-help < print this info.')
    print('')
    print('-nicv code [-c int(N top traces)] [kalman|dwt] < calculate NICV for')
    print('     traces with chosen code, mark N top traces')
    print('     within group and print statistics.')
    print('')
    print('-nicv code [-s] < print statistics for traces with chosen code.')
    print('')
    print('-load code \path\to\traces [\path\to\clear\texts] [\path\to\encr\texts]')
    print('load traces to database marking with chosen code.')
    print('Attention: text file should have the same name as corresponding trace.')
    print('')
    print('-kalman code < kalman transform on traces with chosen code.')
    print('')
    print('-dwt code < discrete wavelet transform on traces with chosen code.')

if parameters == 1 or sys.argv[1] == '-help':
    print_help()

elif sys.argv[1] == '-nicv':
    if parameters < 4 or parameters > 6:
        print_help()
    elif sys.argv[3] == '-c' and isinstance(sys.argv[4], int):
        code = sys.argv[2]
        top = sys.argv[4]
        if parameters == 6 and sys.argv[5] == '-kalman':
            print('I\'m in NICV for kalman!')
            print('TODO: NICV calculating on kalman transformed traces')
            #TODO: NICV calculating on kalman transformed traces
        elif parameters == 6 and sys.argv[5] == '-dwt':
            print('I\'m in NICV for dwt!')
            print('TODO: NICV calculating on dwt transformed traces')
            #TODO: NICV calculating on dwt transformed traces
        else:
            print('I\'m in classic NICV!')
            print('TODO: NICV calculating on original traces')
            #TODO: NICV calculating on original traces
    elif sys.argv[3] == '-s':
        code = sys.argv[2]
        print('I\'m in printing statistics of NICV!')
        print('TODO: NICV statistics printing')
        #TODO: NICV statistics printing

elif sys.argv[1] == '-load':
    if parameters == 4:
        code = sys.argv[2]
        print('I\'m loading traces!')
        print('TODO: loading traces + clear and encr texts.')
        #TODO: loading traces + clear and encr texts.

elif sys.argv[1] == '-kalman':
    if parameters == 3:
        code = sys.argv[2]
        print('I\'m in kalman!')
        print('TODO: kalman transformation.')
        #TODO: kalman transformation.

elif sys.argv[1] == '-dwt':
    if parameters == 3:
        code = sys.argv[2]
        print('I\'m in dwt!')
        print('TODO: dwt transformation.')
        #TODO: dwt transformation.

# -----------
# PROCEDURES:
# -----------


"""
pairsList = []
meanList = []

for i in range(len(os.listdir(sys.argv[1]))):
    pathToTrace = sys.argv[1] + "\\" + os.listdir(sys.argv[1])[i]
    pathToText = sys.argv[2] + "\\" + os.listdir(sys.argv[2])[i]

#    with open(pathToTrace, "r") as tmpTraceFile:
#        tmpTrace = tmpTraceFile.read()

    with open(pathToText, "r") as tmpTextFile:
        tmpText = tmpTextFile.read()

#    tmpTraceFile.close()
    tmpTextFile.close()

#    pairsList.append(TextTracePair(tmpText, tmpTrace, pathToText, pathToTrace))
    pairsList.append(TextTracePair(tmpText, pathToText, pathToTrace))
    pairsList[i].setTrace(pathToTrace)

    pairsList[i].setMean()
    pairsList[i].setVariance()
    meanList.append(pairsList[i].getMean())

var = statistics.variance(meanList)

for i in range(len(os.listdir(sys.argv[1]))):

    tmpNicv = var / pairsList[i].getVariance()
    pairsList[i].setNicv(tmpNicv)

    print ((pairsList[i].getNicv()))"""