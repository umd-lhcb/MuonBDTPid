#!/usr/bin/env python
# Author: Emily Jiang
# Last Change: Tue Jun 07, 2022 at 08:08 PM -0400
#
# Description: to use this script, first generate shasum txt files on lxplus
#              with naming conventions outlined in MuonBDTPid/spec/pidcalib.yml,
#              e.g. Mu_nopt-2016-MagDown. Then download to your local copy of
#              MuonBDTPid.
#
#              I did this by directory, splitting up the decays and the
#              magnetization, since lxplus was complaining about memory usage.
#              This script checks the hash file generated for the original files
#              with the copied files to make sure nothing went wrong.
#
# Instructions: on lxplus, generate shasum txt files with naming conventions
#               outlined in MuonBDTPid/spec/pidcalib.yml, e.g.
#               Mu_nopt-2016-MagDown. I did this one by one, since I was having
#               trouble with memory usage on lxplus trying to do everything at
#               once.

import argparse
import os
import yaml
import hashlib


parser = argparse.ArgumentParser(description="Process yml filename.")
parser.add_argument(
    "--ymlName",
    type=str,
    help="path to YAML file containing directories of files to be downloaded",
)
args = parser.parse_args()

with open(args.ymlName, "r") as stream:
    files = yaml.safe_load(stream)

local = open("/home/ejiang/MuonBDTPid/hash_file_final.txt")
readLocal = local.read()


for decay in files["data"]:
    for folder in files["data"][decay]:
        for mag in files["data"][decay][folder]:
            with open(
                "/home/ejiang/MuonBDTPid/" + decay + "-" + mag + ".txt"
            ) as remote:
                remoteLines = remote.read().splitlines()
                for line in remoteLines:
                    if line in readLocal:
                        continue
                    else:
                        print(-1)
