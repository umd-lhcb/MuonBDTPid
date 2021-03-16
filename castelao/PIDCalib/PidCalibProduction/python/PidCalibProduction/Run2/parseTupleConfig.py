###############################################################################
# (c) Copyright 2000-2018 CERN for the benefit of the LHCb Collaboration      #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
################################################################################
##                                                                            ##
##  parseTupleConfig.py   -   Setup DaVinci to write nTuples and MicroDSTs    ##
##                                                                            ##
## Example:                                                                   ##
##                                                                            ##
##  configuredAlgorithms = parseConfiguration(                                ##
##      tupleConfiguration,  ## PIDCalib tuple configuration                  ##
##      tesFormat,           ## TES format "/Event/Turbo/<Line>/Particles"    ##
##      mdstOutputFile,      ## MicroDST filename also used as OUTPUT TES!!!  ##
##      mdstOutputPrefix,    ## MicroDST Prefix, to be changed in PRODUCTION  ##
##      varsByType,          ## dictionary of variables per branch type       ##
##      varsByName,          ## dictionary of variables per branch name       ##
##      eventVariables,      ## dictionary of event variables                 ##
##      writeNullWeightCandidates = True,  ## if False filters out sWeight=0  ## 
##    )                                                                       ##
##                                                                            ##
##                                                                            ##
## Example of minimal tupleConfiguration                                      ##
##                                                                            ##
##  tupleConfiguration = {                                                    ##
##    "DSt_PiP" : TupleConfig (                                               ##
##      Decay = "[D*(2010)+ -> ^(D0 -> K- ^pi+) pi+]CC"                       ##
##      , InputLines    = "Hlt2PIDD02KPiTagTurboCalib"                        ##
##      , Filter        = filters.PositiveID                                  ##
##      , Calibration   = "RSDStCalib_Pos"                                    ##
##      , Branches = {                                                        ##
##          "Dst"     : Branch("^([D*(2010)+ -> (D0 -> K- pi+) pi+]CC)", Type='H')
##          , "Dz"    : Branch( "[D*(2010)+ -> ^(D0 -> K- pi+) pi+]CC",  Type='I')
##          , "K"     : Branch( "[D*(2010)+ -> (D0 -> ^K- pi+) pi+]CC",  Type='T')
##          , "probe" : Branch( "[D*(2010)+ -> (D0 -> K- ^pi+) pi+]CC",  Type='T', isAlso=['pi'])
##          , "pis"   : Branch( "[D*(2010)+ -> (D0 -> K- pi+) ^pi+]CC",  Type='T', isAlso=['pi'])
##        }                                                                   ##
##      ),                                                                    ##
##    }                                                                       ##
##                                                                            ##
## Example of varsByType                                                      ##
##   LokiVarsByType = {                                                       ##
##        "HEAD" : {                                                          ##
##          "ENDVERTEX_CHI2"   : "VFASPF(VCHI2)"                              ##
##          ,"ENDVERTEX_NDOF" : "VFASPF(VDOF)"                                ##
##          ,"Mass" : "M"                                                     ##
##        },                                                                  ##
##                                                                            ##
##        "INTERMEDIATE" : {                                                  ##
##          ,"BPVLTCHI2" : "BPVLTCHI2()"                                      ##
##          ,"Mass" : "M"                                                     ##
##        },                                                                  ##
##                                                                            ##
##        "TRACK" : {                                                         ##
##          , "Loki_MINIPCHI2": "BPVIPCHI2()"                                 ##
##        },                                                                  ##
##                                                                            ##
##        "NEUTRAL" : {                                                       ##
##        }                                                                   ##
##     }                                                                      ##
##                                                                            ##
##                                                                            ##
##                                                                            ##
## Example of varsByName                                                      ##
##   varsByName = {                                                           ##
##                                                                            ##
##     "Lc" : {'WM_PiKPi': "WM('pi+', 'K-', 'pi+')" # D->Kpipi,               ##
##            ,'WM_KPiPi' : "WM('K-', 'pi+', 'pi+')" # D->Kpipi               ##
##            ,'WM_KKPi'  : "WM('K-', 'K+', 'pi+')" # D->KKpi                 ##
##     },                                                                     ##
##                                                                            ##
##     "Dz" : {'WM_PiPi'    : "WM('pi+','pi-')"                               ##
##              ,'WM_KK'      : "WM('K+','K-')"                               ##
##              ,'WM_DCS'     : "WM('pi+','K-')"                              ##
##                                                                            ##
##     },                                                                     ##
##                                                                            ##
##     "K"  : {                                                               ##
##     },                                                                     ##
##   }                                                                        ##
##                                                                            ##
##                                                                            ##
##                                                                            ##
################################################################################

