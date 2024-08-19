# Author: Alex Fernez

# Want to check that 2017-2018 KPiMu, P, Mu_noppt PIDCalib samples are ok:
#   - they should have the same tree structure as 2016 for all files
#   - all brs in 2016 should be present in 2017-2018 (ignore any new brs)
#   - all brs in trees should be nonempty and have nonzero mean/std, within reasonable margin from 2016 (slowest check, so don't do for every file)

# NEED TO USE ROOT6 TO BE ABLE TO OPEN 2017/2018 FILES

import ROOT
import os
import argparse
from copy import deepcopy

ROOT.gErrorIgnoreLevel = ROOT.kFatal

pid_path = '/home/public/pidcalib_ntuples'
remote_path = f'{pid_path}/remote'
particles = ['KPiMu', 'Mu_nopt', 'P']
years_check = ['2017', '2018']
year_ref = '2016'
pols = ['MagUp', 'MagDown']
margin = 0.2 # really just want to make sure things filled in correctly, 20% margin of error is ok I think

parser = argparse.ArgumentParser(description=f'Check 2017-2018 PIDCalib production, copied to {remote_path}')
parser.add_argument('--test', action='store_true', help='test, only check 1 ntp')
args = parser.parse_args()

missing_trees = {}
missing_branches = {}
bad_branches = {}
for particle in particles:
    for pol in pols:
        ntp_ref_path = f'{remote_path}/{particle}-{year_ref}-{pol}/' + os.listdir(f'{remote_path}/{particle}-{year_ref}-{pol}')[0]
        ntp_ref = ROOT.TFile(ntp_ref_path)
        trees_ref_copy = [tree.GetName() for tree in ntp_ref.GetListOfKeys()]
        trees_ref = deepcopy(trees_ref_copy)
        for tree in trees_ref_copy:
            if not 'Tuple' in tree: trees_ref.remove(tree)
        for year in years_check:
            print(f'\n\n----- Checking {particle} {pol} {year} -----\n\n')
            ntp_count = 0
            missing_trees[f'{particle}-{pol}-{year}'] = []
            missing_branches[f'{particle}-{pol}-{year}'] = {}
            bad_branches[f'{particle}-{pol}-{year}'] = {}
            for ntp_path in [f'{remote_path}/{particle}-{year}-{pol}/{ntp}' for ntp in os.listdir(f'{remote_path}/{particle}-{year}-{pol}')]:
                if ntp_path[-4:]!='root': continue # weird??
                if args.test and ntp_count > 0: continue
                ntp = ROOT.TFile(ntp_path)
                trees_copy = [tree.GetName() for tree in ntp.GetListOfKeys()]
                trees = deepcopy(trees_copy)
                for tree in trees_copy:
                    if not 'Tuple' in tree: trees.remove(tree)
                if len(trees) > len(trees_ref): print(f'Extra trees in {ntp_path} vs {ntp_ref_path}?\n')
                for tree in trees_ref:
                    if tree in missing_trees[f'{particle}-{pol}-{year}']: continue # already found that tree is missing
                    if not tree in trees:
                        if ntp_count > 0: print(f'Missing {tree} in {ntp_path}, but it was found in previous files in this folder??\n')
                        else: print(f'Missing {tree} in {ntp_path}?\n')
                        missing_trees[f'{particle}-{pol}-{year}'].append(tree)
                        continue
                    missing_branches[f'{particle}-{pol}-{year}'][tree] = []
                    bad_branches[f'{particle}-{pol}-{year}'][tree] = []
                    tr = ntp_ref.Get(f'{tree}/DecayTree')
                    t = ntp.Get(f'{tree}/DecayTree')
                    branches_ref = [br.GetName() for br in tr.GetListOfBranches()]
                    branches = [br.GetName() for br in t.GetListOfBranches()]
                    for branch in branches_ref:
                        if branch in missing_branches[f'{particle}-{pol}-{year}'][tree]: continue # already found that branch is missing
                        if not branch in branches:
                            if ntp_count > 0: print(f'Missing {branch} in {ntp_path}:{tree}, but it was found in previous files in this folder??\n')
                            else: print(f'Missing {branch} in {ntp_path}?\n')
                            missing_branches[f'{particle}-{pol}-{year}'][tree].append(branch)
                            continue
                        if ntp_count == 0: # for first file, check if branches all look reasonable
                            h_ref = ROOT.TH1D(f'{year_ref}-{tree}-{branch}', f'{year_ref}-{tree}-{branch}', 1, 0, 1e20)
                            tr.Draw(f'{branch}>>'+f'{year_ref}-{tree}-{branch}')
                            h = ROOT.TH1D(f'{year}-{tree}-{branch}', f'{year}-{tree}-{branch}', 1, 0, 1e20)
                            t.Draw(f'{branch}>>'+f'{year}-{tree}-{branch}')
                            if not h_ref.GetMean() == 0:
                                if (h_ref.GetMean() - h.GetMean()) / h_ref.GetMean() > margin: bad_branches[f'{particle}-{pol}-{year}'][tree].append(branch)
                            else:
                                if not h.GetMean() == 0: bad_branches[f'{particle}-{pol}-{year}'][tree].append(branch)
                            if not h_ref.GetStdDev() == 0:
                                if (h_ref.GetStdDev() - h.GetStdDev()) / h_ref.GetStdDev() > margin: bad_branches[f'{particle}-{pol}-{year}'][tree].append(branch)
                            else:
                                if not h.GetStdDev() == 0: bad_branches[f'{particle}-{pol}-{year}'][tree].append(branch)
                ntp_count += 1
print(f'Missing Trees:\n{missing_trees}')
print(f'Missing Branches:\n{missing_branches}')
print(f'Bad (mean or std > {round(margin*100)}% off ref) Branches:\n{bad_branches}')