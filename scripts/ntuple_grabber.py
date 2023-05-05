#!/usr/bin/env python
# Author: Emily Jiang
# Last Change: Wed Jun 08, 2022 at 04:49 AM -0400
#
# Description: Parse a yaml file containing the location of files on lxplus,
#              copying them to a glacier directory (also specified in yaml)

import argparse
import subprocess
import yaml


parser = argparse.ArgumentParser(description="Download PIDCalib ntuples from lxplus.")
parser.add_argument(
    "--ymlName",
    help="path to YAML file containing directories of files to be downloaded",
)
parser.add_argument("--lxplusUser", help="your username for remote host")
parser.add_argument(
    "--host",
    default="lxplus.cern.ch",
    help="specify remote host name (default to lxplus)",
)
parser.add_argument("--dryRun", action="store_true", help="dry run")
args = parser.parse_args()


with open(args.ymlName, "r") as stream:
    config = yaml.safe_load(stream)

for species, directive in config["data"].items():
    for mag, remoteBaseDir in directive.items():
        localDir = f"{config['local_ntuple_folders']['remote']}/{species}-{mag}/"
        remoteDir = f"{args.lxplusUser}@{args.host}:{remoteBaseDir}/"

        if args.dryRun:
            print(f"mkdir -p {localDir}")
            print(f"rsync -a {remoteDir} {localDir}")
        else:
            subprocess.run(["mkdir", "-p", localDir])
            subprocess.run(["rsync", "-a", remoteDir, localDir])
