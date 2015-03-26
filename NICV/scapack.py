#!/usr/bin/python

import sys
import peewee
from peewee import *
import os
import statistics
from TextTracePair import Trace_tmp
import mlpy

parameters = len(sys.argv)
code = None
top = 0

# <-- DATABASE INITIATION

db = MySQLDatabase('scapack', user='scapack', passwd='scapack')

class Trace(peewee.Model):

    original_path = peewee.CharField()
    code__id = peewee.IntegerField()
    clear_text = peewee.TextField()
    encr_text = peewee.TextField()
    nicv = peewee.FloatField()
    last_top = peewee.IntegerField()
    is_top = peewee.IntegerField()
    dwt_path = peewee.CharField()
    kalman_path = peewee.CharField()

    class Meta:
        database = db

class Code(peewee.Model):
    symbol = peewee.CharField()
    description = peewee.CharField()

    class Meta:
        database = db

""" code = Code(symbol='peet', description='Peewee is cool')
code.save()
for code in Code.filter(symbol='peet'):
    print code.description """

# DATABASE INITIATION -->

# <-- PROCEDURES INITIATION
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
    print('-load code \path_to_traces [\path_to_clear_texts] [\path_to_encr_texts]')
    print('load traces to database marking with chosen code.')
    print('Attention: text file should have the same name as corresponding trace.')
    print('')
    print('-kalman code < kalman transform on traces with chosen code.')
    print('')
    print('-dwt code < discrete wavelet transform on traces with chosen code.')

# PROCEDURES INITIATION -->

# <-- MAIN

if parameters == 1 or sys.argv[1] == '-help':
    print_help()

elif sys.argv[1] == '-nicv':
    if parameters < 4 or parameters > 6:
        print_help()
    elif sys.argv[3] == '-c':
        meanList = []
        traceList = []
        code_id = Code.get(Code.symbol == sys.argv[2]).id
        top = sys.argv[4]
        print('-nicv code -c top')
        if parameters == 6 and sys.argv[5] == '-kalman':
            print('I\'m in NICV for kalman!')
            print('TODO: NICV calculating on kalman transformed traces')
            #TODO: NICV calculating on kalman transformed traces
        elif parameters == 6 and sys.argv[5] == '-dwt':
            print('I\'m in NICV for dwt!')
            print('TODO: NICV calculating on dwt transformed traces')
            #TODO: NICV calculating on dwt transformed traces
        else:
            for i in Trace.select().where(Trace.code__id == code_id):
                print (i.original_path + '...')
                i = Trace_tmp(i.original_path)
                i.setMean()
                i.setVariance()
                meanList.append(i.getMean())
                traceList.append(i)

            i.draw(i.getTrace())

            mVariance = statistics.variance(meanList)

            for i in range(len(traceList)):

                traceList[i].setNicv(mVariance / traceList[i].getVariance())
                q = Trace.select().where(Trace.original_path == traceList[i].getPathToTrace()).get()
                q.nicv = traceList[i].getNicv()
                q.last_top = sys.argv[4]
                q.save() #Will do the SQL update query.

            print('I\'m in classic NICV!')
            print('TODO: NICV TOP + optimization + testing')
            #TODO: TODO: NICV TOP + optimization + testing'

    elif sys.argv[3] == '-s':
        code_id = Code.get(Code.symbol == sys.argv[2]).id
        print 'here'
        for i in Trace.select().where(Trace.code__id == code_id):
            print i.nicv, ' - top ', i.last_top

        print('I\'m in printing statistics of NICV!')
        print('TODO: testing.')
        #TODO: testing

elif sys.argv[1] == '-load':
    if parameters == 4:
        try:
            code = Code.get(symbol = sys.argv[2])
        except Code.DoesNotExist:
            q = Code(symbol = sys.argv[2], description = 'default')
            q.save()
        code_id = Code.get(Code.symbol == sys.argv[2]).id
        for i in range(len(os.listdir(sys.argv[3]))):
            pathToTrace = sys.argv[3] + "/" + os.listdir(sys.argv[3])[i]
            trace = Trace(original_path = pathToTrace, code__id = code_id)
            trace.save()

        print('I\'m loading traces!')
        print('TODO:loading clear and encr texts.')
        print('TODO:loading copying to path with original')
        #TODO: loading clear and encr texts.
        #TODO:loading copying to path with original

elif sys.argv[1] == '-kalman':
    if parameters == 3:
        code_id = Code.get(Code.symbol == sys.argv[2]).id
        print('I\'m in kalman!')
        print('TODO: kalman transformation.')
        #TODO: kalman transformation.

elif sys.argv[1] == '-dwt':
    if parameters == 3:
        code_id = Code.get(Code.symbol == sys.argv[2]).id
        for i in Trace.select().where(Trace.code__id == code_id):
            print (i.original_path + '...')
            i = Trace_tmp(i.original_path)
            i.setDwt()

        i.draw(i.getDwt())

        print('I\'m in dwt!')
        print('TODO: dwt transformation.')
        #TODO: dwt transformation.

elif sys.argv[1] == '-fft':
    if parameters == 3:
        code_id = Code.get(Code.symbol == sys.argv[2]).id
        for i in Trace.select().where(Trace.code__id == code_id):
            print (i.original_path + '...')
            i = Trace_tmp(i.original_path)
            i.setFft()
            #pathToFft = i.writeTrace(i.getFft())
            #Trace.update(i, fft = pathToFft)

        i.draw(i.getTrace())
        i.draw(i.getFft())

        print('I\'m in fft!')
        print('TODO: testing of fft transformation.')
        #TODO: testing of fft transformation.

# MAIN -->

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