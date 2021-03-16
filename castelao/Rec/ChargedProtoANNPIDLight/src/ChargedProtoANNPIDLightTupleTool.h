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
#ifndef CHARGEDPROTOANNPIDLIGHTTUPLETOOL_H
#define CHARGEDPROTOANNPIDLIGHTTUPLETOOL_H 1

// STL
#include <memory>
#include <unordered_map>

// base class
#include "ChargedProtoANNPIDToolBase.h"

// interfaces
#include "MCInterfaces/IRichRecMCTruthTool.h"
#include "RecInterfaces/IChargedProtoANNPIDTupleTool.h"

// Event
#include "Event/MCParticle.h"

namespace ANNGlobalPID {

  /** @class ChargedProtoANNPIDTupleTool ChargedProtoANNPIDTupleTool.h
   *
   *  Tool to fill the ANN PID variables into a tuple
   *
   *  @author Chris Jones   Christopher.Rob.Jones@cern.ch
   *  @date   2011-02-04
   */

  class ChargedProtoANNPIDLightTupleTool final : public ChargedProtoANNPIDToolBase,
                                                 virtual public IChargedProtoANNPIDTupleTool {

  public:
    /// Standard constructor
    ChargedProtoANNPIDLightTupleTool(const std::string& type, const std::string& name, const IInterface* parent );

    /// Destructor
    virtual ~ChargedProtoANNPIDLightTupleTool() = default;

    StatusCode initialize() override; ///< Algorithm initialization

  public:
    // Fill the tuple tool with information for the given ProtoParticle
    StatusCode fill( Tuples::Tuple& tuple, const LHCb::ProtoParticle* proto,
                     const LHCb::ParticleID pid = LHCb::ParticleID() ) const override;

  private:
    StringInputs m_variables; ///< ProtoParticle variables as strings to add to the ntuple

    /// Use RICH tool to get MCParticle associations for Tracks (To avoid annoying Linkers)
    const Rich::Rec::MC::IMCTruthTool* m_truth = nullptr;

    /// map of accessor objects for each variable by name
    typedef std::unordered_map<std::string, ChargedProtoANNPIDToolBase::Input::SmartPtr> Inputs;
    // variables to fill
    Inputs m_inputs;
  };

} // namespace ANNGlobalPID

#endif // CHARGEDPROTOANNPIDLIGHTTUPLETOOL_H
