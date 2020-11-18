#include <cstdlib>
#include <iostream>
#include <map>
#include <string>
using namespace std;

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

#if not defined(__CINT__) || defined(__MAKECINT__)
// needs to be included when makecint runs (ACLIC)
#include "TMVA/Factory.h"
#include "TMVA/MethodCuts.h"
#include "TMVA/Reader.h"
#include "TMVA/Tools.h"
#endif

using namespace TMVA;

void uBoostEval() {

  // gSystem->Load("$TMVALOC/lib/libTMVA.1.so");

  TMVA::Reader *reader;
  float m2ab, m2ac, y1, y2, y3, pmin, BDT;
  TString weightName = "weights/TMVA_UBDT.weights.xml";
  TMVA::Tools::Instance();
  reader = new TMVA::Reader("!Color:Silent");
  reader->AddVariable("Y1", &y1);
  reader->AddVariable("Y2", &y2);
  reader->AddVariable("Y3", &y3);
  reader->AddSpectator("M2AB", &m2ab);
  reader->AddSpectator("M2AC", &m2ac);
  reader->BookMVA("UBDT method", weightName);

  // input signal training sample
  TFile *inputS = new TFile("test/signal.root");
  TTree *ts = (TTree *)inputS->Get("T");
  ts->SetBranchAddress("M2AB", &m2ab);
  ts->SetBranchAddress("M2AC", &m2ac);
  ts->SetBranchAddress("Y1", &y1);
  ts->SetBranchAddress("Y2", &y2);
  ts->SetBranchAddress("Y3", &y3);
  ts->SetBranchAddress("PMIN", &pmin);
  int ns = (int)ts->GetEntries();

  // input background training sample
  TFile *inputB = new TFile("test/bkgd.root");
  TTree *tb = (TTree *)inputB->Get("T");
  tb->SetBranchAddress("M2AB", &m2ab);
  tb->SetBranchAddress("M2AC", &m2ac);
  tb->SetBranchAddress("Y1", &y1);
  tb->SetBranchAddress("Y2", &y2);
  tb->SetBranchAddress("Y3", &y3);
  tb->SetBranchAddress("PMIN", &pmin);
  int nb = (int)tb->GetEntries();

  // input high statistics signal evaluation sample
  TFile *input = new TFile("test/signal5e5.root");
  TTree *t5e5 = (TTree *)input->Get("T");
  t5e5->SetBranchAddress("M2AB", &m2ab);
  t5e5->SetBranchAddress("M2AC", &m2ac);
  t5e5->SetBranchAddress("Y1", &y1);
  t5e5->SetBranchAddress("Y2", &y2);
  t5e5->SetBranchAddress("Y3", &y3);
  t5e5->SetBranchAddress("PMIN", &pmin);
  int nHighStat = (int)t5e5->GetEntries();

  cout << "Done loading input data" << endl;

  // write uBDT response values to trees
  TFile *outputSignalResponse = new TFile("test/signalResp.root", "recreate");
  TTree *tsResponse = new TTree("TResponse", "");
  float signalResponse;
  tsResponse->Branch("RESPONSE", &signalResponse);

  TFile *outputBkgdResponse = new TFile("test/bkgdResp.root", "recreate");
  TTree *tbResponse = new TTree("TResponse", "");
  float bkgdResponse;
  tbResponse->Branch("RESPONSE", &bkgdResponse);

  TFile *outputSignal5e5Response = new TFile("test/signal5e5Resp.root", "recreate");
  TTree *ts5e5Response = new TTree("TResponse", "");
  float signal5e5Response;
  ts5e5Response->Branch("RESPONSE", &signal5e5Response);

  // signal response distribution
  cout << endl
       << "Processing " << ns
       << " signal events from train/test sample:" << endl;
  for (int e = 0; e < ns; e++) {
    if (e % 10000 == 0)
      cout << "...... " << e << " events complete" << endl;
    ts->GetEntry(e);
    BDT = reader->EvaluateMVA("UBDT method");
    signalResponse = BDT;
    tsResponse->Fill();
  }

  // background response distribution
  cout << endl
       << "Processing " << ns
       << " background events from train/test sample:" << endl;
  for (int e3 = 0; e3 < nb; e3++) {
    if (e3 % 10000 == 0)
      cout << "...... " << e3 << " events complete" << endl;
    tb->GetEntry(e3);
    BDT = reader->EvaluateMVA("UBDT method");
    bkgdResponse = BDT;
    tbResponse->Fill();
  }

  // high stats signal response distribution
  cout << endl
       << "Processing " << nHighStat
       << " signal events from independent high statisitics sample:" << endl;
  for (int e4 = 0; e4 < nHighStat; e4++) {
    if (e4 % 100000 == 0)
      cout << "...... " << e4 << " events complete" << endl;
    t5e5->GetEntry(e4);
    BDT = reader->EvaluateMVA("UBDT method");
    signal5e5Response = BDT;
    ts5e5Response->Fill();
  }

  // write and close response trees
  outputSignalResponse->Write();
  outputSignalResponse->Close();
  outputBkgdResponse->Write();
  outputBkgdResponse->Close();
  outputSignal5e5Response->Write();
  outputSignal5e5Response->Close();

  return;
}
