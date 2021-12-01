#!/usr/bin/env python
# Author: Yipeng Sun
# Last Change: Wed Dec 01, 2021 at 02:02 AM +0100
#
# Description: Plot the following form-factor related figures
#              - q2, normalized
#              - FF weights
#              - line shapes of various D**, normalized

import os
import uproot

from pyTuplingUtils.io import read_branch as readBr


###########
# Helpers #
###########

def runCmd(cmd):
    print(cmd)
    os.system(cmd)


#########
# Plots #
#########

def plotComp(ntp1, br1, ntp2, br2, output,
             tree='Jpsinopt_MuMTuple/DecayTree', labels=[],
             normalize=True, wtBr='wff', xRange=None):
    cmd = fr'''
        plotbr -o {output} \
            -n {ntp1}/{tree} -b {br1} -l "{labels[0]}" \
            -n {ntp2}/{tree} -b {br2} -l "{labels[1]}" \
            --title "Jpsi nopt MuM"'''

    if normalize:
        cmd += ' --normalize -YL "Normalized"'

    if xRange:
        xRange = ' '.join([str(i) for i in xRange])
        cmd += f' -XD {xRange}'

    runCmd(cmd)


ntpOld = '../samples/Jpsi--21_02_05--pidcalib--data_turbo--2016--mu--Mu_nopt-subset.root'
ntpNew = '../samples/Jpsi--21_11_30--pidcalib--data_turbo--2016--mu--Mu_nopt-subset.root'

brPref1 = 'probe_Brunel_ANNTraining_'
brPref2 = 'probe_Brunel_'
ubdtInputBrs = [
    ("TrackChi2PerDof", brPref1+"TrackChi2PerDof"),
    ("TrackNumDof", brPref1+"TrackNumDof"),
    ("TrackGhostProbability", brPref1+"TrackGhostProb"),
    ("TrackFitMatchChi2", brPref1+"TrackFitMatchChi2"),
    ("TrackFitVeloChi2", brPref1+"TrackFitVeloChi2"),
    ("TrackFitVeloNDoF", brPref1+"TrackFitVeloNDoF"),
    ("TrackFitTChi2", brPref1+"TrackFitTChi2"),
    ("TrackFitTNDoF", brPref1+"TrackFitTNDoF"),
    ("RichUsedR1Gas", brPref2+"RICH1GasUsed"),
    ("RichUsedR2Gas", brPref2+"RICH2GasUsed"),
    ("RichAboveMuThres", brPref2+"RICHThresholdMu"),
    ("RichAboveKaThres", brPref2+"RICHThresholdKa"),
    ("RichDLLe", brPref1+"RichDLLe"),
    ("RichDLLmu", brPref1+"RichDLLmu"),
    ("RichDLLk", brPref1+"RichDLLk"),
    ("RichDLLp", brPref1+"RichDLLp"),
    ("RichDLLbt", brPref1+"RichDLLbt"),
    ("MuonBkgLL", brPref1+"MuonLLBkg"),
    ("MuonMuLL", brPref1+"MuonLLMu"),
    ("MuonNShared", brPref1+"MuonNShared"),
    ("InAccEcal", brPref1+"InAccEcal"),
    ("EcalPIDe", brPref1+"EcalPIDe"),
    ("EcalPIDmu", brPref1+"EcalPIDmu"),
    ("InAccHcal", brPref1+"InAccHcal"),
    ("HcalPIDe", brPref1+"HcalPIDe"),
    ("HcalPIDmu", brPref1+"HcalPIDmu"),
    ("InAccPrs", brPref1+"InAccPrs"),
    ("PrsPIDe", brPref1+"PrsPIDe"),
    ("InAccBrem", brPref1+"InAccBrem"),
    ("BremPIDe", brPref1+"BremPIDe"),
    ("VeloCharge", brPref1+"VeloCharge"),
    ("probe_isMuonTight", "probe_Brunel_isMuonTight"),
    ("TrackP", brPref1+"TrackP"),
    ("TrackPt", brPref1+"TrackPt"),
]

ntpOldLoaded = uproot.open(ntpOld)

for (varOld, varNew) in ubdtInputBrs:
    legendOld = varOld.replace('probe', 'P')
    legendNew = varNew.replace('probe_Brunel', 'PB').replace(
        'ANNTraining', 'A')
    tree = 'Jpsinopt_MuMTuple/DecayTree'

    brOld = readBr(ntpOldLoaded, tree, varOld)
    xRange = [brOld.min(), brOld.max()]

    outputFigName = f'../gen/{varOld}_MuM.png'
    plotComp(ntpOld, varOld, ntpNew, varNew, outputFigName,
             tree=tree, labels=[legendOld, legendNew], xRange=xRange)
