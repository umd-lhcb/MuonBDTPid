# Author: Yipeng Sun
# Last Change: Wed Jun 08, 2022 at 03:37 AM -0400

BINPATH	:=	bin
VPATH	:=	$(BINPATH)
VPATH	:=	test:src:$(VPATH)

# Compiler settings
COMPILER	:=	$(shell root-config --cxx)
CXXFLAGS	:=	$(shell root-config --cflags)
LINKFLAGS	:=	$(shell root-config --libs)
ADDCXXFLAGS	:=	-g -O1
ADDLINKFLAGS	:=	-lTreePlayer -lMinuit -lFoam -lXMLIO -lTMVA

CASTELAO_VERSION=Castelao-v3r4

.PHONY: clean

exe: AddUBDTBranchRun2 AddUBDTBranchRun2PidCalib

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
.PHONY: test-apply test-nix-pkg

# Apply UBDT to a PIDCalib sample
test-apply: \
	samples/Jpsi--21_02_05--pidcalib--data_turbo--2016--mu--Mu_nopt-subset.root AddUBDTBranchRun2 \
	samples/Jpsi--21_11_30--pidcalib--data_turbo--2016--mu--Mu_nopt-subset.root AddUBDTBranchRun2PidCalib
	bin/AddUBDTBranchRun2 \
		-i samples/Jpsi--21_02_05--pidcalib--data_turbo--2016--mu--Mu_nopt-subset.root \
		-o gen/pidcalib_old.root \
		-p probe -x weights/weights_run2_no_cut_ubdt.xml -b UBDT \
		-t "Jpsinopt_MuMTuple/DecayTree","Jpsinopt_MuPTuple/DecayTree"
	bin/AddUBDTBranchRun2PidCalib \
		-i samples/Jpsi--21_11_30--pidcalib--data_turbo--2016--mu--Mu_nopt-subset.root \
		-o gen/pidcalib_new.root \
		-p probe -x weights/weights_run2_no_cut_ubdt.xml -b UBDT \
		-t "Jpsinopt_MuMTuple/DecayTree","Jpsinopt_MuPTuple/DecayTree"
	plotbr \
		-o ./gen/mu_bdt_mu_MuM_comp_norm.png \
		-n ./gen/pidcalib_old.root/Jpsinopt_MuMTuple/DecayTree \
		-b probe_UBDT -l "UBDT, MuM, old" \
		-n ./gen/pidcalib_new.root/Jpsinopt_MuMTuple/DecayTree \
		-b probe_UBDT -l "MuM, new" \
		--normalize -YL "Normalized"
	plotbr \
		-o ./gen/mu_bdt_mu_MuM_comp.png \
		-n ./gen/pidcalib_old.root/Jpsinopt_MuMTuple/DecayTree \
		-b probe_UBDT -l "UBDT, MuM, old" \
		-n ./gen/pidcalib_new.root/Jpsinopt_MuMTuple/DecayTree \
		-b probe_UBDT -l "MuM, new"


# Test that the wrapped nix package also works
test-nix-pkg: samples/Jpsi--21_11_30--pidcalib--data_turbo--2016--mu--Mu_nopt-subset.root
	AddUBDTBranchPidCalib -i $< -o gen/pidcalib_w_nix_pkg.root \
		-p probe -b UBDT -t "Jpsinopt_MuMTuple/DecayTree","Jpsinopt_MuPTuple/DecayTree"


###############
# Executables #
###############

AddUBDTBranchRun2:

AddUBDTBranchRun2PidCalib: AddUBDTBranchRun2.cpp
	$(COMPILER) $(CXXFLAGS) -DPIDCALIB -o $(BINPATH)/$@ $< $(LINKFLAGS) $(ADDLINKFLAGS)


####################################
# PIDCalib ntuple w/ UBDT workflow #
####################################

test-grab-ntp:
	./scripts/ntuple_grabber.py --ymlName ./spec/pidcalib.yml --lxplusUser ejiang --dryRun

test-check-hash:
	./scripts/hash_checker.py --ymlName ./spec/pidcalib.yml --localFileHashes gen/test_local_hash.yml --dryRun


####################
# General patterns #
####################

%.dbg: %.cpp
	$(COMPILER) $(CXXFLAGS) $(ADDCXXFLAGS) -o $(BINPATH)/$@ $< $(LINKFLAGS) $(ADDLINKFLAGS)

%: %.cpp
	$(COMPILER) $(CXXFLAGS) -o $(BINPATH)/$@ $< $(LINKFLAGS) $(ADDLINKFLAGS)
