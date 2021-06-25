# Author: Yipeng Sun
# Last Change: Fri Jun 25, 2021 at 05:27 AM +0200

# Compiler settings
COMPILER	:=	$(shell root-config --cxx)
CXXFLAGS	:=	$(shell root-config --cflags)
LINKFLAGS	:=	$(shell root-config --libs)
ADDCXXFLAGS	:=	-g -O1
ADDLINKFLAGS	:=	-lTreePlayer -lMinuit -lFoam -lXMLIO -lTMVA

addUBDTBranchRun2:

%: %.cpp
	$(COMPILER) $(CXXFLAGS) -o $@ $< $(LINKFLAGS) $(ADDLINKFLAGS)
