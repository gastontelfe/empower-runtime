#!/usr/bin/env python3


"""Scan App."""

from empower.core.app import EmpowerApp
from empower.core.app import DEFAULT_PERIOD
from empower.events.wtpup import wtpup
from empower.events.wtpdown import wtpdown
from empower.events.lvapjoin import lvapjoin
from empower.events.lvapleave import lvapleave
from empower.events.scanreceived import scanreceived
from empower.lvapp.lvappserver import LVAPPServer
from empower.main import RUNTIME
from empower.scan.centralizedAlgorithm import CentralizedAlgorithm
from empower.core.tenant import T_TYPE_SHARED
from empower.core.tenant import T_TYPE_UNIQUE
from empower.core.utils import generate_bssid
from empower.datatypes.etheraddress import EtherAddress
from empower.datatypes.ssid import SSID



import pdb
import empower.logger
import threading
LOG = empower.logger.get_logger()


class ScanApp(EmpowerApp):
    """Scan App.

    Example:

        ID="3b678156-477f-4b54-84ff-aa80699eb984"
        ./empower-runtime.py apps.scan_app.scan_app --tenant-id=e8911430-0c59-483d-8af3-90f6b29b3946
    """

    def __init__(self, server, **kwargs):        
        EmpowerApp.__init__(self, **kwargs)
        self._server = server
        self.scanreceived(callback=self.scanreceived_callback)

    def send_scan_request(self):
        self.scan_count = 0
        self.scan_count_r = 0
        self.scan_info = {}

        for wtp in self.wtps():
            if wtp.label == 'router16':
                wtp.connection.send_scan_request()

    def scanreceived_callback(self, scan):
        for n in scan.neighbors:
            LOG.info("---------- SSID: %s %s" % (n.ssid, n.addr))


    def generateGraph(self):
        graph = [[]] * self.scan_count
        neighborsConstraint = [None] * self.scan_count

        ids = [] * self.scan_count
        for wtp in self.wtps():
            pdb.set_trace()
            if wtp.connection:
                ids.append(wtp.addr)

        for bucket in range(len(self.scan_info)):
            n = self.scan_info[bucket]
            for neighbor in n.neighbors:
                if self.isInDomain(neighbor, ids):
                    if graph[bucket] is None:
                        graph[bucket] = []
                    graph[bucket].append(neighbor)
                else:
                    if neighborsConstraint[bucket] is None:
                        neighborsConstraint[bucket] = []
                    neighborsConstraint[bucket].append(neighbor)
        # llamamos al algoritmo
        #pdb.set_trace()        
        alg = CentralizedAlgorithm(graph, neighborsConstraint)
        sol = alg.invoke()
        self.switchChannels(self.scan_info, sol)

    def switchChannels(self, scan_info, sol):
        # cambia los canales de los wtps
        for i in range(len(scan_info)):
            # arreglar para no cambiar el canal si es el mismo 
            LOG.info("----------Cambiando canal del WTP %s a %d---------" % (scan_info[i].wtp.addr, sol[i]))
            scan_info[i].wtp.connection.send_set_channel(sol[i])        


    def isInDomain(self, neighbor, ids):
        addr = neighbor.getAddr()
        return (addr in ids)

    def loop(self):        
        LOG.info('---------------------------------------->')
        self.send_scan_request()


def launch(tenant_id, every=30000):
    """ Initialize the module. """
    server = RUNTIME.components[LVAPPServer.__module__]
    return ScanApp(server, tenant_id=tenant_id, every=every)
