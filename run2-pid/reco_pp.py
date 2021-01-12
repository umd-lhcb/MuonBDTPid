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

##################################################
###      C O N F I G U R A T I O N   1     #######
###. . . . . . . . . . . . . . . . . . . . #######
###        Variables by branch type        #######
##################################################
###  List here variables for each TYPE of branch.
### Branches are: "HEAD", the head of the decay chain
###               "INTERMEDIATE", produced and decayed
###               "TRACK", charged basic particle
###               "NEUTRAL", photons or pi0
##################################################

LokiVarsByType = {
  "HEAD" : {
    "ENDVERTEX_CHI2"   : "VFASPF(VCHI2)"
    , "ENDVERTEX_NDOF" : "VFASPF(VDOF)"
    , "IPCHI2" : "BPVIPCHI2()"
    , "IP"     : "BPVIP()"
    ,"BPVLTCHI2" : "BPVLTCHI2()"
    , "BPVDLS"   : "BPVDLS"
    ,"Mass" : "M"
  },
  
  "INTERMEDIATE" : {
    "ENDVERTEX_CHI2"   : "VFASPF(VCHI2)"
    , "ENDVERTEX_NDOF" : "VFASPF(VDOF)"
   , "IPCHI2" : "BPVIPCHI2()"
    , "IP"     : "BPVIP()"
    , "BPVDLS"   : "BPVDLS"
    ,"BPVLTCHI2" : "BPVLTCHI2()"
    ,"Mass" : "M"
  }, 

  "TRACK" : {
    "LoKi_PT"      : "PT"     ## These variables are also saved from the PIDCalib
    , "LoKi_P"     : "P"      ## tuple tool, so they are a waste of disk space
    , "LoKi_ETA"   : "ETA"    ## however the correct thing would be to keep them
    , "Loki_PIDK"  : "PIDK"   ## here and removing them from PIDCalib.
    , "Loki_PIDmu" : "PIDmu"  ##  ... to be done ...
    , "Loki_PIDp"  : "PIDp"   ## 
    , "sWeight"    : "WEIGHT"
    , "Loki_MINIPCHI2": "BPVIPCHI2()"
    , "RichDLLe"      : "PPFUN ( PP_RichDLLe )"
    , "RichDLLpi"     : "PPFUN ( PP_RichDLLpi )"
    , "RichDLLmu"     : "PPFUN ( PP_RichDLLmu )"
    , "RichDLLk"      : "PPFUN ( PP_RichDLLk )"
    , "RichDLLp"      : "PPFUN ( PP_RichDLLp )"
    , "RichDLLbt"     : "PPFUN ( PP_RichDLLbt )"
    , "MuonMuLL"      : "PPFUN ( PP_MuonMuLL )"
    , "MuonBgLL"      : "PPFUN ( PP_MuonBkgLL )"
    , "Charge"        : "switch ( ID > 0, +1, -1 )"
    , "MuonUnbiased"  : "switch ("\
                        "(TIS('L0.*Decision', 'L0TriggerTisTos')) & "\
                        "(TIS('Hlt1(?!ODIN)(?!L0)(?!Lumi)(?!Tell1)(?!MB)(?!NZS)(?!Velo)(?!BeamGas)(?!Incident).*Decision', 'Hlt1TriggerTisTos')) &"\
                        "(TIS('Hlt2(?!Forward)(?!DebugEvent)(?!Express)(?!Lumi)(?!Transparent)(?!PassThrough).*Decision', 'Hlt2TriggerTisTos')) , " \
                        "1,0)"
    , "ElectronUnbiased" : "switch ( "\
                        "(TIS('L0ElectronDecision', 'L0TriggerTisTos')) & "\
                        "(TIS('Hlt1PhysDecision', 'Hlt1TriggerTisTos')) &"\
                        "(TIS('Hlt2PhysDecision', 'Hlt2TriggerTisTos')) , " \
                        "1,0)"
    , "TRCHI2NDOF" :  "TRCHI2DOF"
    , "TRACK_GHOSTPROB" : "TRGHP"
  },
  
  "NEUTRAL" : {
  }
}


EventInfo = {
  "nPVs"              : "RECSUMMARY( LHCb.RecSummary.nPVs              , -9999)"
#  , "nLongTracks"       : "RECSUMMARY( LHCb.RecSummary.nLongTracks       , -9999)"
#  , "nDownstreamTracks" : "RECSUMMARY( LHCb.RecSummary.nDownstreamTracks , -9999)"
#  , "nUpstreamTracks"   : "RECSUMMARY( LHCb.RecSummary.nUpstreamTracks   , -9999)"
#  , "nVeloTracks"       : "RECSUMMARY( LHCb.RecSummary.nVeloTracks       , -9999)"
#  , "nTTracks"          : "RECSUMMARY( LHCb.RecSummary.nTTracks          , -9999)"
#  , "nBackTracks"       : "RECSUMMARY( LHCb.RecSummary.nBackTracks       , -9999)"
  , "nTracks"           : "RECSUMMARY( LHCb.RecSummary.nTracks           , -9999)"
  , "nRich1Hits"        : "RECSUMMARY( LHCb.RecSummary.nRich1Hits        , -9999)"
  , "nRich2Hits"        : "RECSUMMARY( LHCb.RecSummary.nRich2Hits        , -9999)"
#  , "nVeloClusters"     : "RECSUMMARY( LHCb.RecSummary.nVeloClusters     , -9999)"
#  , "nITClusters"       : "RECSUMMARY( LHCb.RecSummary.nITClusters       , -9999)"
#  , "nTTClusters"       : "RECSUMMARY( LHCb.RecSummary.nTTClusters       , -9999)"
#  , "nUTClusters"       : "RECSUMMARY( LHCb.RecSummary.nUTClusters       , -9999)"
#  , "nOTClusters"       : "RECSUMMARY( LHCb.RecSummary.nOTClusters       , -9999)"
#  , "nFTClusters"       : "RECSUMMARY( LHCb.RecSummary.nFTClusters       , -9999)"
  , "nSPDhits"          : "RECSUMMARY( LHCb.RecSummary.nSPDhits          , -9999)"
#  , "nMuonCoordsS0"     : "RECSUMMARY( LHCb.RecSummary.nMuonCoordsS0     , -9999)"
#  , "nMuonCoordsS1"     : "RECSUMMARY( LHCb.RecSummary.nMuonCoordsS1     , -9999)"
#  , "nMuonCoordsS2"     : "RECSUMMARY( LHCb.RecSummary.nMuonCoordsS2     , -9999)"
#  , "nMuonCoordsS3"     : "RECSUMMARY( LHCb.RecSummary.nMuonCoordsS3     , -9999)"
#  , "nMuonCoordsS4"     : "RECSUMMARY( LHCb.RecSummary.nMuonCoordsS4     , -9999)"
  , "nMuonTracks"       : "RECSUMMARY( LHCb.RecSummary.nMuonTracks       , -9999)"
}   


##################################################
###      C O N F I G U R A T I O N   2     #######
###. . . . . . . . . . . . . . . . . . . . #######
###        Variables by branch name        #######
##################################################
###  List here variables for each Branch name
###   The purpose of this configuration is to allow 
###   to set a variable for all "Lambda_c+" as long
###   as all Lambda_c+ will be named "Lc"
##################################################

