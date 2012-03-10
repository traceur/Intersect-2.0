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


