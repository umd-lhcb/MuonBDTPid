# MuonBDTPid
Muon PID with a uboost BDT (in ROOT 5). Also include code for PID efficiency studies.

## PIDCalib samples
This is generated with `Castelao`.
Below we list some related links
- WG prodcution [twiki](https://twiki.cern.ch/twiki/bin/viewauth/LHCbPhysics/WGproductionPID)
- Calib sample modes and cuts [option file](https://gitlab.cern.ch/lhcb/Castelao/-/blob/master/PIDCalib/PidCalibProduction/options/Run-2/makeTuples.py)
- PIDCalib package [twiki](https://twiki.cern.ch/twiki/bin/view/LHCb/PIDCalibPackage)

## uboost BDT (uBDT)

### Required input variables
According to the [ANA note](https://github.com/umd-lhcb/group-talks/blob/master/ana_thesis/RD_RDst_ANA_21-01-05.pdf), p.16,
these are the input variables to the uBDT
(These names are also used in the [source](https://github.com/umd-lhcb/MuonBDTPid/blob/master/src/AddUboostBranchRun2.cpp)):

```
TrackChi2PerDof       -> TRCHI2NDOF
TrackNumDof           -> ?
TrackLikelihood       -> ?
TrackGhostProbability -> TRACK_GHOSTPROB
TrackFitMatchChi2     -> TRACH_MatchCHI2
TrackFitVeloChi2      -> ?
TrackFitVeloNDoF      -> ?
TrackFitTChi2         -> ?
TrackFitTNDoF         -> ?
```

```
RichUsedAero     -> RICHAerogelUsed
RichUsedR1Gas    -> RICH1GasUsed
RichUsedR2Gas    -> RICH2GasUsed
RichAboveMuThres -> RICHThresholdMu
RichAboveKaThres -> RICHThresholdKa
RichDLLe         -> RichDLLe
RichDLLmu        -> RichDLLmu
RichDLLk         -> RichDLLk
RichDLLp         -> RichDLLp
RichDLLbt        -> RichDLLbt
```

```
MuonBkgLL   -> MuonBgLL
MuonMuLL    -> MuonMuLL
MuonNShared -> NShared
```

```
InAccEcal   -> ?
EcalPIDe    -> EcalPIDe
InAccHcal   -> ?
HcalPIDe    -> HcalPIDe
HcalPIDmu   -> ?
InAccPrs    -> ?
PrsPIDe     -> PrsPIDe
InAccBrem   -> ?
BremPIDe    -> ?
VeloCharge  -> VeloCharge
isMuonTight -> isMuonTight
```

```
TrackP  -> P
TrackPt -> PT
```