LokiVarsByName = {

  "Lc" : {'WM_PiKPi': "WM('pi+', 'K-', 'pi+')" # D->Kpipi,
         ,'WM_KPiPi' : "WM('K-', 'pi+', 'pi+')" # D->Kpipi          
         ,'WM_KKPi'  : "WM('K-', 'K+', 'pi+')" # D->KKpi    
  },

  "Dz" : {'WM_PiPi'    : "WM('pi+','pi-')"                                     
           ,'WM_KK'      : "WM('K+','K-')"                                      
           ,'WM_DCS'     : "WM('pi+','K-')"  

  },

  "K"  : {
  },
  
  "mu" : {
     "MuonTOS"  :      "switch((TOS('L0MuonDecision', 'L0TriggerTisTos')) & "\
                        "(TOS('Hlt1(TrackAllL0|TrackMuon|SingleMuonHighPT)Decision', 'Hlt1TriggerTisTos')), "\
                        "1,0)"
     ,"MuonProbe" :     "switch((P>3000) & (PT>800) & (BPVIPCHI2()>10) & (TRCHI2DOF<3), 1,0)"
     ,"MuonTag" :     "switch((P>6000) & (PT>1500) & (BPVIPCHI2()>25) & (TRCHI2DOF<3) & (ISMUON), 1,0)"


  },

 "phi" : {
    "WM_PiPi"   :  "WM('pi+', 'pi-')"   # for completeness 
    , "WM_PiK"   :  "WM('pi+', 'K-')"   # D+ decay to K- pi+ pi+ with one of the pi+ -> K-
    , "WM_KPi"   :  "WM('K+',  'pi-')"  # DCS D decay, for completeness
    , "WM_PK"    :  "WM('p+',  'K-')"   # Lc -> p K pi with p -> K
    , "WM_KP"    :  "WM('K+',  'p~-')"  # for completeness
  },

  "Ds" : {
    "WM_PiPiPi"  : "WM('pi+', 'pi-', 'pi+')"
    , "WM_PiPiK"   : "WM('pi+', 'pi-', 'K+')"
    , "WM_PiPiP"   : "WM('pi+', 'pi-', 'p+')"
    , "WM_PiKPi"   : "WM('pi+', 'K-', 'pi+')"
    , "WM_PiKK"    : "WM('pi+', 'K-', 'K+')"
    , "WM_PiKP"    : "WM('pi+', 'K-', 'p+')"
    , "WM_PiKPi"   : "WM('pi+', 'p~-', 'pi+')"
    , "WM_PiKK"    : "WM('pi+', 'p~-', 'K+')"
    , "WM_PiKP"    : "WM('pi+', 'p~-', 'p+')"
    , "WM_KPiPi"   : "WM('K+', 'pi-', 'pi+')"
    , "WM_KPiK"    : "WM('K+', 'pi-', 'K+')"
    , "WM_KPiP"    : "WM('K+', 'pi-', 'p+')"
    , "WM_KKPi"    : "WM('K+', 'K-', 'pi+')"
    , "WM_KKK"     : "WM('K+', 'K-', 'K+')"
    , "WM_KKP"     : "WM('K+', 'K-', 'p+')"
    , "WM_KPPi"    : "WM('K+', 'p~-', 'pi+')"
    , "WM_KPK"     : "WM('K+', 'p~-', 'K+')"
    , "WM_KPP"     : "WM('K+', 'p~-', 'p+')"
    , "WM_PPiPi"   : "WM('p+', 'pi-', 'pi+')"
    , "WM_PPiK"    : "WM('p+', 'pi-', 'K+')"
    , "WM_PPiP"    : "WM('p+', 'pi-', 'p+')"
    , "WM_PKPi"    : "WM('p+', 'K-', 'pi+')"
    , "WM_PKK"     : "WM('p+', 'K-', 'K+')"
    , "WM_PKP"     : "WM('p+', 'K-', 'p+')"
    , "WM_PPPi"    : "WM('p+', 'p~-', 'pi+')"
    , "WM_PPK"     : "WM('p+', 'p~-', 'K+')"
    , "WM_PPP"     : "WM('p+', 'p~-', 'p+')"
  },
  
  "e" : {
#    "ElectronTOS" : "switch ( "\
#                        "(TOS('L0ElectronDecision', 'L0TriggerTisTos')) & "\
#                        "(TOS('Hlt1PhysDecision', 'TriggerTisTos')) &"\
#                        "(TOS('Hlt2PhysDecision', 'TriggerTisTos')) , " \
#                        "1,0)"
#    "ElectronProbe" :   "switch((P>3000) & (PT>500) & (BPVIPCHI2()>9) , 1,0)"
#    ,"ElectronTag" :     "switch((P>6000) & (PT>1500) & (BPVIPCHI2()>9) & (PIDe>5), 1,0)"    

}

}

##################################################
###      C O N F I G U R A T I O N   3     #######
###. . . . . . . . . . . . . . . . . . . . #######
###        Filter definition               #######
##################################################
### Filters used to define the various nTuples
##################################################


from Configurables import TupleToolPIDCalib as TTpid
_l0TisTagCrit   = TTpid.getDefaultProperty('MuonTisL0Criterion')
_hlt1TisTagCrit = TTpid.getDefaultProperty('MuonTisHlt1Criterion')
_hlt2TisTagCrit = TTpid.getDefaultProperty('MuonTisHlt2Criterion')

_l0TosTagCrit   = TTpid.getDefaultProperty('MuonTosL0Criterion')
_hlt1TosTagCrit = TTpid.getDefaultProperty('MuonTosHlt1Criterion')
_hlt2TosTagCrit = TTpid.getDefaultProperty('MuonTosHlt2Criterion')

### Service functions
def L0TIS(code):
    return "TIS('{0}', 'L0TriggerTisTos')".format(code)
def L0TOS(code):
    return "TOS('{0}', 'L0TriggerTisTos')".format(code)
def Hlt1TIS(code):
    return "TIS('{0}', 'Hlt1TriggerTisTos')".format(code)
def Hlt1TOS(code):
    return "TOS('{0}', 'Hlt1TriggerTisTos')".format(code)
def Hlt2TIS(code):
    return "TIS('{0}', 'Hlt2TriggerTisTos')".format(code)
def Hlt2TOS(code):
    return "TOS('{0}', 'Hlt2TriggerTisTos')".format(code)

class FilterCut:
  def __init__ (self, cut):
    self.cut = "(" + cut + ")"
  def __add__ (self, cut):
    ret = FilterCut(self.cut)
    if isinstance(cut, str):
      ret.cut += "& ( " + cut + ")"
    else:
      ret.cut += "& ( " + cut.cut + ")"
    return ret
  def printout (self):
    print "self.cut = %s" % self.cut


class filters:
  LoP = FilterCut("NINTREE( ('p+'==ABSID) & (P<40000) )==1")
  HiP = FilterCut("NINTREE( ('p+'==ABSID) & (P>40000) )==1")

  LoP.printout()

  PositiveID = FilterCut("ID > 0")
  NegativeID = FilterCut("ID < 0")

  # Require at least one 'MuonUnBiased' daughter
  MuonUnBiased = FilterCut("NINTREE( (ISBASIC) & ({l0}) "
                         "& ({hlt1}) & ({hlt2}) )>0".format(
       l0=L0TIS(_l0TisTagCrit), hlt1=Hlt1TIS(_hlt1TisTagCrit),
       hlt2=Hlt2TIS(_hlt2TisTagCrit)))
 # MuonUnBiased.printout()
  # Require at least one 'MuonUnBiased' granddaughter
  MuonUnBiased_2 = FilterCut(("NINGENERATION( (ISBASIC) & ({l0}) & "
              "({hlt1}) & ({hlt2}), 2 )>0").format(
       l0=L0TIS(_l0TisTagCrit), hlt1=Hlt1TIS(_hlt1TisTagCrit),
       hlt2=Hlt2TIS(_hlt2TisTagCrit)))

  # Require at least one 'Muon TOS-tagged' daughter
  MuonTosTagged = FilterCut(("NINTREE( (ISBASIC) & ({l0}) & "
                              "({hlt1}) & ({hlt2}) )>0").format(
      l0=L0TOS(_l0TosTagCrit), hlt1=Hlt1TOS(_hlt1TosTagCrit),
      hlt2=Hlt2TOS(_hlt2TosTagCrit)))

  # Require at least one 'Muon TOS-tagged' granddaughter
  MuonTosTagged = FilterCut(("NINGENERATION( (ISBASIC) & ({l0}) "
                         "& ({hlt1}) & ({hlt2}), 2 )>0").format(
       l0=L0TOS(_l0TosTagCrit), hlt1=Hlt1TOS(_hlt1TosTagCrit),
       hlt2=Hlt2TOS(_hlt2TosTagCrit)))

  # Require Lambda_b decay is unbiased with respect to proton PID
  Lb2LcMuNu = FilterCut(("( ({l0Tos}) | ({l0Tis}) ) & "
                                  "({hlt1Tos}) & ({hlt2Tos})").format(
                                  l0Tos=L0TOS("L0(Muon|Hadron)Decision"),
                                  l0Tis=L0TIS("L0.*Decision"),
                                  hlt1Tos=Hlt1TOS("Hlt1(TrackAllL0|TrackMuon|SingleMuonHighPT)Decision"),
                                  hlt2Tos=Hlt2TOS("Hlt2(SingleMuon|TopoMu).*Decision")))

 
 



  IncLc2PKPi = FilterCut(("(BPVIPCHI2()<4) & (VFASPF(VCHI2/VDOF)<5) & (BPVLTCHI2()>9) & (ADWM('D_s+',WM('K-','K+','pi+'))>25.*MeV) & (ADWM('D+',WM('K-','K+','pi+'))>25.*MeV) &(ADWM('D*(2010)+',WM('K-','pi+','pi+'))>20.*MeV) & ((WM('K-','pi+','pi+')>1.905*GeV) | (WM('K-','pi+','pi+')<1.80*GeV))  & (INTREE((ABSID=='p+') &(PT>100*MeV) &(TRGHOSTPROB<0.35) &(BPVIPCHI2()>9.)))  & (INTREE((ABSID=='K+') &(PT>400*MeV) &(TRGHOSTPROB<0.35) &(BPVIPCHI2()>9.) &(PROBNNk>0.3))) &(INTREE((ABSID=='pi+')&(PT>400*MeV) &(TRGHOSTPROB<0.35) &(BPVIPCHI2()>9.) &(PROBNNpi>0.2))) & (({LcHlt2Tos}) |(INTREE((ABSID=='p+') &({PHlt2Tis})) ))").format( LcHlt2Tos=Hlt2TOS("Hlt2(CharmHadD2HHH|CharmHadD2HHHDWideMass)Decision"),PHlt2Tis=Hlt2TIS("Hlt2.*Decision")))






  Jpsiee = FilterCut("(BPVIPCHI2()<9.0) & (VFASPF(VCHI2/VDOF)<9) & (abs(MM-CHILD(MM,1)-2182.3)<100) & (inRange(2250,CHILD(MM,1),3600)) & (NINTREE(('e-'==ABSID)&(BPVIPCHI2()>25) )==2)")



  Jpsiee.printout()
  
