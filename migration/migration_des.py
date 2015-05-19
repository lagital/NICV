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

    pathToTrace = sys.argv[1] + "/" + fileName
    raw_data = open(pathToTrace, "r").read()
    bytes = []

    bytes = map(ord, raw_data)

    key = re.search('(?<=k=)(.*)(?=_m)', fileName).group(0)
    message = re.search('(?<=m=)(.*)(?=_c)', fileName).group(0)
    cipher = re.search('(?<=c=)(.*)(?=\.)', fileName).group(0)

    query = "INSERT INTO trace (name, data, key, message, cipher, kind) VALUES (%s, %s, %s, %s, %s, %s);"
    content = (fileName, bytearray(bytes), key, message, cipher, 'des_second')
    cursor.execute(query, content)

    print 'File number: ', i, '/', lenDir

conn.commit()
print 'COMMIT IT!'