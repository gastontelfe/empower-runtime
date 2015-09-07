#!/usr/bin/env python3
#
# Copyright (c) 2016, Roberto Riggio
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

from empower.main import main


if __name__ == "__main__":

    # Default modules
    ARGVS = ['core.restserver',
             'scylla.lvnfp.lvnfpserver',
             'charybdis.lvapp.lvappserver',
             'core.energinoserver',
             'charybdis.link_stats.link_stats',
             'charybdis.events.wtpdown',
             'charybdis.events.wtpup',
             'charybdis.events.lvapleave',
             'charybdis.events.lvapjoin',
             'charybdis.counters.packets_counter',
             'charybdis.counters.bytes_counter',
             'charybdis.maps.ucqm',
             'charybdis.maps.ncqm',
             'charybdis.triggers.rssi',
             'charybdis.triggers.summary',
             'scylla.events.cppdown',
             'scylla.events.cppup',
             'scylla.events.lvnfjoin',
             'scylla.events.lvnfleave',
             'scylla.handlers.read_handler',
             'scylla.handlers.write_handler',
             'scylla.stats.lvnf_stats',
             ]

    main(ARGVS)