##################################################
###      C O N F I G U R A T I O N   4     #######
###. . . . . . . . . . . . . . . . . . . . #######
### Configuration of the decay structures  #######
##################################################
### List of all the decays, input stripping line,
###  decay structure, and its branch
### TupleConfig and Branch are tricks to ensure
### all the mandatory entries are set or to
### raise an exception here in the configuration
### in case they are not.
### The keywork "Type" allows to set the Type of 
### the branch in order to inherit the proper set
### of Loki variables as configured in 
### "Configuration1".
### The Name of the branch as defined in the 
### dictionary is used to inherit variables as 
### defined in configuration2.
### Finally, the keyword "isAlso" allows to set
### other inheritance from configuration2.
### For example, the two muons from the J/psi
### are named mup and mum, but you want both to
### inherit from "mu" since they are muons.
##################################################
class TupleConfig:
  def __init__ (self                 
                  , Decay
                  , InputLines
                  , Branches
                  , Calibration
                  , Filter = None
                ):
    self.Decay = Decay; self.Branches = Branches; 

    if isinstance ( InputLines, list ):
      self.InputLines = InputLines
    else:
      self.InputLines = [InputLines]

    self.Calibration = Calibration
    self.Filter = Filter

class Branch:
  def __init__ (self
                , Particle
                , Type
                , isAlso = None
                , LokiVariables = None
               ):
    if LokiVariables == None : LokiVariables = {}
    if isAlso == None        : isAlso        = []

    if   Type == "H" : Type = "HEAD"
    elif Type == "I" : Type = "INTERMEDIATE"
    elif Type == "T" : Type = "TRACK"
    elif Type == "N" : Type = "NEUTRAL"
    self.Particle = Particle; self.LokiVariables = LokiVariables
    self.Type = Type; self.isAlso = isAlso
    

