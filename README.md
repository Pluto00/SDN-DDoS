## 第一步：搭建网络拓扑结构

1. 启动old控制器
2. 启动sflow-rt
3. 启动mininet

## 第二步：运行检测文件

运行 `main.py` 文件

## 第三步：模拟攻击

1. 使用 `h3 hping3 h1 -i u400 -p 80 -S` 模拟 ddos 攻击
2. 查看检测文件输出和 sflow webui 的流量统计，验证是否防御成功。