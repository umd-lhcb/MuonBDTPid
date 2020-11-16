# Author: Yipeng Sun
# Last Change: Mon Nov 16, 2020 at 01:53 AM +0100

BINPATH	:=	bin
VPATH	:=	$(BINPATH)

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

# General patterns
%: %.cpp
	$(COMPILER) $(CXXFLAGS) -o $(BINPATH)/$@ $< $(LINKFLAGS) $(ADDLINKFLAGS)
