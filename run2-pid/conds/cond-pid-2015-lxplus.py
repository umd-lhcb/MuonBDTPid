from GaudiConf import IOHelper
from os import environ

HOME = environ['HOME']
IOHelper().inputFiles([
    HOME+'/eos/run2-pid/data-2015-mu/00050412_00000001_4.fullturbo.dst',
    HOME+'/eos/run2-pid/data-2015-mu/00050412_00000002_4.fullturbo.dst',
], clear=True)
