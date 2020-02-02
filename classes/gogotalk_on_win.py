import serial
import time
import sys
from pywinusb import hid

class gogoTalkOnWin:
    def __init__(self):

        self.version                        = 1

        self.GOGO_VEDOR_ID = 0x461
        self.GOGO_PRODUCT_ID = 0x20
        self.ENDPOINT_ID = 0

        # board types
        self.GOGOBOARD                     = 1
        self.PITOPPING                     = 2
        self.WIRELESSGOGO                  = 3

        # category names
        self.CATEGORY_OUTPUT_CONTROL        = 0
        self.CATEGORY_MEMORY_CONTROL        = 1
        self.CATEGORY_RASPBERRY_PI_CONTROL  = 2

        # Output contorl command names
        self.CMD_PING                          = 1
        self.CMD_MOTOR_ON_OFF                  = 2
        self.CMD_MOTOR_DIRECTION               = 3
        self.CMD_MOTOR_RD                      = 4
        self.CMD_SET_POWER                     = 6
        self.CMD_SET_ACTIVE_PORTS              = 7
        self.CMD_TOGGLE_ACTIVE_PORT            = 8
        self.CMD_SET_SERVO_DUTY                = 9
        self.CMD_LED_CONTROL                   = 10
        self.CMD_BEEP                          = 11
        self.CMD_AUTORUN_STATE                 = 12
        self.CMD_LOGO_CONTROL                  = 13
        self.CMD_SYNC_RTC                      = 50
        self.CMD_READ_RTC                       = 51
        self.CMD_SHOW_SHORT_TEXT               = 60
        self.CMD_SHOW_LONG_TEXT                = 61
        self.CMD_CLEAR_SCREEN                  = 62
        
        self.CMD_VOICE_PLAY_PAUSE              = 70
        self.CMD_VOICE_NEXT_TRACK              = 71
        self.CMD_VOICE_PREV_TRACK              = 72
        self.CMD_VOICE_GOTO_TRACK              = 73
        self.CMD_VOICE_ERASE_ALL_TRACKS        = 74

        self.CMD_I2C_WRITE                     = 14
        self.CMD_I2C_READ                      = 15 


        self.CMD_REBOOT                        = 100


        # Memory control command names
        self.MEM_LOGO_SET_POINTER               = 1
        self.MEM_SET_POINTER                    = 2
        self.MEM_WRITE                          = 3
        self.MEM_READ                           = 4

        # Raspberry Pi Commands

        self.RPI_SHUTDOWN                       = 1
        self.RPI_REBOOT                         = 2
        self.RPI_CAMERA_CONTROL                 = 10
        self.RPI_FIND_FACE_CONTROL              = 11
        self.RPI_TAKE_SNAPSHOT                  = 12

        self.RPI_WIFI_CONNECT                   = 15
        self.RPI_WIFI_DISCONNECT                = 16

        self.RPI_EMAIL_CONFIG                   = 17
        self.RPI_EMAIL_SEND                     = 18
        self.RPI_SMS_SEND                       = 19

        self.RPI_SET_TX_BUFFER                  = 20

        self.RPI_RFID_INIT                      = 25
        self.RPI_RFID_COMMAND                   = 26

        # output buffer location names
        self.ENDPOINT               = 0
        self.CATEGORY_ID            = 1
        self.CMD_ID                 = 2
        self.PARAMETER1             = 3
        self.PARAMETER2             = 4
        self.PARAMETER3             = 5
        self.PARAMETER4             = 6
        self.PARAMETER5             = 7
        self.PARAMETER6             = 8
        self.PARAMETER7             = 9

        self.TX_PACKET_SIZE = 64
        self.RX_PACKET_SIZE = 64

        self.RETRIES_ALLOWED = 5  # number of attempts to connect to HID device

        self.firmware_length = 0
        # * firmware init packet: 0x54 0xfe 0x04 0x00 0x00 0xc9 0xc9
        self.gblPkt = []
        
        self.initPkt = [0x00, 0x00, 0xc9]
        self.beepPkt  = [0x00, 0x00, self.CMD_BEEP]
        self.mOnPkt  = [0x00, 0x00, self.CMD_MOTOR_ON_OFF,0x01]
        self.mOffPkt  = [0x00, 0x00, self.CMD_MOTOR_ON_OFF,0x00]
        self.talkMotorPkt  = [0x00, 0x00, self.CMD_TOGGLE_ACTIVE_PORT]
        

    def beep(self):
        print(" cmd beep! ")
        self.gblPkt = self.beepPkt
        self.processCMD()
        
    def mOn(self):
        print(" cmd mOnPkt! ")
        self.gblPkt = self.mOnPkt
        self.processCMD()

    def mOff(self):
        print(" cmd mOffPkt! ")
        self.gblPkt = self.mOffPkt
        self.processCMD()

    def talkToMotor(self,number):
        print(" cmd talk motor! : ",number)
        self.gblPkt = self.talkMotorPkt
        self.gblPkt.insert(4,int(number))
        self.processCMD()

    def processNone(self):
        print(" none command ! ")
        self.gblPkt = self.initPkt
        self.processCMD()

    def processCMD(self):
        device = hid.HidDeviceFilter(vendor_id=0x0461, product_id=0x0020).get_devices()[0]
        device.open()
        
        for out_report in device.find_output_reports():
            SIZE = 64

            buffer = [0 for i in range(SIZE-len(self.gblPkt))]
            self.gblPkt.extend(buffer)
            print(self.gblPkt, len(self.gblPkt))

            # print("send init packet")
            if out_report.send(self.gblPkt):
                print("send packet success")
            time.sleep(0.01)

    


# if __name__ == "__main__":
#     gogoTalkOnWin.gogoTalk()
#     print("finish")
