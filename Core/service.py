import os
import json
import time
from Core.utils import TcpDumpUtils
from Core.utils import FlowManager
from copy import deepcopy
from Model import FusionModel, Dataset
from PyQt5.QtCore import QThread, pyqtSignal, QObject


class WorkThread(QThread, QObject):
    (NORMAL, WARNING, DANGEROUS) = (5, 2, 1)
    ATTACK = 'syn'
    trigger = pyqtSignal(dict)

    def __init__(self, interface='s3-eth1', datafile='./tmp/data.pcap'):
        super(WorkThread, self).__init__()
        self.model = FusionModel(pre_path="./Model/")
        self.__state = WorkThread.NORMAL
        self.__tdu = TcpDumpUtils(interface, datafile)
        self.__flow = FlowManager('openflow:3', '0', '1')
        self.__dataFile = os.path.abspath(datafile)
        self.__FeatureFile = os.path.abspath(datafile + '_Flow.csv')
        self.__dataDir = os.path.abspath('./tmp/')
        self.__dropData = json.load(open('drop.json'))
        self.__attackIp = []
        self.__flow.delete()

    def __send(self, text, type='info'):
        current = time.strftime("[%H:%M:%S] ", time.localtime())
        if type == 'info':
            text = "SYSTEM: " + str(text)
        msg = {'type': type, 'text': current + str(text) + '\n'}
        self.trigger.emit(msg)

    def _predict(self, x):
        try:
            pred_Y = self.model.predict(x)
        except ValueError:
            return []
        return pred_Y

    def __toggleState(self, change=False):
        if change:
            if self.__state == WorkThread.NORMAL:
                self.__state = WorkThread.WARNING
            elif self.__state == WorkThread.WARNING:
                self.__state = WorkThread.DANGEROUS
        else:
            self.__state = WorkThread.NORMAL

    def run(self):
        while True:
            self.__tdu.startWithTime(self.__state)
            os.system(f"sudo ./static/cic.sh {self.__dataFile} {self.__dataDir}")
            try:
                data = Dataset([self.__FeatureFile, ])
                X = data.getX()
                if X.shape[0] > 10:
                    Y = self._predict(X)
                    data.setLabel(Y)
                    self.__toggleState(WorkThread.ATTACK in Y)
                    self.__attackIp = data.getSrcIp(WorkThread.ATTACK)
            except FileNotFoundError:
                self.__toggleState()

            if self.__state == WorkThread.NORMAL:
                self.__send("NETWORK OK")
                self.__attackIp = []
            else:
                if self.__state == WorkThread.WARNING:
                    self.__send("DDOS ATTACK DETECTED")
                    self.__send("START DEEP INSPECTION")
                else:
                    self.__send("START DEFENSE")
                    self.__send("START SEND FLOW TABLE")
                    for ip in self.__attackIp:
                        self.__send(ip, 'attack')
                        flowId = sum(list(map(int, ip.split('.'))))
                        data = deepcopy(self.__dropData)
                        data['flow'][0]['match']['ipv4-source'] = ip + '/32'
                        data['flow'][0]['id'] = flowId
                        data['flow'][0]['flow-name'] = 'drop' + ip
                        data['flow'][0]['cookie'] = flowId
                        print("HANDLER: send flow data ---> " + str(data))
                        print("RESPONSE: " + str(self.__flow.put(str(data), flowId)))
                    self.__send("SEND COMPELETE")
                    self.__send("DEFENSE SUCCESS")
                print("FLOW TABLE GET:" + str(self.__flow.get()))


if __name__ == '__main__':
    WorkThread = WorkThread('s3-eth1')
    WorkThread.run()
