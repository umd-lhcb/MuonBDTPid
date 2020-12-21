from Gaudi.Configuration import *
from Configurables import DaVinci
from PidCalibProduction.Run2 import parseConfiguration
from PidCalibProduction.Run2 import Branch
from PidCalibProduction.Run2 import TupleConfig

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
    "HEAD": {
        "ENDVERTEX_CHI2": "VFASPF(VCHI2)",
        "ENDVERTEX_NDOF": "VFASPF(VDOF)",
        "IPCHI2": "BPVIPCHI2()",
        "IP": "BPVIP()",
        "BPVLTCHI2": "BPVLTCHI2()",
        "BPVDLS": "BPVDLS",
        "BPVDIRA": "BPVDIRA",
        "M": "M",
        "M_DTF": "DTF_FUN(M,False)",
        "M_DTF_PV": "DTF_FUN(M,True)",
        "M_DTF_Jpsi": "DTF_FUN(M,True,'J/psi(1S)')",
    },
    "INTERMEDIATE": {
        "ENDVERTEX_CHI2": "VFASPF(VCHI2)",
        "ENDVERTEX_NDOF": "VFASPF(VDOF)",
        "IPCHI2": "BPVIPCHI2()",
        "IP": "BPVIP()",
        "BPVDLS": "BPVDLS",
        "BPVLTCHI2": "BPVLTCHI2()",
        "BPVDIRA": "BPVDIRA",
        "M": "M",
        "M_DTF": "DTF_FUN(M,False)",
        "M_DTF_PV": "DTF_FUN(M,True)",
    },
    "TRACK": {
        "PT": "PT",  ## These variables are also saved from the PIDCalib
        "P": "P",  ## tuple tool, so they are a waste of disk space
        "ETA": "ETA",  ## however the correct thing would be to keep them
        "PHI": "PHI",  ## however the correct thing would be to keep them
        "PIDK": "PIDK",  ## here and removing them from PIDCalib.
        "PIDmu": "PIDmu",  ##  ... to be done ...
        "PIDp": "PIDp",  ##
        "PIDe": "PIDe",
        "PIDd": "PPFUN ( PP_INFO ( LHCb.ProtoParticle.CombDLLd , -9999 ) )",
        "sWeight": "WEIGHT",
        "IPCHI2": "BPVIPCHI2()",
        "RichDLLd": "PPFUN ( PP_INFO ( LHCb.ProtoParticle.RichDLLd , -9999 ) )",
        "RichDLLe": "PPFUN ( PP_RichDLLe )",
        "RichDLLpi": "PPFUN ( PP_RichDLLpi )",
        "RichDLLmu": "PPFUN ( PP_RichDLLmu )",
        "RichDLLk": "PPFUN ( PP_RichDLLk )",
        "RichDLLp": "PPFUN ( PP_RichDLLp )",
        "RichDLLbt": "PPFUN ( PP_RichDLLbt )",
        "MuonMuLL": "PPFUN ( PP_MuonMuLL )",
        "MuonBgLL": "PPFUN ( PP_MuonBkgLL )",
        "Charge": "switch ( Q > 0, +1, -1 )",
        "MuonUnbiased": "switch ("
        "(TIS('L0.*Decision', 'L0TriggerTisTos')) & "
        "(TIS('Hlt1(?!ODIN)(?!L0)(?!Lumi)(?!Tell1)(?!MB)(?!NZS)(?!Velo)(?!BeamGas)(?!Incident).*Decision', 'Hlt1TriggerTisTos')) &"
        "(ALL) , "
        "1,0)",
        "ElectronUnbiased": "switch ( "
        "(TIS('L0ElectronDecision', 'L0TriggerTisTos')) & "
        "(TIS('Hlt1(?!ODIN)(?!L0)(?!Lumi)(?!Tell1)(?!MB)(?!NZS)(?!Velo)(?!BeamGas)(?!Incident).*Decision', 'Hlt1TriggerTisTos')) &"
        "(ALL) , "
        "1,0)",
        "TRCHI2NDOF": "TRCHI2DOF",
        "TRACK_GHOSTPROB": "TRGHP",
    },
    "NEUTRAL": {},
}


