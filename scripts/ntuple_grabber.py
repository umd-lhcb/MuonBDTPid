#!/usr/bin/env python
# Author: Emily Jiang
# Last Change: Tues May 10, 2022 at 02:24 PM +0100
#
# Description: Parse a yaml file containing the location of files on lxplus,
#              copying them to a glacier directory (also specified in yaml)

import argparse
import yaml
import subprocess

parser = argparse.ArgumentParser(
    description="Process yml filename and lxplus username."
)
parser.add_argument(
    "--ymlName",
    type=str,
    help="path to YAML file containing directories of files to be downloaded",
)
parser.add_argument("--lxplusUsr", type=str, help="your username for lxplus")
args = parser.parse_args()

with open(args.ymlName, "r") as stream:
    files = yaml.safe_load(stream)

for decay in files["data"]:
    for folder in files["data"][decay]:
        for mag in files["data"][decay][folder]:
            localDir = files["local_ntuple_folders"][folder] + "/" + decay + "-" + mag
            remoteDir = (
                args.lxplusUsr
                + "@lxplus.cern.ch:"
                + files["data"][decay][folder][mag]
                + "/"
            )
            subprocess.run(["mkdir", "-p", localDir])
            subprocess.run(["rsync", "-a", remoteDir, localDir])
