#include <cstdlib>
#include <iostream>
#include <map>
#include <string>
using namespace std;

#include "TChain.h"
#include "TFile.h"
#include "TObjString.h"
#include "TPluginManager.h"
#include "TROOT.h"
#include "TString.h"
#include "TSystem.h"
#include "TTree.h"

#if not defined(__CINT__) || defined(__MAKECINT__)
// needs to be included when makecint runs (ACLIC)
#include "TMVA/Factory.h"
#include "TMVA/MethodCuts.h"
#include "TMVA/Reader.h"
#include "TMVA/Tools.h"
#endif

using namespace TMVA;

int main() {

  //gSystem->Load("$TMVALOC/lib/libTMVA.1.so");

  TMVA::Tools::Instance();
  TString weightName = "TMVA";

  TFile *outFile = new TFile("test/" + weightName + "UBDT.root", "recreate");
  TMVA::Factory *factory =
      new TMVA::Factory(weightName, outFile,
                        "!V:!Silent:Color:DrawProgressBar:Transformations=I");

  // variables used in BDT training
  factory->AddVariable("Y1", "y_{1}", "", 'F');
  factory->AddVariable("Y2", "y_{2}", "", 'F');
  factory->AddVariable("Y3", "y_{3}", "", 'F');

  // variables which uniformity is desired (used to define kNN)
  factory->AddSpectator("M2AB", "M_{AB}^{2}", "GeV/c^{2}", 'F');
  factory->AddSpectator("M2AC", "M_{AC}^{2}", "GeV/c^{2}", 'F');

  // get data
  TFile *fs = new TFile("test/signal.root");
  TFile *fb = new TFile("test/bkgd.root");
  TTree *ts = (TTree *)fs->Get("T");
  TTree *tb = (TTree *)fb->Get("T");

  factory->AddSignalTree(ts, 1.);
  factory->AddBackgroundTree(tb, 1.);

  factory->SetSignalWeightExpression("W");     // eventwise weights
  factory->SetBackgroundWeightExpression("W"); // eventwise weights

  factory->PrepareTrainingAndTestTree("", "",
                                      "nTrain_Signal=0:nTrain_Background=0:"
                                      "SplitMode=Block:NormMode=NumEvents:!V");

  TString bdt = "!H:!V:NTrees=100:nEventsMin=100:MaxDepth=4:BoostType=AdaBoost:"
                "AdaBoostBeta=1.0:PruneMethod=NoPruning:SeparationType="
                "GiniIndex:nCuts=200";
  factory->BookMethod(TMVA::Types::kBDT, "BDT", bdt);
  bdt += ":uBoostFlag=1"; // add flag to use uBoost
  factory->BookMethod(
      TMVA::Types::kUBDT, "UBDT",
      "nKNN=100:UBDT_Num=10:UBDT_MinEffic=0.0:UBDT_MaxEffic=1.0:" +
          bdt); // 100 efficiency steps between 0 and 100%

  factory->TrainAllMethods();
  factory->TestAllMethods();
  factory->EvaluateAllMethods();

  fs->Close();
  fb->Close();
  outFile->Close();
  delete factory;

  return 0;
}
