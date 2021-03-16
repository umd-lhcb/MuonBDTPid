/*****************************************************************************\
* (c) Copyright 2000-2018 CERN for the benefit of the LHCb Collaboration      *
*                                                                             *
* This software is distributed under the terms of the GNU General Public      *
* Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   *
*                                                                             *
* In applying this licence, CERN does not waive the privileges and immunities *
* granted to it by virtue of its status as an Intergovernmental Organization  *
* or submit itself to any jurisdiction.                                       *
\*****************************************************************************/
// $Id: $

#include "TupleToolANNPIDTrainingLight.h"

//-----------------------------------------------------------------------------
// Implementation file for class : TupleToolANNPIDTrainingLight
//-----------------------------------------------------------------------------

// Declaration of the Tool Factory
DECLARE_COMPONENT( TupleToolANNPIDTrainingLight )

//=============================================================================
// Standard constructor, initializes variables
//=============================================================================
TupleToolANNPIDTrainingLight::TupleToolANNPIDTrainingLight( const std::string& type, const std::string& name,
                                                            const IInterface* parent )
    : TupleToolBase( type, name, parent ), m_tuple( NULL ) {
  declareInterface<IParticleTupleTool>( this );
}

//=============================================================================

StatusCode TupleToolANNPIDTrainingLight::initialize() {
  const StatusCode sc = TupleToolBase::initialize();
  if ( sc.isFailure() ) return sc;

  m_tuple =
      tool<ANNGlobalPID::IChargedProtoANNPIDTupleTool>( "ANNGlobalPID::ChargedProtoANNPIDLightTupleTool", "Tuple", this );

  return sc;
}

//=============================================================================

StatusCode TupleToolANNPIDTrainingLight::fill( const LHCb::Particle*, const LHCb::Particle* P, const std::string& /* head */
                                               ,
                                               Tuples::Tuple& tuple ) {
  // const std::string prefix = fullName(head);

  // Fill the ANNPID variables
  // Note, prefix is not used here, so can only use this tool on a single particle at a time...
  return m_tuple->fill( tuple, P );
}