from Gaudi.Configuration import *
from Configurables import DaVinci, MicroDSTWriter
from PhysConf.MicroDST import uDstConf
from PhysSelPython.Wrappers import DataOnDemand
from PhysSelPython.Wrappers import (Selection, 
                                    MergedSelection,
                                    SelectionSequence, 
                                    MultiSelectionSequence)
# make a FilterDesktop
from Configurables import FilterDesktop

from DecayTreeTuple import *
from DecayTreeTuple.Configuration import *
from Configurables import LoKi__Hybrid__EvtTupleTool as LokiEventTool
from Configurables import LoKi__Hybrid__TupleTool as LokiTool
from Configurables import TupleToolTwoParticleMatching as MatcherTool

from Configurables import StoreExplorerAlg
from PidCalibProduction.Configuration import ProbNNRecalibrator as ProbNNcalib
from Configurables import ApplySWeights
from PhysConf.MicroDST import uDstConf
## from Configurables import DaVinci
from copy import copy

# for MicroDST writing
from PhysSelPython.Wrappers import SelectionSequence
from DSTWriters.microdstelements import *
from DSTWriters.Configuration import ( SelDSTWriter,stripMicroDSTStreamConf,
                       stripMicroDSTElements, stripCalibMicroDSTStreamConf,
                       stripDSTElements, stripDSTStreamConf)

from Configurables import CopyAndMatchCombination

from TupleConfig import Branch
from TupleConfig import TupleConfig
from Configurables import TupleToolPIDCalib as TTpid

from Configurables import MuonIDPlusTool #added from Giacomo



################################################################################
## Configuration of the MicroDST writer                                       ##
################################################################################
def configureMicroDSTwriter( name, prefix, sequences ):
  # Configure the dst writers for the output
  pack = True

  microDSTwriterInput = MultiSelectionSequence ( name , Sequences = sequences )

  # Configuration of MicroDST
  # per-event an per-line selective writing of the raw event is active (selectiveRawEvent=True)
  mdstStreamConf = stripMicroDSTStreamConf(pack=pack)#, selectiveRawEvent = False)
  mdstElements   = stripMicroDSTElements(pack=pack)

  # Configuration of SelDSTWriter
  # per-event an per-line selective writing of the raw event is active (selectiveRawEvent=True)
  SelDSTWriterElements = {'default': mdstElements }
  SelDSTWriterConf = {'default': mdstStreamConf}
#  SelDSTWriterConf = {'default': stripCalibMicroDSTStreamConf(pack=pack, selectiveRawEvent=False)}

  dstWriter = SelDSTWriter( "MyDSTWriter",
                            StreamConf = SelDSTWriterConf,
                            MicroDSTElements = SelDSTWriterElements,
                            OutputFileSuffix = prefix,
                            SelectionSequences = [microDSTwriterInput]
                          )

  from Configurables import StoreExplorerAlg
  return [microDSTwriterInput.sequence(), 
          dstWriter.sequence()]


################################################################################
## CONFIGURATION OF THE JOB                                                   ##
################################################################################
def parseConfiguration(tupleConfig,  # TupleConfig object describing sample
                       tesFormat,    # Input TES with "<line>" placeholder
                       mdstOutputFile,  # MicroDST output extension
                       mdstOutputPrefix,# MicroDST prefix for production
                       varsByType,   # requested variables by type
                       varsByName,   # requested variables by name
                       eventVariables, # event variables
                       writeNullWeightCandidates = True, 
                       writeMuonPIDPlus = True, 
                       mdstInput = False, 
                       tupleOutput = True
                      ):
  cfg = tupleConfig
  reviveSequences = [] # mark sequences to unpack std particles
  swSequences     = [] # mark sequences to apply sWeights
  filterSequences = [] # mark sequences to be written in tuples
  matchSequences  = [] # mark sequences to be written in tuples
  tupleSequences  = [] # mark tuple sequences
  dstSequences    = [] # sequences writing (Micro)DST files

  triggerList = [
    "L0MuonDecision", 
    "L0HadronDecision", 
    "L0ElectronDecision", 

    "Hlt1TrackMVADecision" ,
    "Hlt1TrackMuonDecision" ,
  ]

  for basicPart in ["Muons", "Pions", "Kaons", "Protons", "Electrons"]:
    location = "Phys/StdAllNoPIDs{s}/Particles".format ( s = basicPart )
    reviveSequences += [SelectionSequence("fs_std" + basicPart , 
                          TopSelection = DataOnDemand(location))]

  for basicPart in ["DownPions", "DownKaons", "DownProtons", "DownElectrons"]:
    location = "Phys/StdNoPIDs{s}/Particles".format ( s = basicPart )
    reviveSequences += [SelectionSequence("fs_std" + basicPart , 
                          TopSelection = DataOnDemand(location))]

  location = "Phys/StdLooseDownMuons/Particles"
  reviveSequences += [SelectionSequence("fs_std" + "DownMuons" , 
                          TopSelection = DataOnDemand(location))]


  for sample in cfg:
