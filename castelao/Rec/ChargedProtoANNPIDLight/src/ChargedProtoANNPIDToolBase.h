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

//-----------------------------------------------------------------------------
/** @file ChargedProtoANNPIDToolBase.h
 *
 * Header file for algorithm ChargedProtoANNPIDToolBase
 *
 * @author Chris Jones   Christopher.Rob.Jones@cern.ch
 * @date 2010-03-09
 */
//-----------------------------------------------------------------------------

#ifndef ChargedProtoANNPID_ChargedProtoANNPIDToolBase_H
#define ChargedProtoANNPID_ChargedProtoANNPIDToolBase_H 1

// from Gaudi
#include "GaudiAlg/GaudiTupleTool.h"

// local
#include "ChargedProtoANNPIDCommonBase.h"

namespace ANNGlobalPID {

  //-----------------------------------------------------------------------------
  /** @class ChargedProtoANNPIDToolBase ChargedProtoANNPIDToolBase.h
   *
   *  Base class for all ProtoParticle ANN based PID algorithms
   *
   *  @author Chris Jones   Christopher.Rob.Jones@cern.ch
   *  @date   2010-03-09
   */
  //-----------------------------------------------------------------------------

  class ChargedProtoANNPIDToolBase : public ANNGlobalPID::ChargedProtoANNPIDCommonBase<GaudiTupleTool> {

  public:
    /// Standard constructor
    ChargedProtoANNPIDToolBase( const std::string& type, const std::string& name, const IInterface* parent )
        : ANNGlobalPID::ChargedProtoANNPIDCommonBase<GaudiTupleTool>( type, name, parent ) {}
  };

} // namespace ANNGlobalPID

#endif // ChargedProtoANNPID_ChargedProtoANNPIDToolBase_H
