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
  // Configure branches to be loaded
  // NOTE: The ordering matters!
  // clang-format off
  auto varBrNames = vector<TString>{
    "TrackChi2PerDof", "TrackNumDof", "TrackGhostProbability",
    "TrackFitMatchChi2", "TrackFitVeloChi2", "TrackFitVeloNDoF",
    "TrackFitTChi2", "TrackFitTNDoF",
    //
    //"RichUsedAero",  <-- Not needed for run 2!
    "RichUsedR1Gas", "RichUsedR2Gas",
    "RichAboveMuThres", "RichAboveKaThres",
    "RichDLLe", "RichDLLmu", "RichDLLk", "RichDLLp", "RichDLLbt",
    //
    "MuonBkgLL", "MuonMuLL", "MuonNShared",
    //
    "InAccEcal", "EcalPIDe", "EcalPIDmu",
    //
    "InAccHcal", "HcalPIDe", "HcalPIDmu",
    //
    "InAccPrs", "PrsPIDe",
    //
    "InAccBrem", "BremPIDe",
    //
    "VeloCharge",
    //
    isMuonTightBrName,
    //
    "TrackP", "TrackPt"
  };
  // clang-format on
  auto obBrNames = vector<TString>{"TrackP", "TrackPt"};

  auto *tree = (TTree *)dynamic_cast<TTree *>(ntp->Get(treename));
  auto numEntries = static_cast<int>(tree->GetEntries());

  // Define variables to be loaded in the tree
  auto treeFormulae = map<TString, TTreeFormula>{};
  for (auto name : varBrNames) {
    treeFormulae.emplace(std::piecewise_construct, std::make_tuple(name),
                         std::make_tuple(name, name, tree));
  }

  cout << "Done loading input data" << endl;

  // Define temp variable to store loaded branches in each loop
  map<TString, float> tempVars;
  for (auto name : varBrNames) {
    tempVars.emplace(name, 0.);
  }

  // Pointing temp variables to the TMVA reader
  auto reader = new TMVA::Reader("!Color:Silent");

  for (auto name : varBrNames) {
    if (name == isMuonTightBrName) {
      reader->AddVariable("muminus_isMuonTight", &tempVars[name]);
    } else {
      reader->AddVariable(name, &tempVars[name]);
    }
  }

  for (auto name : obBrNames) {
    reader->AddSpectator(name, &tempVars[name]);
  }

  reader->BookMVA("UBDT method", weightName);

  // Output branch
  float signalResponse;
  TBranch *br = tree->Branch(outputBrName, &signalResponse);

  // Start processing
  cout << endl
       << "Processing " << numEntries
       << " events from PIDCalib sample:" << endl;
  for (int e = 0; e < numEntries; e++) {
    if (e % 10000 == 0) cout << "...... " << e << " events complete" << endl;
    tree->GetEntry(e);

    for (auto name : varBrNames) {
      tempVars[name] = treeFormulae[name].EvalInstance();
    }

    signalResponse = reader->EvaluateMVA("UBDT method");
    br->Fill();
  }

  ntp->Write("", TObject::kOverwrite);  // Keep latest cycle only
  delete reader;
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