################################################################################
## Configure sWeighting                                                       ##
################################################################################
    for line in cfg[sample].InputLines:
      location = tesFormat.replace('<line>', line) 
      protoLocation = location.replace('/Particles', '/Protos') 

#     swSequences+=[ProbNNcalib ("TurboProbNN" + line, protoLocation).sequence()]
      if cfg[sample].Calibration:
        swSequences += [ 
          ApplySWeights ("ApplySW"+sample,
           InputTes   = location,
           sTableDir  = cfg[sample].Calibration,
           sTableName = "sTableSignal", 
          )
         ]


################################################################################
## Creates filter sequences to fill nTuples                                   ##
################################################################################

    selectionName = sample
    _cut = "DECTREE ('{}')".format ( cfg[sample].Decay.replace("^","") )

    if writeNullWeightCandidates == False:
      _cut += " & ( WEIGHT != 0 ) "

    if cfg[sample].Filter:
      _cut += " & ({}) ".format (  cfg[sample].Filter.cut )

    inputSelection = MergedSelection ( "input" + selectionName ,
          RequiredSelections = [
            DataOnDemand(tesFormat.replace('<line>', line))
              for line in  cfg[sample].InputLines ],
        )

    selection = Selection(selectionName,
        RequiredSelections = [ inputSelection ],
        Algorithm = FilterDesktop("alg_" + selectionName,
                                  Code = _cut),
      )

    filterSequence = SelectionSequence("Seq"+selectionName,
      TopSelection = selection)

    filterSequences += [filterSequence]

################################################################################
## Creates matching selections (used to create the proper locations in mdst)  ##
################################################################################
    matchingSel = Selection("Match" + selectionName,
        Algorithm = CopyAndMatchCombination ( 
          "MatchAlg" + selectionName, 
          Downstream = cfg[sample].Downstream, 
        ),
        RequiredSelections = [selection]
    )

    matchingSeq = SelectionSequence ( "SeqMatch"+ selectionName,
          TopSelection = matchingSel )

    matchSequences += [ matchingSeq ]

    partsInBranches = []

    for branchName in cfg[sample].Branches:

      partName = branchName
      if len(cfg[sample].Branches[branchName].isAlso)>0 : 
        partName = cfg[sample].Branches[branchName].isAlso[0]

      partsInBranches += [ partName ]

    #print("partsInBranches = ", partsInBranches)

