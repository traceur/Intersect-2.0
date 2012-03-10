def NetworkMap():
   # Combine ARP then portscan. Send IPs to list and iterate through for the scan
   # Add service identification via socket for all open ports
   # Add traceroute after finding live hosts. Send all results to graph report.
   
    print("[+] Searching for live hosts...")
    os.mkdir(Temp_Dir+"/hosts")
    os.chdir(Temp_Dir+"/hosts")
    localIP = [x[4] for x in scapy.all.conf.route.routes if x[2] != '0.0.0.0'][0]
    splitIP = localIP.split('.')
    splitIP[3:] = (['0/24'])
    IPRange = '.'.join(splitIP)
    conf.verb=0
    ans,unans=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=IPRange),timeout=2)
    file = open("livehosts.txt", "a")
    file.write("LAN IP Range: " + IPRange +"\n\n")
    for snd,rcv in ans:
        mac_address=rcv.sprintf("%Ether.src%")
        ip_address=rcv.sprintf("%ARP.psrc%")
        #print rcv.sprintf("\n\n[+] Live Host\nMAC %Ether.src%\nIP: %ARP.psrc%\n ")
        file.write("\n\n[+] Live Host\nIP: "+ip_address + " MAC"+ mac_address + "\n")
    file.write("\n")
    file.close

    externalIP = ip = urllib2.urlopen("http://whatismyip.org").read()
    file = open("external.txt", "a")
    file.write("External IP Address: " + externalIP +"\n\n")
    file.close

# --------------- ARP scan then SYN scan each live IP ---------------------------------
#portscan  
#tcp = TCP(dport=[21,22,23,80,1433],sport=[53],flags="S",seq=40)
#ans,unans = sr(ip/tcp)
    
#for sent,rcvd in ans:
   #if not rcvd or rcvd.getlayer(TCP).flags != 0x12:
      #print str(sent.dport)+" : closed"
   #else:
      #services = socket.getservbyport(sent.dport)
      #print str(sent.dport)+" "+services+" : open"
      
#-----------------------------------Traceroute ---------------------------------------------    
#res,unans = traceroute(["target"],dport=[{"open ports from scan or port 80"}],maxttl=20,retry=-2
#
#
#------------------------------Get MAC addr-------------------------------------------------
## Don't need this snippet yet but it's here so I don't lose it
#
# data = commands.getoutput("ifconfig " + iface)
#  words = data.split()
#  found = 0
#  for x in words:
      #print x
#      if found != 0:
#         mac = x
#          break
#      if x == "HWaddr":
#          found = 1
#  if len(mac) == 0:
#      mac = 'Mac not found'
#  mac = mac[:17]
#  print mac
    
