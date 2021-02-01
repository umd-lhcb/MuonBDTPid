# MuonBDTPid
Muon PID with a uboost BDT (in ROOT 5). Also include code for PID efficiency studies.
Below we list some related links:

- A list of centrally produced [calibration data](https://twiki.cern.ch/twiki/bin/view/LHCbPhysics/ChargedPID#Calibration_data)
- WG prodcution [twiki](https://twiki.cern.ch/twiki/bin/viewauth/LHCbPhysics/WGproductionPID)
- PIDCalib package [twiki](https://twiki.cern.ch/twiki/bin/view/LHCb/PIDCalibPackage)
- PIDCalib sample modes and cuts [option file](https://gitlab.cern.ch/lhcb/Castelao/-/blob/master/PIDCalib/PidCalibProduction/options/Run-2/makeTuples.py)


## PIDCalib samples

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


## PIDCalib sample production
PIDCalib samples are generated with `Castelao`. For run 1 and 2,
`Castelao/v3r4` is used.

### On `lxplus`
Follow these commands to setup a Castelao dev environment on `lxplus`:

```
lb-dev Castelao/v3r4
cd ./CastelaoDev_v3r4

git lb-use Castelao
git lb-checkout Castelao/run2-patches PIDCalib/PidCalibProduction
git lb-clone-pkg WG/PIDCalib -b v9r3
```

### With a `Castelao` docker image:

First, spawn a container with an image built by us:
```
make docker-cl
```

Then follow the instructions in the previous section.


## uboost BDT (uBDT)

### Required input variables
According to the [ANA note](https://github.com/umd-lhcb/group-talks/blob/master/ana_thesis/RD_RDst_ANA_21-01-05.pdf), p.16,
these are the input variables to the uBDT
(These names are also used in the [source](https://github.com/umd-lhcb/MuonBDTPid/blob/master/src/AddUboostBranchRun2.cpp)):

```
TrackChi2PerDof
TrackNumDof
TrackLikelihood
TrackGhostProbability
TrackFitMatchChi2
TrackFitVeloChi2
TrackFitVeloNDoF
TrackFitTChi2
TrackFitTNDoF
```

```
RichUsedAero
RichUsedR1Gas
RichUsedR2Gas
RichAboveMuThres
RichAboveKaThres
RichDLLe
RichDLLmu
RichDLLk
RichDLLp
RichDLLbt
```

```
MuonBkgLL
MuonMuLL
MuonNShared
```

```
InAccEcal
EcalPIDe
InAccHcal
HcalPIDe
HcalPIDmu
InAccPrs
PrsPIDe
InAccBrem
BremPIDe
VeloCharge
isMuonTight
```

```
TrackP
TrackPt
```