tupleConfiguration = {
  "DSt_PiP" : TupleConfig (
    Decay = "[D*(2010)+ -> ^(D0 -> K- ^pi+) pi+]CC"
    , InputLines    = "Hlt2PIDD02KPiTagTurboCalib"
    , Filter        = filters.PositiveID
    , Calibration   = "RSDStCalib_Pos"
    , Branches = {
        "Dst"     : Branch("^([D*(2010)+ -> (D0 -> K- pi+) pi+]CC)", Type='H')
        , "Dz"    : Branch( "[D*(2010)+ -> ^(D0 -> K- pi+) pi+]CC",  Type='I')
        #, "K"     : Branch( "[D*(2010)+ -> (D0 -> ^K- pi+) pi+]CC",  Type='T')
        , "probe" : Branch( "[D*(2010)+ -> (D0 -> K- ^pi+) pi+]CC",  Type='T', isAlso = ['pi'])
        #, "pis"   : Branch( "[D*(2010)+ -> (D0 -> K- pi+) ^pi+]CC",  Type='T', isAlso=['pi'])
      }
    ),

  "DSt_PiM" : TupleConfig (
    Decay = "[D*(2010)+ -> ^(D0 -> K- ^pi+) pi+]CC"
    , InputLines    = "Hlt2PIDD02KPiTagTurboCalib"
    , Filter        = filters.NegativeID
    , Calibration   = "RSDStCalib_Neg"
    , Branches = {
        "Dst"     : Branch("^([D*(2010)+ -> (D0 -> K- pi+) pi+]CC)", Type='H')
        , "Dz"    : Branch( "[D*(2010)+ -> ^(D0 -> K- pi+) pi+]CC",  Type='I')
        #, "K"     : Branch( "[D*(2010)+ -> (D0 -> ^K- pi+) pi+]CC",  Type='T')
        , "probe" : Branch( "[D*(2010)+ -> (D0 -> K- ^pi+) pi+]CC",  Type='T', isAlso = ['pi'])
        #, "pis"   : Branch( "[D*(2010)+ -> (D0 -> K- pi+) ^pi+]CC",  Type='T', isAlso=['pi'])
      }
    ),

  "DSt_KP" : TupleConfig (
    Decay = "[D*(2010)+ -> ^(D0 -> ^K- pi+) pi+]CC"
    , InputLines    = "Hlt2PIDD02KPiTagTurboCalib"
    , Calibration   = "RSDStCalib_Neg"
    , Filter        = filters.NegativeID #WARNING! K has opposite sign to D*
    , Branches = {
        "Dst"     : Branch("^([D*(2010)+ -> (D0 -> K- pi+) pi+]CC)", Type='H')
        , "Dz"    : Branch( "[D*(2010)+ -> ^(D0 -> K- pi+) pi+]CC",  Type='I')
        , "probe" : Branch( "[D*(2010)+ -> (D0 -> ^K- pi+) pi+]CC",  Type='T', isAlso=['K'])
        #, "pi"    : Branch( "[D*(2010)+ -> (D0 -> K- ^pi+) pi+]CC",  Type='T')
        #, "pis"   : Branch( "[D*(2010)+ -> (D0 -> K- pi+) ^pi+]CC",  Type='T', isAlso=['pi'])
      }
    ),

  "DSt_KM" : TupleConfig (
    Decay = "[D*(2010)+ -> ^(D0 -> ^K- pi+) pi+]CC"
    , InputLines    = "Hlt2PIDD02KPiTagTurboCalib"
    , Calibration   = "RSDStCalib_Pos"
    , Filter        = filters.PositiveID #WARNING! K has opposite sign to D*
    , Branches = {
        "Dst"     : Branch("^([D*(2010)+ -> (D0 -> K- pi+) pi+]CC)", Type='H')
        , "Dz"    : Branch( "[D*(2010)+ -> ^(D0 -> K- pi+) pi+]CC",  Type='I')
        , "probe" : Branch( "[D*(2010)+ -> (D0 -> ^K- pi+) pi+]CC",  Type='T', isAlso=['K'])
        #, "pi"    : Branch( "[D*(2010)+ -> (D0 -> K- ^pi+) pi+]CC",  Type='T')
        #, "pis"   : Branch( "[D*(2010)+ -> (D0 -> K- pi+) ^pi+]CC",  Type='T', isAlso=['pi'])
      }
    ),

    "Lam0_P" : TupleConfig (
      Decay =  "[Lambda0 -> ^p+ pi-]CC"
      , InputLines    = ["Hlt2PIDLambda2PPiLLTurboCalib"]
      , Calibration   = "Lam0Calib_Pos"
      , Filter        = filters.PositiveID
      , Branches = {
          "L0"      : Branch("^([Lambda0 -> p+ pi-]CC)", Type='H')
          , "probe" : Branch("[Lambda0 -> ^p+ pi-]CC", Type='T', isAlso=['p'])
          #, "pi" : Branch("[Lambda0 -> p+ ^pi-]CC", Type='T')
        }
      ),

    "Lam0_Pbar" : TupleConfig (
      Decay =  "[Lambda0 -> ^p+ pi-]CC"
      , InputLines    = ["Hlt2PIDLambda2PPiLLTurboCalib"]
      , Calibration   = "Lam0Calib_Neg"
      , Filter        = filters.NegativeID
      , Branches = {
          "L0"      : Branch("^([Lambda0 -> p+ pi-]CC)", Type='H')
          , "probe" : Branch("[Lambda0 -> ^p+ pi-]CC", Type='T', isAlso=['p'])
          #, "pi" : Branch("[Lambda0 -> p+ ^pi-]CC", Type='T')
        }
      ),

    "Lam0_HPT_P" : TupleConfig (
      Decay =  "[Lambda0 -> ^p+ pi-]CC"
      , InputLines    = ["Hlt2PIDLambda2PPiLLhighPTTurboCalib"]
      , Calibration   = "Lam0Calib_HPT_Pos"
      , Filter        = filters.PositiveID
      , Branches = {
          "L0"      : Branch("^([Lambda0 -> p+ pi-]CC)", Type='H')
          , "probe" : Branch("[Lambda0 -> ^p+ pi-]CC", Type='T', isAlso=['p'])
          #, "pi" : Branch("[Lambda0 -> p+ ^pi-]CC", Type='T')
        }
      ),

    "Lam0_HPT_Pbar" : TupleConfig (
      Decay =  "[Lambda0 -> ^p+ pi-]CC"
      , InputLines    = ["Hlt2PIDLambda2PPiLLhighPTTurboCalib"]
      , Calibration   = "Lam0Calib_HPT_Neg"
      , Filter        = filters.NegativeID
      , Branches = {
          "L0"      : Branch("^([Lambda0 -> p+ pi-]CC)", Type='H')
          , "probe" : Branch("[Lambda0 -> ^p+ pi-]CC", Type='T', isAlso=['p'])
          #, "pi" : Branch("[Lambda0 -> p+ ^pi-]CC", Type='T')
        }
      ),

    "Lam0_VHPT_P" : TupleConfig (
      Decay =  "[Lambda0 -> ^p+ pi-]CC"
      , InputLines    = ["Hlt2PIDLambda2PPiLLveryhighPTTurboCalib"]
      , Calibration   = "Lam0Calib_VHPT_Pos"
      , Filter        = filters.PositiveID
      , Branches = {
          "L0"      : Branch("^([Lambda0 -> p+ pi-]CC)", Type='H')
          , "probe" : Branch("[Lambda0 -> ^p+ pi-]CC", Type='T', isAlso=['p'])
          #, "pi" : Branch("[Lambda0 -> p+ ^pi-]CC", Type='T')
        }
      ),

    "Lam0_VHPT_Pbar" : TupleConfig (
      Decay =  "[Lambda0 -> ^p+ pi-]CC"
      , InputLines    = ["Hlt2PIDLambda2PPiLLveryhighPTTurboCalib"]
      , Calibration   = "Lam0Calib_VHPT_Neg"
      , Filter        = filters.NegativeID
      , Branches = {
          "L0"      : Branch("^([Lambda0 -> p+ pi-]CC)", Type='H')
          , "probe" : Branch("[Lambda0 -> ^p+ pi-]CC", Type='T', isAlso=['p'])
          #, "pi" : Branch("[Lambda0 -> p+ ^pi-]CC", Type='T')
        }
      ),


    "Lam0_P_isMuon" : TupleConfig (
      Decay =  "[Lambda0 -> ^p+ pi-]CC"
      , InputLines    = ["Hlt2PIDLambda2PPiLLisMuonTurboCalib"]
      , Calibration   = "Lam0Calib_Pos"
      , Filter        = filters.PositiveID
      , Branches = {
          "L0"      : Branch("^([Lambda0 -> p+ pi-]CC)", Type='H')
          , "probe" : Branch("[Lambda0 -> ^p+ pi-]CC", Type='T', isAlso=['p'])
          #, "pi" : Branch("[Lambda0 -> p+ ^pi-]CC", Type='T')
        }
      ),

    "Lam0_Pbar_isMuon" : TupleConfig (
      Decay =  "[Lambda0 -> ^p+ pi-]CC"
      , InputLines    = ["Hlt2PIDLambda2PPiLLisMuonTurboCalib"]
      , Calibration   = "Lam0Calib_Neg"
      , Filter        = filters.NegativeID
      , Branches = {
          "L0"      : Branch("^([Lambda0 -> p+ pi-]CC)", Type='H')
          , "probe" : Branch("[Lambda0 -> ^p+ pi-]CC", Type='T', isAlso=['p'])
          #, "pi" : Branch("[Lambda0 -> p+ ^pi-]CC", Type='T')
        }
      ),

    "B_Jpsi_EP" : TupleConfig (
      Decay = "[B+]cc -> ^(J/psi(1S) -> ^e+ ^e-) ^([K+]cc)"
      , InputLines    = ["Hlt2PIDB2KJPsiEENegTaggedTurboCalib"]
      , Calibration   = "BJpsiEECalib_Pos"
      , Filter        = None
      , Branches = {
          "B"    : Branch("^([B+]cc ->  (J/psi(1S) ->  e+  e-) [ K+]cc)", Type='H')
          , "Jpsi" : Branch("[B+]cc -> ^(J/psi(1S) ->  e+  e-) [ K+]cc", Type='I')
          , "probe": Branch("[B+]cc ->  (J/psi(1S) -> ^e+  e-) [ K+]cc", Type='T', isAlso = ['e'])
          , "tag"  : Branch("[B+]cc ->  (J/psi(1S) ->  e+ ^e-) [ K+]cc", Type='T', isAlso = ['e'])
          , "K"    : Branch("[B+]cc ->  (J/psi(1S) ->  e+  e-) ^([K+]cc)", Type='T')
        }
      ),

    "B_Jpsi_EM" : TupleConfig (
      Decay = "[B+]cc -> ^(J/psi(1S) -> ^e+ ^e-) ^([K+]cc)"
      , InputLines    = ["Hlt2PIDB2KJPsiEEPosTaggedTurboCalib"]
      , Calibration   = "BJpsiEECalib_Neg"
      , Filter        = None
      , Branches = {
          "B"    : Branch("^([B+]cc ->  (J/psi(1S) ->  e+  e-) [ K+]cc)", Type='H')
          , "Jpsi" : Branch("[B+]cc -> ^(J/psi(1S) ->  e+  e-) [ K+]cc", Type='I')
          , "probe": Branch("[B+]cc ->  (J/psi(1S) ->  e+ ^e-) [ K+]cc", Type='T', isAlso = ['e'])
          , "tag"  : Branch("[B+]cc ->  (J/psi(1S) -> ^e+  e-) [ K+]cc", Type='T', isAlso = ['e'])
          , "K"    : Branch("[B+]cc ->  (J/psi(1S) ->  e+  e-) ^([K+]cc)", Type='T')
        }
      ),

    "Jpsi_MuP" : TupleConfig (
      Decay = "J/psi(1S) -> ^mu+ ^mu-"
      , InputLines     = ["Hlt2PIDDetJPsiMuMuNegTaggedTurboCalib"]
      , Calibration   = "JpsiCalib_Pos"
      , Filter        = filters.MuonUnBiased
#      , Filter        = None
      , Branches = {
          "Jpsi" : Branch("^(J/psi(1S) -> mu+ mu-)", Type='H')
          , "probe": Branch("J/psi(1S) -> ^mu+ mu-", Type='T', isAlso = ['mu'])
          , "tag"  : Branch("J/psi(1S) -> mu+ ^mu-", Type='T', isAlso = ['mu'])
        }
      ),

    "Jpsi_MuM" : TupleConfig (
      Decay = "J/psi(1S) -> ^mu+ ^mu-"
      , InputLines     = ["Hlt2PIDDetJPsiMuMuPosTaggedTurboCalib"]
      , Calibration   = "JpsiCalib_Neg"
      , Filter        = filters.MuonUnBiased
#      , Filter        = None
      , Branches = {
          "Jpsi" : Branch("^(J/psi(1S) -> mu+ mu-)", Type='H')
          , "tag"  : Branch("J/psi(1S) -> ^mu+ mu-", Type='T', isAlso = ['mu'])
          , "probe": Branch("J/psi(1S) -> mu+ ^mu-", Type='T', isAlso = ['mu'])
        }
      ),

    "KS_PiP" : TupleConfig (
      Decay = "KS0 -> pi+ pi-"
      , InputLines     = ["Hlt2PIDKs2PiPiLLTurboCalib"]
      , Calibration   = "KS0Calib"
      , Filter        = None
      , Branches = {
          "KS" : Branch("^(KS0 -> pi+ pi-)", Type='H')
          , "tag"  : Branch("KS0 -> pi+ ^pi-", Type='T', isAlso = ['pi'])
          , "probe": Branch("KS0 -> ^pi+ pi-", Type='T', isAlso = ['pi'])
        }
      ),

    "KS_PiM" : TupleConfig (
      Decay = "KS0 -> pi+ pi-"
      , InputLines     = ["Hlt2PIDKs2PiPiLLTurboCalib"]
      , Calibration   = "KS0Calib"
      , Filter        = None
      , Branches = {
          "KS" : Branch("^(KS0 -> pi+ pi-)", Type='H')
          , "tag"  : Branch("KS0 -> ^pi+ pi-", Type='T', isAlso = ['pi'])
          , "probe": Branch("KS0 -> pi+ ^pi-", Type='T', isAlso = ['pi'])
        }
      ),

    "DsPhi_KP_notag" : TupleConfig (
      Decay = "[D_s+]cc -> ^(phi(1020) -> ^K- ^K+) ^([pi+]cc)"
      , InputLines    = ["Hlt2PIDDs2PiPhiKKUnbiasedTurboCalib"]
      , Calibration   = "DsPhiCalib_notag"
      , Filter        = None
      , Branches = {
          "Ds"     : Branch("^([D_s+]cc -> (phi(1020) ->  K-  K+) [ pi+]cc)", Type='H')
          , "phi"  : Branch("[D_s+]cc -> ^(phi(1020) ->  K-  K+) [ pi+]cc", Type='I')
          , "probe": Branch("[D_s+]cc ->  (phi(1020) ->  K- ^K+) [ pi+]cc", Type='T', isAlso = ['K'])
          , "tag"  : Branch("[D_s+]cc ->  (phi(1020) -> ^K-  K+) [ pi+]cc", Type='T', isAlso = ['K'])
          , "pi"   : Branch("[D_s+]cc ->  (phi(1020) ->  K-  K+) ^([pi+]cc)", Type='T')
        }
      ),

    "DsPhi_KM_notag" : TupleConfig (
      Decay = "[D_s+]cc -> ^(phi(1020) -> ^K- ^K+) ^([pi+]cc)"
      , InputLines    = ["Hlt2PIDDs2PiPhiKKUnbiasedTurboCalib"]
      , Calibration   = "DsPhiCalib_notag"
      , Filter        = None
      , Branches = {
          "Ds"     : Branch("^([D_s+]cc -> (phi(1020) ->  K-  K+) [ pi+]cc)", Type='H')
          , "phi"  : Branch("[D_s+]cc -> ^(phi(1020) ->  K-  K+) [ pi+]cc", Type='I')
          , "tag"  : Branch("[D_s+]cc ->  (phi(1020) ->  K- ^K+) [ pi+]cc", Type='T', isAlso = ['K'])
          , "probe": Branch("[D_s+]cc ->  (phi(1020) -> ^K-  K+) [ pi+]cc", Type='T', isAlso = ['K'])
          , "pi"   : Branch("[D_s+]cc ->  (phi(1020) ->  K-  K+) ^([pi+]cc)", Type='T')
        }
      ),


    "LbLcMu_P" : TupleConfig (
      Decay = "[Lambda_b0 -> ^(Lambda_c+ -> ^p+ ^K- ^pi+) ^mu-]CC"
      , InputLines    = ["Hlt2PIDLb2LcMuNuTurboCalib"]
      , Calibration   = "LbLcMuCalib"
      , Filter        = filters.PositiveID
      , Branches = {
          "Lb"      : Branch("^([Lambda_b0 ->  (Lambda_c+ ->  p+  K-  pi+)  mu-]CC)", Type='H')
          , "Lc"    : Branch("[Lambda_b0 -> ^(Lambda_c+ ->  p+  K-  pi+)  mu-]CC", Type='I')
          , "K"     : Branch("[Lambda_b0 ->  (Lambda_c+ ->  p+ ^K-  pi+)  mu-]CC", Type='T')
          , "pi"    : Branch("[Lambda_b0 ->  (Lambda_c+ ->  p+  K- ^pi+)  mu-]CC", Type='T')
          , "probe" : Branch("[Lambda_b0 ->  (Lambda_c+ -> ^p+  K-  pi+)  mu-]CC", Type='T', isAlso = ['p'])
          , "mu"    : Branch("[Lambda_b0 ->  (Lambda_c+ ->  p+  K-  pi+) ^mu-]CC", Type='T')
        }
      ),


    "LbLcMu_Pbar" : TupleConfig (
      Decay = "[Lambda_b0 -> ^(Lambda_c+ -> ^p+ ^K- ^pi+) ^mu-]CC"
      , InputLines    = ["Hlt2PIDLb2LcMuNuTurboCalib"]
      , Calibration   = "LbLcMuCalib"
      , Filter        = filters.NegativeID
      , Branches = {
          "Lb"      : Branch("^([Lambda_b0 ->  (Lambda_c+ ->  p+  K-  pi+)  mu-]CC)", Type='H')
          , "Lc"    : Branch("[Lambda_b0 -> ^(Lambda_c+ ->  p+  K-  pi+)  mu-]CC", Type='I')
          , "K"     : Branch("[Lambda_b0 ->  (Lambda_c+ ->  p+ ^K-  pi+)  mu-]CC", Type='T')
          , "pi"    : Branch("[Lambda_b0 ->  (Lambda_c+ ->  p+  K- ^pi+)  mu-]CC", Type='T')
          , "probe" : Branch("[Lambda_b0 ->  (Lambda_c+ -> ^p+  K-  pi+)  mu-]CC", Type='T', isAlso = ['p'])
          , "mu"    : Branch("[Lambda_b0 ->  (Lambda_c+ ->  p+  K-  pi+) ^mu-]CC", Type='T')
        }
      ),


    "DsPhi_MuP" : TupleConfig (
      Decay = "[D_s+]cc -> ^(phi(1020) -> ^mu- ^mu+) ^([pi+]cc)"
      , InputLines    = ["Hlt2PIDDs2PiPhiMuMuNegTaggedTurboCalib"]
      , Calibration   = None
      , Filter        = None
      , Branches = {
          "Ds" : Branch("^([D_s+]cc -> (phi(1020) -> mu- mu+) [pi+]cc)", Type='H')
          , "phi" : Branch("[D_s+]cc -> ^(phi(1020) -> mu- mu+) [pi+]cc", Type='I')
          , "probe" : Branch("[D_s+]cc ->  (phi(1020) ->  mu- ^mu+)  ([pi+]cc)", Type='T', isAlso = ['mu'])
          , "tag"   : Branch("[D_s+]cc ->  (phi(1020) -> ^mu-  mu+)  ([pi+]cc)", Type='T', isAlso = ['mu'])
        }
      ),

    "DsPhi_MuM" : TupleConfig (
      Decay = "[D_s+]cc -> ^(phi(1020) -> ^mu- ^mu+) ^([pi+]cc)"
      , InputLines    = ["Hlt2PIDDs2PiPhiMuMuPosTaggedTurboCalib"]
      , Calibration   = None
      , Filter        = None
      , Branches = {
          "Ds" : Branch("^([D_s+]cc -> (phi(1020) -> mu- mu+) [pi+]cc)", Type='H')
          , "phi" : Branch("[D_s+]cc -> ^(phi(1020) -> mu- mu+) [pi+]cc", Type='I')
          , "probe" : Branch("[D_s+]cc ->  (phi(1020) -> ^mu-  mu+)  ([pi+]cc)", Type='T', isAlso = ['mu'])
          , "tag"   : Branch("[D_s+]cc ->  (phi(1020) ->  mu- ^mu+)  ([pi+]cc)", Type='T', isAlso = ['mu'])
        }
      ),

    "DsPhi_KP" : TupleConfig (
      Decay = "[D_s+]cc -> ^(phi(1020) -> ^K- ^K+) ^([pi+]cc)"
      , InputLines    = ["Hlt2PIDDs2PiPhiKKNegTaggedTurboCalib"]
      , Calibration   = "DsPhiCalib_Pos"
      , Filter        = None
      , Branches = {
          "Ds" : Branch("^([D_s+]cc -> (phi(1020) -> K- K+) [pi+]cc)", Type='H')
          , "phi" : Branch("[D_s+]cc -> ^(phi(1020) -> K- K+) [pi+]cc", Type='I')
          , "probe" : Branch("[D_s+]cc ->  (phi(1020) ->  K- ^K+)  ([pi+]cc)", Type='T', isAlso = ['K'])
          , "tag"   : Branch("[D_s+]cc ->  (phi(1020) -> ^K-  K+)  ([pi+]cc)", Type='T', isAlso = ['K'])
        }
      ),

    "DsPhi_KM" : TupleConfig (
      Decay = "[D_s+]cc -> ^(phi(1020) -> ^K- ^K+) ^([pi+]cc)"
      , InputLines    = ["Hlt2PIDDs2PiPhiKKPosTaggedTurboCalib"]
      , Calibration   = "DsPhiCalib_Neg"
      , Filter        = None
      , Branches = {
          "Ds" : Branch("^([D_s+]cc -> (phi(1020) -> K- K+) [pi+]cc)", Type='H')
          , "phi" : Branch("[D_s+]cc -> ^(phi(1020) -> K- K+) [pi+]cc", Type='I')
          , "probe" : Branch("[D_s+]cc ->  (phi(1020) -> ^K-  K+)  ([pi+]cc)", Type='T', isAlso = ['K'])
          , "tag"   : Branch("[D_s+]cc ->  (phi(1020) ->  K- ^K+)  ([pi+]cc)", Type='T', isAlso = ['K'])
        }
      ),

    "B_Jpsi_P" : TupleConfig (
      Decay = "[B+]cc -> ^(J/psi(1S) -> ^p+ ^p~-) ^([K+]cc)"
      , InputLines     = ["Hlt2PIDB2KJPsiPPNegTaggedTurboCalib"]
      , Calibration   = None
      , Filter        = None
      , Branches = {
          "B"    : Branch("^([B+]cc ->  (J/psi(1S) ->  p+  p~-) [ K+]cc)", Type='H')
          , "Jpsi" : Branch("[B+]cc -> ^(J/psi(1S) ->  p+  p~-) [ K+]cc", Type='I')
          , "probe": Branch("[B+]cc ->  (J/psi(1S) -> ^p+  p~-) [ K+]cc", Type='T', isAlso = ['p'])
          , "tag"  : Branch("[B+]cc ->  (J/psi(1S) ->  p+ ^p~-) [ K+]cc", Type='T', isAlso = ['p'])
          , "K"    : Branch("[B+]cc ->  (J/psi(1S) ->  p+  p~-) ^([K+]cc)", Type='T')
        }
      ),

    "B_Jpsi_Pbar" : TupleConfig (
      Decay = "[B+]cc -> ^(J/psi(1S) -> ^p+ ^p~-) ^([K+]cc)"
      , InputLines     = ["Hlt2PIDB2KJPsiPPPosTaggedTurboCalib"]
      , Calibration   = None
      , Filter        = None
      , Branches = {
          "B"    : Branch("^([B+]cc ->  (J/psi(1S) ->  p+  p~-) [ K+]cc)", Type='H')
          , "Jpsi" : Branch("[B+]cc -> ^(J/psi(1S) ->  p+  p~-) [ K+]cc", Type='I')
          , "tag"  : Branch("[B+]cc ->  (J/psi(1S) -> ^p+  p~-) [ K+]cc", Type='T', isAlso = ['p'])
          , "probe": Branch("[B+]cc ->  (J/psi(1S) ->  p+ ^p~-) [ K+]cc", Type='T', isAlso = ['p'])
          , "K"    : Branch("[B+]cc ->  (J/psi(1S) ->  p+  p~-) ^([K+]cc)", Type='T')
        }
      ),

    "B_Jpsi_MuP" : TupleConfig (
      Decay = "[B+]cc -> ^(J/psi(1S) -> ^mu+ ^mu-) ^([K+]cc)"
      , InputLines     = ["Hlt2PIDB2KJPsiMuMuNegTaggedTurboCalib"]
      , Calibration   = "BJpsiCalib_Pos"
      , Filter        = None
      , Branches = {
          "B"    : Branch("^([B+]cc ->  (J/psi(1S) ->  mu+  mu-) [ K+]cc)", Type='H')
          , "Jpsi" : Branch("[B+]cc -> ^(J/psi(1S) ->  mu+  mu-) [ K+]cc", Type='I')
          , "probe": Branch("[B+]cc ->  (J/psi(1S) -> ^mu+  mu-) [ K+]cc", Type='T', isAlso = ['mu'])
          , "tag"  : Branch("[B+]cc ->  (J/psi(1S) ->  mu+ ^mu-) [ K+]cc", Type='T', isAlso = ['mu'])
          , "K"    : Branch("[B+]cc ->  (J/psi(1S) ->  mu+  mu-) ^([K+]cc)", Type='T')
        }
      ),

    "B_Jpsi_MuM" : TupleConfig (
      Decay = "[B+]cc -> ^(J/psi(1S) -> ^mu+ ^mu-) ^([K+]cc)"
      , InputLines     = ["Hlt2PIDB2KJPsiMuMuPosTaggedTurboCalib"]
      , Calibration   = "BJpsiCalib_Neg"
      , Filter        = None
      , Branches = {
          "B"    : Branch("^([B+]cc ->  (J/psi(1S) ->  mu+  mu-) [ K+]cc)", Type='H')
          , "Jpsi" : Branch("[B+]cc -> ^(J/psi(1S) ->  mu+  mu-) [ K+]cc", Type='I')
          , "tag"  : Branch("[B+]cc ->  (J/psi(1S) -> ^mu+  mu-) [ K+]cc", Type='T', isAlso = ['mu'])
          , "probe": Branch("[B+]cc ->  (J/psi(1S) ->  mu+ ^mu-) [ K+]cc", Type='T', isAlso = ['mu'])
          , "K"    : Branch("[B+]cc ->  (J/psi(1S) ->  mu+  mu-) ^([K+]cc)", Type='T')
        }
      ),

    "Jpsi_EP" : TupleConfig (
      Decay = "J/psi(1S) -> ^e+ ^e-"
      , InputLines     = ["Hlt2PIDDetJPsiEENegTaggedTurboCalib"]
      , Calibration   = None
      , Filter        = None
      , Branches = {
          "Jpsi" : Branch("^(J/psi(1S) -> e+ e-)", Type='H')
          , "probe": Branch("J/psi(1S) -> ^e+ e-", Type='T', isAlso = ['e'])
          , "tag"  : Branch("J/psi(1S) -> e+ ^e-", Type='T', isAlso = ['e'])
        }
      ),

    "Jpsi_EM" : TupleConfig (
      Decay = "J/psi(1S) -> ^e+ ^e-"
      , InputLines     = ["Hlt2PIDDetJPsiEEPosTaggedTurboCalib"]
      , Calibration   = None
      , Filter        = None
      , Branches = {
          "Jpsi" : Branch("^(J/psi(1S) -> e+ e-)", Type='H')
          , "tag"  : Branch("J/psi(1S) -> ^e+ e-", Type='T', isAlso = ['e'])
          , "probe": Branch("J/psi(1S) -> e+ ^e-", Type='T', isAlso = ['e'])
        }
      ),

    "Sigmac0_P" : TupleConfig (
      Decay = "Sigma_c0 -> ^(Lambda_c+ -> ^p+ ^pi+ ^K-) ^pi-"
      , InputLines     = ["Hlt2PIDSc02LcPiTurboCalib"]
      , Calibration   = None
      , Filter        = filters.PositiveID
      , Branches = {
          "Sigmacz" : Branch("^(Sigma_c0 ->  (Lambda_c+ ->  p+  pi+  K-)  pi-)", Type='H')
          , "Lc"      : Branch("Sigma_c0 -> ^(Lambda_c+ ->  p+  pi+  K-)  pi-", Type='I')
          , "probe"   : Branch("Sigma_c0 ->  (Lambda_c+ -> ^p+  pi+  K-)  pi-", Type='T')
          , "pi_Lc"   : Branch("Sigma_c0 ->  (Lambda_c+ ->  p+ ^pi+  K-)  pi-", Type='T')
          , "K_Lc"    : Branch("Sigma_c0 ->  (Lambda_c+ ->  p+  pi+ ^K-)  pi-", Type='T')
          , "pim"     : Branch("Sigma_c0 ->  (Lambda_c+ ->  p+  pi+  K-) ^pi-", Type='T')
        }
      ),

    "Sigmac0_Pbar" : TupleConfig (
      Decay = "[Sigma_c0 -> ^(Lambda_c+ -> ^p+ ^pi+ ^K-) ^pi-]CC"
      , InputLines     = ["Hlt2PIDSc02LcPiTurboCalib"]
      , Calibration   = None
      , Filter        = filters.NegativeID
      , Branches = {
          "Sigmacz" : Branch("^([Sigma_c0 ->  (Lambda_c+ ->  p+  pi+  K-)  pi-]CC)", Type='H')
          , "Lc"      : Branch("[Sigma_c0 -> ^(Lambda_c+ ->  p+  pi+  K-)  pi-]CC", Type='I')
          , "probe"   : Branch("[Sigma_c0 ->  (Lambda_c+ -> ^p+  pi+  K-)  pi-]CC", Type='T')
          , "pi_Lc"   : Branch("[Sigma_c0 ->  (Lambda_c+ ->  p+ ^pi+  K-)  pi-]CC", Type='T')
          , "K_Lc"    : Branch("[Sigma_c0 ->  (Lambda_c+ ->  p+  pi+ ^K-)  pi-]CC", Type='T')
          , "pim"     : Branch("[Sigma_c0 ->  (Lambda_c+ ->  p+  pi+  K-) ^pi-]CC", Type='T')
        }
      ),
    
    "Sigmacpp_P" : TupleConfig (
      Decay = "Sigma_c++ -> ^(Lambda_c+ -> ^p+ ^pi+ ^K-) ^pi+"
      , InputLines     = ["Hlt2PIDScpp2LcPiTurboCalib"]
      , Calibration   = None
      , Filter        = None
      , Branches = {
          "Sigmac"  : Branch("^(Sigma_c++ ->  (Lambda_c+ ->  p+  pi+  K-)  pi+)", Type='H')
          , "Lc"      : Branch("Sigma_c++ -> ^(Lambda_c+ ->  p+  pi+  K-)  pi+", Type='I')
          , "probe"   : Branch("Sigma_c++ ->  (Lambda_c+ -> ^p+  pi+  K-)  pi+", Type='T')
          , "pi_Lc"   : Branch("Sigma_c++ ->  (Lambda_c+ ->  p+ ^pi+  K-)  pi+", Type='T')
          , "K_Lc"    : Branch("Sigma_c++ ->  (Lambda_c+ ->  p+  pi+ ^K-)  pi+", Type='T')
          , "pim"     : Branch("Sigma_c++ ->  (Lambda_c+ ->  p+  pi+  K-) ^pi+", Type='T')
        }
      ),

    "Sigmacpp_Pbar" : TupleConfig (
      Decay = "Sigma_c~-- -> ^(Lambda_c~- -> ^p~- ^pi- ^K+) ^pi-"
      , InputLines     = ["Hlt2PIDScpp2LcPiTurboCalib"]
      , Calibration   = None
      , Filter        = None
      , Branches = {
          "Sigmac"  : Branch("^(Sigma_c~-- ->  (Lambda_c~- ->  p~-  pi-  K+)  pi-)", Type='H')
          , "Lc"      : Branch("Sigma_c~-- -> ^(Lambda_c~- ->  p~-  pi-  K+)  pi-", Type='I')
          , "probe"   : Branch("Sigma_c~-- ->  (Lambda_c~- -> ^p~-  pi-  K+)  pi-", Type='T')
          , "pi_Lc"   : Branch("Sigma_c~-- ->  (Lambda_c~- ->  p~- ^pi-  K+)  pi-", Type='T')
          , "K_Lc"    : Branch("Sigma_c~-- ->  (Lambda_c~- ->  p~-  pi- ^K+)  pi-", Type='T')
          , "pim"     : Branch("Sigma_c~-- ->  (Lambda_c~- ->  p~-  pi-  K+) ^pi-", Type='T')
        }
      ),
    
    "Jpsi_P" : TupleConfig (
      Decay = "J/psi(1S) -> ^p+ ^p~-"
      , InputLines     = ["Hlt2PIDDetJPsiPPNegTaggedTurboCalib"]
      , Calibration   = None
      , Filter        = None
      , Branches = {
          "Jpsi" : Branch("^(J/psi(1S) ->  p+  p~-)", Type='H')
          , "probe": Branch("J/psi(1S) -> ^p+  p~-", Type='T', isAlso = ['p'])
          , "tag"  : Branch("J/psi(1S) ->  p+ ^p~-", Type='T', isAlso = ['p'])
        }
      ),

    "Jpsi_Pbar" : TupleConfig (
      Decay = "J/psi(1S) -> ^p+ ^p~-"
      , InputLines     = ["Hlt2PIDDetJPsiPPPosTaggedTurboCalib"]
      , Calibration   = None
      , Filter        = None
      , Branches = {
          "Jpsi" : Branch("^(J/psi(1S) ->  p+  p~-)", Type='H')
          , "tag"  : Branch("J/psi(1S) -> ^p+  p~-", Type='T', isAlso = ['p'])
          , "probe": Branch("J/psi(1S) ->  p+ ^p~-", Type='T', isAlso = ['p'])
        }
      ),


    "DSt3Pi_PiP" : TupleConfig (
      Decay = "[D*(2010)+ -> ^(D0 -> K- ^pi+ pi- pi+) pi+]CC"
      , InputLines    = "Hlt2PIDD02KPiPiPiTagTurboCalib"
      , Filter        = filters.PositiveID
      , Calibration   = "DSt4bCalib_Pos"
      , Branches = {
          "Dst"     : Branch("^([D*(2010)+ -> (D0 -> K- pi+ pi- pi+) pi+]CC)", Type='H')
          , "Dz"    : Branch( "[D*(2010)+ -> ^(D0 -> K- pi+ pi- pi+) pi+]CC",  Type='I')
          #, "K"     : Branch( "[D*(2010)+ -> (D0 -> ^K- pi+ pi- pi+) pi+]CC",  Type='T')
          , "probe" : Branch( "[D*(2010)+ -> (D0 -> K- ^pi+ pi- pi+) pi+]CC",  Type='T', isAlso = ['pi'])
          #, "pis"   : Branch( "[D*(2010)+ -> (D0 -> K- pi+ pi- pi+) ^pi+]CC",  Type='T', isAlso=['pi'])
        }
      ),
  
    "DSt3Pi_PiM" : TupleConfig (
      Decay = "[D*(2010)+ -> ^(D0 -> K- ^pi+ pi- pi+) pi+]CC"
      , InputLines    = "Hlt2PIDD02KPiPiPiTagTurboCalib"
      , Filter        = filters.NegativeID
      , Calibration   = "DSt4bCalib_Neg"
      , Branches = {
          "Dst"     : Branch("^([D*(2010)+ -> (D0 -> K- pi+ pi- pi+) pi+]CC)", Type='H')
          , "Dz"    : Branch( "[D*(2010)+ -> ^(D0 -> K- pi+ pi- pi+) pi+]CC",  Type='I')
          #, "K"     : Branch( "[D*(2010)+ -> (D0 -> ^K- pi+ pi- pi+) pi+]CC",  Type='T')
          , "probe" : Branch( "[D*(2010)+ -> (D0 -> K- ^pi+ pi- pi+) pi+]CC",  Type='T', isAlso = ['pi'])
          #, "pis"   : Branch( "[D*(2010)+ -> (D0 -> K- pi+ pi- pi+) ^pi+]CC",  Type='T', isAlso=['pi'])
        }
      ),
    
    "DSt3Pi_KP" : TupleConfig (
      Decay = "[D*(2010)+ -> ^(D0 -> ^K- pi+ pi- pi+) pi+]CC"
      , InputLines    = "Hlt2PIDD02KPiPiPiTagTurboCalib"
      , Calibration   = "DSt4bCalib_Neg"
      , Filter        = filters.NegativeID #WARNING! K has opposite sign to D*
      , Branches = {
          "Dst"     : Branch("^([D*(2010)+ -> (D0 -> K- pi+ pi- pi+) pi+]CC)", Type='H')
          , "Dz"    : Branch( "[D*(2010)+ -> ^(D0 -> K- pi+ pi- pi+) pi+]CC",  Type='I')
          , "probe" : Branch( "[D*(2010)+ -> (D0 -> ^K- pi+ pi- pi+) pi+]CC",  Type='T', isAlso=['K'])
          #, "pi"    : Branch( "[D*(2010)+ -> (D0 -> K- ^pi+) pi+]CC",  Type='T')
          #, "pis"   : Branch( "[D*(2010)+ -> (D0 -> K- pi+) ^pi+]CC",  Type='T', isAlso=['pi'])
        }
      ),
  
    "DSt3Pi_KM" : TupleConfig (
      Decay = "[D*(2010)+ -> ^(D0 -> ^K- pi+ pi- pi+) pi+]CC"
      , InputLines    = "Hlt2PIDD02KPiPiPiTagTurboCalib"
      , Calibration   = "DSt4bCalib_Pos"
      , Filter        = filters.PositiveID #WARNING! K has opposite sign to D*
      , Branches = {
          "Dst"     : Branch("^([D*(2010)+ -> (D0 -> K- pi+ pi- pi+) pi+]CC)", Type='H')
          , "Dz"    : Branch( "[D*(2010)+ -> ^(D0 -> K- pi+ pi- pi+) pi+]CC",  Type='I')
          , "probe" : Branch( "[D*(2010)+ -> (D0 -> ^K- pi+ pi- pi+) pi+]CC",  Type='T', isAlso=['K'])
          #, "pi"    : Branch( "[D*(2010)+ -> (D0 -> K- ^pi+ pi- pi+) pi+]CC",  Type='T')
          #, "pis"   : Branch( "[D*(2010)+ -> (D0 -> K- pi+ pi- pi+) ^pi+]CC",  Type='T', isAlso=['pi'])
        }
      ),

    "Phi_MuP" : TupleConfig (
      Decay = "phi(1020) -> ^mu+ ^mu-"
      , InputLines     = ["Hlt2PIDDetPhiMuMuNegTaggedTurboCalib"]
      , Calibration   = None
      , Filter        = filters.MuonUnBiased
      , Branches = {
          "phi" : Branch("^(phi(1020) -> mu+ mu-)", Type='H')
          , "probe": Branch("phi(1020) -> ^mu+ mu-", Type='T', isAlso = ['mu'])
          , "tag"  : Branch("phi(1020) -> mu+ ^mu-", Type='T', isAlso = ['mu'])
        }
      ),

    "Phi_MuM" : TupleConfig (
      Decay = "phi(1020) -> ^mu+ ^mu-"
      , InputLines     = ["Hlt2PIDDetPhiMuMuPosTaggedTurboCalib"]
      , Calibration   = None
      , Filter        = filters.MuonUnBiased
      , Branches = {
          "phi" : Branch("^(phi(1020) -> mu+ mu-)", Type='H')
          , "tag"  : Branch("phi(1020) -> ^mu+ mu-", Type='T', isAlso = ['mu'])
          , "probe": Branch("phi(1020) -> mu+ ^mu-", Type='T', isAlso = ['mu'])
        }
      ),


    "LbLcPi_P" : TupleConfig (
      Decay = "[Lambda_b0 -> ^(Lambda_c+ -> ^p+ ^K- ^pi+) ^pi-]CC"
      , InputLines    = ["Hlt2PIDLb2LcPiTurboCalib"]
      , Calibration   = None
      , Filter        = filters.PositiveID
      , Branches = {
          "Lb"    : Branch("^([Lambda_b0 ->  (Lambda_c+ ->  p+  K-  pi+)  pi-]CC)", Type='H')
          , "Lc"    : Branch("[Lambda_b0 -> ^(Lambda_c+ ->  p+  K-  pi+)  pi-]CC", Type='I')
          , "K"     : Branch("[Lambda_b0 ->  (Lambda_c+ ->  p+ ^K-  pi+)  pi-]CC", Type='T')
          , "pi"    : Branch("[Lambda_b0 ->  (Lambda_c+ ->  p+  K- ^pi+)  pi-]CC", Type='T')
          , "probe" : Branch("[Lambda_b0 ->  (Lambda_c+ -> ^p+  K-  pi+)  pi-]CC", Type='T', isAlso = ['p'])
          , "mu"    : Branch("[Lambda_b0 ->  (Lambda_c+ ->  p+  K-  pi+) ^pi-]CC", Type='T')
        }
      ),


    "LbLcPi_Pbar" : TupleConfig (
      Decay = "[Lambda_b0 -> ^(Lambda_c+ -> ^p+ ^K- ^pi+) ^pi-]CC"
      , InputLines    = ["Hlt2PIDLb2LcPiTurboCalib"]
      , Calibration   = None
      , Filter        = filters.NegativeID
      , Branches = {
          "Lb"      : Branch("^([Lambda_b0 ->  (Lambda_c+ ->  p+  K-  pi+)  pi-]CC)", Type='H')
          , "Lc"    : Branch("[Lambda_b0 -> ^(Lambda_c+ ->  p+  K-  pi+)    pi-]CC", Type='I')
          , "K"     : Branch("[Lambda_b0 ->  (Lambda_c+ ->  p+ ^K-  pi+)    pi-]CC", Type='T')
          , "pi"    : Branch("[Lambda_b0 ->  (Lambda_c+ ->  p+  K- ^pi+)    pi-]CC", Type='T')
          , "probe" : Branch("[Lambda_b0 ->  (Lambda_c+ -> ^p+  K-  pi+)    pi-]CC", Type='T', isAlso = ['p'])
          , "mu"    : Branch("[Lambda_b0 ->  (Lambda_c+ ->  p+  K-  pi+)   ^pi-]CC", Type='T')
        }
      ),


    "Phi_KP" : TupleConfig (
      Decay = "phi(1020) -> ^K+ ^K-"
      , InputLines     = ["Hlt2PIDDetPhiKKNegTaggedTurboCalib"]
      , Calibration   = "PhiCalib_Pos"
      , Filter        = None
      , Branches = {
          "phi"  : Branch("^(phi(1020) ->  K+  K-)", Type='H')
          , "probe": Branch("phi(1020) -> ^K+  K-", Type='T', isAlso = ['K'])
          , "tag"  : Branch("phi(1020) ->  K+ ^K-", Type='T', isAlso = ['K'])
        }
      ),


    "Phi_KM" : TupleConfig (
      Decay = "phi(1020) -> ^K+ ^K-"
      , InputLines     = ["Hlt2PIDDetPhiKKPosTaggedTurboCalib"]
      , Calibration   = "PhiCalib_Neg"
      , Filter        = None
      , Branches = {
          "phi"  : Branch("^(phi(1020) ->  K+  K-)", Type='H')
          , "tag"  : Branch("phi(1020) -> ^K+  K-", Type='T', isAlso = ['K'])
          , "probe": Branch("phi(1020) ->  K+ ^K-", Type='T', isAlso = ['K'])
        }
      ),


    "Phi_KP_notag" : TupleConfig (
      Decay = "phi(1020) -> ^K+ ^K-"
      , InputLines     = ["Hlt2PIDDetPhiKKUnbiasedTurboCalib"]
      , Calibration   = None
      , Filter        = None
      , Branches = {
          "phi"  : Branch("^(phi(1020) ->  K+  K-)", Type='H')
          , "probe": Branch("phi(1020) -> ^K+  K-", Type='T', isAlso = ['K'])
          , "tag"  : Branch("phi(1020) ->  K+ ^K-", Type='T', isAlso = ['K'])
        }
      ),


    "Phi_KM_notag" : TupleConfig (
      Decay = "phi(1020) -> ^K+ ^K-"
      , InputLines     = ["Hlt2PIDDetPhiKKUnbiasedTurboCalib"]
      , Calibration   = None
      , Filter        = None
      , Branches = {
          "phi"  : Branch("^(phi(1020) ->  K+  K-)", Type='H')
          , "tag"  : Branch("phi(1020) -> ^K+  K-", Type='T', isAlso = ['K'])
          , "probe": Branch("phi(1020) ->  K+ ^K-", Type='T', isAlso = ['K'])
        }
      ),



}


