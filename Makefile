# Author: Yipeng Sun
# Last Change: Mon Nov 16, 2020 at 01:55 AM +0100

BINPATH	:=	bin
VPATH	:=	$(BINPATH)
VPATH	:=	src:$(VPATH)

export PATH	:=	$(BINPATH):$(PATH)

# Compiler settings
COMPILER	:=	$(shell root-config --cxx)
CXXFLAGS	:=	$(shell root-config --cflags)
LINKFLAGS	:=	$(shell root-config --libs)
ADDLINKFLAGS	:=	-lTreePlayer -lMinuit -lFoam -lXMLIO -lTMVA
# Current nix root5 derivation doesn't have RooFit library.
#ADDLINKFLAGS	:=	-lTreePlayer -lRooFitCore -lRooFit -lMinuit -lFoam -lXMLIO -lTMVA

# Executables
AddUboostBranchRun2:

# Helpers
.PHONY: clean
clean:
	@rm -rf $(BINPATH)/*

# General patterns
%: %.cpp
	$(COMPILER) $(CXXFLAGS) -o $(BINPATH)/$@ $< $(LINKFLAGS) $(ADDLINKFLAGS)
