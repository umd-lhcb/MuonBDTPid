# Author: Alex Fernez

# wrapper to more easily manage filesystem stuff, calls copy_branches_for_ubdt.cpp
# meant to be run on glacier (where remote PID tuples are stored)

import os
import argparse

pid_path = '/home/public/pidcalib_ntuples'
remote_path = f'{pid_path}/remote'
new_remote_path = f'{pid_path}/remote-ubdt-only'
copy_script_path = '/home/alex/MuonBDTPid/scripts/copy_branches_for_ubdt.cpp'
particles = {'KPiMu', 'Mu_nopt', 'P'}
years = {'2017', '2018'}
pols = {'MagUp', 'MagDown'}

parser = argparse.ArgumentParser(description=f'Copy PIDCalib UBDT branches to {new_remote_path}')
parser.add_argument('--test', action='store_true', help='test, only copy 1 ntp')
args = parser.parse_args()

os.system(f'mkdir -p {new_remote_path}') # make folder if DNE
for particle in particles:
    for year in years:
        for pol in pols:
            os.system(f'mkdir -p {new_remote_path}/{particle}-{year}-{pol}')
            ntp_count = 0
            for file in os.listdir(f'{remote_path}/{particle}-{year}-{pol}'):
                if args.test and ntp_count > 0: continue
                os.system(f"root -l -q -e '.L {copy_script_path}' -e 'copy_branches_for_ubdt(" + f'"{remote_path}", "{new_remote_path}", "{particle}-{year}-{pol}/{file}")' + "'")
                ntp_count += 1