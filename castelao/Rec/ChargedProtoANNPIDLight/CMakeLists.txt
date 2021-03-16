###############################################################################
# (c) Copyright 2000-2019 CERN for the benefit of the LHCb Collaboration      #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
# Package: ChargedProtoANNPIDLight
###############################################################################
gaudi_subdir(ChargedProtoANNPIDLight v1r0)

gaudi_depends_on_subdirs(Event/MCEvent
                         Event/PhysEvent
                         Event/RecEvent
                         GaudiAlg
                         Rec/RecInterfaces)

find_package(ROOT)
find_package(VDT)

find_package(Boost)
include_directories(SYSTEM ${Boost_INCLUDE_DIRS} ${ROOT_INCLUDE_DIRS})

gaudi_add_module(ChargedProtoANNPIDLight
                 src/*.cpp
                 INCLUDE_DIRS ROOT VDT Rec/RecInterfaces
                 LINK_LIBRARIES ROOT VDT MCEvent PhysEvent RecEvent GaudiAlgLib)