EventInfo = {
    "VOID": {
        "nPVs_Brunel": "RECSUMMARY( LHCb.RecSummary.nPVs              , -9999)",
        "nPVs": "RECSUMMARY( LHCb.RecSummary.nPVs              , -9999, '/Event/Turbo/Rec/Summary')",
        "nLongTracks_Brunel": "RECSUMMARY( LHCb.RecSummary.nLongTracks       , -9999)",
        "nLongTracks": "RECSUMMARY( LHCb.RecSummary.nLongTracks       , -9999, '/Event/Turbo/Rec/Summary')",
        "nDownstreamTracks_Brunel": "RECSUMMARY( LHCb.RecSummary.nDownstreamTracks , -9999)",
        "nDownstreamTracks": "RECSUMMARY( LHCb.RecSummary.nDownstreamTracks , -9999, '/Event/Turbo/Rec/Summary')",
        "nVeloTracks_Brunel": "RECSUMMARY( LHCb.RecSummary.nVeloTracks       , -9999)",
        "nVeloTracks": "RECSUMMARY( LHCb.RecSummary.nVeloTracks       , -9999, '/Event/Turbo/Rec/Summary')",
        "nTracks_Brunel": "RECSUMMARY( LHCb.RecSummary.nTracks           , -9999)",
        "nTracks": "RECSUMMARY( LHCb.RecSummary.nTracks           , -9999, '/Event/Turbo/Rec/Summary')",
        "nRich1Hits_Brunel": "RECSUMMARY( LHCb.RecSummary.nRich1Hits        , -9999)",
        "nRich1Hits": "RECSUMMARY( LHCb.RecSummary.nRich1Hits        , -9999, '/Event/Turbo/Rec/Summary')",
        "nRich2Hits_Brunel": "RECSUMMARY( LHCb.RecSummary.nRich2Hits        , -9999)",
        "nRich2Hits": "RECSUMMARY( LHCb.RecSummary.nRich2Hits        , -9999, '/Event/Turbo/Rec/Summary')",
        "nVeloClusters_Brunel": "RECSUMMARY( LHCb.RecSummary.nVeloClusters     , -9999)",
        "nVeloClusters": "RECSUMMARY( LHCb.RecSummary.nVeloClusters     , -9999, '/Event/Turbo/Rec/Summary')",
        "nSPDhits_Brunel": "RECSUMMARY( LHCb.RecSummary.nSPDhits          , -9999)",
        "nSPDhits": "RECSUMMARY( LHCb.RecSummary.nSPDhits          , -9999, '/Event/Turbo/Rec/Summary')",
        "nMuonTracks_Brunel": "RECSUMMARY( LHCb.RecSummary.nMuonTracks       , -9999)",
        "nMuonTracks": "RECSUMMARY( LHCb.RecSummary.nMuonTracks       , -9999, '/Event/Turbo/Rec/Summary')",
    },
    "ODIN": {
        "runNumber": "ODIN_RUN",
        "eventNumber1": "ODIN_EVT1 ( 1000000000L )",
        "eventNumber2": "ODIN_EVT2 ( 1000000000L )",
        "eventNumber": " ODIN_EVT1 ( 1000000000L ) + 1000000000L * ODIN_EVT2 ( 1000000000L )",
        "TCK": "ODIN_TCK",
    },
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
    "Lc": {
        "WM_PiKPi": "WM('pi+', 'K-', 'pi+')",  # D->Kpipi,
        "WM_KPiPi": "WM('K-', 'pi+', 'pi+')",  # D->Kpipi
        "WM_KKPi": "WM('K-', 'K+', 'pi+')",  # D->KKpi
    },
    "Dz": {
        "WM_PiPi": "WM('pi+','pi-')",
        "WM_KK": "WM('K+','K-')",
        "WM_DCS": "WM('pi+','K-')",
    },
    "K": {},
    "mu": {
        "MuonTOS": "switch((TOS('L0MuonDecision', 'L0TriggerTisTos')) & "
        "(TOS('Hlt1(TrackAllL0|TrackMuon|SingleMuonHighPT)Decision', 'Hlt1TriggerTisTos')), "
        "1,0)",
        "MuonProbe": "switch((P>3000) & (PT>800) & (BPVIPCHI2()>10) & (TRCHI2DOF<3), 1,0)",
        "MuonTag": "switch((P>6000) & (PT>1500) & (BPVIPCHI2()>25) & (TRCHI2DOF<3) & (ISMUON), 1,0)",
    },
    "phi": {
        "WM_PiPi": "WM('pi+', 'pi-')",  # for completeness
        "WM_PiK": "WM('pi+', 'K-')",  # D+ decay to K- pi+ pi+ with one of the pi+ -> K-
        "WM_KPi": "WM('K+',  'pi-')",  # DCS D decay, for completeness
        "WM_PK": "WM('p+',  'K-')",  # Lc -> p K pi with p -> K
        "WM_KP": "WM('K+',  'p~-')",  # for completeness
    },
    "Ds": {
        "WM_PiPiPi": "WM('pi+', 'pi-', 'pi+')",
        "WM_PiPiK": "WM('pi+', 'pi-', 'K+')",
        "WM_PiPiP": "WM('pi+', 'pi-', 'p+')",
        "WM_PiKPi": "WM('pi+', 'K-', 'pi+')",
        "WM_PiKK": "WM('pi+', 'K-', 'K+')",
        "WM_PiKP": "WM('pi+', 'K-', 'p+')",
        "WM_PiKPi": "WM('pi+', 'p~-', 'pi+')",
        "WM_PiKK": "WM('pi+', 'p~-', 'K+')",
        "WM_PiKP": "WM('pi+', 'p~-', 'p+')",
        "WM_KPiPi": "WM('K+', 'pi-', 'pi+')",
        "WM_KPiK": "WM('K+', 'pi-', 'K+')",
        "WM_KPiP": "WM('K+', 'pi-', 'p+')",
        "WM_KKPi": "WM('K+', 'K-', 'pi+')",
        "WM_KKK": "WM('K+', 'K-', 'K+')",
        "WM_KKP": "WM('K+', 'K-', 'p+')",
        "WM_KPPi": "WM('K+', 'p~-', 'pi+')",
        "WM_KPK": "WM('K+', 'p~-', 'K+')",
        "WM_KPP": "WM('K+', 'p~-', 'p+')",
        "WM_PPiPi": "WM('p+', 'pi-', 'pi+')",
        "WM_PPiK": "WM('p+', 'pi-', 'K+')",
        "WM_PPiP": "WM('p+', 'pi-', 'p+')",
        "WM_PKPi": "WM('p+', 'K-', 'pi+')",
        "WM_PKK": "WM('p+', 'K-', 'K+')",
        "WM_PKP": "WM('p+', 'K-', 'p+')",
        "WM_PPPi": "WM('p+', 'p~-', 'pi+')",
        "WM_PPK": "WM('p+', 'p~-', 'K+')",
        "WM_PPP": "WM('p+', 'p~-', 'p+')",
    },
    "e": {
        #    "ElectronTOS" : "switch ( "\
        #                        "(TOS('L0ElectronDecision', 'L0TriggerTisTos')) & "\
        #                        "(TOS('Hlt1PhysDecision', 'TriggerTisTos')) &"\
        #                        "(TOS('Hlt2PhysDecision', 'TriggerTisTos')) , " \
        #                        "1,0)"
        #    "ElectronProbe" :   "switch((P>3000) & (PT>500) & (BPVIPCHI2()>9) , 1,0)"
        #    ,"ElectronTag" :     "switch((P>6000) & (PT>1500) & (BPVIPCHI2()>9) & (PIDe>5), 1,0)"
    },
}


##################################################
###      C O N F I G U R A T I O N   3     #######
###. . . . . . . . . . . . . . . . . . . . #######
###        Filter definition               #######
##################################################
### Filters used to define the various nTuples
##################################################


from Configurables import TupleToolPIDCalib as TTpid

