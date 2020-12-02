import requests
from requests.auth import HTTPBasicAuth


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


if __name__ == "__main__":
    flow = FlowManager('openflow:3', '0', '1')
    print(flow.get())
    print(flow.delete())
    # url = 'http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:1/flow-node-inventory:table/0/flow/1'
