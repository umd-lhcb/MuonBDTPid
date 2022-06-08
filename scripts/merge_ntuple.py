#!/usr/bin/env python
# Author: Yipeng Sun
# Last Change: Wed Jun 08, 2022 at 05:24 AM -0400

import argparse
import os
import sys
import yaml
import uproot

from glob import glob
from os.path import basename


parser = argparse.ArgumentParser(description="Merge UBDT branch to PIDCalib ntuples.")
parser.add_argument(
    "--ymlName",
    help="path to YAML file containing directories of files to be downloaded",
)
parser.add_argument("--testRun", action="store_true", help="just process 1 file")
parser.add_argument(
    "--branchName", default="probe_UBDT", help="specify UBDT branch name"
)

args = parser.parse_args()


with open(args.ymlName, "r") as stream:
    config = yaml.safe_load(stream)

for species, directive in config["data"].items():
    for mag, remoteBaseDir in directive.items():
        mainDir = f"{config['local_ntuple_folders']['remote']}/{species}-{mag}/"
        friendDir = f"{config['local_ntuple_folders']['friends']}/{species}-{mag}/"
        outputDir = f"{config['local_ntuple_folders']['merged']}/{species}-{mag}/"
        os.system("mkdir -p " + outputDir)
        print(f"Working in {outputDir}...")

        for mainInput in glob(mainDir + "*.root"):
            ntpName = basename(mainInput)
            print(f"  Working on {ntpName}...")

            friendInput = friendDir + ntpName
            fOutput = outputDir + basename(mainInput)

            mainRootFile = uproot.open(mainInput)
            trees = [t.replace(";1", "") for t in mainRootFile if "DecayTree" in t]
            print(f"    trees: {','.join(trees)}")

            friendRootFile = uproot.open(friendInput)

            outputRootFile = uproot.recreate(fOutput)
            for t in trees:
                mainContent = mainRootFile[t]
                mainContent[args.branchName] = friendRootFile[t][args.branchName]
                outputRootFile[t] = mainContent

            if args.testRun:
                sys.exit(0)
