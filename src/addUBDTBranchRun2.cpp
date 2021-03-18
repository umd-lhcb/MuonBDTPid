// Author: Gregory Ciezarek, Yipeng Sun
// Last Change: Thu Mar 18, 2021 at 04:20 AM +0100

#include <iostream>
#include <map>
#include <vector>

#include "TFile.h"
#include "TMVA/Reader.h"
#include "TString.h"
#include "TTree.h"
#include "TTreeFormula.h"

using namespace std;

void addMuBDT(TFile *ntp, TString treename, TString isMuonTightBrName,
              TString outputBrName = "mu_bdt",
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

  auto *tree = dynamic_cast<TTree *>(ntp->Get(treename));
  auto numEntries = static_cast<int>(tree->GetEntries());

  // Define variables to be loaded in the tree
  auto treeFormulae = map<TString, TTreeFormula>{};
  for (auto name : varBrNames) {
    treeFormulae.emplace(piecewise_construct, make_tuple(name),
                         make_tuple(name, name, tree));
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
  TString isMuonTightBrName = argv[2];
  auto *ntp = new TFile(filename, "update");
  cout << "Input file: " << filename << endl;
  cout << "isMuonTight branch name is: " << isMuonTightBrName << endl;

  for (int i = 3; i < argc; i++) {
    TString treename = argv[i];
    cout << "Processing tree: " << treename << endl;
    addMuBDT(ntp, treename, isMuonTightBrName);
  }

  ntp->Close();
  delete ntp;

  return 0;
}
