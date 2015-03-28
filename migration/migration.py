import os
import sys
import struct
import re
import psycopg2

print 'Initialize db connection: Start'
conn = psycopg2.connect(
	host = '127.0.0.1',
	database = 'scapack',
	user = 'postgres',
	password = 'postgres'
)
cursor = conn.cursor()
print 'Initialize db connection: Done'

lenDir = len(os.listdir(sys.argv[1]))
listDir = os.listdir(sys.argv[1])
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

    buffer = struct.pack('i'*len_lines, *lines)
    key = re.search('(?<=k=)(.*)(?=_m)', fileName).group(0)
    message = re.search('(?<=m=)(.*)(?=_c)', fileName).group(0)
    cipher = re.search('(?<=c=)(.*)(?=\.)', fileName).group(0)

    print 'File number: ', i, '/', lenDir

    query = "INSERT INTO trace (name, data, key, message, cipher) VALUES (%s,  %s, %s, %s, %s);"
    content = (fileName, buffer.encode('hex_codec'), key, message, cipher)

    cursor.execute(query, content)

    print '------------------------------------------------'
    print 'key: ', key
    print 'message: ', message
    print 'cipher: ', cipher
    print fileName + '\nDone'

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