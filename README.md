## 第一步：搭建网络拓扑结构

1. 启动 odl 控制器 `./distribution-karaf-0.6.4-Carbon/bin/karaf`
2. 启动 mininet `sudo mn  --custom topo.py --topo=mytopo --controller=remote,ip=127.0.0.1,port=6633 --switch ovsk,protocols=OpenFlow13`
3. 检测网络拓扑连通性 `pingall`

## 第二步：运行检测系统

1. 运行检测系统 `app.py` 文件 `python app.py`
2. 点击 `START` 按钮开始检测
3. 查看系统输出

## 第三步：模拟攻击

1. 使用 `h3 hping3 h1 -i u400 -p 80 -S` 模拟攻击
2. 可以看到系统检测到了攻击并开始下发流表进行防御
3. 网络流量恢复正常
4. 使用 `pingall` 验证是否防御成功
5. 如果看到 h3 和 h1 无法 ping 通则说明防御成功（下发流表拦截掉了 h3 的包）


### 演示结束，谢谢观看！！