################################################################################
################################################################################
####                                                                        ####
####                                                                        ####
####              S T O P   H E R E                                         ####
####                                                                        ####
####  99% of use cases won't require you to modify what is below            ####
####                                                                        ####
################################################################################
################################################################################


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

  dstWriter = SelDSTWriter( "DSTWriter",
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
def parseConfiguration_Run2(tupleConfig,  # TupleConfig object describing sample
                            tesFormat,    # Input TES with "<line>" placeholder
                            sTableFile,   # Input file for the sTables
                            mdstOutputFile,  # MicroDST output extension
                            mdstOutputPrefix # MicroDST prefix for production
                           ):
  cfg = tupleConfig
  reviveSequences = [] # mark sequences to unpack std particles
  swSequences     = [] # mark sequences to apply sWeights
  filterSequences = [] # mark sequences to be written in tuples
  matchSequences  = [] # mark sequences to be written in tuples
  tupleSequences  = [] # mark tuple sequences
  dstSequences    = [] # sequences writing (Micro)DST files

  for basicPart in ["Muons", "Pions", "Kaons", "Protons", "Electrons"]:
    location = "Phys/StdAllNoPIDs{s}/Particles".format ( s = basicPart )
    reviveSequences += [SelectionSequence("fs_std" + basicPart , 
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
           sTableFile = sTableFile, 
           sTableDir  = cfg[sample].Calibration,
           sTableName = "sTableSignal", 
          )
         ]


################################################################################
## Creates filter sequences to fill nTuples                                   ##
################################################################################

    selectionName = sample
    _cut = "DECTREE ('{}')".format ( cfg[sample].Decay.replace("^","") )

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
        Algorithm = CopyAndMatchCombination ( "MatchAlg" + selectionName ),
        RequiredSelections = [selection]
        )

    matchingSeq = SelectionSequence ( "SeqMatch"+ selectionName,
          TopSelection = matchingSel )

    matchSequences += [ matchingSeq ]



