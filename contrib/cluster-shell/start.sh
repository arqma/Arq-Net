#!/bin/bash
set +x
cd arq1
nohup ./arqnet1 $PWD/arqnet.ini &
# seed node needs some time to write RC to make sure it's not expired on load for the rest
sleep 1
cd ../arq2
nohup ./arqnet2 $PWD/arqnet.ini &
cd ../arq3
nohup ./arqnet3 $PWD/arqnet.ini &
cd ../arq4
nohup ./arqnet4 $PWD/arqnet.ini &
cd ../arq5
nohup ./arqnet5 $PWD/arqnet.ini &
cd ..
tail -f arq*/nohup.out
