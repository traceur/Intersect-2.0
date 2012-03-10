def NetworkInfo():
   print("[+] Collecting network info: services, ports, active connections, dns, gateways, etc...")
   os.mkdir(Temp_Dir+"/network")
   networkdir = (Temp_Dir+"/network")
   os.chdir(networkdir) 

   proc = Popen('netstat --tcp --listening',
        shell=True,
        stdout=PIPE,
        )
   output = proc.communicate()[0]

   file = open("nstat.txt","a")
   for items in output:
       file.write(items),
   file.close() 

   os.system("lsof -nPi > lsof.txt")
   ports = ["nstat.txt","lsof.txt"]
   content = ''
   for f in ports:
       content = content + '\n' + open(f).read()
   open('Connections.txt','wb').write(content)
   os.system("rm nstat.txt lsof.txt")
   os.system("iptables -L -n > iptablesLN.txt") 
   os.system("iptables-save > iptables_save.txt")
   os.system("ifconfig -a > ifconfig.txt")
   os.system("hostname -I > localIP.txt && hostname -f > hostname.txt")
   netfiles = ["localIP.txt","hostname.txt","ifconfig.txt"]
   content = ''
   for f in netfiles:
       content = content + '\n' + open(f).read()
   open('NetworkInfo.txt','wb').write(content)
   os.system("rm localIP.txt hostname.txt ifconfig.txt")

   network = [ "/etc/hosts.deny", "/etc/hosts.allow", "/etc/inetd.conf", "/etc/host.conf", "/etc/resolv.conf" ]
   for x in network:
       if os.path.exists(x) is True:
           shutil.copy2(x, networkdir)
   
