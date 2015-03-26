import os
import sys
import struct
import re
import psycopg2

conn = psycopg2.connect(
	host = '127.0.0.1',
	database = 'scapack',
	user = 'postgres',
	password = 'postgres'
)

cursor = conn.cursor()

for i in range(len(os.listdir(sys.argv[1]))):
    fileName = os.listdir(sys.argv[1])[i]
    if os.listdir(sys.argv[1])[i] != 'tmp_file.tmp':
        tmp_file = open(sys.argv[1] + 'tmp_file.tmp', 'w+')
        pathToTrace = sys.argv[1] + "/" + fileName
        lines = open(pathToTrace, "r").read().splitlines()

        del lines[0:24]
        len_lines = len(lines)

        for j in range(len_lines):
            lines[j] = int(lines[j])
        len_lines = len(lines)

        buffer = struct.pack('i'*len_lines, *lines)
        tmp_file.seek(0)
        tmp_file.truncate()
        tmp_file.write(buffer)

        key = re.search('(?<=k=)(.*)(?=_m)', fileName).group(0)
        message = re.search('(?<=m=)(.*)(?=_c)', fileName).group(0)
        cipher = re.search('(?<=c=)(.*)(?=\.)', fileName).group(0)

        fileData = tmp_file.read()

        query = "INSERT INTO trace (name, data, key, message, cipher) VALUES (%s,  %s, %s, %s, %s);"
        content = (fileName, fileData, key, message, cipher)

        tmp_file.close()

        cursor.execute(query, content)

        conn.commit()

        print '------------------------------------------------'
        print 'key: ', key
        print 'message: ', message
        print 'cipher: ', cipher
        print fileName + '\nDone'

    """
    for j in range(len(lines)):
        lines[j] = "{0:b}".format(int(lines[j]))
        #print lines[j]
    tmp_file.write(str(lines))
    tmp_file.close()
    #[int(m) for m in lines]
    #for t in range (30):
    #    print
    """
    """
    with open(pathToTrace, "r") as tmpTraceFile:
        tmpArray = tmpTraceFile.readlines()
        tmpTrace = tmpTraceFile.read()
        #lines = (line.rstrip('\n') for line in open(pathToTrace, "r"))
        lines = open(tmpTraceFile).read().splitlines()
    tmpTraceFile.close()
    """
    """
for i in range (24):
    print lines[i]
    """