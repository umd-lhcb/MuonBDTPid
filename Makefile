# Author: Yipeng Sun
# Last Change: Mon Dec 21, 2020 at 03:07 AM +0100

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

CASTELAO_VERSION=Castelao-v10r0

# Executables
AddUboostBranchRun2:

uBoostTrain.dbg:

# Helpers
.PHONY: clean
clean:
	@rm -rf $(BINPATH)/*

# Castelao docker image
.PHONY: docker-cl

ifeq ($(OS),Darwin)
CL_CMD = "docker run --rm -it -v $(PWD):/data -e UID=$$(id -u) -e GID=$$(id -g) --net=host umdlhcb/lhcb-stack-cc7:${CASTELAO_VERSION}"
else
CL_CMD = "docker run --rm -it -v $(PWD):/data -v $$HOME/.Xauthority:/home/physicist/.Xauthority -e DISPLAY -e UID=$$(id -u) -e GID=$$(id -g) --net=host umdlhcb/lhcb-stack-cc7:${CASTELAO_VERSION}"
endif

docker-cl:
	@eval $(CL_CMD)

# General patterns
%.dbg: %.cpp
	$(COMPILER) $(CXXFLAGS) $(ADDCXXFLAGS) -o $(BINPATH)/$@ $< $(LINKFLAGS) $(ADDLINKFLAGS)

%: %.cpp
	$(COMPILER) $(CXXFLAGS) -o $(BINPATH)/$@ $< $(LINKFLAGS) $(ADDLINKFLAGS)
