# Author: Yipeng Sun
# Last Change: Thu Mar 18, 2021 at 04:04 AM +0100

BINPATH	:=	bin
VPATH	:=	$(BINPATH)
VPATH	:=	test:src:$(VPATH)

export PATH	:=	$(BINPATH):$(PATH)

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
test-apply: gen/pidcalib.root addUBDTBranchRun2
	$(word 2, $^) $< "Jpsinopt_MuMTuple/DecayTree" "Jpsinopt_MuPTuple/DecayTree"

gen/pidcalib.root: samples/JPsi--21_02_05--pidcalib--data--2016--nopt-subset.root
	@cp $< $@
	@chmod 644 $@


###############
# Executables #
###############

addUBDTBranchRun2:

# Executables (w/ debug symbols)
uBoostTrain.dbg:


####################
# General patterns #
####################

%.dbg: %.cpp
	$(COMPILER) $(CXXFLAGS) $(ADDCXXFLAGS) -o $(BINPATH)/$@ $< $(LINKFLAGS) $(ADDLINKFLAGS)

%: %.cpp
	$(COMPILER) $(CXXFLAGS) -o $(BINPATH)/$@ $< $(LINKFLAGS) $(ADDLINKFLAGS)
