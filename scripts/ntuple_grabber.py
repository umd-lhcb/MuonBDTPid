import os
import yaml
import subprocess
import hashlib

with open('/home/ejiang/MuonBDTPid/spec/pidcalib.yml', 'r') as stream:
    files = yaml.safe_load(stream)

hash_file = open('/home/ejiang/MuonBDTPid/hash_file_final.txt', "a")
    
for decay in files["data"]:
    for folder in files["data"][decay]:
        for updown in files["data"][decay][folder]:
            localDir = files["local_ntuple_folders"][folder]+"/"+decay+"-"+updown
            remoteDir = "ejiang@lxplus.cern.ch:"+files["data"][decay][folder][updown]+"/"
            #subprocess.run(["mkdir", "-p", localDir])
            #subprocess.run(["rsync", "-a", remoteDir, localDir])    
            for filename in os.listdir(localDir):
                fLocal = localDir+"/"+filename
                with open(fLocal, "rb") as f:
                    bytes = f.read()
                    hash = hashlib.sha256(bytes).hexdigest()
                    hash_file.write(hash+"\n")
                print(fLocal+" done")
                #fRemote = remoteDir+filename
                #subprocess.run(["sha256sum", fLocal])
                #subprocess.Popen("sha256sum "+fLocal+" >> checksum", shell=True)

hash_file.close()
#clean up notation,                 
#print(filenames["data"]["Mu_nopt"]["remote"]["2016-MagDown"])
#subprocess.run(["mkdir", "-p", "/home/public/pidcalib_ntuples/remote/Mu_nopt-2016-MagDown"])
#subprocess.run(["rsync", "-a", "ejiang@lxplus.cern.ch:/eos/lhcb/grid/prod/lhcb/LHCb/Collision16/PIDCALIB.ROOT/00152085/0000/", "/home/public/pidcalib_ntuples/remote/Mu_nopt-2016-MagDown"])
#get all hashes, save to file, sort by filename? compare files with diff
#for filename in os.listdir(directory):
    

#subprocess.run(["mkdir", "-p", "/home/public/pidcalib_ntuples/remote/Mu_nopt-2016-MagUp"])
#subprocess.run(["rsync", "-a", "ejiang@lxplus.cern.ch:/eos/lhcb/grid/prod/lhcb/LHCb/Collision16/PIDCALIB.ROOT/00152087/0000/", "/home/public/pidcalib_ntuples/remote/Mu_nopt-2016-MagUp"])

#subprocess.run(["mkdir", "-p", "/home/public/pidcalib_ntuples/remote/KPiMu-2016-MagDown"])
#subprocess.run(["rsync", "-a", "-progress", "ejiang@lxplus.cern.ch:/eos/lhcb/grid/prod/lhcb/LHCb/Collision16/PIDCALIB.ROOT/00152077/0000/","/home/public/pidcalib_ntuples/remote/KPiMu-2016-MagDown"])

#subprocess.run(["mkdir", "-p", "/home/public/pidcalib_ntuples/remote/KPiMu-2016-MagUp"])
#subprocess.run(["rsync", "-a", "ejiang@lxplus.cern.ch:/eos/lhcb/grid/prod/lhcb/LHCb/Collision16/PIDCALIB.ROOT/00152079/0000/","/home/public/pidcalib_ntuples/remote/KPiMu-2016-MagUp"])

#subprocess.run(["mkdir", "-p", "/home/public/pidcalib_ntuples/remote/P-2016-MagDown"])
#subprocess.run(["rsync", "-a", "ejiang@lxplus.cern.ch:/eos/lhcb/grid/prod/lhcb/LHCb/Collision16/PIDCALIB.ROOT/00152081/0000/","/home/public/pidcalib_ntuples/remote/P-2016-MagDown"])

#subprocess.run(["mkdir", "-p", "/home/public/pidcalib_ntuples/remote/P-2016-MagUp"])
#subprocess.run(["rsync", "-a", "ejiang@lxplus.cern.ch:/eos/lhcb/grid/prod/lhcb/LHCb/Collision16/PIDCALIB.ROOT/00152083/0000/","/home/public/pidcalib_ntuples/remote/P-2016-MagUp"])