################################################################################
## Parses the configuration dictionaries and configure the tuples             ##
################################################################################
    tuple = DecayTreeTuple(sample + "Tuple")
    tuple.Inputs = [filterSequence.outputLocation()]
    tuple.Decay  = cfg[sample].Decay
    tuple.ToolList = [ "TupleToolEventInfo" ]
    eventTool = tuple.addTupleTool("LoKi::Hybrid::EvtTupleTool/LoKiEvent")
    eventTool.VOID_Variables = EventInfo
    eventTool.Preambulo = [
      "from LoKiTracks.decorators import *",
      "from LoKiCore.functions import *"
    ]
    tuple.addTool( eventTool )

    matchingLocation = {
      "mu+"        :  "Phys/StdAllNoPIDsMuons/Particles",
      "pi+"        :  "Phys/StdAllNoPIDsPions/Particles",
      "K+"         :  "Phys/StdAllNoPIDsKaons/Particles",
      "p+"         :  "Phys/StdAllNoPIDsProtons/Particles",
      "e+"         :  "Phys/StdAllNoPIDsElectrons/Particles",
    }

    tupleSequences += [tuple]

    for branchName in cfg[sample].Branches:
      b = tuple.addBranches({branchName : cfg[sample].Branches[branchName].Particle})
      b = b[branchName]
      matcher = b.addTupleTool ( "TupleToolTwoParticleMatching/Matcher_" + branchName )
      matcher.ToolList = []
      matcher.Prefix = ""; matcher.Suffix = "_Brunel"
      matcher.MatchLocations = matchingLocation

      lokitool = b.addTupleTool("LoKi::Hybrid::TupleTool/LoKi_"+branchName)
      vardict = copy(LokiVarsByType[ cfg[sample].Branches[branchName].Type ])
      pidcalibtool = b.addTupleTool ( "TupleToolPIDCalib/PIDCalibTool_"+branchName )
      pidcalibtool_matched = TTpid( "PIDCalibTool_match_"+branchName )
      for partName in [branchName] + cfg[sample].Branches[branchName].isAlso:
        if partName in LokiVarsByName:
          vardict.update ( LokiVarsByName[partName] )
