import os
import sys
import struct
import re
import psycopg2
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

    #tmp_file = open(sys.argv[1] + 'tmp_file.tmp', 'w+')
    pathToTrace = sys.argv[1] + "/" + fileName
    lines = open(pathToTrace, "r").read().splitlines()

    del lines[0:24]
    len_lines = len(lines)

    for j in range(len_lines):
        lines[j] = int(lines[j])
    len_lines = len(lines)

    #buffer = struct.pack('<'+'h'*len_lines, *lines)

    buffer = struct.pack('h'*len_lines, *lines)

    #print str(buffer)

    #print fileName

    key = re.search('(?<=k=)(.*)(?=_m)', fileName).group(0)
    message = re.search('(?<=m=)(.*)(?=_c)', fileName).group(0)
    cipher = re.search('(?<=c=)(.*)(?=\.)', fileName).group(0)
    #hex_buffer = ''.join( [ "%02X " % ord( x ) for x in buffer ] ).strip()
    #print sys.getsizeof(hex_buffer)
    query = "INSERT INTO trace2 (name, data, key, message, cipher) VALUES (%s,  %s, %s, %s, %s);"
    content = (fileName, buffer.encode('hex_codec'), key, message, cipher)

    print 'File number: ', i, '/', lenDir

    cursor.execute(query, content)

    #print '------------------------------------------------'
    #print 'key: ', key
    #print 'message: ', message
    #print 'cipher: ', cipher

conn.commit()
print 'COMMIT IT!'

"""
    for j in range(len(lines)):
        lines[j] = "{0:b}".format(int(lines[j]))
        #print lines[j]
    tmp_file.write(str(lines))
    tmp_file.close()
    #[int(m) for m in lines]
    #for t in range (30):
    #    print

    with open(pathToTrace, "r") as tmpTraceFile:
        tmpArray = tmpTraceFile.readlines()
        tmpTrace = tmpTraceFile.read()
        #lines = (line.rstrip('\n') for line in open(pathToTrace, "r"))
        lines = open(tmpTraceFile).read().splitlines()
    tmpTraceFile.close()
for i in range (24):
    print lines[i]
"""
