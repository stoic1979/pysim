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
from pySim.utils import *

from constants import *
from utils import *

from binascii import hexlify, unhexlify

from sms import SMSmessage
import traceback


class Reader():
    """
    Multipurpose reader class inspired from pySIm's reader
    """

    def __init__(self, device, baudrate):

        # create trasnport
	self.sl = SerialSimLink(device=device, baudrate=baudrate)

        # create command layer
        self.scc = SimCardCommands(transport=self.sl)

        # wait for SIM card
        print("[Reader] Waiting for SIM card ...")
        self.sl.wait_for_card()

        # program the card
        print("[Reader] Reading SIM card ...")

    def get_iccid(self):
	# EF.ICCID
	(res, sw) = self.scc.read_binary([MF, '2fe2'])
	if sw == '9000':
	    print("[Reader] ICCID: %s" % (dec_iccid(res),))
	else:
	    print("[Reader] ICCID: Can't read, response code = %s" % (sw,))

    def get_smsp(self):
	# EF.SMSP
	(res, sw) = self.scc.read_record([MF, '7f10', '6f42'], 1)
	if sw == '9000':
	    print("[Reader] SMSP: %s" % (res,))
	else:
	    print("[Reader] SMSP: Can't read, response code = %s" % (sw,))

    def get_acc(self):
	# EF.ACC
	(res, sw) = self.scc.read_binary([MF, '7f20', '6f78'])
	if sw == '9000':
	    print("[Reader] ACC: %s" % (res,))
	else:
	    print("[Reader] ACC: Can't read, response code = %s" % (sw,))

    def get_msisdn(self):
	# EF.MSISDN
	try:
	    (res, sw) = self.scc.read_record([MF, DF_TELECOM, EF_MSISDN], 1)
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
	    (res, sw) = self.scc.read_record([MF, '0000'], 1)
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
	(res, sw) = self.scc.read_binary([MF, '2f05'])
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
	(res, sw) = self.scc.read_binary([MF, '2fe6'])
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
	(res, sw) = self.scc.read_binary([MF, '2f00'])
	if sw == '9000':
	    print("[Reader] DIR: %s" % (dec_iccid(res),))
	else:
	    print("[Reader] DIR: Can't read, response code = %s" % (sw,))


    # FIXME - it crashes
    def get_usim(self):
        """
        Universal Subscriber Identity Module

        
        """
	# EF.USIM
	(res, sw) = self.scc.read_binary([MF, '6f05'])
	if sw == '9000':
	    print("[Reader] USIM: %s" % (dec_iccid(res),))
	else:
	    print("[Reader] USIM: Can't read, response code = %s" % (sw,))


    def get_telecom(self):
        """
        
        """
	# EF.TELECOM
	r = self.scc.select_file([MF, DF_TELECOM, EF_ADN])
        print "r:", r

    
    def get_imsi(self):
	# EF.IMSI
	(res, sw) = self.scc.read_binary([MF, DF_GSM, EF_IMSI])
	if sw == '9000':
	    print("[Reader] IMSI: %s" % (dec_imsi(res),))
	else:
	    print("[Reader] IMSI: Can't read, response code = %s" % (sw,))

    def get_plmn(self):
	# EF.PLMN
	(res, sw) = self.scc.read_binary([MF, DF_GSM, '6F30'])
        print ("res: ", res)
	if sw == '9000':
	    print("[Reader] PLMN: %s" % (dec_plmn(res),))
	else:
	    print("[Reader] PLMN: Can't read, response code = %s" % (sw,))


    def get_phase(self):
	(res, sw) = self.scc.read_binary(["3F00", "7F20", "6FAE"])
	if sw == '9000':
            if res == "00":
                phase = 'Phase 1'
            elif res == "01":
                phase = 'Phase 2'
            else:
                phase = 'Phase 2+'

	    print("[Reader] Phase: %s" % phase)
	else:
	    print("[Reader] Phase: Can't read, response code = %s" % (sw,))

    def send_apdu_list(self, lst):
        for apdu in lst:
            print ("In: %s" % apdu)
            out, sw = self.sl.send_apdu_raw(apdu)
            print "SW:", sw
            print "OUT:", out
            print

    def send_apdu_list_prefixed(self, lst):
        lst = ["A0A4000002" + l for l in lst]
        print ("Prefixed list: %s" % lst)
        self.send_apdu_list(lst)

    def connect_to_sim(self):
        connect_sim_apdu_lst = ['A0A40000023F00', 'A0F200000D', 'A0F2000016']
        print ("Connecting to SIM...")
        ret = self.send_apdu_list(connect_sim_apdu_lst)
        print ("Connected")
        print

    def get_phonebook(self):

        phone_lst = []

        print ("Selecting file")
        self.send_apdu_list_prefixed(['3F00', '7F10', '6F3A'])

        data, sw = self.sl.send_apdu_raw("A0C000000F")

        rec_len  = int(data[28:30], 16) # Usually 0x20

        # Now we can work out the name length & number of records
        name_len = rec_len - 14 # Defined GSM 11.11
        num_recs = int(data[4:8], 16) / rec_len

        print ("rec_len: %d, name_len: %d, num_recs: %d" % (rec_len, name_len, num_recs))


        apdu_str = "A0B2%s04" + IntToHex(rec_len)
        hexNameLen = name_len << 1

        try:
            for i in range(1, num_recs + 1):
                apdu = apdu_str % IntToHex(i)
                data, sw = self.sl.send_apdu_raw(apdu)

                print ("Contact #%d" % i)
                print ("In: %s" % apdu)
                print "SW:", sw
                print "OUT:", data

                if data[0:2] != 'FF':
                    name = GSM3_38ToASCII(unhexlify(data[:hexNameLen]))
                    if ord(name[-1]) > 0x80:
                        # Nokia phones add this as a group identifier. Remove it.
                        name = name[:-1].rstrip()
                    number = ""

                    numberLen = int(data[hexNameLen:hexNameLen+2], 16)
                    if numberLen > 0 and numberLen <= (11): # Includes TON/NPI byte
                        hexNumber = data[hexNameLen+2:hexNameLen+2+(numberLen<<1)]
                        if hexNumber[:2] == '91':
                            number = "+"
                        number += GSMPhoneNumberToString(hexNumber[2:])
                    #self.itemDataMap[i] = (name, number)
                    print "Name: ", name
                    print "Number: ", number
                    phone_lst.append((name, number))

                print
        except Exception as exp:
            print "\n\nget_phonebook() got exception :: %s\n\n" % exp

        return phone_lst

    def get_sms(self):

        sms_lst = []

        print ("Selecting SMS file")
        self.send_apdu_list_prefixed(['3F00', '7F10', '6F3C'])

        data, sw = self.sl.send_apdu_raw("A0C000000F")

        rec_len = int(data[28:30], 16) # Should be 0xB0 (176)
        num_recs = int(data[4:8], 16) / rec_len

        print ("rec_len: %d, num_recs: %d" % (rec_len, num_recs))

        apdu_str = "A0B2%s04" + IntToHex(rec_len)

        try:
            for i in range(1, num_recs + 1):
                apdu = apdu_str % IntToHex(i)
                data, sw = self.sl.send_apdu_raw(apdu)

                print ("SMS #%d" % i)
                print ("In: %s" % apdu)
                print "SW:", sw
                print "OUT:", data
                print

                # See if SMS record is used
                status = int(data[0:2], 16)
                if status & 1 or data[2:4] != 'FF':
                    try:
                        sms = SMSmessage()
                        sms.smsFromData(data)
                        sms_lst.append( (sms.status, sms.timestamp, sms.number, sms.message) )
                    except Exception as exp:
                        pass
                        #print "\n\nget_sms() got exception: %s\n while fetching SMS from data, for SMS #%d\n\n" % (exp, i)
                        #print traceback.format_exc()
        except Exception as exp:
            print "\n\nget_sms() got exception :: %s\n\n" % exp
            print traceback.format_exc()

        return sms_lst

    def list_applets(self):
        apdu = "80f21000024f0000c0000000"
        self.send_apdu_list([apdu])




if __name__ == '__main__':
    device="/dev/ttyUSB0"
    baudrate = 9600
    reader = Reader(device, baudrate)

    # reader.get_iccid()
    # reader.get_smsp()
    # reader.get_acc()
    # reader.get_msisdn()
    # reader.get_uid()
    # reader.get_pl()
    # reader.get_arr()
    reader.get_dir()
    # reader.get_usim()
    # reader.get_telecom()

    # reader.get_imsi()
    # reader.get_plmn()

    # reader.get_phase()
    #print reader.get_phonebook()
    #print reader.get_sms()
    reader.list_applets()



