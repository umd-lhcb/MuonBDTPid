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
    './data/data-2015/00050412_00000025_4.fullturbo.dst',
    './data/data-2015/00050412_00000026_4.fullturbo.dst',
], clear=True)
