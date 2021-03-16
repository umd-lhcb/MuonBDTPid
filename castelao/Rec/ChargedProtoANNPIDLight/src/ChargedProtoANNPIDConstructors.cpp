/*****************************************************************************\
* (c) Copyright 2000-2019 CERN for the benefit of the LHCb Collaboration      *
*                                                                             *
* This software is distributed under the terms of the GNU General Public      *
* Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   *
*                                                                             *
* In applying this licence, CERN does not waive the privileges and immunities *
* granted to it by virtue of its status as an Intergovernmental Organization  *
* or submit itself to any jurisdiction.                                       *
\*****************************************************************************/

#include "ChargedProtoANNPIDCommonBase.h"

// from Gaudi
#include "GaudiAlg/GaudiTupleAlg.h"
#include "GaudiAlg/GaudiTupleTool.h"

namespace ANNGlobalPID {
  //=============================================================================
  // Implementation for GaudiTupleTool
  //=============================================================================

  template <>
  ChargedProtoANNPIDCommonBase<GaudiTupleTool>::ChargedProtoANNPIDCommonBase( const std::string& type,
                                                                              const std::string& name,
                                                                              const IInterface*  parent )
      : GaudiTupleTool( type, name, parent ) {
    this->initCommonConstructor();
  }

  template <>
  ChargedProtoANNPIDCommonBase<GaudiTupleTool>::ChargedProtoANNPIDCommonBase( const std::string& /* name */,
                                                                              ISvcLocator* /* pSvcLocator */ )
      : GaudiTupleTool( "ERROR", "ERROR", nullptr ) {
    throw GaudiException( "Invalid ChargedProtoANNPIDCommonBase<GaudiTupleTool> constructor",
                          "ANNGlobalPID::ChargedProtoANNPIDBase", StatusCode::FAILURE );
  }

} // namespace ANNGlobalPID
