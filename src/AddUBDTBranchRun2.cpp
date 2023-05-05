// Author: Gregory Ciezarek, Yipeng Sun
// Last Change: Fri Jul 29, 2022 at 04:13 PM -0400

#include <cmath>
#include <iomanip>
#include <iostream>
#include <map>
#include <ostream>
#include <sstream>
#include <string>
#include <vector>

#include <TFile.h>
#include <TMVA/Reader.h>
#include <TString.h>
#include <TTree.h>
#include <TTreeFormula.h>

#include <cxxopts.hpp>

using namespace std;

////////
// UI //
////////

class progressBar {
  // Stolen from:
  //   https://codereview.stackexchange.com/questions/186535/progress-bar-in-c
  static const auto overhead = sizeof " [100%]";

  std::ostream &    os;
  const std::size_t bar_width;
  std::string       message;
  const std::string full_bar;

 public:
  progressBar(std::ostream &os, std::size_t line_width, std::string message_,
              const char symbol = '.')
      : os{os},
        bar_width{line_width - overhead},
        message{std::move(message_)},
        full_bar{std::string(bar_width, symbol) + std::string(bar_width, ' ')} {
    if (message.size() + 1 >= bar_width || message.find('\n') != message.npos) {
      os << message << '\n';
      message.clear();
    } else {
      message += ' ';
    }
    write(0.0);
  }

  // not copyable
  progressBar(const progressBar &) = delete;
  progressBar &operator=(const progressBar &) = delete;

  ~progressBar() {
    write(1.0);
    os << '\n';
  }

  void write(double fraction);
};

void progressBar::write(double fraction) {
  // clamp fraction to valid range [0,1]
  if (fraction < 0)
    fraction = 0;
  else if (fraction > 1)
    fraction = 1;

  auto width  = bar_width - message.size();
  auto offset = bar_width - static_cast<unsigned>(width * fraction);

  os << '\r' << message;
  os.write(full_bar.data() + offset, width);
  os << " [" << std::setw(3) << static_cast<int>(100 * fraction) << "%] "
     << std::flush;
}

/////////////
// Helpers //
/////////////

