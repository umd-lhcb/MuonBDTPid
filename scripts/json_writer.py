#!/usr/bin/env python
# Author: Emily Jiang
# Last Change: Mon Jun 13, 2022 at 01:08 PM -0400

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
    for mag in directive:
        mergedDir = f"{config['local_ntuple_folders']['merged']}/{species}-{mag}"

        files = []
        for filename in os.listdir(mergedDir):
            files.append(mergedDir + filename)

        year, polarity = mag.split("-")
        year = year[2:]

        if species in ["Mu_nopt", "P"]:
            key = f"Turbo{year}-{polarity}-{species}"
            jsonDict[key] = {"files": files}
        elif species == "KPiMu":
            for part in ["K", "Pi", "Mu"]:
                key = f"Turbo{year}-{polarity}-{part}"
                jsonDict[key] = {"files": files}


# Writing to a output JSON file
with open(args.outputJson, "w") as outfile:
    outfile.write(json.dumps(jsonDict, indent=4))
