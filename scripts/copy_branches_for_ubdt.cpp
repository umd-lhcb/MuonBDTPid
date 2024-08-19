// Author: Alex Fernez

// For whatever reason (some file compression incompatibility?) can't open 2017/2018 PIDCalib
// files using ROOT5, but only have uBoost added onto ROOT5 (not ROOT6), so here I'll copy the
// files in our glacier 'remote' dir to a 'remote-ubdt-only' dir (only keeping the branches needed
// for ubdt evaluation)

// NEED TO USE ROOT6 TO BE ABLE TO OPEN 2017/2018 FILES

using namespace std;

void copy_branches_for_ubdt(TString remote_to_copy, TString remote_new, TString rel_path) {
    // from AddUBDTBranchRun2.cpp (with some adjustments for missing things)
    vector<TString> ubdtVarNames{
        "eventNumber", "runNumber",
        "TrackChi2PerDof", "TrackNumDof", "TrackGhostProb",
        "TrackFitMatchChi2", "TrackFitVeloChi2", "TrackFitVeloNDoF",
        "TrackFitTChi2", "TrackFitTNDoF",
        "RichUsedR1Gas", "RichUsedR2Gas", "RICH1GasUsed", "RICH2GasUsed",
        "RichAboveMuThres", "RichAboveKaThres", "RICHThresholdMu", "RICHThresholdKa"
        "RichDLLe", "RichDLLmu", "RichDLLk", "RichDLLp", "RichDLLbt",
        "MuonLLBkg", "MuonLLMu",
        "MuonBkgLL", "MuonMuLL", "MuonNShared",
        "InAccEcal", "EcalPIDe", "EcalPIDmu",
        "InAccHcal", "HcalPIDe", "HcalPIDmu",
        "InAccPrs", "PrsPIDe",
        "InAccBrem", "BremPIDe",
        "VeloCharge",
        "isMuonTight",
        "TrackP", "TrackPt"};

    gErrorIgnoreLevel = kFatal;
    TFile* ref = new TFile(remote_to_copy + "/" + rel_path);
    TFile* copied = new TFile(remote_new + "/" + rel_path, "recreate");
    int tree_count = 0;
    cout << "Copying " << remote_to_copy << "/" << rel_path << " to " << remote_new << endl;
    // loop over trees in ref, copy tree structure in new file, and copy relevant parts of trees
    for (auto ch : *(ref->GetListOfKeys())) {
        if (tree_count>0) copied = new TFile(remote_new + "/" + rel_path, "update");
        TString ch_name = ch->GetName();
        if (ch_name.Index("Tuple")==-1) continue;
        cout << "  Tree: " << ch_name << "/DecayTree" << endl;
        TTree* t = (TTree*)ref->Get(ch_name + "/DecayTree");
        copied->mkdir(ch_name);
        copied->cd(ch_name);
        // deactivate all but needed branches
        // t->SetBranchStatus("*",0);
        // for (auto br: *(t->GetListOfBranches())) {
        //     TString br_name = br->GetName();
        //     for (auto var : ubdtVarNames) {
        //         if (br_name.Index(var)!=-1) t->SetBranchStatus(br_name, 1);
        //     }
        // }
        TTree* tn = t->CloneTree();
        copied->Write();
        copied->Close();
        tree_count++;
    }
}