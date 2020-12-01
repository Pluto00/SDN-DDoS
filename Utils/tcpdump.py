#!/usr/bin/env python
# coding=utf-8
import time
import subprocess


class TcpDumpUtils:

    def __init__(self, interface='any', outFile='data.pcap'):
        self.__interface = interface
        self.__outFile = outFile
        self.__cmd = ['tcpdump', '-i', self.__interface, '-s', '0', '-w', self.__outFile]

    def start(self):
        self.__tcpprocess = subprocess.Popen(self.__cmd)

    def stop(self):
        self.__tcpprocess.kill()

    def startWithTime(self, passtime=None):
        self.start()
        if passtime is None:
            passtime = self.interval
        time.sleep(passtime)
        self.stop()
