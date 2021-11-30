# Author: Yipeng Sun
# Last Change: Tue Nov 30, 2021 at 04:06 PM +0100

# Compiler settings
COMPILER	:=	$(shell root-config --cxx)
CXXFLAGS	:=	$(shell root-config --cflags)
LINKFLAGS	:=	$(shell root-config --libs)
ADDCXXFLAGS	:=	-O2
ADDLINKFLAGS	:=	-lTreePlayer -lMinuit -lFoam -lXMLIO -lTMVA

bin: addUBDTBranchRun2 addUBDTBranchRun2PidCalib

addUBDTBranchRun2:

addUBDTBranchRun2PidCalib: addUBDTBranchRun2.cpp
	$(COMPILER) $(CXXFLAGS) -DPIDCALIB -o $@ $< $(LINKFLAGS) $(ADDLINKFLAGS)

%: %.cpp
	$(COMPILER) $(CXXFLAGS) $(ADDCXXFLAGS) -o $@ $< $(LINKFLAGS) $(ADDLINKFLAGS)