################################################################################
## Parses the configuration dictionaries and configure the tuples             ##
################################################################################
    tuple = DecayTreeTuple(sample + "Tuple")
    tuple.Inputs = [filterSequence.outputLocation()]
    tuple.Decay  = cfg[sample].Decay
    tuple.ToolList = [ "TupleToolANNPID" ]
    if mdstInput : 
      tuple.RootInTES = "/Event/Turbo"

    if "e" in partsInBranches : 
      ttBrem = tuple.addTupleTool("TupleToolBremInfo")
      ttBrem.Particle = ["pi+", "p", "K+", "mu+", "e+"]
      ttBrem.Verbose = True
      ttBrem.RootInTES = "" #### !!!!

    ttPPD = tuple.addTupleTool("TupleToolProtoPData")
    ttPPD.DataList = ["VeloCharge","CaloEoverP", "CaloEcalChi2", "CaloPrsE", "CaloHcalE", "EcalPIDe", "PrsPIDe", "HcalPIDe", "CaloEcalE"]

    if writeMuonPIDPlus and ("mu" in partsInBranches) : 
      muidPlus = tuple.addTupleTool("TupleToolMuonPidPlus");
      muidPlus.MuonIDPlusToolName = "MuonIDPlusTool"
      muidPlus.OutputLevel = 5
      muidPlus.RootInTES=""  ####  !!!!!
      muidPlus.addTool(MuonIDPlusTool)
      muidPlus.MuonIDPlusTool.OutputLevel=5
      muidPlus.MuonIDPlusTool.RootInTES=""  ####  !!!!!
      muidPlus.MuonIDPlusTool.ReleaseObjectOwnership = False
      muidPlus.MuonIDPlusTool.MatchToolName="MuonChi2MatchTool"
      muidPlus.Verbose = True;

    eventTool = tuple.addTupleTool("LoKi::Hybrid::EvtTupleTool/LoKiEvent")
    if 'VOID' in eventVariables.keys():
      eventTool.VOID_Variables = eventVariables['VOID']

    if not mdstInput : 
      if 'ODIN' in eventVariables.keys():
        eventTool.ODIN_Variables = eventVariables['ODIN']

    if 'HLT' in eventVariables.keys():
      eventTool.HLT_Variables = eventVariables['HLT']

    if 'L0DU' in eventVariables.keys():
      eventTool.L0DU_Variables = eventVariables['L0DU']

    eventTool.Preambulo = [
      "from LoKiTracks.decorators import *",
      "from LoKiCore.functions import *"
    ]
    tuple.addTool( eventTool )

    if mdstInput : 
      matchingLocation = {
        "mu+"        :  "/Event/PIDCALIB/Phys/Match"+sample+"/Particles",
        "pi+"        :  "/Event/PIDCALIB/Phys/Match"+sample+"/Particles",
        "K+"         :  "/Event/PIDCALIB/Phys/Match"+sample+"/Particles",
        "p+"         :  "/Event/PIDCALIB/Phys/Match"+sample+"/Particles",
        "e+"         :  "/Event/PIDCALIB/Phys/Match"+sample+"/Particles",
      }
    else : 
      if cfg[sample].Downstream : 
        matchingLocation = {
        "mu+"        :  "Phys/StdLooseDownMuons/Particles",
        "pi+"        :  "Phys/StdNoPIDsDownPions/Particles",
        "K+"         :  "Phys/StdNoPIDsDownKaons/Particles",
        "p+"         :  "Phys/StdNoPIDsDownProtons/Particles",
        "e+"         :  "Phys/StdNoPIDsDownElectrons/Particles",
        }
      else : 
        matchingLocation = {
        "mu+"        :  "Phys/StdAllNoPIDsMuons/Particles",
        "pi+"        :  "Phys/StdAllNoPIDsPions/Particles",
        "K+"         :  "Phys/StdAllNoPIDsKaons/Particles",
        "p+"         :  "Phys/StdAllNoPIDsProtons/Particles",
        "e+"         :  "Phys/StdAllNoPIDsElectrons/Particles",
        }

    tupleSequences += [tuple]

    for branchName in cfg[sample].Branches:

      partName = branchName
      if len(cfg[sample].Branches[branchName].isAlso)>0 : 
        partName = cfg[sample].Branches[branchName].isAlso[0]

      #print ("PartName = ", partName)

      b = tuple.addBranches({branchName : cfg[sample].Branches[branchName].Particle})
      b = b[branchName]
      matcher = b.addTupleTool ( "TupleToolTwoParticleMatching/Matcher_" + branchName )
      matcher.ToolList = []
      matcher.Prefix = ""; matcher.Suffix = "_Brunel"
      matcher.MatchLocations = matchingLocation

      lokitool = b.addTupleTool("LoKi::Hybrid::TupleTool/LoKi_"+branchName)
      vardict = copy(varsByType[ cfg[sample].Branches[branchName].Type ])
      pidcalibtool = b.addTupleTool ( "TupleToolPIDCalib/PIDCalibTool_"+branchName )
      pidcalibtool_matched = TTpid( "PIDCalibTool_match_"+branchName )
      for partName in [branchName] + cfg[sample].Branches[branchName].isAlso:
        if partName in varsByName:
          vardict.update ( varsByName[partName] )
