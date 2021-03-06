#!/usr/bin/env python3
#
# Copyright (c) 2016 Roberto Riggio
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.

"""Launch the EmPOWER runtime."""

from empower.main import main


if __name__ == "__main__":

    # Default modules
    ARGVS = ['restserver.restserver',
             'lvnfp.lvnfpserver',
             'lvapp.lvappserver',
             'energinoserver.energinoserver',
             'lvap_stats.lvap_stats',
             'events.wtpdown',
             'events.wtpup',
             'events.lvapleave',
             'events.lvapjoin',
             'events.scanreceived',
             'counters.packets_counter',
             'counters.bytes_counter',
             'maps.ucqm',
             'maps.ncqm',
             'triggers.rssi',
             'triggers.summary',
             #'events.cppdown',
             #'events.cppup',
             #'events.lvnfjoin',
             #'events.lvnfleave',
             #'handlers.read_handler',
             #'handlers.write_handler',
             #'lvnf_stats.lvnf_stats',
             ]

    main(ARGVS)
