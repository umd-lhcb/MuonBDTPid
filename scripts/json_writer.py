#!/usr/bin/env python
# Author: Emily Jiang
# Last Change: Wed Jun 08, 2022 at 05:11 AM -0400

import argparse
import os
import json
import yaml


parser = argparse.ArgumentParser(
    description="Generate PIDCalib file location JSON file."
)
parser.add_argument(
    "--ymlName",
    help="path to YAML file containing directories of files to be downloaded",
)
parser.add_argument(
    "--outputJson",
    help="path to output JSON",
)
args = parser.parse_args()


with open(args.ymlName, "r") as stream:
    config = yaml.safe_load(stream)

jsonDict = {}

for species, directive in config["data"].items():
    for mag, remoteBaseDir in directive.items():
        localDir = f"{config['local_ntuple_folders']['remote']}/{species}-{mag}"
        mergedDir = f"{config['local_ntuple_folders']['merged']}/{species}-{mag}"

        files = []
        for filename in os.listdir(localDir):
            files.append(mergedDir + filename)

        jsonDict[species + "-" + mag] = {}
        jsonDict[species + "-" + mag]["files"] = files


# Writing to a output JSON file
with open(args.outputJson, "w") as outfile:
    outfile.write(json.dumps(jsonDict, indent=4))
