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

    fsresult = parse_binary(raw_data)
    #print fsresult
    print raw_data
    print 'LEN: ', len(fsresult)
    time.sleep(5)

    query = "DELETE FROM trace WHERE kind = 'migtst'"
    cursor.execute(query)
    conn.commit()

    print 'DELETED'

    key = re.search('(?<=k=)(.*)(?=_m)', fileName).group(0)
    message = re.search('(?<=m=)(.*)(?=_c)', fileName).group(0)
    cipher = re.search('(?<=c=)(.*)(?=\.)', fileName).group(0)

#------------------------------------------- testing place

    raw_data = open(pathToTrace, "r").read()

    bytes = []
    lenbytes = len(raw_data)

    bytes = map(ord, raw_data)

    print bytes

    #encoded = raw_data.encode('hex')
    """
    lenn = len(encoded)/4
    buffer = []
    intencoded = []
    for j in range (lenn):
        intencoded.append(int(encoded[j*4:j*4+3], 16))

    buffer = struct.pack('>'+'h'*len(intencoded), *intencoded)

    """

    query = "INSERT INTO trace (name, data, key, message, cipher, kind) VALUES (%s, %s, %s, %s, %s, %s);"
    content = (fileName, bytearray(bytes), key, message, cipher, 'migtst')
    cursor.execute(query, content)
    conn.commit()

    print 'INSERTED'

    query = "SELECT message, cipher, data FROM trace WHERE kind = 'migtst'"
    cursor.execute(query)
    one = cursor.fetchone()
    msg, crypt, raw_data = one

    print 'SELECTED'

#------------------------------------------- testing place

    dbresult = parse_binary(raw_data)
    print dbresult
    print 'LEN: ', len(dbresult)

"""

    encoded = lines.encode('hex')
    lenn = len(encoded)/4
    #print lenn
    buffer = []
    intencoded = []
    for j in range (lenn):
        intencoded.append(int(encoded[j*4:j*4+3], 16))

    buffer = struct.pack('>'+'h'*len(intencoded), *intencoded)

    #print buffer
    #del lines[0:24]
    #len_lines = len(lines)

    #for j in range(len(buffer)):
        #buffer[j] = int(buffer[j])
    #len_lines = len(lines)

    #buffer = struct.pack('h'*len_lines, *lines)

    #print str(buffer)

    #print len(lines)
    #print lines.encode('hex_codec')
    #print lines
    #lenn = len(lines)
    #buffer = []
    #for i in range (lenn):
    #    buffer.append(struct.pack('h', lines[i*8:i*8+4]))

    #print buffer
    #print lines.encode('hex_codec')
    #sys.exit()

    key = re.search('(?<=k=)(.*)(?=_m)', fileName).group(0)
    message = re.search('(?<=m=)(.*)(?=_c)', fileName).group(0)
    cipher = re.search('(?<=c=)(.*)(?=\.)', fileName).group(0)
    #hex_buffer = ''.join( [ "%02X " % ord( x ) for x in buffer ] ).strip()
    #print sys.getsizeof(hex_buffer)

    query = "INSERT INTO trace (name, data, key, message, cipher, kind) VALUES (%s, %s, %s, %s, %s, %s);"
    content = (fileName, buffer.encode('hex_codec'), key, message, cipher, 'des_third')
    #content = (fileName, lines, key, message, cipher, 'des_first')

    print 'File number: ', i, '/', lenDir

    cursor.execute(query, content)

    #print '------------------------------------------------'
    #print 'key: ', key
    #print 'message: ', message
    #print 'cipher: ', cipher

conn.commit()
print 'COMMIT IT!'
"""