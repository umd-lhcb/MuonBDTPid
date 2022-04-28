import yaml
import subprocess
import os

with open('/home/ejiang/MuonBDTPid/spec/pidcalib.yml', 'r') as stream:
    files = yaml.safe_load(stream)
    
for decay in files["data"]:
    for folder in files["data"][decay]:
        for mag in files["data"][decay][folder]:
            localDir = files["local_ntuple_folders"][folder]+"/"+decay+"-"+mag
            remoteDir = "ejiang@lxplus.cern.ch:"+files["data"][decay][folder][mag]+"/"
            subprocess.run(["mkdir", "-p", localDir])
            subprocess.run(["rsync", "-a", remoteDir, localDir])    
           
