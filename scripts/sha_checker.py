import os
import yaml
import hashlib

with open('/home/ejiang/MuonBDTPid/spec/pidcalib.yml', 'r') as stream:
    files = yaml.safe_load(stream)

for decay in files["data"]:
    for folder in files["data"][decay]:
        for mag in files["data"][decay][folder]:
            localDir = files["local_ntuple_folders"][folder]+"/"+decay+"-"+mag
            remoteDir = "ejiang@lxplus.cern.ch:"+files["data"][decay][folder][mag]+"/"
            for filename in os.listdir(localDir):
                fLocal = localDir+"/"+filename
                with open(fLocal, "rb") as f:
                    bytes = f.read()
                    hash = hashlib.sha256(bytes).hexdigest()
                    hash_file.write(hash+"\n")
    
with (
        open('/home/ejiang/MuonBDTPid/hash_file_final.txt') as local,
        open("/home/ejiang/MuonBDTPid/mu_down.txt") as muDown,
        open("/home/ejiang/MuonBDTPid/mu_up.txt") as muUp,
        open("/home/ejiang/MuonBDTPid/kpi_down.txt") as kpiDown,
        open("/home/ejiang/MuonBDTPid/kpi_up.txt") as kpiUp,
        open("/home/ejiang/MuonBDTPid/p_down.txt") as pDown,
        open("/home/ejiang/MuonBDTPid/p_up.txt") as pUp
):
    muDownLines = muDown.read().splitlines()
    muUpLines = muUp.read().splitlines()
    kpiDownLines = kpiDown.read().splitlines()
    kpiUpLines = kpiUp.read().splitlines()
    pDownLines = pDown.read().splitlines()
    pUpLines = pUp.read().splitlines()
    readLocal = local.read()
    for line in muDownLines:
        if line in readLocal:
            continue
        else:
            print(-1)
    for line in muUpLines:
        if line in readLocal:
            continue
        else:
            print(-1)
    for line in kpiDownLines:
        if line in readLocal:
            continue
        else:
            print(-1)
    for line in kpiUpLines:
        if line in readLocal:
            continue
        else:
            print(-1)
    for line in pDownLines:
        if line in readLocal:
            continue
        else:
            print(-1)
    for line in pUpLines:
        if line in readLocal:
            continue
        else:
            print(-1)
