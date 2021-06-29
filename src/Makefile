# Author: Yipeng Sun
# Last Change: Tue Jun 29, 2021 at 03:38 PM +0200

# Compiler settings
COMPILER	:=	$(shell root-config --cxx)
CXXFLAGS	:=	$(shell root-config --cflags)
LINKFLAGS	:=	$(shell root-config --libs)
ADDCXXFLAGS	:=	-g -O1
ADDLINKFLAGS	:=	-lTreePlayer -lMinuit -lFoam -lXMLIO -lTMVA

addUBDTBranchRun2:

%: %.cpp
	$(COMPILER) -std=c++11 $(CXXFLAGS) -o $@ $< $(LINKFLAGS) $(ADDLINKFLAGS)
