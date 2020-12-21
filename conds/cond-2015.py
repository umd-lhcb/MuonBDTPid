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
