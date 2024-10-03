#!/usr/bin/env python
# Author: Emily Jiang, Manuel Franco Sevilla
# Last Change: Sat Aug 06, 2022 at 06:35 PM -0400
#
# Description: Apply the UBDT to root files in directories specified by a yml
#              file (input), and write them to specified output directory.

from subprocess import Popen, PIPE, STDOUT
import argparse
import yaml
import os
import uproot

from glob import glob
from os.path import basename


#################################
# Command line arguments parser #
#################################

def parseInput():
    parser = argparse.ArgumentParser(description="Apply UBDT to PIDCalib ntuples.")
    parser.add_argument('-y', '--ymlName', help="path to YAML file containing directories of files to be downloaded")
    parser.add_argument('-d', "--dryRun", action="store_true", help="dry run")

    return parser.parse_args()


## Add colors for terminal output
def cTerm(msg, color):
    num = 30
    if color == 'red':     num = 91
    if color == 'green':   num = 92
    if color == 'yellow':  num = 93
    if color == 'blue':    num = 94
    if color == 'magenta': num = 95
    if color == 'cyan':    num = 96
    return f'\033[{num};1m{msg}\033[0m'

########
# Main #
########

if __name__ == '__main__':
    args = parseInput()
    
    with open(args.ymlName, "r") as stream:
        config = yaml.safe_load(stream)
    
    if not args.dryRun:
        retCode = os.system('make')
        if retCode != 0:
            print(cTerm('Compilation failed', 'red'))
            sys.exit(1)
            
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

                    ## Finding trees in the ntuple
                    trees = []
                    for tname in rootFile:
                        if 'DecayTree' not in tname: continue
                        newtree = tname.split(';')[0] # Remove the ";#" after the tree name  
                        if newtree not in trees: trees.append(newtree)
                    trees = ",".join(trees)
    
                    # Call UBDT
                    cmd = f'./bin/AddUBDTBranchRun2PidCalib -i {fInput} -o {fOutput} -p probe -b UBDT '
                    cmd += f'-t {trees} -x weights/weights_run2_all_cuts_ubdt.xml'
    
                    if not args.dryRun:
                        print(cTerm(cmd,'magenta'))
                        retCode = os.system(cmd)
                        if retCode != 0:
                            print(f"  WARNING: {cmd} did not execute properly!")
    
            except KeyboardInterrupt:
                break
