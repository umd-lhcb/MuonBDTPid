# MuonBDTPid
Muon PID with a uboost BDT (in ROOT 5). Also include code for PID efficiency studies.


## PIDCalib samples
These samples are generated with `Castelao`.
Below we list some related links
- WG prodcution [twiki](https://twiki.cern.ch/twiki/bin/viewauth/LHCbPhysics/WGproductionPID)
- Calib sample modes and cuts [option file](https://gitlab.cern.ch/lhcb/Castelao/-/blob/master/PIDCalib/PidCalibProduction/options/Run-2/makeTuples.py)
- PIDCalib package [twiki](https://twiki.cern.ch/twiki/bin/view/LHCb/PIDCalibPackage)
- A list of centrally produced [calibration data](https://twiki.cern.ch/twiki/bin/view/LHCbPhysics/ChargedPID#Calibration_data)

### Run 2 `J/psi -> mu+ mu-`, no `PT` cut
The sample is produced centrally with request ID `69972`.
They are available at this eos location:
```
/eos/lhcb/grid/prod/lhcb/LHCb/Collision16/PIDCALIB.ROOT/00111665/0000
```

From file `00111665_00000001_1.pidcalib.root`, tree `Jpsinopt_MuMTuple/DecayTree`,
I've validated that the `probe_PT` doesn't have a cut, as the minimal value is
`8.63`; the `tag_PT` has a `PT > 1500*MeV` cut, as the minimal value `1500.0003`.

From DIRAC, this sample is produced with:
```
Conditions: Beam6500GeV-VeloClosed-MagUp type:
Processing pass: Real Data/Reco16/Turbo02a
Input file type: FULLTURBO.DST
DQ flag: OK
Input production: ALL
TCKs: ALL

Processing Pass: PIDCalibTuples9r3p1/PIDMerge05
Step 1 PIDCalibTuples9r3 2016 Jpsinopt(142199/PIDCalibTuples9r3p1) : Castelao-v3r4
System config: x86_64-centos7-gcc8-opt MC TCK:
Options: $PIDCALIBROOT/scriptsR2/makeTuples_pp_2016_reprocessing_Jpsinopt.py;$PIDCALIBROOT/scriptsR2/DataType-2016repro.py Options format: WGProd Multicore: N
DDDB: Condition DB: DQTag:
Extra: WG/PIDCalib.v9r3 Runtime projects:
Visible: Y Usable:Yes
Input file types: FULLTURBO.DST Output file types: DAVINCIHIST,PIDCALIB.ROOT

Step 2 PIDCalib-Ntuples-Merge(131852/PIDMerge05) : Noether-v1r4
System config: MC TCK:
Options: $APPCONFIGOPTS/DataQuality/DQMergeRun.py Options format: Multicore: N
DDDB: Condition DB: DQTag:
Extra: AppConfig.v3r332 Runtime projects:
Visible: Y Usable:Yes
Input file types: PIDCALIB.ROOT Output file types: PIDCALIB.ROOT
```


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
