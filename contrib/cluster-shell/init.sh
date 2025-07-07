#!/bin/sh
# copy a arqnet binary into this cluster
cp ../../arqnet .
# generate default config file
./arqnet -g -r arqnet.ini
# make seed node
./makenode.sh 1
# establish bootstrap
ln -s arq1/self.signed bootstrap.signed
