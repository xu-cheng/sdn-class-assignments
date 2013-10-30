'''
Coursera:
- Software Defined Networking (SDN) course
-- Module 3 Programming Assignment

Professor: Nick Feamster
Teaching Assistant: Muhammad Shahbaz
'''

from mininet.topo import Topo


class CustomTopo(Topo):

    "Simple Data Center Topology"

    "linkopts - (1:core, 2:aggregation, 3: edge) parameters"
    "fanout - number of child switch per parent switch"

    def __init__(self, linkopts1, linkopts2, linkopts3, fanout=2, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)
        self.fanout = fanout
        # Create core
        c1 = self.addSwitch('c1')
        # Create aggregation
        for i in range(fanout):
            a = self.addSwitch('a%d' % (i + 1))
            self.addLink(a, c1, **linkopts1)
            # Create edge
            for j in range(fanout):
                e = self.addSwitch('e%d' % (j + 1 + i * fanout))
                self.addLink(e, a, **linkopts2)
                # Create host
                for k in range(fanout):
                    h = self.addHost('h%d' % (k + 1 + i * fanout + j * fanout))
                    self.addLink(h, e, **linkopts3)


topos = {'custom': (lambda: CustomTopo())}

def simpleTest(fanout=2):
    from mininet.net import Mininet
    from mininet.link import TCLink
    from mininet.util import dumpNodeConnections
    linkopts = {'bw': 10, 'delay': '5ms'}
    topo = CustomTopo(linkopts, linkopts, linkopts, fanout)
    net = Mininet(topo, link=TCLink)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"
    net.pingAll()
    net.stop()

if __name__ == '__main__':
    from mininet.log import setLogLevel
    setLogLevel('info')
    simpleTest()