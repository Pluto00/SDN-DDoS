#!/usr/bin/env python
# coding=utf-8
from mininet.topo import Topo


class MyTopo(Topo):

    def __init__(self):
        # 初始化
        Topo.__init__(self)

        # 定义主机和交换机
        host1 = self.addHost('h1')
        host2 = self.addHost('h2')
        host3 = self.addHost('h3')
        host4 = self.addHost('h4')
        host5 = self.addHost('h5')

        switch1 = self.addSwitch('s1')
        switch2 = self.addSwitch('s2')
        switch3 = self.addSwitch('s3')
        switch4 = self.addSwitch('s4')

        # 设置通路
        self.addLink(host1, switch1)
        self.addLink(host2, switch2)

        self.addLink(switch1, switch3)
        self.addLink(switch2, switch3)
        self.addLink(switch3, switch4)

        self.addLink(switch4, host3)
        self.addLink(switch4, host4)
        self.addLink(switch4, host5)


topos = {'mytopo': (lambda: MyTopo())}