#        if partName == 'e':
#          pidcalibtool.FillBremInfo = True
#          pidcalibtool_matched.FillBremInfo = True

      lokimatchedtool = LokiTool("LoKi_match_"+branchName)
       
      matcher.addTool ( pidcalibtool_matched )
      matcher.ToolList += ["LoKi::Hybrid::TupleTool/LoKi_match_"+branchName ,
                           "TupleToolPIDCalib/PIDCalibTool_match_" + branchName ]
      
      vardict.update (cfg[sample].Branches[branchName].LokiVariables)
      lokimatchedtool.Variables = vardict
      lokitool.Variables        = vardict

      matcher.addTool ( lokimatchedtool )


  print "Input TES: " 
  print "\n".join ( [f.outputLocation() for f in filterSequences] )
  if mdstOutputFile:
    dstSequences += configureMicroDSTwriter ( mdstOutputFile, 
                                              mdstOutputPrefix, 
                                              filterSequences + matchSequences)
      

  return (reviveSequences 
          + swSequences 
          + filterSequences 
          + matchSequences
          + tupleSequences 
          + dstSequences
      )


                    


## Entry point for ganga configuration
def configurePIDCalibTupleProduction(
      DataType
      , TupleFile
      , Simulation 
      , Lumi
      , Stream
      , InputType = 'DST'
      , EvtMax    = -1
      , tesFormat = "/Event/<stream>/<line>/Particles"
      , sTableFile = None
      , protoRecalibrationSequences = None
      , mdstOutputFile   = None
      , mdstOutputPrefix = None
   ):
