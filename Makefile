# Author: Yipeng Sun
# Last Change: Wed Apr 20, 2022 at 09:06 PM -0400

BINPATH	:=	bin
VPATH	:=	$(BINPATH)
VPATH	:=	test:src:$(VPATH)

# Compiler settings
COMPILER	:=	$(shell root-config --cxx)
CXXFLAGS	:=	$(shell root-config --cflags)
LINKFLAGS	:=	$(shell root-config --libs)
ADDCXXFLAGS	:=	-g -O1
ADDLINKFLAGS	:=	-lTreePlayer -lMinuit -lFoam -lXMLIO -lTMVA
# Current nix root5 derivation doesn't have RooFit library.
#ADDLINKFLAGS	:=	-lTreePlayer -lRooFitCore -lRooFit -lMinuit -lFoam -lXMLIO -lTMVA

CASTELAO_VERSION=Castelao-v3r4

.PHONY: clean
clean:
	@rm -rf $(BINPATH)/*
	@rm -rf gen/*
	@rm -rf test/TMVAUBDT.root
	@rm -rf weights/TMVA_BDT.class.C
	@rm -rf weights/TMVA_BDT.weights.xml


#####################
# Run docker images #
#####################

.PHONY: docker-cl

ifeq ($(OS),Darwin)
CL_CMD = "docker run --rm -it -v $(PWD):/data -e UID=$$(id -u) -e GID=$$(id -g) --net=host umdlhcb/lhcb-stack-cc7:${CASTELAO_VERSION}"
else
CL_CMD = "docker run --rm -it -v $(PWD):/data -v $$HOME/.Xauthority:/home/physicist/.Xauthority -e DISPLAY -e UID=$$(id -u) -e GID=$$(id -g) --net=host umdlhcb/lhcb-stack-cc7:${CASTELAO_VERSION}"
endif

docker-cl:
	@eval $(CL_CMD)


#########
# Tests #
#########

# Apply UBDT to a PIDCalib sample
.PHONY: test-apply
test-apply: \
	samples/Jpsi--21_02_05--pidcalib--data_turbo--2016--mu--Mu_nopt-subset.root addUBDTBranchRun2 \
	samples/Jpsi--21_11_30--pidcalib--data_turbo--2016--mu--Mu_nopt-subset.root addUBDTBranchRun2PidCalib
	bin/addUBDTBranchRun2 \
		samples/Jpsi--21_02_05--pidcalib--data_turbo--2016--mu--Mu_nopt-subset.root \
		"probe_isMuonTight" "weights/weights_run2_no_cut_ubdt.xml" "gen/pidcalib_old.root" \
		"Jpsinopt_MuMTuple/DecayTree" "Jpsinopt_MuPTuple/DecayTree"
	bin/addUBDTBranchRun2PidCalib \
		samples/Jpsi--21_11_30--pidcalib--data_turbo--2016--mu--Mu_nopt-subset.root \
		"probe_Brunel_isMuonTight" "weights/weights_run2_no_cut_ubdt.xml" "gen/pidcalib_new.root" \
		"Jpsinopt_MuMTuple/DecayTree" "Jpsinopt_MuPTuple/DecayTree"
	plotbr \
		-o ./gen/mu_bdt_mu_MuM_comp_norm.png \
		-n ./gen/pidcalib_old.root/Jpsinopt_MuMTuple/DecayTree \
		-b mu_bdt_mu -l "UBDT, MuM, old" \
		-n ./gen/pidcalib_new.root/Jpsinopt_MuMTuple/DecayTree \
		-b mu_bdt_mu -l "MuM, new" \
	    --normalize -YL "Normalized"
	plotbr \
		-o ./gen/mu_bdt_mu_MuM_comp.png \
		-n ./gen/pidcalib_old.root/Jpsinopt_MuMTuple/DecayTree \
		-b mu_bdt_mu -l "UBDT, MuM, old" \
		-n ./gen/pidcalib_new.root/Jpsinopt_MuMTuple/DecayTree \
		-b mu_bdt_mu -l "MuM, new"


###############
# Executables #
###############

addUBDTBranchRun2:

addUBDTBranchRun2PidCalib: addUBDTBranchRun2.cpp
	$(COMPILER) $(CXXFLAGS) -DPIDCALIB -o $(BINPATH)/$@ $< $(LINKFLAGS) $(ADDLINKFLAGS)


####################
# General patterns #
####################

%.dbg: %.cpp
	$(COMPILER) $(CXXFLAGS) $(ADDCXXFLAGS) -o $(BINPATH)/$@ $< $(LINKFLAGS) $(ADDLINKFLAGS)

%: %.cpp
	$(COMPILER) $(CXXFLAGS) -o $(BINPATH)/$@ $< $(LINKFLAGS) $(ADDLINKFLAGS)
