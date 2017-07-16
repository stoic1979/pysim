#!/usr/bin/env python

#
# Utility to display some informations about a SIM card
#
#
# Copyright (C) 2017  Navjot Singh <weavebytes@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from pySim.commands import SimCardCommands
from pySim.transport.serial import SerialSimLink

class Reader():
    """
    Multipurpose reader class inspired from pySIm's reader
    """


    def __init__(self, device, baudrate):
	sl = SerialSimLink(device=device, baudrate=baudrate)

        # Create command layer
        scc = SimCardCommands(transport=sl)

        # Wait for SIM card
        sl.wait_for_card()

        # Program the card
        print("Reading ...")


if __name__ == '__main__':
    device="/dev/ttyUSB0"
    baudrate = 9600
    reader = Reader(device, baudrate)

