import argparse
import yaml
import subprocess
import os
import json

parser = argparse.ArgumentParser(description='Process yml filename and lxplus username.')
parser.add_argument('--ymlName', type=str,
                    help='path to YAML file containing directories of files to be downloaded')
args = parser.parse_args()

with open(args.ymlName, 'r') as stream:
    files = yaml.safe_load(stream)

jsonDict = {}

for decay in files["data"]:
    for folder in files["data"][decay]:
        for mag in files["data"][decay][folder]:
            localDir = files["local_ntuple_folders"][folder]+"/"+decay+"-"+mag
            jsonDict[decay+"-"+mag] = {}
            jsonDict[decay+"-"+mag]["files"] = []

            for filename in os.listdir(localDir):
                jsonDict[decay+"-"+mag]["files"].append(filename)
#print(jsonDict)

json_object = json.dumps(jsonDict, indent = 4)
  
# Writing to sample.json
with open("samples.json", "w") as outfile:
    outfile.write(json_object)
