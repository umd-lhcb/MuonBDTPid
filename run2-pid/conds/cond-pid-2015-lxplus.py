from Configurables import DaVinci

DaVinci().DataType = "2015"
DaVinci().EvtMax = -1
DaVinci().TupleFile = "pid.root"


# from Configurables import SWeightsTableFiles
# import os
#
# SWeightsTableFiles(
#     sTableMagUpFile=os.environ["PIDCALIBROOT"] + "/sTables/sPlotTables-2015MagUp.root",
#     sTableMagDownFile=os.environ["PIDCALIBROOT"]
#     + "/sTables/sPlotTables-2015MagDown.root",
# )

from GaudiConf import IOHelper


IOHelper().inputFiles([
    '/afs/cern.ch/user/s/suny/eos/run2-pid/data-2015-mu/00050412_00000001_4.fullturbo.dst',
    '/afs/cern.ch/user/s/suny/eos/run2-pid/data-2015-mu/00050412_00000002_4.fullturbo.dst',
], clear=True)
