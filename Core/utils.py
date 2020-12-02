import time
import subprocess
import requests
from requests.auth import HTTPBasicAuth


class TcpDumpUtils:

    def __init__(self, interface='any', outFile='data.pcap'):
        self.__cmd = ['tcpdump', '-i', interface, '-s', '0', '-w', outFile]

    def start(self):
        self.__tcpprocess = subprocess.Popen(self.__cmd)

    def stop(self):
        self.__tcpprocess.kill()

    def startWithTime(self, passtime=5):
        self.start()
        time.sleep(passtime)
        self.stop()


class FlowManager:
    def __init__(self, nodeId, tableId, flowId):
        self.__headers = {'Content-Type': 'application/json'}
        self.__auth = HTTPBasicAuth('admin', 'admin')
        self.setUrl(nodeId, tableId, flowId)

    def setUrl(self, nodeId, tableId, flowId):
        self.__nodeId = nodeId
        self.__tableId = tableId
        self.__flowId = flowId
        self.__url = f'http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/{nodeId}/flow-node-inventory:table/{tableId}/flow/{flowId}'
        self.__genUrl = f'http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/{nodeId}/flow-node-inventory:table/{tableId}'

    def put(self, data, flowId=None):
        if flowId is not None:
            self.setUrl(self.__nodeId, self.__tableId, flowId)
        return requests.put(
            self.__url,
            data,
            headers=self.__headers,
            auth=self.__auth
        ).content

    def get(self):
        return requests.get(
            self.__genUrl,
            headers=self.__headers,
            auth=self.__auth
        ).content

    def delete(self):
        return requests.delete(
            self.__genUrl,
            headers=self.__headers,
            auth=self.__auth
        ).content

    def post(self, data):
        return requests.post(
            self.__url,
            data,
            headers=self.__headers,
            auth=self.__auth
        ).content