_l0TisTagCrit = TTpid.getDefaultProperty("MuonTisL0Criterion")
_hlt1TisTagCrit = TTpid.getDefaultProperty("MuonTisHlt1Criterion")
_hlt2TisTagCrit = TTpid.getDefaultProperty("MuonTisHlt2Criterion")

_l0TosTagCrit = TTpid.getDefaultProperty("MuonTosL0Criterion")
_hlt1TosTagCrit = TTpid.getDefaultProperty("MuonTosHlt1Criterion")
_hlt2TosTagCrit = TTpid.getDefaultProperty("MuonTosHlt2Criterion")

### Service functions
def L0TIS(code):
    return "TIS('{0}', 'L0TriggerTisTos')".format(code)


def L0TOS(code):
    return "TOS('{0}', 'L0TriggerTisTos')".format(code)


def Hlt1TIS(code):
    return "TIS('{0}', 'Hlt1TriggerTisTos')".format(code)


def Hlt1TOS(code):
    return "TOS('{0}', 'Hlt1TriggerTisTos')".format(code)


class FilterCut:
    def __init__(self, cut):
        self.cut = "(" + cut + ")"

    def __add__(self, cut):
        ret = FilterCut(self.cut)
        if isinstance(cut, str):
            ret.cut += "& ( " + cut + ")"
        else:
            ret.cut += "& ( " + cut.cut + ")"
        return ret

    def printout(self):
        print "self.cut = %s" % self.cut


class filters:
    LoP = FilterCut("NINTREE( ('p+'==ABSID) & (P<40000) )==1")
    HiP = FilterCut("NINTREE( ('p+'==ABSID) & (P>40000) )==1")

    LoP.printout()

    PositiveID = FilterCut("ID > 0")
    NegativeID = FilterCut("ID < 0")

    # Require at least one 'MuonUnBiased' daughter
    MuonUnBiased = FilterCut(
        "NINTREE( (ISBASIC) & ({l0}) "
        "& ({hlt1}) )>0".format(l0=L0TIS(_l0TisTagCrit), hlt1=Hlt1TIS(_hlt1TisTagCrit))
    )
    # MuonUnBiased.printout()
    # Require at least one 'MuonUnBiased' granddaughter
    MuonUnBiased_2 = FilterCut(
        ("NINGENERATION( (ISBASIC) & ({l0}) & " "({hlt1}), 2 )>0").format(
            l0=L0TIS(_l0TisTagCrit), hlt1=Hlt1TIS(_hlt1TisTagCrit)
        )
    )

    # Require at least one 'Muon TOS-tagged' daughter
    MuonTosTagged = FilterCut(
        ("NINTREE( (ISBASIC) & ({l0}) & " "({hlt1}) )>0").format(
            l0=L0TOS(_l0TosTagCrit), hlt1=Hlt1TOS(_hlt1TosTagCrit)
        )
    )

    # Require at least one 'Muon TOS-tagged' granddaughter
    MuonTosTagged = FilterCut(
        ("NINGENERATION( (ISBASIC) & ({l0}) " "& ({hlt1}) , 2 )>0").format(
            l0=L0TOS(_l0TosTagCrit), hlt1=Hlt1TOS(_hlt1TosTagCrit)
        )
    )

    # Require Lambda_b decay is unbiased with respect to proton PID
    Lb2LcMuNu = FilterCut(
        ("( ({l0Tos}) | ({l0Tis}) ) & " "({hlt1Tos}) ").format(
            l0Tos=L0TOS("L0(Muon|Hadron)Decision"),
            l0Tis=L0TIS("L0.*Decision"),
            hlt1Tos=Hlt1TOS("Hlt1(TrackAllL0|TrackMuon|SingleMuonHighPT)Decision"),
        )
    )

    IncLc2PKPi = FilterCut(
        "(BPVIPCHI2()<4) & (VFASPF(VCHI2/VDOF)<5) & (BPVLTCHI2()>9) & (ADWM('D_s+',WM('K-','K+','pi+'))>25.*MeV) & (ADWM('D+',WM('K-','K+','pi+'))>25.*MeV) &(ADWM('D*(2010)+',WM('K-','pi+','pi+'))>20.*MeV) & ((WM('K-','pi+','pi+')>1.905*GeV) | (WM('K-','pi+','pi+')<1.80*GeV))  & (INTREE((ABSID=='p+') &(PT>100*MeV) &(TRGHOSTPROB<0.35) &(BPVIPCHI2()>9.)))  & (INTREE((ABSID=='K+') &(PT>400*MeV) &(TRGHOSTPROB<0.35) &(BPVIPCHI2()>9.) &(PROBNNk>0.3))) &(INTREE((ABSID=='pi+')&(PT>400*MeV) &(TRGHOSTPROB<0.35) &(BPVIPCHI2()>9.) &(PROBNNpi>0.2)))"
    )

    Jpsiee = FilterCut(
        "(BPVIPCHI2()<9.0) & (VFASPF(VCHI2/VDOF)<9) & (NINTREE(('e-'==ABSID)&(BPVIPCHI2()>25) )==2)"
    )

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

