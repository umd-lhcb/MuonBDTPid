#include <cstdlib>
#include <iostream>
#include <map>
#include <string>
#include <vector>

#include "TBranch.h"
#include "TCanvas.h"
#include "TChain.h"
#include "TColor.h"
#include "TFile.h"
#include "TGraph.h"
#include "TH2F.h"
#include "TLatex.h"
#include "TMath.h"
#include "TObjString.h"
#include "TPluginManager.h"
#include "TROOT.h"
#include "TString.h"
#include "TSystem.h"
#include "TTree.h"
#include "TTreeFormula.h"

#if not defined(__CINT__) || defined(__MAKECINT__)
// needs to be included when makecint runs (ACLIC)
#include "TMVA/Factory.h"
#include "TMVA/MethodCuts.h"
#include "TMVA/Reader.h"
#include "TMVA/Tools.h"
#endif

using namespace std;
using namespace TMVA;

void addMuBDT(TFile *ntp, TString treename, TString outputBrName = "mu_bdt",
              TString isMuonTightBrName = "tag_isMuonTight",
              TString weightName = "weights/TMVA_Run2NoCut_UBDT.weights.xml") {
  auto *ts = (TTree *)dynamic_cast<TTree *>(ntp->Get(treename));
  auto ns = static_cast<int>(ts->GetEntries());

  TTreeFormula TrackChi2PerDof_tf("TrackChi2PerDof", "TrackChi2PerDof", ts);
  TTreeFormula TrackNumDof_tf("TrackNumDof", "TrackNumDof", ts);
  TTreeFormula TrackLikelihood_tf("TrackLikelihood", "TrackLikelihood", ts);
  TTreeFormula TrackGhostProbability_tf("TrackGhostProbability",
                                        "TrackGhostProbability", ts);
  TTreeFormula TrackFitMatchChi2_tf("TrackFitMatchChi2", "TrackFitMatchChi2",
                                    ts);
  TTreeFormula TrackFitVeloChi2_tf("TrackFitVeloChi2", "TrackFitVeloChi2", ts);
  TTreeFormula TrackFitVeloNDoF_tf("TrackFitVeloNDoF", "TrackFitVeloNDoF", ts);
  TTreeFormula TrackFitTChi2_tf("TrackFitTChi2", "TrackFitTChi2", ts);
  TTreeFormula TrackFitTNDoF_tf("TrackFitTNDoF", "TrackFitTNDoF", ts);
  TTreeFormula RichUsedAero_tf("RichUsedAero", "RichUsedAero", ts);
  TTreeFormula RichUsedR1Gas_tf("RichUsedR1Gas", "RichUsedR1Gas", ts);
  TTreeFormula RichUsedR2Gas_tf("RichUsedR2Gas", "RichUsedR2Gas", ts);
  TTreeFormula RichAboveMuThres_tf("RichAboveMuThres", "RichAboveMuThres", ts);
  TTreeFormula RichAboveKaThres_tf("RichAboveKaThres", "RichAboveKaThres", ts);
  TTreeFormula RichDLLe_tf("RichDLLe", "RichDLLe", ts);
  TTreeFormula RichDLLmu_tf("RichDLLmu", "RichDLLmu", ts);
  TTreeFormula RichDLLk_tf("RichDLLk", "RichDLLk", ts);
  TTreeFormula RichDLLp_tf("RichDLLp", "RichDLLp", ts);
  TTreeFormula RichDLLbt_tf("RichDLLbt", "RichDLLbt", ts);
  TTreeFormula MuonBkgLL_tf("MuonBkgLL", "MuonBkgLL", ts);
  TTreeFormula MuonMuLL_tf("MuonMuLL", "MuonMuLL", ts);
  TTreeFormula MuonNShared_tf("MuonNShared", "MuonNShared", ts);
  TTreeFormula InAccEcal_tf("InAccEcal", "InAccEcal", ts);
  TTreeFormula EcalPIDe_tf("EcalPIDe", "EcalPIDe", ts);
  TTreeFormula EcalPIDmu_tf("EcalPIDmu", "EcalPIDmu", ts);
  TTreeFormula InAccHcal_tf("InAccHcal", "InAccHcal", ts);
  TTreeFormula HcalPIDe_tf("HcalPIDe", "HcalPIDe", ts);
  TTreeFormula HcalPIDmu_tf("HcalPIDmu", "HcalPIDmu", ts);
  TTreeFormula InAccPrs_tf("InAccPrs", "InAccPrs", ts);
  TTreeFormula PrsPIDe_tf("PrsPIDe", "PrsPIDe", ts);
  TTreeFormula InAccBrem_tf("InAccBrem", "InAccBrem", ts);
  TTreeFormula BremPIDe_tf("BremPIDe", "BremPIDe", ts);
  TTreeFormula VeloCharge_tf("VeloCharge", "VeloCharge", ts);
  TTreeFormula mu_isMuonTight_tf("mu_isMuonTight", isMuonTightBrName, ts);
  TTreeFormula TrackP_tf("TrackP", "TrackP", ts);
  TTreeFormula TrackPt_tf("TrackPt", "TrackPt", ts);

  cout << "Done loading input data" << endl;
  TMVA::Reader *reader;

  float TrackChi2PerDof;
  float TrackNumDof;
  float TrackLikelihood;
  float TrackGhostProbability;
  float TrackFitMatchChi2;
  float TrackFitVeloChi2;
  float TrackFitVeloNDoF;
  float TrackFitTChi2;
  float TrackFitTNDoF;
  float RichUsedAero;
  float RichUsedR1Gas;
  float RichUsedR2Gas;
  float RichAboveMuThres;
  float RichAboveKaThres;
  float RichDLLe;
  float RichDLLmu;
  float RichDLLk;
  float RichDLLp;
  float RichDLLbt;
  float MuonBkgLL;
  float MuonMuLL;
  float MuonNShared;
  float InAccEcal;
  float EcalPIDe;
  float EcalPIDmu;
  float InAccHcal;
  float HcalPIDe;
  float HcalPIDmu;
  float InAccPrs;
  float PrsPIDe;
  float InAccBrem;
  float BremPIDe;
  float VeloCharge;
  float TrackP;
  float TrackPt;
  float mu_isMuonTight;

  TMVA::Tools::Instance();
  reader = new TMVA::Reader("!Color:Silent");

  reader->AddVariable("TrackChi2PerDof", &TrackChi2PerDof);
  reader->AddVariable("TrackNumDof", &TrackNumDof);
  reader->AddVariable("TrackGhostProbability", &TrackGhostProbability);
  reader->AddVariable("TrackFitMatchChi2", &TrackFitMatchChi2);
  reader->AddVariable("TrackFitVeloChi2", &TrackFitVeloChi2);
  reader->AddVariable("TrackFitVeloNDoF", &TrackFitVeloNDoF);
  reader->AddVariable("TrackFitTChi2", &TrackFitTChi2);
  reader->AddVariable("TrackFitTNDoF", &TrackFitTNDoF);
  reader->AddVariable("RichUsedR1Gas", &RichUsedR1Gas);
  reader->AddVariable("RichUsedR2Gas", &RichUsedR2Gas);
  reader->AddVariable("RichAboveMuThres", &RichAboveMuThres);
  reader->AddVariable("RichAboveKaThres", &RichAboveKaThres);
  reader->AddVariable("RichDLLe", &RichDLLe);
  reader->AddVariable("RichDLLmu", &RichDLLmu);
  reader->AddVariable("RichDLLk", &RichDLLk);
  reader->AddVariable("RichDLLp", &RichDLLp);
  reader->AddVariable("RichDLLbt", &RichDLLbt);
  reader->AddVariable("MuonBkgLL", &MuonBkgLL);
  reader->AddVariable("MuonMuLL", &MuonMuLL);
  reader->AddVariable("MuonNShared", &MuonNShared);
  reader->AddVariable("InAccEcal", &InAccEcal);
  reader->AddVariable("EcalPIDe", &EcalPIDe);
  reader->AddVariable("EcalPIDmu", &EcalPIDmu);
  reader->AddVariable("InAccHcal", &InAccHcal);
  reader->AddVariable("HcalPIDe", &HcalPIDe);
  reader->AddVariable("HcalPIDmu", &HcalPIDmu);
  reader->AddVariable("InAccPrs", &InAccPrs);
  reader->AddVariable("PrsPIDe", &PrsPIDe);
  reader->AddVariable("InAccBrem", &InAccBrem);
  reader->AddVariable("BremPIDe", &BremPIDe);
  reader->AddVariable("VeloCharge", &VeloCharge);
  reader->AddVariable("muminus_isMuonTight", &mu_isMuonTight);
  reader->AddVariable("TrackP", &TrackP);
  reader->AddVariable("TrackPt", &TrackPt);

  reader->AddSpectator("TrackP", &TrackP);
  reader->AddSpectator("TrackPt", &TrackPt);

  reader->BookMVA("UBDT method", weightName);

  float signalResponse;
  TBranch *br = ts->Branch(outputBrName, &signalResponse);

  cout << endl
       << "Processing " << ns << " events from PIDCalib sample:" << endl;
  for (int e = 0; e < ns; e++) {
    if (e % 10000 == 0) cout << "...... " << e << " events complete" << endl;
    ts->GetEntry(e);

    TrackChi2PerDof = TrackChi2PerDof_tf.EvalInstance();
    TrackNumDof = TrackNumDof_tf.EvalInstance();
    TrackLikelihood = TrackLikelihood_tf.EvalInstance();
    TrackGhostProbability = TrackGhostProbability_tf.EvalInstance();
    TrackFitMatchChi2 = TrackFitMatchChi2_tf.EvalInstance();
    TrackFitVeloChi2 = TrackFitVeloChi2_tf.EvalInstance();
    TrackFitVeloNDoF = TrackFitVeloNDoF_tf.EvalInstance();
    TrackFitTChi2 = TrackFitTChi2_tf.EvalInstance();
    TrackFitTNDoF = TrackFitTNDoF_tf.EvalInstance();
    RichUsedAero = RichUsedAero_tf.EvalInstance();
    RichUsedR1Gas = RichUsedR1Gas_tf.EvalInstance();
    RichUsedR2Gas = RichUsedR2Gas_tf.EvalInstance();
    RichAboveMuThres = RichAboveMuThres_tf.EvalInstance();
    RichAboveKaThres = RichAboveKaThres_tf.EvalInstance();
    RichDLLe = RichDLLe_tf.EvalInstance();
    RichDLLmu = RichDLLmu_tf.EvalInstance();
    RichDLLk = RichDLLk_tf.EvalInstance();
    RichDLLp = RichDLLp_tf.EvalInstance();
    RichDLLbt = RichDLLbt_tf.EvalInstance();
    MuonBkgLL = MuonBkgLL_tf.EvalInstance();
    MuonMuLL = MuonMuLL_tf.EvalInstance();
    MuonNShared = MuonNShared_tf.EvalInstance();
    InAccEcal = InAccEcal_tf.EvalInstance();
    EcalPIDe = EcalPIDe_tf.EvalInstance();
    EcalPIDmu = EcalPIDmu_tf.EvalInstance();
    InAccHcal = InAccHcal_tf.EvalInstance();
    HcalPIDe = HcalPIDe_tf.EvalInstance();
    HcalPIDmu = HcalPIDmu_tf.EvalInstance();
    InAccPrs = InAccPrs_tf.EvalInstance();
    PrsPIDe = PrsPIDe_tf.EvalInstance();
    InAccBrem = InAccBrem_tf.EvalInstance();
    BremPIDe = BremPIDe_tf.EvalInstance();
    VeloCharge = VeloCharge_tf.EvalInstance();
    mu_isMuonTight = mu_isMuonTight_tf.EvalInstance();
    TrackP = TrackP_tf.EvalInstance();
    TrackPt = TrackPt_tf.EvalInstance();

    signalResponse = reader->EvaluateMVA("UBDT method");

    br->Fill();
  }

  ntp->Write("", TObject::kOverwrite);  // Keep latest cycle only
}

int main(int argc, char *argv[]) {
  TString filename = argv[1];
  auto *ntp = new TFile(filename, "update");

  auto treesToProcess = vector<TString>{"Jpsinopt_MuMTuple/DecayTree",
                                        "Jpsinopt_MuPTuple/DecayTree"};

  for (auto treename : treesToProcess) {
    addMuBDT(ntp, treename);
  }

  ntp->Close();
  delete ntp;

  return 0;
}