#        if partName == 'e':
#          pidcalibtool.FillBremInfo = True
#          pidcalibtool_matched.FillBremInfo = True

      lokimatchedtool = LokiTool("LoKi_match_"+branchName)

      matcher.addTool ( pidcalibtool_matched )
      matcher.ToolList += ["LoKi::Hybrid::TupleTool/LoKi_match_"+branchName ,
                           "TupleToolPIDCalib/PIDCalibTool_match_" + branchName ]

      from Configurables import TupleToolTISTOS
      tistostool = TupleToolTISTOS("TISTOSForTheOffline"+branchName)
      tistostool.FillL0 = True
      tistostool.FillHlt1 = True
      tistostool.FillHlt2 = False
      tistostool.Verbose = True    # 16/01/2020 for L0Calo
      tistostool.VerboseL0 = True
      tistostool.VerboseHlt1 = True
      tistostool.VerboseHlt2 = False
      tistostool.TriggerList = triggerList
      matcher.addTool(tistostool)
      matcher.ToolList += ["TupleToolTISTOS/TISTOSForTheOffline"+branchName]

      # 16/01/2020 for L0Calo variables
      from Configurables import TupleToolL0Calo
      l0calotool = TupleToolL0Calo("L0CaloForTheOffline"+branchName)
      l0calotool.WhichCalo = "HCAL"
      l0calotool.TriggerClusterLocation = "Trig/L0/FullCalo"  # Added 29/01/2020 for "trigger" variables
      matcher.addTool(l0calotool)
      matcher.ToolList += ["TupleToolL0Calo/L0CaloForTheOffline"+branchName]

      from Configurables import TupleToolBremInfo, TupleToolProtoPData, TupleToolANNPID, TupleToolMuonPidPlus

      if partName == "e" : 
        ttbi = TupleToolBremInfo("BremInfoForTheOffline"+branchName)
        ttbi.Particle = ["pi+", "p", "K+", "mu+", "e+"]
        ttbi.RootInTES = ""
        matcher.addTool(ttbi)
        matcher.ToolList += ["TupleToolBremInfo/BremInfoForTheOffline"+branchName]

      ttppd = TupleToolProtoPData("ProtoPDataForTheOffline"+branchName)
      ttppd.DataList = ["VeloCharge","CaloEoverP", "CaloEcalChi2", "CaloPrsE", "CaloHcalE", "EcalPIDe", "PrsPIDe", "HcalPIDe", "CaloEcalE"]
      matcher.addTool(ttppd)
      matcher.ToolList += ["TupleToolProtoPData/ProtoPDataForTheOffline"+branchName]

      ttann = TupleToolANNPID("ANNPIDForTheOffline"+branchName)
      ttann.PIDTypes = [ "Electron","Muon","Pion","Kaon","Proton","Ghost","Deuteron" ]
#      ttann.PIDTypes = [ "Electron","Muon","Pion","Kaon","Proton","Ghost" ]
      ttann.ANNPIDTunes= ["MC12TuneV2", "MC12TuneV3","MC12TuneV4", "MC15TuneV1","MC15TuneDNNV1", "MC15TuneCatBoostV1", "MC15TuneFLAT4dV1"]
      matcher.addTool(ttann)
      matcher.ToolList += ["TupleToolANNPID/ANNPIDForTheOffline"+branchName]

      if writeMuonPIDPlus and partName == "mu" : 
        ttmuidPlus = TupleToolMuonPidPlus("TupleToolMuonPidPlusForTheOffline"+branchName);
        ttmuidPlus.MuonIDPlusToolName = "MuonIDPlusTool"
        ttmuidPlus.OutputLevel = 5
        ttmuidPlus.RootInTES=""  ####  !!!!!
        ttmuidPlus.addTool(MuonIDPlusTool)
        ttmuidPlus.MuonIDPlusTool.OutputLevel=5
        ttmuidPlus.MuonIDPlusTool.RootInTES=""  ####  !!!!!
        ttmuidPlus.MuonIDPlusTool.ReleaseObjectOwnership = False
        ttmuidPlus.MuonIDPlusTool.MatchToolName="MuonChi2MatchTool"
        ttmuidPlus.Verbose = True;
        matcher.addTool(ttmuidPlus);
        matcher.ToolList += ["TupleToolMuonPidPlus/TupleToolMuonPidPlusForTheOffline"+branchName]

      vardict.update (cfg[sample].Branches[branchName].LokiVariables)
      lokimatchedtool.Variables = vardict
      lokitool.Variables        = vardict

      matcher.addTool ( lokimatchedtool )

      # Additional variables for Greg/Phoebe's uBDT
      from Configurables import TupleToolANNPIDTrainingLight
      if hasattr(tuple, 'probe'):
          tuple.probe.addTool(TupleToolANNPIDTrainingLight, name='TupleToolANNPIDTrainingLight')
          tuple.probe.ToolList+=['TupleToolANNPIDTrainingLight/TupleToolANNPIDTrainingLight']

  print "Input TES: " 
  print "\n".join ( [f.outputLocation() for f in filterSequences] )
  if mdstOutputFile:
    dstSequences += configureMicroDSTwriter ( mdstOutputFile, 
                                              mdstOutputPrefix, 
                                              filterSequences + matchSequences)


  if mdstInput : 
    return (reviveSequences + swSequences + filterSequences + matchSequences + tupleSequences)
  else : 
    if tupleOutput : 
      return (reviveSequences + swSequences + filterSequences + matchSequences + dstSequences + tupleSequences )
    else : 
      return (reviveSequences + filterSequences + matchSequences + dstSequences )