# class Decay(object):
#  def __init__(self, other=None):
#    if other != None:
#      self.__dict__ = other.__dict__.copy()
#
# Jpsi_MuM_decay_dict = {
#    "tuple_name"             : "My_Jpsi_MuM",
#    "decay_descriptor"       : "J/psi(1S) -> ^mu+ ^mu-",
#    "inputs"                 : filters.MuonUnBiased,
#    "descriptor_Jpsi"        : "^(J/psi(1S) -> mu+ mu-)",
#    "descriptor_tag"         : "J/psi(1S) -> ^mu+ mu-",
#    "descriptor_probe"       : "J/psi(1S) -> mu+ ^mu-",
#    }
#
# Jpsi_MuM_decay = Decay()
# Jpsi_MuM_decay.__dict__ = Jpsi_MuM_decay_dict
#
# from Configurables import TupleToolTrackPosition
# from Configurables import TupleToolPrimaries
# from Configurables import TupleToolTrackInfo
# from Configurables import TupleToolPid
# from Configurables import TupleToolANNPIDTraining
# from Gaudi.Configuration import *
# from DecayTreeTuple.Configuration import *
#
# tuple_tools = ["TupleToolTrackPosition",
#               "TupleToolPrimaries",
#               "TupleToolTrackInfo"
# ]
#
# loki_variables = {"LOKI_ENERGY"     : "E",
#                  "LOKI_ETA"        : "ETA",
#                  "LOKI_PHI"        : "PHI"}
#
# def CreateTupleTool(decay):
#  print "-----------------------------------------------------------------------"
#  print "Adding decay " + decay.decay_descriptor
#  print "Location:", decay.inputs
#  print "Tuple name:", decay.tuple_name
#  tuple = DecayTreeTuple(decay.tuple_name)
#  tuple.Inputs =  [decay.inputs]
#  tuple.Decay = decay.decay_descriptor
#
#  tuple.ToolList = tuple_tools[:]
#
#  tt_kinematic = tuple.addTupleTool("TupleToolKinematic")
#  tt_kinematic.Verbose = True
#
#  tt_loki_general = tuple.addTupleTool("LoKi::Hybrid::TupleTool/tt_loki_general")
#  tt_loki_general.Variables = loki_variables
#
#  tt_recostats = tuple.addTupleTool("TupleToolRecoStats")
#  tt_recostats.Verbose = True
#
#  tt_geometry = tuple.addTupleTool("TupleToolGeometry")
#  tt_geometry.Verbose = True
#  tt_geometry.RefitPVs = False
#  tt_geometry.FillMultiPV = True
#
#  tt_PID = tuple.addTupleTool("TupleToolPid")
#  tt_PID.Verbose = True
#
#  branches = {}
#  name_jpsibranch = "Jpsi"
#  name_tagbranch = "tag"
#  name_probebranch = "probe"
#  branches[name_jpsibranch] = decay.descriptor_Jpsi
#  branches[name_tagbranch] = decay.descriptor_tag
#  branches[name_probebranch] = decay.descriptor_probe
#  print "Decay branches:", branches
#  tuple.addBranches(branches)
#  tuple.probe.addTool(TupleToolANNPIDTraining, name="TupleToolANNPIDTraining")
#  tuple.probe.ToolList+=["TupleToolANNPIDTraining/TupleToolANNPIDTraining"]
#
#  return tuple

