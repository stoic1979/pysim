from pySim.commands import SimCardCommands
from pySim.transport.serial import SerialSimLink
from pySim.utils import *

from constants import *
from utils import *

from binascii import hexlify, unhexlify

from sms import SMSmessage
import traceback

"""
References:

Universal Integrated Circuit Card (UICC) File Structure
http://www.tech-invite.com/fo-uicc/tinv-fo-uicc-mf.html

Conformance Testing
http://www.3gpp.org/technologies/keywords-acronyms/108-conformance-testing-ue


"""

class RsSIMReader():
    """
    Multipurpose reader class inspired from pySIm's reader
    """

    def __init__(self, device, baudrate):

        # create trasnport
	self.sl = SerialSimLink(device=device, baudrate=baudrate)

        # create command layer
        self.scc = SimCardCommands(transport=self.sl)

        # wait for SIM card
        print("[INFO] Waiting for SIM card ...")
        self.sl.wait_for_card()

        # program the card
        print("[INFO] Reading SIM card ...")

    def get_iccid(self):
	# EF.ICCID
	(res, sw) = self.scc.read_binary([MF, '2fe2'])
	if sw == '9000':
	    print("[INFO] ICCID: %s" % (dec_iccid(res),))
	else:
	    print("[INFO] ICCID: Can't read, response code = %s" % (sw,))

    def get_msisdn(self):
        print " --- get_msisdn --- "
	# EF.MSISDN
	try:
	    (res, sw) = self.scc.read_record([MF, DF_TELECOM, EF_MSISDN], 1)
            print "get_msisdn for sw", sw
            print "get_msisdn for res", res
	    if sw == '9000':
		if res[1] != 'f':
		    print("[INFO] MSISDN: %s" % (res,))
		else:
		    print("[INFO] MSISDN: Not available")
	    else:
		print("[INFO] MSISDN: Can't read, response code = %s" % (sw,))
	except:
	    print "[INFO] MSISDN: Can't read. Probably not existing file"

    def get_opc(self):
        print " --- get_opc --- "
	# EF.MSISDN
	try:
	    (res, sw) = self.scc.read_binary([MF, '7F20', '00F7'])
            print "get_opc for sw", sw
            print "get_opc for res", res
	    if sw == '9000':
		if res[1] != 'f':
		    print("[INFO] OPC: %s" % (res,))
		else:
		    print("[INFO] OPC: Not available")
	    else:
		print("[INFO] OPC: Can't read, response code = %s" % (sw,))
	except:
	    print "[INFO] MSISDN: Can't read. Probably not existing file"

    def get_pl(self):
	# EF.PL
	(res, sw) = self.scc.read_binary([MF, '2f05'])
	if sw == '9000':
	    print("[INFO] PL: %s" % (res,))
	else:
	    print("[INFO] PL: Can't read, response code = %s" % (sw,))

    def get_imsi(self):
	# EF.IMSI
	(res, sw) = self.scc.read_binary([MF, DF_GSM, EF_IMSI])
	if sw == '9000':
	    print("[INFO] IMSI: %s" % (dec_imsi(res),))
	else:
	    print("[INFO] IMSI: Can't read, response code = %s" % (sw,))


    def list_applets(self):
        apdu = "80f21000024f0000c0000000"
        self.send_apdu_list([apdu])

    def get_global_pin(self):
        print ("[INFO] :: getting global PIN")
        file_id = '2205'
        file_size = 52
        path = ['3F00', file_id]

	#(res, sw) = self.scc.read_binary(path)
	(res, sw) = self.scc.read_record(path, 1)
        print "res", res
        print "sw", sw

    def get_native_apps(self):
        print ("[INFO] :: getting native apps")
        path = ['3F00', '2207']

	num_records = self.scc.record_count(path)
	print ("Native Applications: %d records available" % num_records)
	for record_id in range(1, num_records + 1):
		print self.scc.read_record(path, record_id)

        print

    def get_arr_mf(self):
        print ("[INFO] :: getting ARR MF")
        path = ['3F00', '2f06']

	num_records = self.scc.record_count(path)
	print ("ARR MF: %d records available" % num_records)
	for record_id in range(1, num_records + 1):
		print self.scc.read_record(path, record_id)

        print

    def get_arr_telecom(self):
        """
        Access rules may be shared between files in the UICC by referencing.
        This is accomplished by storing the security attributes in the EF ARR file under the MF. 

        The second possibility allows the usage of different access rules in different security environments. 
        """
        print ("[INFO] :: getting ARR TELECOM")
        path = ['3F00', '7f10', '6f06']

	num_records = self.scc.record_count(path)
	print ("ARR TELECOM: %d records available" % num_records)
	for record_id in range(1, num_records + 1):
		print self.scc.read_record(path, record_id)

        print

    def get_df_phonebook(self):
        print ("[INFO] :: getting DF PHONEBOOK")
        path = ['3F00', '7f10', '5f3a']

	num_records = self.scc.record_count(path)
	print ("DF PHONEBOOK: %d records available" % num_records)
	for record_id in range(1, num_records + 1):
		print self.scc.read_record(path, record_id)

        print

    def get_df_toolkit(self):
        print ("[INFO] :: getting DF TOOLKIT")
        path = ['3F00', '7FDE']

	num_records = self.scc.record_count(path)
	print ("DF TOOLKIT: %d records available" % num_records)
	for record_id in range(1, num_records + 1):
		print self.scc.read_record(path, record_id)

        print

    def get_ef_dir(self):
        print ("[INFO] :: getting EF DIR")
        path = ['3F00', '2F00']

	num_records = self.scc.record_count(path)
	print ("EF DIR: %d records available" % num_records)
	for record_id in range(1, num_records + 1):
		print self.scc.read_record(path, record_id)

        print

    def get_ef_atr(self):
        print ("[INFO] :: getting EF ATR")
        path = ['3F00', '2F01']

	(res, sw) = self.scc.read_binary(path)
        print "res", res
        print "sw", sw


def try_except(fn, tag):
    try:
        fn()
    except Exception as exp:
        print "%s :: got exception %s" % (tag, exp)

if __name__ == '__main__':
    device="/dev/ttyUSB0"
    baudrate = 9600
    sim = RsSIMReader(device, baudrate)
    sim.get_iccid()
    # sim.get_imsi()
    # sim.get_opc()
    # try_except(sim.get_pl, "[GET-PL]")

    # try_except(sim.get_global_pin, "[GET-GLOBAL0-PIN]")
    # try_except(sim.get_native_apps, "[GET-NATIVE-APPS]")
    # try_except(sim.get_arr_mf,      "[GET-ARR-MF]")
    # try_except(sim.get_arr_telecom, "[GET-ARR-TELECOM]")
    # try_except(sim.get_df_phonebook, "[GET-DFF-PHONEBOOK]")
    # try_except(sim.get_df_toolkit, "[GET-DFF-TOOLKIT]")
    try_except(sim.get_ef_dir, "[GET-EF-DIR]")
    try_except(sim.get_ef_atr, "[GET-EF-ATR]")
