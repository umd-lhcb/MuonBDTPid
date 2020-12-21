#!/bin/bash

case $3 in
    debug)
        lb-run Castelao/latest gaudirun.py ./reco_pp.py $1 \
            --option="from Configurables import DaVinci; DaVinci().EvtMax = 5000"
        ;;

    *)
        lb-run Castelao/latest gaudirun.py ./reco_pp.py $1
        ;;
esac
