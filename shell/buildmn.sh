#!/bin/bash
sudo mn --custom ~/sdn/sflow-rt/extras/sflow.py --custom topo.py --topo=mytopo --controller=remote,ip=127.0.0.1,port=6633 --switch ovsk,protocols=OpenFlow13
