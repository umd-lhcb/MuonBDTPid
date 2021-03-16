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

// local
#include "ChargedProtoANNPIDLightTupleTool.h"

//-----------------------------------------------------------------------------
// Implementation file for class : ChargedProtoANNPIDTupleTool
//
// 2011-02-04 : Chris Jones
//-----------------------------------------------------------------------------

using namespace ANNGlobalPID;

// Declaration of the Tool Factory
DECLARE_COMPONENT( ChargedProtoANNPIDLightTupleTool )

//=============================================================================
// Standard constructor, initializes variables
//=============================================================================
ChargedProtoANNPIDLightTupleTool::ChargedProtoANNPIDLightTupleTool( const std::string& type, const std::string& name,
                                                                    const IInterface* parent )
    : ChargedProtoANNPIDToolBase( type, name, parent ) {

  // interface
  declareInterface<IChargedProtoANNPIDTupleTool>( this );

  // Job options
  declareProperty(
      "Variables",
      m_variables = {
          // Tracking
          "TrackP", "TrackPt",
          "TrackChi2PerDof", "TrackNumDof", "TrackLikelihood",
          "TrackGhostProbability", "TrackFitMatchChi2", "TrackFitVeloChi2",
          "TrackFitVeloNDoF", "TrackFitTChi2", "TrackFitTNDoF",
          // RICH
          "RichUsedAero", "RichUsedR1Gas", "RichUsedR2Gas", "RichAboveMuThres",
          "RichAboveKaThres", "RichDLLe", "RichDLLmu", "RichDLLk",
          "RichDLLp", "RichDLLbt",
          // MUON
          "MuonMuLL", "MuonBkgLL", "MuonNShared",
          // ECAL
          "InAccEcal", "EcalPIDe", "EcalPIDmu",
          // HCAL
          "InAccHcal", "HcalPIDe", "HcalPIDmu",
          // PRS
          "InAccPrs", "PrsPIDe",
          // SPD
          // BREM
          "InAccBrem", "BremPIDe",
          // VELO
          "VeloCharge"} );

  // Turn off Tuple printing during finalize
  setProperty( "NTuplePrint", false ).ignore( /* AUTOMATICALLY ADDED FOR gaudi/Gaudi!763 */ );
}

//=============================================================================
// Initialization
//=============================================================================
StatusCode ChargedProtoANNPIDLightTupleTool::initialize() {
  const StatusCode sc = ChargedProtoANNPIDToolBase::initialize();
  if ( sc.isFailure() ) return sc;

  // get tools
  m_truth = tool<Rich::Rec::MC::IMCTruthTool>( "Rich::Rec::MC::MCTruthTool", "MCTruth", this );

  // Get a vector of input accessor objects for the configured variables
  for ( const auto& i : m_variables ) { m_inputs[i] = getInput( i ); }

  // return
  return sc;
}

//=============================================================================

StatusCode ChargedProtoANNPIDLightTupleTool::fill(Tuples::Tuple& tuple, const LHCb::ProtoParticle* proto,
                                                  const LHCb::ParticleID pid ) const {
  StatusCode sc = StatusCode::SUCCESS;

  // Get track
  const auto* track = proto->track();
  if ( !track ) return Error( "ProtoParticle is neutral!" );

  // Loop over reconstruction variables
  for ( const auto& i : m_inputs ) {
    // get the variable and fill ntuple
    if ( sc ) sc = tuple->column( i.first, (float)i.second->value( proto ) );
  }

  // PID info
  if ( sc ) sc = tuple->column( "RecoPIDcode", pid.pid() );

  // return
  return sc;
}
