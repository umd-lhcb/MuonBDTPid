#!/usr/bin/env python                                                                                                       
# Author: Emily Jiang                                                                                                       
# Last Change: Tues May 10, 2022 at 02:24 PM +0100                                                                          
#                                                                                                                           
# Description: Apply the UBDT to root files in directories specified by a yml file (input), and write them to specified
# output directory.

import argparse
import yaml
import os
import uproot

parser = argparse.ArgumentParser(description='Process yml filename.')
parser.add_argument('--ymlName', type=str,
                    help='path to YAML file containing directories of files to be downloaded')
args = parser.parse_args()

with open(args.ymlName, 'r') as stream:
    files = yaml.safe_load(stream)
    
for decay in files["data"]:
    for folder in files["data"][decay]:
        i = 0
        for mag in files["data"][decay][folder]:
            inputDir = files["local_ntuple_folders"][folder]+"/"+decay+"-"+mag
            outputDir = files["local_ntuple_folders"]["friends"]+"/"+decay+"-"+mag
            #i = 0
            os.system("mkdir -p "+outputDir)
            for filename in os.listdir(inputDir):
                fInput = inputDir+"/"+filename
                fOutput = outputDir+"/"+filename
                # Get names of trees--only need to do this once per decay, hence the counter
                if i==0:
                    rootFile = uproot.open(fInput)
                    trees = []
                    for tree in rootFile.keys():
                        if "DecayTree" in tree:
                            trees.append(tree.replace(';1',''))
                            print(trees)
                    i=1

                #Call BDT
                cmd = "AddUBDTBranchPidCalib -i "+fInput+" -o "+fOutput+" -p probe -b UBDT -t "
                for tree in trees:
                    cmd=cmd+tree+","
                #cmd=cmd[:-1]
                print(cmd)
                ret_code = os.system(cmd)
                if ret_code!=0:
                    print("WARNING: "+cmd+" did not execute properly!")