vector<string> split(const string &s, char delim) {
  stringstream   ss(s);
  string         item;
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

void addMuBDT(TFile *ntpIn, TFile *ntpOut, string treeName, TString particle,
              TString weightName, TString outputBrName) {
  cout << "Working on " << treeName << endl;
  // Configure branches to be loaded
  // NOTE: The ordering matters!
  // clang-format off
  auto ubdtVarNames = vector<TString>{
    "TrackChi2PerDof", "TrackNumDof", "TrackGhostProbability",
    "TrackFitMatchChi2", "TrackFitVeloChi2", "TrackFitVeloNDoF",
    "TrackFitTChi2", "TrackFitTNDoF",
    //
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
    "muminus_isMuonTight",
    //
    "TrackP", "TrackPt"
  };

#ifdef PIDCALIB
  TString prefix = particle + "_Brunel_ANNTraining_";
  TString prefix2 = particle + "_Brunel_";

  auto varBrNames = vector<TString>{
    prefix+"TrackChi2PerDof", prefix+"TrackNumDof", prefix+"TrackGhostProb",
    prefix+"TrackFitMatchChi2", prefix+"TrackFitVeloChi2", prefix+"TrackFitVeloNDoF",
    prefix+"TrackFitTChi2", prefix+"TrackFitTNDoF",
    //
    // "RichUsedAero",     <-- Not needed for run 2!
    // "TrackLikelihood",  <-- Not needed for run 2!
    //
    prefix2+"RICH1GasUsed", prefix2+"RICH2GasUsed",
    prefix2+"RICHThresholdMu", prefix2+"RICHThresholdKa",
    prefix+"RichDLLe", prefix+"RichDLLmu", prefix+"RichDLLk", prefix+"RichDLLp", prefix+"RichDLLbt",
    //
    prefix+"MuonLLBkg", prefix+"MuonLLMu", prefix+"MuonNShared + 1",
    // "+1" to align the offset. For more info, see https://github.com/umd-lhcb/MuonBDTPid/issues/10
    //
    prefix+"InAccEcal", prefix+"EcalPIDe", prefix+"EcalPIDmu",
    //
    prefix+"InAccHcal", prefix+"HcalPIDe", prefix+"HcalPIDmu",
    //
    prefix+"InAccPrs", prefix+"PrsPIDe",
    //
    prefix+"InAccBrem", prefix+"BremPIDe",
    //
    prefix+"VeloCharge",
    //
    prefix2 + "isMuonTight",
    //
    prefix+"TrackP", prefix+"TrackPt"
  };
#else
  auto varBrNames = vector<TString>{
    "TrackChi2PerDof", "TrackNumDof", "TrackGhostProbability",
    "TrackFitMatchChi2", "TrackFitVeloChi2", "TrackFitVeloNDoF",
    "TrackFitTChi2", "TrackFitTNDoF",
    //
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
    "BachMu_isMuonTight", //originally particle + ""
    //
    "TrackP", "TrackPt"
  };
#endif
  // clang-format on
  auto obVarNames = vector<TString>{"TrackP", "TrackPt"};

  auto treeIn     = dynamic_cast<TTree *>(ntpIn->Get(TString(treeName)));
  auto numEntries = static_cast<int>(treeIn->GetEntries());

  // Recreate the same folder structure in output
  auto treeDir  = dirname(treeName);
  auto treeBase = basename(treeName);

  ntpOut->cd();
  if (treeDir != TString("")) {
    ntpOut->mkdir(treeDir);
    ntpOut->cd(treeDir);
  }

  auto treeOut = new TTree(treeBase, treeBase);

  // Define variables to be loaded in the tree
  auto treeFormulae = map<TString, TTreeFormula>{};
  for (auto idx = 0; idx < ubdtVarNames.size(); idx++) {
    auto key     = ubdtVarNames[idx];
    auto formula = varBrNames[idx];
    treeFormulae.emplace(piecewise_construct, make_tuple(key),
                         make_tuple(key, formula, treeIn));
  }

  cout << "Done loading input data" << endl;

  // Define temp variable to store loaded branches in each loop
  map<TString, float> tempVars;
  for (auto name : ubdtVarNames) {
    tempVars.emplace(name, 0.);
  }

  // Pointing temp variables to the TMVA reader
  auto reader = new TMVA::Reader("!Color:Silent");

  for (auto name : ubdtVarNames) {
    reader->AddVariable(name, &tempVars[name]);
  }

  for (auto name : obVarNames) {
    reader->AddSpectator(name, &tempVars[name]);
  }

  reader->BookMVA("UBDT method", weightName);

  // Output branch
  float signalResponse;
  treeOut->Branch(particle + "_" + outputBrName, &signalResponse);

  // run and event Numbers
#ifdef PIDCALIB
  double runNumber;
  double eventNumber;
#else
  UInt_t    runNumber;
  ULong64_t eventNumber;
#endif
  treeIn->SetBranchAddress("runNumber", &runNumber);
  treeIn->SetBranchAddress("eventNumber", &eventNumber);
  treeOut->Branch("runNumber", &runNumber);
  treeOut->Branch("eventNumber", &eventNumber);

  // Start processing
  cout << treeName << " has " << numEntries << " entries" << endl;
  Long64_t stepSize = max(1ll, numEntries / 100ll);
  auto     progress = new progressBar(std::clog, 79u, string("Processing"));

  for (int e = 0; e < numEntries; e++) {
    if (!(e % stepSize))
      progress->write(static_cast<float>(e) / static_cast<float>(numEntries));
    treeIn->GetEntry(e);

    for (auto name : ubdtVarNames) {
      tempVars[name] = treeFormulae[name].EvalInstance();
    }

    signalResponse = reader->EvaluateMVA("UBDT method");
    treeOut->Fill();
  }

  ntpOut->Write("", TObject::kOverwrite);  // Keep latest cycle only
  delete reader;
  delete treeIn;
  delete treeOut;
  delete progress;
}

int main(int argc, char **argv) {
  cxxopts::Options argOpts("AddUBDTBranchRun2",
                           "add UBDT branch for run 2 ntuples.");

  // clang-format off
  argOpts.add_options()
    ("h,help", "print help")
    ("i,input", "input ntuple", cxxopts::value<string>())
    ("o,output", "output ntuple", cxxopts::value<string>())
    ("x,xml", "BDT XML export file", cxxopts::value<string>())
    ("b,ubdtBrName", "UBDT branch name",
     cxxopts::value<string>()->default_value("bdt_mu"))
    ("p,particle", "particle name",
     cxxopts::value<string>()->default_value("mu"))
    ("t,trees", "tree names", cxxopts::value<vector<string>>())
  ;
  // clang-format on

  auto parsedArgs = argOpts.parse(argc, argv);
  if (parsedArgs.count("help")) {
    cout << argOpts.help() << endl;
    return 0;
  }

  auto inputFilename  = TString(parsedArgs["input"].as<string>());
  auto outputFilename = TString(parsedArgs["output"].as<string>());
  auto xmlFilename    = TString(parsedArgs["xml"].as<string>());
  auto particle       = TString(parsedArgs["particle"].as<string>());
  auto ubdtBrName     = TString(parsedArgs["ubdtBrName"].as<string>());
  auto trees          = parsedArgs["trees"].as<vector<string>>();

  auto ntpIn  = new TFile(inputFilename, "read");
  auto ntpOut = new TFile(outputFilename, "recreate");

  for (auto t : trees)
    addMuBDT(ntpIn, ntpOut, t, particle, xmlFilename, ubdtBrName);

  ntpIn->Close();
  ntpOut->Close();
  delete ntpIn;
  delete ntpOut;

  return 0;
}