tupleConfiguration = {
    # ============ Kaons - Pions ===============================#
    "DSt_PiP": TupleConfig(
        Decay="[D*(2010)+ -> ^(D0 -> K- ^pi+) pi+]CC",
        InputLines="Hlt2PIDD02KPiTagTurboCalib",
        Filter=filters.PositiveID,
        Calibration="RSDStCalib_Pos",
        Branches={
            "Dst": Branch("^([D*(2010)+ -> (D0 -> K- pi+) pi+]CC)", Type="H"),
            "Dz": Branch("[D*(2010)+ -> ^(D0 -> K- pi+) pi+]CC", Type="I"),
            "K": Branch("[D*(2010)+ -> (D0 -> ^K- pi+) pi+]CC", Type="T"),
            "probe": Branch(
                "[D*(2010)+ -> (D0 -> K- ^pi+) pi+]CC", Type="T", isAlso=["pi"]
            ),
            "pis": Branch(
                "[D*(2010)+ -> (D0 -> K- pi+) ^pi+]CC", Type="T", isAlso=["pi"]
            ),
        },
    ),
    "DSt_PiM": TupleConfig(
        Decay="[D*(2010)+ -> ^(D0 -> K- ^pi+) pi+]CC",
        InputLines="Hlt2PIDD02KPiTagTurboCalib",
        Filter=filters.NegativeID,
        Calibration="RSDStCalib_Neg",
        Branches={
            "Dst": Branch("^([D*(2010)+ -> (D0 -> K- pi+) pi+]CC)", Type="H"),
            "Dz": Branch("[D*(2010)+ -> ^(D0 -> K- pi+) pi+]CC", Type="I"),
            "K": Branch("[D*(2010)+ -> (D0 -> ^K- pi+) pi+]CC", Type="T"),
            "probe": Branch(
                "[D*(2010)+ -> (D0 -> K- ^pi+) pi+]CC", Type="T", isAlso=["pi"]
            ),
            "pis": Branch(
                "[D*(2010)+ -> (D0 -> K- pi+) ^pi+]CC", Type="T", isAlso=["pi"]
            ),
        },
    ),
    "DSt_KP": TupleConfig(
        Decay="[D*(2010)+ -> ^(D0 -> ^K- pi+) pi+]CC",
        InputLines="Hlt2PIDD02KPiTagTurboCalib",
        Calibration="RSDStCalib_Neg",
        Filter=filters.NegativeID,  # WARNING! K has opposite sign to D*
        Branches={
            "Dst": Branch("^([D*(2010)+ -> (D0 -> K- pi+) pi+]CC)", Type="H"),
            "Dz": Branch("[D*(2010)+ -> ^(D0 -> K- pi+) pi+]CC", Type="I"),
            "probe": Branch(
                "[D*(2010)+ -> (D0 -> ^K- pi+) pi+]CC", Type="T", isAlso=["K"]
            ),
            "pi": Branch("[D*(2010)+ -> (D0 -> K- ^pi+) pi+]CC", Type="T"),
            "pis": Branch(
                "[D*(2010)+ -> (D0 -> K- pi+) ^pi+]CC", Type="T", isAlso=["pi"]
            ),
        },
    ),
    "DSt_KM": TupleConfig(
        Decay="[D*(2010)+ -> ^(D0 -> ^K- pi+) pi+]CC",
        InputLines="Hlt2PIDD02KPiTagTurboCalib",
        Calibration="RSDStCalib_Pos",
        Filter=filters.PositiveID,  # WARNING! K has opposite sign to D*
        Branches={
            "Dst": Branch("^([D*(2010)+ -> (D0 -> K- pi+) pi+]CC)", Type="H"),
            "Dz": Branch("[D*(2010)+ -> ^(D0 -> K- pi+) pi+]CC", Type="I"),
            "probe": Branch(
                "[D*(2010)+ -> (D0 -> ^K- pi+) pi+]CC", Type="T", isAlso=["K"]
            ),
            "pi": Branch("[D*(2010)+ -> (D0 -> K- ^pi+) pi+]CC", Type="T"),
            "pis": Branch(
                "[D*(2010)+ -> (D0 -> K- pi+) ^pi+]CC", Type="T", isAlso=["pi"]
            ),
        },
    ),
    "KSLL_PiP": TupleConfig(
        Decay="KS0 -> ^pi+ ^pi-",
        InputLines=["Hlt2PIDKs2PiPiLLTurboCalib"],
        Calibration="KS0LLCalib",
        Filter=None,
        Branches={
            "KS": Branch("^(KS0 -> pi+ pi-)", Type="H"),
            "tag": Branch("KS0 -> pi+ ^pi-", Type="T", isAlso=["pi"]),
            "probe": Branch("KS0 -> ^pi+ pi-", Type="T", isAlso=["pi"]),
        },
    ),
    "KSLL_PiM": TupleConfig(
        Decay="KS0 -> ^pi+ ^pi-",
        InputLines=["Hlt2PIDKs2PiPiLLTurboCalib"],
        Calibration="KS0LLCalib",
        Filter=None,
        Branches={
            "KS": Branch("^(KS0 -> pi+ pi-)", Type="H"),
            "tag": Branch("KS0 -> ^pi+ pi-", Type="T", isAlso=["pi"]),
            "probe": Branch("KS0 -> pi+ ^pi-", Type="T", isAlso=["pi"]),
        },
    ),
    "DsPhi_KP": TupleConfig(
        Decay="[D_s+]cc -> ^(phi(1020) -> ^K- ^K+) ^([pi+]cc)",
        InputLines=["Hlt2PIDDs2PiPhiKKNegTaggedTurboCalib"],
        Calibration="DsPhiKKCalib_Pos",
        Filter=None,
        Branches={
            "Ds": Branch("^([D_s+]cc -> (phi(1020) -> K- K+) [pi+]cc)", Type="H"),
            "phi": Branch("[D_s+]cc -> ^(phi(1020) -> K- K+) [pi+]cc", Type="I"),
            "probe": Branch(
                "[D_s+]cc ->  (phi(1020) ->  K- ^K+)  ([pi+]cc)", Type="T", isAlso=["K"]
            ),
            "tag": Branch(
                "[D_s+]cc ->  (phi(1020) -> ^K-  K+)  ([pi+]cc)", Type="T", isAlso=["K"]
            ),
            "pi": Branch("[D_s+]cc ->  (phi(1020) -> K-  K+)  ^([pi+]cc)", Type="T"),
        },
    ),
    "DsPhi_KM": TupleConfig(
        Decay="[D_s+]cc -> ^(phi(1020) -> ^K- ^K+) ^([pi+]cc)",
        InputLines=["Hlt2PIDDs2PiPhiKKPosTaggedTurboCalib"],
        Calibration="DsPhiKKCalib_Neg",
        Filter=None,
        Branches={
            "Ds": Branch("^([D_s+]cc -> (phi(1020) -> K- K+) [pi+]cc)", Type="H"),
            "phi": Branch("[D_s+]cc -> ^(phi(1020) -> K- K+) [pi+]cc", Type="I"),
            "probe": Branch(
                "[D_s+]cc ->  (phi(1020) -> ^K-  K+)  ([pi+]cc)", Type="T", isAlso=["K"]
            ),
            "tag": Branch(
                "[D_s+]cc ->  (phi(1020) ->  K- ^K+)  ([pi+]cc)", Type="T", isAlso=["K"]
            ),
            "pi": Branch("[D_s+]cc ->  (phi(1020) -> K-  K+)  ^([pi+]cc)", Type="T"),
        },
    ),
    # ============ Muons ===============================#
    "Jpsi_MuP": TupleConfig(
        Decay="J/psi(1S) -> ^mu+ ^mu-",
        InputLines=["Hlt2PIDDetJPsiMuMuNegTaggedTurboCalib"],
        Calibration="JpsiCalib_Pos",
        Filter=filters.MuonUnBiased,
        Branches={
            "Jpsi": Branch("^(J/psi(1S) -> mu+ mu-)", Type="H"),
            "probe": Branch("J/psi(1S) -> ^mu+ mu-", Type="T", isAlso=["mu"]),
            "tag": Branch("J/psi(1S) -> mu+ ^mu-", Type="T", isAlso=["mu"]),
        },
    ),
    "Jpsi_MuM": TupleConfig(
        Decay="J/psi(1S) -> ^mu+ ^mu-",
        InputLines=["Hlt2PIDDetJPsiMuMuPosTaggedTurboCalib"],
        Calibration="JpsiCalib_Neg",
        Filter=filters.MuonUnBiased,
        Branches={
            "Jpsi": Branch("^(J/psi(1S) -> mu+ mu-)", Type="H"),
            "tag": Branch("J/psi(1S) -> ^mu+ mu-", Type="T", isAlso=["mu"]),
            "probe": Branch("J/psi(1S) -> mu+ ^mu-", Type="T", isAlso=["mu"]),
        },
    ),
    "Jpsinopt_MuP": TupleConfig(
        Decay="J/psi(1S) -> ^mu+ ^mu-",
        InputLines=["Hlt2PIDDetJPsiMuMuNegTaggedTurboCalib"],
        Calibration="JpsinoptCalib_Pos",
        Filter=filters.MuonUnBiased,
        Branches={
            "Jpsi": Branch("^(J/psi(1S) -> mu+ mu-)", Type="H"),
            "probe": Branch("J/psi(1S) -> mu+ ^mu-", Type="T", isAlso=["mu"]),
            "tag": Branch("J/psi(1S) -> ^mu+ mu-", Type="T", isAlso=["mu"]),
        },
    ),
    "Jpsinopt_MuM": TupleConfig(
        Decay="J/psi(1S) -> ^mu+ ^mu-",
        InputLines=["Hlt2PIDDetJPsiMuMuPosTaggedTurboCalib"],
        Calibration="JpsinoptCalib_Neg",
        Filter=filters.MuonUnBiased,
        Branches={
            "Jpsi": Branch("^(J/psi(1S) -> mu+ mu-)", Type="H"),
            "tag": Branch("J/psi(1S) -> ^mu+ mu-", Type="T", isAlso=["mu"]),
            "probe": Branch("J/psi(1S) -> mu+ ^mu-", Type="T", isAlso=["mu"]),
        },
    ),
    "B_Jpsi_MuP": TupleConfig(
        Decay="[B+]cc -> ^(J/psi(1S) -> ^mu+ ^mu-) ^([K+]cc)",
        InputLines=["Hlt2PIDB2KJPsiMuMuNegTaggedTurboCalib"],
        Calibration="BJpsiMMCalib_Pos",
        Filter=None,
        Branches={
            "B": Branch("^([B+]cc ->  (J/psi(1S) ->  mu+  mu-) [ K+]cc)", Type="H"),
            "Jpsi": Branch("[B+]cc -> ^(J/psi(1S) ->  mu+  mu-) [ K+]cc", Type="I"),
            "probe": Branch(
                "[B+]cc ->  (J/psi(1S) -> ^mu+  mu-) [ K+]cc", Type="T", isAlso=["mu"]
            ),
            "tag": Branch(
                "[B+]cc ->  (J/psi(1S) ->  mu+ ^mu-) [ K+]cc", Type="T", isAlso=["mu"]
            ),
            "K": Branch("[B+]cc ->  (J/psi(1S) ->  mu+  mu-) ^([K+]cc)", Type="T"),
        },
    ),
    "B_Jpsi_MuM": TupleConfig(
        Decay="[B+]cc -> ^(J/psi(1S) -> ^mu+ ^mu-) ^([K+]cc)",
        InputLines=["Hlt2PIDB2KJPsiMuMuPosTaggedTurboCalib"],
        Calibration="BJpsiMMCalib_Neg",
        Filter=None,
        Branches={
            "B": Branch("^([B+]cc ->  (J/psi(1S) ->  mu+  mu-) [ K+]cc)", Type="H"),
            "Jpsi": Branch("[B+]cc -> ^(J/psi(1S) ->  mu+  mu-) [ K+]cc", Type="I"),
            "probe": Branch(
                "[B+]cc ->  (J/psi(1S) ->  mu+ ^mu-) [ K+]cc", Type="T", isAlso=["mu"]
            ),
            "tag": Branch(
                "[B+]cc ->  (J/psi(1S) -> ^mu+  mu-) [ K+]cc", Type="T", isAlso=["mu"]
            ),
            "K": Branch("[B+]cc ->  (J/psi(1S) ->  mu+  mu-) ^([K+]cc)", Type="T"),
        },
    ),
    #  "DsPhi_MuP" : TupleConfig (
    #     Decay = "[D_s+]cc -> ^(phi(1020) -> ^mu- ^mu+) ^([pi+]cc)"
    #     , InputLines    = ["Hlt2PIDDs2PiPhiMuMuNegTaggedTurboCalib"]
    #     , Calibration   = "DsPhiMMCalib_Pos"
    #     , Filter        = None
    #     , Branches = {
    #        "Ds" : Branch("^([D_s+]cc -> (phi(1020) -> mu- mu+) [pi+]cc)", Type='H')
    #        , "phi" : Branch("[D_s+]cc -> ^(phi(1020) -> mu- mu+) [pi+]cc", Type='I')
    #        , "probe" : Branch("[D_s+]cc ->  (phi(1020) ->  mu- ^mu+)  ([pi+]cc)", Type='T', isAlso = ['mu'])
    #        , "tag"   : Branch("[D_s+]cc ->  (phi(1020) -> ^mu-  mu+)  ([pi+]cc)", Type='T', isAlso = ['mu'])
    #        }
    #     ),
    #  "DsPhi_MuM" : TupleConfig (
    #    Decay = "[D_s+]cc -> ^(phi(1020) -> ^mu- ^mu+) ^([pi+]cc)"
    #    , InputLines    = ["Hlt2PIDDs2PiPhiMuMuPosTaggedTurboCalib"]
    #    , Calibration   = "DsPhiMMCalib_Neg"
    #    , Filter        = None
    #    , Branches = {
    #       "Ds" : Branch("^([D_s+]cc -> (phi(1020) -> mu- mu+) [pi+]cc)", Type='H')
    #       , "phi" : Branch("[D_s+]cc -> ^(phi(1020) -> mu- mu+) [pi+]cc", Type='I')
    #       , "probe" : Branch("[D_s+]cc ->  (phi(1020) -> ^mu-  mu+)  ([pi+]cc)", Type='T', isAlso = ['mu'])
    #       , "tag"   : Branch("[D_s+]cc ->  (phi(1020) ->  mu- ^mu+)  ([pi+]cc)", Type='T', isAlso = ['mu'])
    #       }
    #    ),
    # ============ Protons ===============================#
    "Lam0LL_P": TupleConfig(
        Decay="[Lambda0 -> ^p+ pi-]CC",
        InputLines=["Hlt2PIDLambda2PPiLLTurboCalib"],
        Calibration="Lam0LLCalib_Pos",
        Filter=filters.PositiveID,
        Branches={
            "L0": Branch("^([Lambda0 -> p+ pi-]CC)", Type="H"),
            "probe": Branch("[Lambda0 -> ^p+ pi-]CC", Type="T", isAlso=["p"]),
            "pi": Branch("[Lambda0 -> p+ ^pi-]CC", Type="T"),
        },
    ),
    "Lam0LL_Pbar": TupleConfig(
        Decay="[Lambda0 -> ^p+ pi-]CC",
        InputLines=["Hlt2PIDLambda2PPiLLTurboCalib"],
        Calibration="Lam0LLCalib_Neg",
        Filter=filters.NegativeID,
        Branches={
            "L0": Branch("^([Lambda0 -> p+ pi-]CC)", Type="H"),
            "probe": Branch("[Lambda0 -> ^p+ pi-]CC", Type="T", isAlso=["p"]),
            "pi": Branch("[Lambda0 -> p+ ^pi-]CC", Type="T"),
        },
    ),
    "Lam0LL_HPT_P": TupleConfig(
        Decay="[Lambda0 -> ^p+ pi-]CC",
        InputLines=["Hlt2PIDLambda2PPiLLhighPTTurboCalib"],
        Calibration="Lam0LLCalib_HPT_Pos",
        Filter=filters.PositiveID,
        Branches={
            "L0": Branch("^([Lambda0 -> p+ pi-]CC)", Type="H"),
            "probe": Branch("[Lambda0 -> ^p+ pi-]CC", Type="T", isAlso=["p"]),
            "pi": Branch("[Lambda0 -> p+ ^pi-]CC", Type="T"),
        },
    ),
    "Lam0LL_HPT_Pbar": TupleConfig(
        Decay="[Lambda0 -> ^p+ pi-]CC",
        InputLines=["Hlt2PIDLambda2PPiLLhighPTTurboCalib"],
        Calibration="Lam0LLCalib_HPT_Neg",
        Filter=filters.NegativeID,
        Branches={
            "L0": Branch("^([Lambda0 -> p+ pi-]CC)", Type="H"),
            "probe": Branch("[Lambda0 -> ^p+ pi-]CC", Type="T", isAlso=["p"]),
            "pi": Branch("[Lambda0 -> p+ ^pi-]CC", Type="T"),
        },
    ),
    "Lam0LL_VHPT_P": TupleConfig(
        Decay="[Lambda0 -> ^p+ pi-]CC",
        InputLines=["Hlt2PIDLambda2PPiLLveryhighPTTurboCalib"],
        Calibration="Lam0LLCalib_VHPT_Pos",
        Filter=filters.PositiveID,
        Branches={
            "L0": Branch("^([Lambda0 -> p+ pi-]CC)", Type="H"),
            "probe": Branch("[Lambda0 -> ^p+ pi-]CC", Type="T", isAlso=["p"]),
            "pi": Branch("[Lambda0 -> p+ ^pi-]CC", Type="T"),
        },
    ),
    "Lam0LL_VHPT_Pbar": TupleConfig(
        Decay="[Lambda0 -> ^p+ pi-]CC",
        InputLines=["Hlt2PIDLambda2PPiLLveryhighPTTurboCalib"],
        Calibration="Lam0LLCalib_VHPT_Neg",
        Filter=filters.NegativeID,
        Branches={
            "L0": Branch("^([Lambda0 -> p+ pi-]CC)", Type="H"),
            "probe": Branch("[Lambda0 -> ^p+ pi-]CC", Type="T", isAlso=["p"]),
            "pi": Branch("[Lambda0 -> p+ ^pi-]CC", Type="T"),
        },
    ),
    "Lam0LL_P_isMuon": TupleConfig(
        Decay="[Lambda0 -> ^p+ ^pi-]CC",
        InputLines=["Hlt2PIDLambda2PPiLLisMuonTurboCalib"],
        Calibration="Lam0LLisMuonCalib_Pos",
        Filter=filters.PositiveID,
        Branches={
            "L0": Branch("^([Lambda0 -> p+ pi-]CC)", Type="H"),
            "probe": Branch("[Lambda0 -> ^p+ pi-]CC", Type="T", isAlso=["p"]),
            "pi": Branch("[Lambda0 -> p+ ^pi-]CC", Type="T"),
        },
    ),
    "Lam0LL_Pbar_isMuon": TupleConfig(
        Decay="[Lambda0 -> ^p+ ^pi-]CC",
        InputLines=["Hlt2PIDLambda2PPiLLisMuonTurboCalib"],
        Calibration="Lam0LLisMuonCalib_Neg",
        Filter=filters.NegativeID,
        Branches={
            "L0": Branch("^([Lambda0 -> p+ pi-]CC)", Type="H"),
            "probe": Branch("[Lambda0 -> ^p+ pi-]CC", Type="T", isAlso=["p"]),
            "pi": Branch("[Lambda0 -> p+ ^pi-]CC", Type="T"),
        },
    ),
    "LbLcMu_P": TupleConfig(
        Decay="[Lambda_b0 -> ^(Lambda_c+ -> ^p+ ^K- ^pi+) ^mu-]CC",
        InputLines=["Hlt2PIDLb2LcMuNuTurboCalib"],
        Calibration="LbLcMuCalib_Pos",
        Filter=filters.PositiveID,
        Branches={
            "Lb": Branch(
                "^([Lambda_b0 ->  (Lambda_c+ ->  p+  K-  pi+)  mu-]CC)", Type="H"
            ),
            "Lc": Branch(
                "[Lambda_b0 -> ^(Lambda_c+ ->  p+  K-  pi+)  mu-]CC", Type="I"
            ),
            "K": Branch("[Lambda_b0 ->  (Lambda_c+ ->  p+ ^K-  pi+)  mu-]CC", Type="T"),
            "pi": Branch(
                "[Lambda_b0 ->  (Lambda_c+ ->  p+  K- ^pi+)  mu-]CC", Type="T"
            ),
            "probe": Branch(
                "[Lambda_b0 ->  (Lambda_c+ -> ^p+  K-  pi+)  mu-]CC",
                Type="T",
                isAlso=["p"],
            ),
            "mu": Branch(
                "[Lambda_b0 ->  (Lambda_c+ ->  p+  K-  pi+) ^mu-]CC", Type="T"
            ),
        },
    ),
    "LbLcMu_Pbar": TupleConfig(
        Decay="[Lambda_b0 -> ^(Lambda_c+ -> ^p+ ^K- ^pi+) ^mu-]CC",
        InputLines=["Hlt2PIDLb2LcMuNuTurboCalib"],
        Calibration="LbLcMuCalib_Neg",
        Filter=filters.NegativeID,
        Branches={
            "Lb": Branch(
                "^([Lambda_b0 ->  (Lambda_c+ ->  p+  K-  pi+)  mu-]CC)", Type="H"
            ),
            "Lc": Branch(
                "[Lambda_b0 -> ^(Lambda_c+ ->  p+  K-  pi+)  mu-]CC", Type="I"
            ),
            "K": Branch("[Lambda_b0 ->  (Lambda_c+ ->  p+ ^K-  pi+)  mu-]CC", Type="T"),
            "pi": Branch(
                "[Lambda_b0 ->  (Lambda_c+ ->  p+  K- ^pi+)  mu-]CC", Type="T"
            ),
            "probe": Branch(
                "[Lambda_b0 ->  (Lambda_c+ -> ^p+  K-  pi+)  mu-]CC",
                Type="T",
                isAlso=["p"],
            ),
            "mu": Branch(
                "[Lambda_b0 ->  (Lambda_c+ ->  p+  K-  pi+) ^mu-]CC", Type="T"
            ),
        },
    ),
    #  "LcMu_P" : TupleConfig (
    #    Decay = "[Lambda_c+ -> ^p+ ^K- ^pi+]CC"
    #    , InputLines    = ["Hlt2PIDLc2KPPiTurboCalib"]
    #    , Calibration   = "LcCalib_Pos"
    #    , Filter        = filters.PositiveID
    #    , Branches = {
    #       "Lc"    : Branch("^([Lambda_c+ ->  p+  K-  pi+]CC)", Type='H')
    #       , "K"     : Branch("[Lambda_c+ ->  p+ ^K-  pi+)]CC", Type='T')
    #       , "pi"    : Branch("[Lambda_c+ ->  p+  K- ^pi+)]CC", Type='T')
    #       , "probe" : Branch("[Lambda_c+ -> ^p+  K-  pi+)]CC", Type='T', isAlso = ['p'])
    #    }
    #    ),
    #  "LcMu_Pbar" : TupleConfig (
    #    Decay = "[Lambda_c+ -> ^p+ ^K- ^pi+]CC"
    #    , InputLines    = ["Hlt2PIDLc2KPPiTurboCalib"]
    #    , Calibration   = "LcMuCalib_Neg"
    #    , Filter        = filters.NegativeID
    #    , Branches = {
    #       "Lc"    : Branch("^([Lambda_c+ ->  p+  K-  pi+]CC)", Type='H')
    #     , "K"     : Branch("[Lambda_c+ ->  p+ ^K-  pi+)]CC", Type='T')
    #     , "pi"    : Branch("[Lambda_c+ ->  p+  K- ^pi+)]CC", Type='T')
    #     , "probe" : Branch("[Lambda_c+ -> ^p+  K-  pi+)]CC", Type='T', isAlso = ['p'])
    #     }
    #    ),
    # ============ Electrons ===============================
    "B_Jpsi_EP": TupleConfig(
        Decay="[B+]cc -> ^(J/psi(1S) -> ^e+ ^e-) ^([K+]cc)",
        InputLines=["Hlt2PIDB2KJPsiEENegTaggedTurboCalib"],
        Calibration="BJpsiEECalib_Pos",
        Filter=filters.Jpsiee,
        Branches={
            "B": Branch("^([B+]cc ->  (J/psi(1S) ->  e+  e-) [ K+]cc)", Type="H"),
            "Jpsi": Branch("[B+]cc -> ^(J/psi(1S) ->  e+  e-) [ K+]cc", Type="I"),
            "probe": Branch(
                "[B+]cc ->  (J/psi(1S) -> ^e+  e-) [ K+]cc", Type="T", isAlso=["e"]
            ),
            "tag": Branch(
                "[B+]cc ->  (J/psi(1S) ->  e+ ^e-) [ K+]cc", Type="T", isAlso=["e"]
            ),
            "K": Branch("[B+]cc ->  (J/psi(1S) ->  e+  e-) ^([K+]cc)", Type="T"),
        },
    ),
    "B_Jpsi_EM": TupleConfig(
        Decay="[B+]cc -> ^(J/psi(1S) -> ^e+ ^e-) ^([K+]cc)",
        InputLines=["Hlt2PIDB2KJPsiEEPosTaggedTurboCalib"],
        Calibration="BJpsiEECalib_Neg",
        Filter=filters.Jpsiee,
        Branches={
            "B": Branch("^([B+]cc ->  (J/psi(1S) ->  e+  e-) [ K+]cc)", Type="H"),
            "Jpsi": Branch("[B+]cc -> ^(J/psi(1S) ->  e+  e-) [ K+]cc", Type="I"),
            "probe": Branch(
                "[B+]cc ->  (J/psi(1S) ->  e+ ^e-) [ K+]cc", Type="T", isAlso=["e"]
            ),
            "tag": Branch(
                "[B+]cc ->  (J/psi(1S) -> ^e+  e-) [ K+]cc", Type="T", isAlso=["e"]
            ),
            "K": Branch("[B+]cc ->  (J/psi(1S) ->  e+  e-) ^([K+]cc)", Type="T"),
        },
    ),
}


