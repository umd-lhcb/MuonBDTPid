# Author: Yipeng Sun
# Last Change: Sun Jul 04, 2021 at 03:48 AM +0200

# Compiler settings
COMPILER	:=	$(shell root-config --cxx)
CXXFLAGS	:=	$(shell root-config --cflags)
LINKFLAGS	:=	$(shell root-config --libs)
ADDCXXFLAGS	:=	-O2
ADDLINKFLAGS	:=	-lTreePlayer -lMinuit -lFoam -lXMLIO -lTMVA

addUBDTBranchRun2:

%: %.cpp
	$(COMPILER) $(ADDCXXFLAGS) $(CXXFLAGS) -o $@ $< $(LINKFLAGS) $(ADDLINKFLAGS)
