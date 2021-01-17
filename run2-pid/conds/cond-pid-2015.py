from Configurables import DaVinci

DaVinci().DataType = "2015"


from Configurables import SWeightsTableFiles

SWeightsTableFiles(
    sTableMagUpFile="./splots/splot_tables-2015-mu.root",
    sTableMagDownFile="./splots/splot_tables-2015-mu.root"
)


from GaudiConf import IOHelper

IOHelper().inputFiles([
    './data/data-2015-mu/00050412_00000001_4.fullturbo.dst',
    './data/data-2015-mu/00050412_00000002_4.fullturbo.dst',
], clear=True)
