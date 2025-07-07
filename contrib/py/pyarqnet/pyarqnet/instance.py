#!/usr/bin/env python3
#
# arqnet runtime wrapper
#

from ctypes import *
import configparser
import signal
import time
import threading
import os
import sys
import requests

from pyarqnet import rc

lib_file = os.path.join(os.path.realpath('.'), 'libarqnet-shared.so')


def log(msg):
    sys.stderr.write("arqnet: {}\n".format(msg))
    sys.stderr.flush()


class ArqNET(threading.Thread):

    lib = None
    ctx = 0
    failed = False
    up = False

    asRouter = True

    def configure(self, lib, conf, ip=None, port=None, ifname=None, seedfile=None, arqmad_host=None, arqmad_port=None):
        log("configure lib={} conf={}".format(lib, conf))
        if not os.path.exists(os.path.dirname(conf)):
            os.mkdir(os.path.dirname(conf))
        try:
            self.lib = CDLL(lib)
        except OSError as ex:
            log("failed to load library: {}".format(ex))
            return False
        if self.lib.llarp_ensure_config(conf.encode('utf-8'), os.path.dirname(conf).encode('utf-8'), True, self.asRouter):
            config = configparser.ConfigParser()
            config.read(conf)
            log('overwrite ip="{}" port="{}" ifname="{}" seedfile="{}" arqmad=("{}", "{}")'.format(
                ip, port, ifname, seedfile, arqmad_host, arqmad_port))
            if seedfile and arqmad_host and arqmad_port:
                if not os.path.exists(seedfile):
                    log('cannot access service node seed at "{}"'.format(seedfile))
                    return False
                config['arqmad'] = {
                    'service-node-seed': seedfile,
                    'enabled': "true",
                    'jsonrpc': "{}:{}".format(arqmad_host, arqmad_port)
                }
            if ip:
                config['router']['public-address'] = '{}'.format(ip)
            if port:
                config['router']['public-port'] = '{}'.format(port)
            if ifname and port:
                config['bind'] = {
                    ifname: '{}'.format(port)
                }
            with open(conf, "w") as f:
                config.write(f)
            self.ctx = self.lib.llarp_main_init(conf.encode('utf-8'))
        else:
            return False
        return self.lib.llarp_main_setup(self.ctx, False) == 0

    def inform_fail(self):
        """
        inform arqnet crashed
        """
        self.failed = True
        self._inform()

    def inform_up(self):
        self.up = True
        self._inform()

    def _inform(self):
        """
        inform waiter
        """

    def wait_for_up(self, timeout):
        """
        wait for arqnet to go up for :timeout: seconds
        :return True if we are up and running otherwise False:
        """
        # return self._up.wait(timeout)

    def signal(self, sig):
        if self.ctx and self.lib:
            self.lib.llarp_main_signal(self.ctx, int(sig))

    def run(self):
        # self._up.acquire()
        self.up = True
        code = self.lib.llarp_main_run(self.ctx)
        log("llarp_main_run exited with status {}".format(code))
        if code:
            self.inform_fail()
        self.up = False
        # self._up.release()

    def close(self):
        if self.lib and self.ctx:
            self.lib.llarp_main_free(self.ctx)


def getconf(name, fallback=None):
    return name in os.environ and os.environ[name] or fallback


def run_main(args):
    seedfile = getconf("ARQMA_SEED_FILE")
    if seedfile is None:
        print("ARQMA_SEED_FILE was not set")
        return

    arqmad_host = getconf("ARQMA_RPC_HOST", "127.0.0.1")
    arqmad_port = getconf("ARQMA_RPC_PORT", "19994")

    root = getconf("ARQNET_ROOT")
    if root is None:
        print("ARQNET_ROOT was not set")
        return

    rc_callback = getconf("ARQNET_SUBMIT_URL")
    if rc_callback is None:
        print("ARQNET_SUBMIT_URL was not set")
        return

    bootstrap = getconf("ARQNET_BOOTSTRAP_URL")
    if bootstrap is None:
        print("ARQNET_BOOTSTRAP_URL was not set")

    lib = getconf("ARQNET_LIB", lib_file)
    if not os.path.exists(lib):
        lib = "libarqnet-shared.so"
    timeout = int(getconf("ARQNET_TIMEOUT", "5"))
    ping_interval = int(getconf("ARQNET_PING_INTERVAL", "60"))
    ping_callback = getconf("ARQNET_PING_URL")
    ip = getconf("ARQNET_IP")
    port = getconf("ARQNET_PORT")
    ifname = getconf("ARQNET_IFNAME")
    if ping_callback is None:
        print("ARQNET_PING_URL was not set")
        return
    conf = os.path.join(root, "daemon.ini")
    log("going up")
    arqma = ArqNET()
    log("bootstrapping...")
    try:
        r = requests.get(bootstrap)
        if r.status_code == 404:
            log("bootstrap gave no RCs, we are probably the seed node")
        elif r.status_code != 200:
            raise Exception("http {}".format(r.status_code))
        else:
            data = r.content
            if rc.validate(data):
                log("valid RC obtained")
                with open(os.path.join(root, "bootstrap.signed"), "wb") as f:
                    f.write(data)
            else:
                raise Exception("invalid RC")
    except Exception as ex:
        log("failed to bootstrap: {}".format(ex))
        arqma.close()
        return
    if arqma.configure(lib, conf, ip, port, ifname, seedfile, arqmad_host, arqmad_port):
        log("configured")

        arqma.start()
        try:
            log("waiting for spawn")
            while timeout > 0:
                time.sleep(1)
                if arqma.failed:
                    log("failed")
                    break
                log("waiting {}".format(timeout))
                timeout -= 1
            if arqma.up:
                log("submitting rc")
                try:
                    with open(os.path.join(root, 'self.signed'), 'rb') as f:
                        r = requests.put(rc_callback, data=f.read(), headers={
                                         "content-type": "application/octect-stream"})
                        log('submit rc reply: HTTP {}'.format(r.status_code))
                except Exception as ex:
                    log("failed to submit rc: {}".format(ex))
                    arqma.signal(signal.SIGINT)
                    time.sleep(2)
                else:
                    while arqma.up:
                        time.sleep(ping_interval)
                        try:
                            r = requests.get(ping_callback)
                            log("ping reply: HTTP {}".format(r.status_code))
                        except Exception as ex:
                            log("failed to submit ping: {}".format(ex))
            else:
                log("failed to go up")
                arqma.signal(signal.SIGINT)
        except KeyboardInterrupt:
            arqma.signal(signal.SIGINT)
            time.sleep(2)
        finally:
            arqma.close()
    else:
        arqma.close()


def main():
    run_main(sys.argv[1:])


if __name__ == "__main__":
    main()
