import os
import sys
import struct
import time
import re
import psycopg2
from parse_binary import parse_binary
from array import array
import binascii

print 'Initialize db connection: Start'
conn = psycopg2.connect(
	host = '127.0.0.1',
	database = 'scapack',
	user = 'postgres',
	password = 'postgres'
)
cursor = conn.cursor()
print 'Initialize db connection: Done'

listDir = os.listdir(sys.argv[1])
lenDir = len(listDir)

print 'Files for migration: ', lenDir


for i in range(lenDir):

    fileName = listDir[i]

    #pathToTrace = sys.argv[1] + "/" + fileName
    #raw_data = open(pathToTrace, "r").read()

    query = "SELECT message, cipher, data FROM trace WHERE name = '"+listDir[i]+"'"
    cursor.execute(query)
    one = cursor.fetchone()
    msg, crypt, raw_data = one

    #print 'SELECTED'

#------------------------------------------- testing place

    dbresult = parse_binary(raw_data)
    #print dbresult
    #print 'LEN: ', len(dbresult)
    print 'finished: ', i