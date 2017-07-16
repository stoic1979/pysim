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
from pySim.utils import h2b, swap_nibbles, rpad, dec_imsi, dec_iccid


class Reader():
    """
    Multipurpose reader class inspired from pySIm's reader
    """

    def __init__(self, device, baudrate):

        # create trasnport
	sl = SerialSimLink(device=device, baudrate=baudrate)

        # create command layer
        self.scc = SimCardCommands(transport=sl)

        # wait for SIM card
        print("[Reader] Waiting for SIM card ...")
        sl.wait_for_card()

        # program the card
        print("[Reader] Reading SIM card ...")

    def get_iccid(self):
	# EF.ICCID
	(res, sw) = self.scc.read_binary(['3f00', '2fe2'])
        print ("res:", res)
	if sw == '9000':
	    print("[Reader] ICCID: %s" % (dec_iccid(res),))
	else:
	    print("[Reader] ICCID: Can't read, response code = %s" % (sw,))

    def get_imsi(self):
	# EF.IMSI
	(res, sw) = self.scc.read_binary(['3f00', '7f20', '6f07'])
	if sw == '9000':
	    print("[Reader] IMSI: %s" % (dec_imsi(res),))
	else:
	    print("[Reader] IMSI: Can't read, response code = %s" % (sw,))

    def get_smsp(self):
	# EF.SMSP
	(res, sw) = self.scc.read_record(['3f00', '7f10', '6f42'], 1)
	if sw == '9000':
	    print("[Reader] SMSP: %s" % (res,))
	else:
	    print("[Reader] SMSP: Can't read, response code = %s" % (sw,))

    def get_acc(self):
	# EF.ACC
	(res, sw) = self.scc.read_binary(['3f00', '7f20', '6f78'])
	if sw == '9000':
	    print("[Reader] ACC: %s" % (res,))
	else:
	    print("[Reader] ACC: Can't read, response code = %s" % (sw,))

    def get_msisdn(self):
	# EF.MSISDN
	try:
	    (res, sw) = self.scc.read_record(['3f00', '7f10', '6f40'], 1)
	    if sw == '9000':
		if res[1] != 'f':
		    print("[Reader] MSISDN: %s" % (res,))
		else:
		    print("[Reader] MSISDN: Not available")
	    else:
		print("[Reader] MSISDN: Can't read, response code = %s" % (sw,))
	except:
	    print "[Reader] MSISDN: Can't read. Probably not existing file"


    # FIXME
    def get_uid(self):
	try:
	    (res, sw) = self.scc.read_record(['ca00', '0000'], 1)
	    if sw == '9000':
		if res[1] != 'f':
		    print("[Reader] UID: %s" % (res,))
		else:
		    print("[Reader] UID: Not available")
	    else:
		print("[Reader] UID: Can't read, response code = %s" % (sw,))
	except:
	    print "[Reader] UID: Can't read. Probably not existing file"

    def get_pl(self):
        """
        Preferred  Languages

        This EF contains the codes for up to n languages. 
        This information, determined by the user/operator, 
        defines the preferred languages of the user, 
        for the UICC, in order of priority. 
        """
	# EF.PL
	(res, sw) = self.scc.read_binary(['3f00', '2f05'])
	if sw == '9000':
	    print("[Reader] PL: %s" % (dec_iccid(res),))
	else:
	    print("[Reader] PL: Can't read, response code = %s" % (sw,))

    # FIXME - it crashes
    def get_arr(self):
        """
        Access  Rule  Reference 

        Access rules may be shared between files in the UICC by referencing. 
        This is accomplished by storing the security attributes in the EF ARR file under the MF.

        The second possibility allows the usage of different access rules in different security environments. 
        """
	# EF.ARR
	(res, sw) = self.scc.read_binary(['3f00', '2fe6'])
	if sw == '9000':
	    print("[Reader] ARR: %s" % (dec_iccid(res),))
	else:
	    print("[Reader] ARR: Can't read, response code = %s" % (sw,))


    # FIXME - cant read
    def get_dir(self):
        """
        Application  DIRectory 

        EF DIR is a linear fixed file under the MF and is under the responsibility of the issuer. 
        
        All applications are uniquely identified by application identifiers (AID) that are obtained from EF DIR. 
        
        These application identifiers are used to select the application. 
        """
	# EF.DIR
	(res, sw) = self.scc.read_binary(['3f00', '2f00'])
	if sw == '9000':
	    print("[Reader] DIR: %s" % (dec_iccid(res),))
	else:
	    print("[Reader] DIR: Can't read, response code = %s" % (sw,))



if __name__ == '__main__':
    device="/dev/ttyUSB0"
    baudrate = 9600
    reader = Reader(device, baudrate)

    # reader.get_iccid()
    # reader.get_imsi()
    # reader.get_smsp()
    # reader.get_acc()
    # reader.get_msisdn()
    # reader.get_uid()
    # reader.get_pl()
    # reader.get_arr()
    reader.get_dir()