from Configurables import MessageSvc

MessageSvc().Format = "% F%60W%S%7W%R%T %0W%M"

# seqB2Dmu = GaudiSequencer('seqB2Dmu')
# TupleSeq = GaudiSequencer('TupleSeq')
#
# TupleSeq.Members += [  CreateTupleTool(Jpsi_MuM_decay)    ]
#
# TupleSeq.ModeOR          = True
# TupleSeq.ShortCircuit    = False
#
# seqB2Dmu.Members      += [TupleSeq]
# seqB2Dmu.ModeOR        = True
# seqB2Dmu.ShortCircuit  = False

dv = DaVinci(InputType="DST", EvtMax=-1, Lumi=True, TupleFile="PIDCALIB.ROOT")

dv.appendToMainSequence(
    parseConfiguration(
        tupleConfiguration,
        tesFormat="/Event/Turbo/<line>/Particles"
        # , mdstOutputFile = "PIDCALIB" # shouldn't change
        ,
        mdstOutputFile=None,  # Lucia's study
        mdstOutputPrefix="",  # SHOULD CHANGE!!!
        varsByType=LokiVarsByType,
        varsByName=LokiVarsByName,
        eventVariables=EventInfo,
        writeNullWeightCandidates=False,
    )
)

# dv.UserAlgorithms += [seqB2Dmu]
