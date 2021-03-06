#
# Constants
#

# References
# http://www.cardwerk.com/smartcards/smartcard_standard_ISO7816-4_5_basic_organizations.aspx
# http://www.tech-invite.com/fo-uicc/tinv-fo-uicc-mf.html


###################################################################
#                                                                 #
# Master File                                                     #
#                                                                 #
# This is the root of the file structure on the ICC (SIM or UICC) #
#                                                                 #
###################################################################
MF = '3F00'


###################################################################
#                                                                 #
# International  Mobile  Subscriber  Identity                     #
#                                                                 #
# EF of IMSI is defined inside DF of GSM                          #
#                                                                 #
###################################################################
EF_IMSI = '6F07'


###################################################################
#                                                                 #
# MSISDN is a number uniquely identifying a subscription in a GSM #
# or a UMTS mobile network                                        #
#                                                                 #
# EF of MSISDN is defined inside DF of TELECOM                    #
#                                                                 #
###################################################################
EF_MSISDN = '6F40'

DF_TELECOM     = '7F10'
DF_PHONEBOOK   = '5F3A'
DF_GRAPHICS    = '5F50'

DF_GSM         = '7F20'
EF_ADN         = '6F3A'
EF_SMS         = '6F3C'
EF_FDN         = '6F3B'
EF_LND         = '6F44'
EF_SPN         = '6F46'



SCARD_PROTOCOL_T0   = 1
SCARD_PROTOCOL_T1   = 2

SIM_STATE_DISCONNECTED  = 0
SIM_STATE_CONNECTED     = 1

SW_OK                   = '9000'
SW_FOLDER_SELECTED_OK   = '9F17'
SW_FILE_SELECTED_OK     = '9F0F'

CHV_ALWAYS              = 0
CHV_READ                = 1
CHV_UPDATE              = 2

ATTRIBUTE_ATR               = 0x90303
ATTRIBUTE_VENDOR_NAME       = 0x10100
ATTRIBUTE_VENDOR_SERIAL_NO  = 0x10103
