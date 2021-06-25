// Author: Gregory Ciezarek, Yipeng Sun
// Last Change: Fri Jun 25, 2021 at 09:22 PM +0200

#include <TFile.h>
#include <TMVA/Reader.h>
#include <TString.h>
#include <TTree.h>
#include <TTreeFormula.h>

#include <iostream>
#include <map>
#include <sstream>
#include <string>
#include <vector>

using namespace std;

/////////////
// Helpers //
/////////////

vector<string> split(const string &s, char delim) {
  stringstream ss(s);
  string item;
  vector<string> elems;

  while (getline(ss, item, delim)) {
    elems.push_back(move(item));
  }

  return elems;
}

TString dirname(string s) {
  auto splitted = split(s, '/');
  if (splitted.size() == 1) return TString("");

  TString dir = "";
  for (int idx = 0; idx < splitted.size() - 1; idx++) {
    dir += splitted[idx];
    if (idx < splitted.size() - 2) dir += "/";
  }

  return dir;
}

TString basename(string s) { return TString(split(s, '/').back()); }

/////////////////////////
// Add Muon BDT branch //
/////////////////////////

void addMuBDT(TFile *ntpIn, TFile *ntpOut, string treeName,
              TString isMuonTightBrName, TString weightName,
              TString outputBrName = "mu_bdt_mu") {
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

  auto treeIn = dynamic_cast<TTree *>(ntpIn->Get(TString(treeName)));
  auto numEntries = static_cast<int>(treeIn->GetEntries());

  // Recreate the same folder structure in output
  auto treeDir = dirname(treeName);
  auto treeBase = basename(treeName);

  ntpOut->cd();
  if (treeDir != TString("")) {
    ntpOut->mkdir(treeDir);
    ntpOut->cd(treeDir);
  }

  auto treeOut = new TTree(treeBase, treeBase);

  // Define variables to be loaded in the tree
  auto treeFormulae = map<TString, TTreeFormula>{};
  for (auto name : varBrNames) {
    treeFormulae.emplace(piecewise_construct, make_tuple(name),
                         make_tuple(name, name, treeIn));
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
  treeOut->Branch(outputBrName, &signalResponse);

  // run and event Numbers
  UInt_t runNumber;
  Long64_t eventNumber;
  treeIn->SetBranchAddress("runNumber", &runNumber);
  treeIn->SetBranchAddress("eventNumber", &eventNumber);
  treeOut->Branch("runNumber", &runNumber);
  treeOut->Branch("eventNumber", &eventNumber);

  // Start processing
  cout << endl
       << "Processing " << numEntries
       << " events from PIDCalib sample:" << endl;
  for (int e = 0; e < numEntries; e++) {
    if (e % 5000 == 0) cout << "...... " << e << " events complete" << endl;
    treeIn->GetEntry(e);

    for (auto name : varBrNames) {
      tempVars[name] = treeFormulae[name].EvalInstance();
    }

    signalResponse = reader->EvaluateMVA("UBDT method");
    treeOut->Fill();
  }

  ntpOut->Write("", TObject::kOverwrite);  // Keep latest cycle only
  delete reader;
  delete treeIn;
  delete treeOut;
}

int main(int argc, char *argv[]) {
  TString inputFilename = argv[1];
  TString isMuonTightBrName = argv[2];
  TString inputXml = argv[3];
  TString outputFilename = argv[4];

  auto *ntpIn = new TFile(inputFilename, "read");
  auto *ntpOut = new TFile(outputFilename, "recreate");

  cout << "Input file: " << inputFilename << endl;
  cout << "isMuonTight branch name is: " << isMuonTightBrName << endl;
  cout << "Input BDT XML: " << inputXml << endl;

  for (int i = 5; i < argc; i++) {
    string treeName = argv[i];
    cout << "Processing tree: " << treeName << endl;
    addMuBDT(ntpIn, ntpOut, treeName, isMuonTightBrName, inputXml);
  }

  ntpIn->Close();
  ntpOut->Close();
  delete ntpIn;
  delete ntpOut;

  return 0;
}
