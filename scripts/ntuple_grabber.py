#!/usr/bin/env python
# Author: Emily Jiang
# Last Change: Wed Jun 08, 2022 at 02:40 AM -0400
#
# Description: Parse a yaml file containing the location of files on lxplus,
#              copying them to a glacier directory (also specified in yaml)

import argparse
import subprocess
import yaml

parser = argparse.ArgumentParser(
    description="Process yml filename and lxplus username."
)
parser.add_argument(
    "--ymlName",
    help="path to YAML file containing directories of files to be downloaded",
)
parser.add_argument("--lxplusUser", help="your username for remote host")
parser.add_argument(
    "--host",
    default="lxplus.cern.ch",
    help="specify remote host name (default to lxplus)"
)
args = parser.parse_args()

with open(args.ymlName, "r") as stream:
    files = yaml.safe_load(stream)

for decay in files["data"]:
    for folder in files["data"][decay]:
        for mag in files["data"][decay][folder]:
            localDir = files["local_ntuple_folders"][folder] + "/" + decay + "-" + mag
            remoteDir = (
                f"{args.lxplusUser}@{args.host}:"
                + files["data"][decay][folder][mag]
                + "/"
            )
            subprocess.run(["mkdir", "-p", localDir])
            subprocess.run(["rsync", "-a", remoteDir, localDir])
