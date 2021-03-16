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
#ifndef _TupleToolANNPIDTrainingLight_H
#define _TupleToolANNPIDTrainingLight_H 1

// Base class
#include "DecayTreeTupleBase/TupleToolBase.h"

// Interfaces
#include "Kernel/IParticleTupleTool.h"
#include "RecInterfaces/IChargedProtoANNPIDTupleTool.h"

//============================================================================

class TupleToolANNPIDTrainingLight : public TupleToolBase, virtual public IParticleTupleTool {

public:
  // Standard constructor
  TupleToolANNPIDTrainingLight( const std::string& type, const std::string& name, const IInterface* parent );

  ~TupleToolANNPIDTrainingLight() {}

  StatusCode initialize() override; ///< Initialise

public:
  StatusCode fill( const LHCb::Particle*, const LHCb::Particle*, const std::string&, Tuples::Tuple& ) override;

private:
  /// Pointer to the ANNPID tuple tool
  const ANNGlobalPID::IChargedProtoANNPIDTupleTool* m_tuple;
};

#endif // _TupleToolANNPIDTrainingLight_H
