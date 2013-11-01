'''
Coursera:
- Software Defined Networking (SDN) course
-- Module 4 Programming Assignment

Professor: Nick Feamster
Teaching Assistant: Muhammad Shahbaz
'''

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os

log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ['HOME']


class Firewall (EventMixin):

    def __init__(self):
        self.listenTo(core.openflow)
        self.rules = []
        with open(policyFile, 'r') as f:
            for line in f:
                try:
                    rule = line.strip().split(',')
                    if rule[0] != 'id':
                        self.rules.append((EthAddr(rule[1]), EthAddr(rule[2])))
                except:
                    pass
        log.debug("Enabling Firewall Module")

    def _handle_ConnectionUp(self, event):
        for src, dst in self.rules:
            msg = of.ofp_flow_mod()
            msg.match = of.ofp_match()
            msg.match.dl_src = src
            msg.match.dl_dst = dst
            msg.priority = 65535
            event.connection.send(msg)
        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))


def launch():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)
