#!/usr/bin/env python
# Author: Emily Jiang
# Last Change: Wed Jun 08, 2022 at 03:34 AM -0400
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
import hashlib
import yaml

from glob import glob
from os.path import basename


parser = argparse.ArgumentParser(
    description="Generate local hash and optionally compare w/ remote."
)
parser.add_argument(
    "--ymlName",
    help="path to YAML file containing directories of files to be downloaded",
)
parser.add_argument("--localFileHashes", help="path to store local file hashes")
parser.add_argument(
    "--remoteFileHashes",
    default=None,
    help="path to YAML file containing hashes to remote files",
)
args = parser.parse_args()


def computeHash(filePath):
    hashVal = hashlib.sha256()
    # Don't read the whole file into RAM! do it chunk by chunk!
    with open(filePath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hashVal.update(chunk)
    return hashVal.hexdigest()


with open(args.ymlName, "r") as stream:
    config = yaml.safe_load(stream)

remoteHashMap = None
if args.remoteFileHashes:
    with open(args.remoteFileHashes, "r") as stream:
        remoteHashMap = yaml.safe_load(stream)

outputHashMap = dict()

for folder in glob(config["local_ntuple_folders"]["remote"] + "/*"):
    print(f"Working in {folder}...")
    keyName = basename(folder)
    result = dict()

    for fileName in glob(folder + "/*.root"):
        fileKey = basename(fileName)
        fileHash = computeHash(fileName)
        result[fileKey] = fileHash

        # compare hash if the remote file hash YAML is supplied
        if remoteHashMap:
            remoteHash = ""
            try:
                remoteHash = remoteHashMap[keyName][fileKey]
            except KeyError:
                print(f"  WARNING: unknown key: {keyName}-{fileKey}")

            try:
                assert fileHash == remoteHash
            except AssertionError:
                print(f"  WARNING: {keyName}/{fileKey} hash is inconsistent!")
                print(f"    local : {fileHash}")
                print(f"    remote: {remoteHash}")


# save local hash into a YAML file
with open(args.localFileHashes, "w") as f:
    dump = yaml.dump(outputHashMap, default_flow_style=False)
    f.write(dump)
