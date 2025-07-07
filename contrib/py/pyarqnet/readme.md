# pyarqnet

arqnet with python 3

    # python3 setup.py install

## bootserv

bootserv is a bootstrap server for accepting and serving RCs

    $ gunicorn -b 0.0.0.0:8000 pyarqnet.bootserv:app

## pyarqnet instance

obtain `libarqnet-shared.so` from a arqnet build

run (root):
    
    # export ARQNET_ROOT=/tmp/arqnet-instance/
    # export ARQNET_LIB=/path/to/libarqnet-shared.so
    # export ARQNET_BOOTSTRAP_URL=http://bootserv.ip.address.here:8000/bootstrap.signed
    # export ARQNET_PING_URL=http://bootserv.ip.address.here:8000/ping
    # export ARQNET_SUBMIT_URL=http://bootserv.ip.address.here:8000/
    # export ARQNET_IP=public.ip.goes.here
    # export ARQNET_PORT=1090
    # export ARQNET_IFNAME=eth0
    # python3 -m pyarqnet