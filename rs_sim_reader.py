from pySim.commands import SimCardCommands
from pySim.transport.serial import SerialSimLink
from pySim.utils import *

from constants import *
from utils import *

from binascii import hexlify, unhexlify

from sms import SMSmessage
import traceback


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
        rec_cnt = 6

	num_records = self.scc.record_count(path)
	print ("Native Applications: %d records available" % num_records)
	for record_id in range(1, num_records + 1):
		print self.scc.read_record(path, record_id)

        print

if __name__ == '__main__':
    device="/dev/ttyUSB0"
    baudrate = 9600
    sim = RsSIMReader(device, baudrate)
    sim.get_iccid()
    sim.get_native_apps()




