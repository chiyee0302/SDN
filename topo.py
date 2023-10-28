from mininet.net import Mininet
from flask import Flask, render_template, jsonify
from mininet.topo import Topo
import json

class ryu_topo(Topo):
    def __init__(self):
        Topo.__init__(self)
        self.addSwitch("s1")
        self.addSwitch("s2")
        self.addHost("h1")
        self.addHost("h2")
        self.addHost("h3")
        self.addHost("h4")
        self.addLink("s1", "h1")
        self.addLink("s1", "h2")
        self.addLink("s2", "h3")
        self.addLink("s2", "h4")
        self.addLink("s1", "s2")

app = Flask(__name__)

@app.route('/')
def index():
    # 创建 Mininet 网络对象，使用 ryu_topo 类
    net = Mininet(topo=ryu_topo())

    # 启动网络
    net.start()

    # 获取拓扑信息
    hosts = net.hosts
    switches = net.switches

    # 将拓扑信息转换为适合 HTML 格式的数据
    topology_data = {
        "hosts": [(host.name,host.IP(),host.MAC()) for host in hosts],
        "switches": [switch.name for switch in switches],
        "links": [(link.intf1.node.name, link.intf2.node.name) for link in net.links]
    }

    # 停止网络
    net.stop()


    return render_template('topology.html', topology_data=topology_data)
    # 使用 json.dumps 将数据转换为 JSON 字符串
   # return jsonify(json.dumps(topology_data))

if __name__ == '__main__':
    app.run(debug=True)
