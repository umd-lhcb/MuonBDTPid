#!/usr/bin/env python
# Author: Yipeng Sun
# Last Change: Thu Jun 09, 2022 at 03:14 AM -0400

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


def getTreeSpec(tree):
    raw = tree.typenames()
    return {k: v.replace("_t", "") for k, v in raw.items()}


with open(args.ymlName, "r") as stream:
    config = yaml.safe_load(stream)

stepSize = 200000  # FIXME: not ideal, but probably fine on our server
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
            mainRootFile = uproot.open(mainInput)
            trees = [t.replace(";1", "") for t in mainRootFile if "DecayTree" in t]

            with uproot.recreate(outputDir + ntpName) as outputRootFile:
                for t in trees:
                    print(f"    Merging tree: {t}")
                    treeSpec = getTreeSpec(mainRootFile[t])
                    treeSpec[args.branchName] = "float"
                    outputRootFile.mktree(t, treeSpec)

                    mainDF = uproot.iterate(
                        f"{mainInput}:{t}", step_size=stepSize, library="np"
                    )
                    friendDF = uproot.iterate(
                        f"{friendInput}:{t}",
                        [args.branchName],
                        step_size=stepSize,
                        library="np",
                    )

                    for m, f in zip(mainDF, friendDF):
                        m[args.branchName] = f[args.branchName]
                        print(f"    {f[args.branchName].size}")
                        outputRootFile[t].extend(m)

                if args.testRun:
                    sys.exit(0)
