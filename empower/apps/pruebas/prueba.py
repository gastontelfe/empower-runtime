#!/usr/bin/env python3
#
# Copyright (c) 2015, Roberto Riggio
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the CREATE-NET nor the
#      names of its contributors may be used to endorse or promote products
#      derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY CREATE-NET ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL CREATE-NET BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Prueba Apps."""

from empower.core.app import EmpowerApp
from empower.core.app import DEFAULT_PERIOD
from empower.events.wtpup import wtpup
from empower.events.wtpdown import wtpdown
from empower.events.cppup import cppup
from empower.events.cppdown import cppdown
from empower.events.lvapjoin import lvapjoin
from empower.events.lvapleave import lvapleave
from empower.lvapp.lvappserver import LVAPPServer
from empower.main import RUNTIME


import empower.logger
LOG = empower.logger.get_logger()


class PruebaApp(EmpowerApp):
    """Prueba App.

    Example:

        ID="640a1560-d3ac-42c8-ba5d-ef4cea0136d9"
        ./empower-runtime.py apps.pruebas.prueba:640a1560-d3ac-42c8-ba5d-ef4cea0136d9

    """

    def __init__(self, tenant_id, period,server):

        EmpowerApp.__init__(self, tenant_id)

        self._server=server
        wtpup(tenant_id=self.tenant.tenant_id,
              callback=self.wtp_up_callback)

    def wtp_up_callback(self, wtp):
        """Called when a new wtp connects to the controller."""

        LOG.info("WTP %s up!" % wtp.addr)
        wtp.connection.send_set_channel(6)
        #self._server.set_channel(6)


def launch(tenant, period=DEFAULT_PERIOD):
    """ Initialize the module. """

    server = RUNTIME.components[LVAPPServer.__module__]
    return PruebaApp(tenant, period, server)
