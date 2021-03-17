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
`Castelao/v3r4` is used, with `CMTCONFIG=x86_64-centos7-gcc8-opt`.

### On `lxplus`
Follow these commands to setup a Castelao dev environment on `lxplus`:

```
lb-dev Castelao/v3r4
cd ./CastelaoDev_v3r4

git lb-use Castelao
git lb-checkout Castelao/run2-patches PIDCalib/PidCalibProduction
git lb-clone-pkg WG/PIDCalib -b v9r3
```

All required changes to Castelao are included in this repository. Copy all
contents in `./castelao` to `CastelaoDev_vXrY` folder.

Finally, comment out the `Input` and `DataType` lines in the
`makeTuples_pp_YYYY_reprocessing*.py` files. Below is an example from
`makeTuples_pp_YYYY_reprocessing_Jpsinopt.py` file:
```python
dv = DaVinci (
        InputType             = "MDST"
            , Turbo           = True
            , RootInTES       = "/Event/Turbo"
#            , DataType        = "2016" #added by me just for this test
            , EvtMax          = -1
            , Lumi            = True
            , TupleFile       = "pidcalib.root"
#            , Input           = ['root://eoslhcb.cern.ch//eos/lhcb/user/p/poluekt/PID/2016_TurCal_DST/00053197_00000610_2.fullturbo.dst']
          )
```

Now, to produce `J/psi` only samples, first, drop into a `bash` shell:
```
./run bash
```

In the `bash` shell, run:
```
gaudirun.py \
    $PIDCALIBROOT/scriptsR2/makeTuples_pp_2016_reprocessing_Jpsinopt.py \
    $PIDCALIBROOT/scriptsR2/DataType-2016repro.py
```

To produce everything else, drop in the same `bash`, then:
```
gaudirun.py \
    $PIDCALIBROOT/scriptsR2/makeTuples_pp_2016_reprocessing.py \
    $PIDCALIBROOT/scriptsR2/DataType-2016repro.py
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
TrackP
TrackPt
```

```
RichUsedAero     -> probe_Brunel_RICHAerogelUsed
RichUsedR1Gas    -> probe_Brunel_RICH1GasUsed
RichUsedR2Gas    -> probe_Brunel_RICH2GasUsed
RichAboveMuThres -> probe_Brunel_RICHThresholdMu
RichAboveKaThres -> probe_Brunel_RICHThresholdKa
RichDLLe         -> probe_Brunel_RichDLLe
RichDLLmu        -> probe_Brunel_RichDLLmu
RichDLLk         -> probe_Brunel_RichDLLk
RichDLLp         -> probe_Brunel_RichDLLp
RichDLLbt        -> probe_Brunel_RichDLLbt
```

```
MuonBkgLL   -> probe_MuonBgLL
MuonMuLL    -> probe_MuonMuLL
MuonNShared -> ?probe_NShared
```

```
InAccEcal
EcalPIDe    -> ?probe_Brunel_PP_EcalPIDe
EcalPIDmu
InAccHcal
HcalPIDe    -> ?probe_Brunel_PP_EcalHcalPIDe
HcalPIDmu
InAccPrs
PrsPIDe     -> ?probe_Brunel_PP_PrsPIDe
InAccBrem
BremPIDe
VeloCharge  -> ?probe_Brunel_PP_VeloCharge
isMuonTight -> probe_isMuonTight
```

### On the seemingly identical branches
Naively, one would expect `RichDLLe` and `probe_Brunel_RichDLLe` are identical.
However, when comparing against each other:
```
idx  RichDLLe  probe_Brunel_RichDLLe
---  --------  ---------------------
12   -29.0931  -29.091299057006836
82   0.0       -1000.0
87   -19.7908  -19.787399291992188
96   -14.7653  -14.826299667358398
127  0.0       -1000.0
165  -2.0359   -1.315000057220459
200  0.0       -1000.0
229  -12.471   -12.465800285339355
230  -47.2728  -47.21480178833008
307  -55.0559  -55.055999755859375
341  -25.4451  -8.821700096130371
600  0.0       -1000.0
682  2.9152    2.915299892425537
701  0.0       -1000.0
702  -20.8758  -20.87540054321289
866  5.6615    5.662499904632568
916  -43.458   -43.38570022583008
1063 0.0987    0.13289999961853027
1123 0.0       -1000.0
1137 -2.8032   -2.803299903869629
1198 3.3484    3.355799913406372
1207 0.0       -1000.0
1247 -8.0879   -0.5562000274658203
1293 -0.1925   -0.1923999935388565
1311 0.0       -1000.0
```
