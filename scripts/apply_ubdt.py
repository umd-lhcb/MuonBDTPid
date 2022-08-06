#!/usr/bin/env python
# Author: Emily Jiang
# Last Change: Sat Aug 06, 2022 at 06:35 PM -0400
#
# Description: Apply the UBDT to root files in directories specified by a yml
#              file (input), and write them to specified output directory.

import argparse
import yaml
import os
import uproot

from glob import glob
from os.path import basename


parser = argparse.ArgumentParser(description="Apply UBDT to PIDCalib ntuples.")
parser.add_argument(
    "--ymlName",
    help="path to YAML file containing directories of files to be downloaded",
)
parser.add_argument("--dryRun", action="store_true", help="dry run")

args = parser.parse_args()


with open(args.ymlName, "r") as stream:
    config = yaml.safe_load(stream)

for species, directive in config["data"].items():
    for mag, remoteBaseDir in directive.items():
        try:
            inputDir = f"{config['local_ntuple_folders']['remote']}/{species}-{mag}/"
            outputDir = f"{config['local_ntuple_folders']['friends']}/{species}-{mag}/"
            os.system("mkdir -p " + outputDir)
            print(f"{inputDir} -> {outputDir}")

            for fInput in glob(inputDir + "*.root"):
                fOutput = outputDir + basename(fInput)
                rootFile = uproot.open(fInput)
                trees = [t.replace(";1", "") for t in rootFile if "DecayTree" in t]
                trees = ",".join(trees)
                print(f"  trees: {trees}")

                # Call UBDT
                cmd = f"  AddUBDTBranchPidCalib -i {fInput} -o {fOutput} -p probe -b UBDT -t {trees}"
                print(cmd)

                if not args.dryRun:
                    retCode = os.system(cmd)
                    if retCode != 0:
                        print(f"  WARNING: {cmd} did not execute properly!")

        except KeyboardInterrupt:
            break