#
  from Configurables import MessageSvc
  MessageSvc().Format = "% F%60W%S%7W%R%T %0W%M"

  if protoRecalibrationSequences == None: 
    protoRecalibrationSequences = []

#  MessageSvc().OutputLevel = DEBUG
#
  dv = DaVinci()
  dv.DataType   = DataType
  dv.InputType  = InputType
  dv.EvtMax = EvtMax
  dv.TupleFile = TupleFile
#   
  if InputType == 'MDST':
    rootInTes = "/Event/"+Stream
#    uDstConf ( rootInTes )


  dv.Simulation = Simulation
  dv.Lumi       = Lumi

  tesFormat = tesFormat.replace('<stream>', Stream)
  

#  BrnlProbNN = ProbNNcalib ("Brnl", "/Event/Rec/ProtoP/Charged")

  configuredAlgorithms = parseConfiguration_Run2(tupleConfiguration, 
                                                 tesFormat, sTableFile,
                                                 mdstOutputFile, mdstOutputPrefix) 

  dv.appendToMainSequence ( 
#    [BrnlProbNN.sequence()]  +
    protoRecalibrationSequences 
    + configuredAlgorithms )


#  if InputType == 'MDST':
#    for alg in  dv.UserAlgorithms:
#      alg.RootInTES = rootInTes

#below for local test

#TupleFile = 'PID_modesL.root'
#DataType = '2012'
#InputType = 'MDST'
#Simulation = False
#Lumi = True
#EvtMax = -1
#Stream = 'PID'
#tesFormat = "/Event/<stream>/Phys/<line>/Particles"
#dv = DaVinci()
#dv.DataType   = DataType
#dv.InputType  = InputType
#dv.EvtMax = EvtMax
#dv.TupleFile = TupleFile

#if InputType == 'MDST':
#    rootInTes = "/Event/Strip"
##    uDstConf ( rootInTes )


#dv.Simulation = Simulation
#dv.Lumi       = Lumi

#tesFormat = tesFormat.replace('<stream>', Stream)
#dv.UserAlgorithms = parseConfiguration(tupleConfiguration, tesFormat)


