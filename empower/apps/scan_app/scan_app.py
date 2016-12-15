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
from empower.datatypes.etheraddress import EtherAddress

import pdb
import empower.logger
import threading
LOG = empower.logger.get_logger()

BASE_MAC = EtherAddress("00:1b:b3:00:00:00")
ALGORITHM_FILE = 'algorithm.txt'
WITHOUT_CONSTRAINT = 0 

class ScanApp(EmpowerApp):
    """Scan App.

    Example:
        ./empower-runtime.py apps.scan_app.scan_app --tenant-id=e8911430-0c59-483d-8af3-90f6b29b3946
    """

    def __init__(self, server, **kwargs):        
        EmpowerApp.__init__(self, **kwargs)
        self._server = server
        self.routers = []
        self.lvaps_cache = []        
        self.scanreceived(callback=self.scanreceived_callback)
        self.filename = 'scan_app.txt'
        with open(ALGORITHM_FILE, 'w') as algofile:
            algofile.write('---- SCAN_APP ----\n')
        with open(self.filename, 'w') as file_d:
            file_d.write('---- SCAN_APP ----\n')

    def send_scan_request(self):
        self.scan_info = []

        for wtp in self.wtps():
            self.routers.append(wtp)
        
        with open(self.filename, 'a') as file_d:
            file_d.write('----- SCAN START ----- \n')

        self.scan_router()
        

    def scan_router(self):
        router = self.routers.pop(0)
        
        if router.connection:
            router.connection.send_scan_request()            
            with open(self.filename, 'a') as file_d:
                file_d.write('scan router %s\n' % (router.label))

        else:
            with open(self.filename, 'a') as file_d:
                file_d.write('router %s erro: no connection\n' % (router.label))
            if len(self.routers) > 0:
                self.scan_router()
            else:
                self.generateGraph()

    def scanreceived_callback(self, scan):        
        self.scan_info.append(scan)
        with open(self.filename, 'a') as file_d:
            file_d.write('scan received router %s\n' % (scan.wtp.label))

        for lvap in RUNTIME.lvaps.values():
            l = LVAPCache(lvap.lvap_bssid, lvap.wtp.label)
            self.lvaps_cache.append(l)

        if len(self.routers) == 0:            
            self.generateGraph()
        else:
            self.scan_router()

    def printScanResult(self, scan):
        with open(self.filename, 'a') as file_d:
            file_d.write('----- SCAN WTP %s -----\n' % (scan.wtp.label))
            for n in scan.neighbors:
                file_d.write('SSID: %s, ADDR: %s, CHANNEL: %d, SIGNAL: %d, QUALITY: %s \n' % (n.ssid, n.addr, n.channel, n.signal, n.qualityStr))
            file_d.write('-----------\n')

    def printAllScanResult(self):
        with open(self.filename, 'a') as file_d:
            for i in range(len(self.scan_info)):
                scan = self.scan_info[i]
                file_d.write('----- SCAN WTP %s -----\n' % (scan.wtp.label))
                for n in scan.neighbors:
                    file_d.write('SSID: %s, ADDR: %s, CHANNEL: %d, SIGNAL: %d, QUALITY: %s \n' % (n.ssid, n.addr, n.channel, n.signal, n.qualityStr))
                file_d.write('-----------\n')

    def printAlgorithm(self, graph, neighborsConstraint):
        with open(ALGORITHM_FILE, 'a') as file_d:
            
            for i in range(len(self.scan_info)):
                file_d.write('----- graph %s ------\n' % (self.scan_info[i].wtp.label))
                for n in graph[i]:
                    file_d.write('SSID: %s, ID: %s, ADDR: %s, CHANNEL: %d, SIGNAL: %d, QUALITY: %s \n' % (n.ssid, n.id, n.addr, n.channel, n.signal, n.qualityStr))

                file_d.write('----- neighborsConstraint %s ------\n' % (self.scan_info[i].wtp.label))
                for n in neighborsConstraint[i]:
                    file_d.write('SSID: %s, ADDR: %s, CHANNEL: %d, SIGNAL: %d, QUALITY: %s \n' % (n.ssid, n.addr, n.channel, n.signal, n.qualityStr))

            file_d.write('-----------\n')

    def generateGraph(self):
        graph = []
        neighborsConstraint = []
        base = str(BASE_MAC).split(":")[0:3]
        self.printAllScanResult()
        # self.logLvaps()
        self.lvaps_cache = list(set(self.lvaps_cache))
        self.logLvaps()

        for bucket in range(len(self.scan_info)):
            n = self.scan_info[bucket]
            graph.append([])
            neighborsConstraint.append([])
            
            for neighbor in n.neighbors:                
                neighbor.id = ''
                str_n = str(neighbor.getAddr()).split(":")[0:3]

                if base == str_n:
                    if self.isInDomain(neighbor):
                        # para hacer el set id hay que buscar a que wtp pertenece el lvap
                        # y ver en el indice al que corresponde
                        neighbor.id = self.findId(neighbor)
                        self.appendToGraph(bucket, neighbor, graph)
                else:
                    if WITHOUT_CONSTRAINT == 0:
                        neighborsConstraint[bucket].append(neighbor)
            # remove duplicates
            neighborsConstraint[bucket] = list(set(neighborsConstraint[bucket]))

        # llamamos al algoritmo
        self.printAlgorithm(graph, neighborsConstraint)
        alg = CentralizedAlgorithm(graph, neighborsConstraint)
        sol = alg.invoke()
        self.switchChannels(self.scan_info, sol)
        del self.lvaps_cache[:]

    def appendToGraph(self, bucket, neighbor, graph):
        # agrega como neighbor solo si no fue agregado antes
        r = [n for n in graph[bucket] if n.getId() == neighbor.getId()]
        if len(r) == 0:
            graph[bucket].append(neighbor)

    def findId(self, neighbor):
        for bucket in range(len(self.scan_info)):
            if self.scan_info[bucket].wtp.label == neighbor.label:
                return bucket

    def switchChannels(self, scan_info, sol):
        for i in range(len(scan_info)):
            with open(ALGORITHM_FILE, 'a') as file_d:
                file_d.write('%s) %s -> %s \n' % (i, self.scan_info[i].wtp.label, sol[i]))

        # cambia los canales de los wtps
        for i in range(len(scan_info)):
            # arreglar para no cambiar el canal si es el mismo 
            LOG.info("----------Cambiando canal del WTP %s a %d---------" % (scan_info[i].wtp.addr, sol[i]))
            scan_info[i].wtp.connection.send_set_channel(sol[i])        

    def isInDomain(self, neighbor):
        addr = neighbor.getAddr()
        # estos lvaps deberian corresponder a los que esten cuando se realizo el scan
        for lvap in self.lvaps_cache: # RUNTIME.lvaps.values():
            if EtherAddress(addr) == lvap.lvap_bssid:
                LOG.info('****** ADDR %s es un router nuestro ********************************************' % addr)
                neighbor.label = lvap.label #lvap.wtp.label
                return True
        return False

    def logLvaps(self):
        with open(ALGORITHM_FILE, 'a') as file_d:
            file_d.write('------ LVAPS CACHE -----\n')
            for lvap in self.lvaps_cache:
                file_d.write('lvap: %s, %s\n' % (lvap.label, lvap.lvap_bssid))

    def loop(self):        
        LOG.info('---------------------------------------->')
        if len(self.routers) == 0:
            self.send_scan_request()


class LVAPCache(object):
    def __init__(self, lvap_bssid_addr, label):
        self.lvap_bssid = lvap_bssid_addr
        self.label = label
        r = 0
        for c in str(self.lvap_bssid):
            r += ord(c)
        for c in self.label:
            r += ord(c)

        self._hash = r

    def __hash__(self):
        return self._hash

    def __eq__(self, other):
        return self.__hash__() == other.__hash__() 

def launch(tenant_id, every=60000):
    """ Initialize the module. """
    server = RUNTIME.components[LVAPPServer.__module__]
    return ScanApp(server, tenant_id=tenant_id, every=every)
