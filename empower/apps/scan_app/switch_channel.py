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
        self.channel = 11

    def switchChannels(self, wtp):
        # cambia los canales de los wtps
        wtp.connection.send_set_channel(self.channel)        

    def loop(self):        
        LOG.info('---------------------------------------->')
        for wtp in self.wtps():
            if wtp.connection:
                LOG.info("Cambiando canal a %s" % (wtp.label))
                self.switchChannels(wtp)


def launch(tenant_id, every=40000):
    """ Initialize the module. """
    server = RUNTIME.components[LVAPPServer.__module__]
    return ScanApp(server, tenant_id=tenant_id, every=every)
