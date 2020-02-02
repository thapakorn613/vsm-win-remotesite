import pywinusb.hid as hid
import time
import datetime

import math
import os
import sys

# import io
# import webbrowser
# import Queue


class gogoTalk:
    def __init__(self):

        self.version                        = 2

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

        self.countNoData = 0

        # self.hidGoGo will be NULL if connection error
        try:
            # self.hidGoGo = hid.device
            # self.hidGoGo.open(self.GOGO_VEDOR_ID, self.GOGO_PRODUCT_ID)
            device = hid.HidDeviceFilter(vendor_id = 0x0461, product_id = 0x0020).get_devices()[0]
            self.hidGoGo = hid.HidDevice
            print(device)
            print("self.hidGoGo : ",self.hidGoGo)
            print("\n")
            # device.open()

            # for out_report in device.find_output_reports():
            #     print("send init packet")
            #     initPkt = [0, 0 , 11]
            #     if out_report.send(initPkt):
            #         print("success")
            #     time.sleep(1)
            # self.hidGoGo = hid.device(self.GOGO_VEDOR_ID, self.GOGO_PRODUCT_ID)

        except IOError as ex:
            print (ex)
            self.hidGoGo = None

    def processCommand(self, command):
        print('command ' + command)
        command = command.split('::')
        del command[0]
        if command[0] == 'ledOn':
            self.ledControl(0,1)  # 0 = the default user led, 1 = 0n
        elif command[0] == 'ledOff':
            self.ledControl(0,0)  # 0 = the default user led, 0 = 0ff
        elif command[0] == 'beep':
            self.beep()
        elif command[0] == 'motorOn':
            self.mOn()
        elif command[0] == 'motorOff':
            self.mOff()
        elif command[0] == 'motorRD':
            self.mRD()
        elif command[0] == 'motorCW':
            self.mCW()
        elif command[0] == 'motorCCW':
            self.mCCW()
        elif command[0] == 'talkToMotor':
            self.talkToMotor(command[1])
        elif command[0] == 'setPower':
            self.setPower(command[1])
        elif command[0] == 'runStop':
            self.LogoControl(2)

    def processNone(self):
        print("Gogo complete none!!!!")

    def setFirmwareProgressCallback(self, function):
        self.firmwareProgressCallback = function


    def downloadLogoCode(self, logoBinaryString):
        ''' Download Logo Byte code to the gogo board
        
            It automatically sets the memory ponter to 0 and
            downloads the code
        '''

        print("Sent Logo mem pointer to 0")
        self.setLogoMemoryPointer(0)

        print ("download the bin code")
        # send the Logo binary code

        self.writeFlashMemory(logoBinaryString)
        self.ledControl(1,0)
        self.beep()




    def setLogoMemoryPointer(self, pointer):
        ''' Set memory point to address 0.
            Note that this memeory address is relative to the 
            Logo code area in the processor's flash memory.
            See setFlashMemoryPointer if you need to point to 
            an absolute flash memory location 
        '''
        cmdList                     = [0]*self.TX_PACKET_SIZE
        cmdList[self.ENDPOINT]      = self.ENDPOINT_ID
        cmdList[self.CATEGORY_ID]   = self.CATEGORY_MEMORY_CONTROL
        cmdList[self.CMD_ID]        = self.MEM_LOGO_SET_POINTER
        cmdList[self.PARAMETER1]    = 0
        cmdList[self.PARAMETER2]    = 0
        self.sendCommand(cmdList)        


    def setFlashMemoryPointer(self, pointer):
        ''' Sets memory pointer to a raw location on the processor
        '''
        #print "Set flash pointer to " + hex(pointer)
        cmdList                     = [0]*self.TX_PACKET_SIZE
        cmdList[self.ENDPOINT]      = self.ENDPOINT_ID
        cmdList[self.CATEGORY_ID]   = self.CATEGORY_MEMORY_CONTROL
        cmdList[self.CMD_ID]        = self.MEM_SET_POINTER
        cmdList[self.PARAMETER1]    = pointer >> 8
        cmdList[self.PARAMETER2]    = pointer & 0xff
        self.sendCommand(cmdList)
        

    def writeFlashMemory(self, content):
        ''' Write content to the flash memory '''

        txLength = len(content)

        totalLoops = int(math.ceil(len(content)/ float((self.TX_PACKET_SIZE-4))))
        # loop and send data 'self.TX_PACKET_SIZE-4' bytes at a time

        for j in range(totalLoops):
            self.firmwareProgressCallback(j, totalLoops) # calls to let parent update the ui
            #self.firmwareProgressCallback.configure(maximum = totalLoops, value=j ) # calls to let parent update the ui

            #print str(j) + "/" + str(totalLoops)
            cmdList                     = [0]*self.TX_PACKET_SIZE
            cmdList[self.ENDPOINT]      = self.ENDPOINT_ID
            cmdList[self.CATEGORY_ID]   = self.CATEGORY_MEMORY_CONTROL
            cmdList[self.CMD_ID]        = self.MEM_WRITE
            
            # if the content cannot fit in one packet
            if txLength > (self.TX_PACKET_SIZE-4):
                cmdList[self.PARAMETER1]    = self.TX_PACKET_SIZE-4
                txLength -= self.TX_PACKET_SIZE-4
            else:
                cmdList[self.PARAMETER1]    = txLength

            # copy the content to be transmitted to the output buffer
            for i in range(cmdList[self.PARAMETER1]):
                cmdList[4+i] = content[(j*(self.TX_PACKET_SIZE-4))+i]

            self.sendCommand(cmdList)

            # this dealy allows the processor to finish writing the 
            # received content to the flash memory before receiving
            # more content
            time.sleep(0.01)

    def sendCommand(self, cmdBuffer):
        ''' Sends a command packet to the gogo board'''
        
        tries = 0

        while tries < self.RETRIES_ALLOWED:
            if self.hidGoGo != None:
                if self.hidGoGo.write(cmdBuffer) != len(cmdBuffer):
                    self.hidGoGo.close()
                    time.sleep(0.01)
                    print ("tries = " + str(tries))
                else:
                    return 1   # success

            try:
                device = hid.HidDeviceFilter(vendor_id = 0x0461, product_id = 0x0020).get_devices()[0]
                device.open()
                # self.hidGoGo = hid.device()
                # self.hidGoGo.open(self.GOGO_VEDOR_ID, self.GOGO_PRODUCT_ID)
            except IOError as ex:
                print (ex)
            tries += 1

        self.hidGoGo = None
        return 0  # failed

    def readPacket(self):

        try:

            if self.hidGoGo == None:
                #print "in Read Packet - reconnecting"
                # self.hidGoGo = hid.device(self.GOGO_VEDOR_ID, self.GOGO_PRODUCT_ID)
                device = hid.HidDeviceFilter(vendor_id = 0x0461, product_id = 0x0020).get_devices()[0]


            #print "Opening device"

            #h = hid.device(0x2405, 0x000a)
            #h = hid.device(0x1941, 0x8021) # Fine Offset USB Weather Station

            #print "Manufacturer: %s" % self.hidGoGo.get_manufacturer_string()
            #print "Product: %s" % self.hidGoGo.get_product_string()
            #print "Serial No: %s" % self.hidGoGo.get_serial_number_string()

            # try non-blocking mode by uncommenting the next line
            self.hidGoGo.set_nonblocking(1) # makes read() returns 0 if input buffer is empty

            d = self.hidGoGo.read(64)

            if len(d) == 63:
                self.countNoData = 0
                output = d
                # while len(d) == 63:
                #     output = d
                #     d = self.hidGoGo.read(64)

                return output

            elif len(d) == 0:  # no data
                self.countNoData += 1
                # if error is not null, then assume connection error and attempt to re-connect
                if self.hidGoGo.error() != "":
                    self.hidGoGo.close()
                    self.hidGoGo = None
                    return -1
                elif self.countNoData > 20:
                    self.countNoData = 0
                    self.hidGoGo = None
                    return -1
                else:
                    return None

            else:
                print ("unknown read packet len " + str(len(d)))
                return -1

        except IOError as ex:
            #print "in Read Packet, " + str(ex)
            self.hidGoGo = None
            #return None
            return -1
    def ping(self):
        ## for gogo board
        cmdList                     = [0]*self.TX_PACKET_SIZE
        cmdList[self.ENDPOINT]      = self.ENDPOINT_ID
        cmdList[self.CATEGORY_ID]   = self.CATEGORY_OUTPUT_CONTROL
        cmdList[self.CMD_ID]        = self.CMD_PING
        cmdList[self.PARAMETER1]    = 0
        self.sendCommand(cmdList)

    def ping(self,nodeAddress):
        ## for gogo wireless
        cmdList                     = [0]*self.TX_PACKET_SIZE
        cmdList[self.ENDPOINT]      = self.ENDPOINT_ID
        cmdList[self.CATEGORY_ID]   = self.CATEGORY_OUTPUT_CONTROL
        cmdList[self.CMD_ID]        = self.CMD_PING
        cmdList[self.PARAMETER1]    = 1
        cmdList[self.PARAMETER2]    = nodeAddress
        self.sendCommand(cmdList)

    def beep(self):
        cmdList                     = [0]*self.TX_PACKET_SIZE
        cmdList[self.ENDPOINT]      = self.ENDPOINT_ID
        cmdList[self.CATEGORY_ID]   = self.CATEGORY_OUTPUT_CONTROL
        cmdList[self.CMD_ID]        = self.CMD_BEEP
        self.sendCommand(cmdList)

    def setAutorun(self, state):
        '''
        :param state: 0 = disabled, 1 = enabled
        :return: none
        '''
        cmdList                     = [0]*self.TX_PACKET_SIZE
        cmdList[self.ENDPOINT]      = self.ENDPOINT_ID
        cmdList[self.CATEGORY_ID]   = self.CATEGORY_OUTPUT_CONTROL
        cmdList[self.CMD_ID]        = self.CMD_AUTORUN_STATE
        cmdList[self.PARAMETER1]    = state
        self.sendCommand(cmdList)

    def LogoControl(self, state):
        '''
        :param state: 0 = stop logo procedure, 1 = run logo procedure
        :return: none
        '''
        cmdList                     = [0]*self.TX_PACKET_SIZE
        cmdList[self.ENDPOINT]      = self.ENDPOINT_ID
        cmdList[self.CATEGORY_ID]   = self.CATEGORY_OUTPUT_CONTROL
        cmdList[self.CMD_ID]        = self.CMD_LOGO_CONTROL
        cmdList[self.PARAMETER1]    = state
        self.sendCommand(cmdList)





    def mOn(self):
        cmdList                     = [0]*self.TX_PACKET_SIZE
        cmdList[self.ENDPOINT]      = self.ENDPOINT_ID
        cmdList[self.CATEGORY_ID]   = self.CATEGORY_OUTPUT_CONTROL
        cmdList[self.CMD_ID]        = self.CMD_MOTOR_ON_OFF
        cmdList[self.PARAMETER1]    = 0
        cmdList[self.PARAMETER2]    = 1
        self.sendCommand(cmdList)

    def mOff(self):
        cmdList                     = [0]*self.TX_PACKET_SIZE
        cmdList[self.ENDPOINT]      = self.ENDPOINT_ID
        cmdList[self.CATEGORY_ID]   = self.CATEGORY_OUTPUT_CONTROL
        cmdList[self.CMD_ID]        = self.CMD_MOTOR_ON_OFF
        cmdList[self.PARAMETER1]    = 0
        cmdList[self.PARAMETER2]    = 0
        self.sendCommand(cmdList)

    def mCW(self):
        cmdList                     = [0]*self.TX_PACKET_SIZE
        cmdList[self.ENDPOINT]      = self.ENDPOINT_ID
        cmdList[self.CATEGORY_ID]   = self.CATEGORY_OUTPUT_CONTROL
        cmdList[self.CMD_ID]        = self.CMD_MOTOR_DIRECTION
        cmdList[self.PARAMETER1]    = 0
        cmdList[self.PARAMETER2]    = 1
        self.sendCommand(cmdList)

    def mCCW(self):
        cmdList                     = [0]*self.TX_PACKET_SIZE
        cmdList[self.ENDPOINT]      = self.ENDPOINT_ID
        cmdList[self.CATEGORY_ID]   = self.CATEGORY_OUTPUT_CONTROL
        cmdList[self.CMD_ID]        = self.CMD_MOTOR_DIRECTION
        cmdList[self.PARAMETER1]    = 0
        cmdList[self.PARAMETER2]    = 0
        self.sendCommand(cmdList)

    def mRD(self):
        cmdList                     = [0]*self.TX_PACKET_SIZE
        cmdList[self.ENDPOINT]      = self.ENDPOINT_ID
        cmdList[self.CATEGORY_ID]   = self.CATEGORY_OUTPUT_CONTROL
        cmdList[self.CMD_ID]        = self.CMD_MOTOR_RD
        cmdList[self.PARAMETER1]    = 0
        self.sendCommand(cmdList)

    def talkToMotor(self, motorBits):
        cmdList                     = [0]*self.TX_PACKET_SIZE
        cmdList[self.ENDPOINT]      = self.ENDPOINT_ID
        cmdList[self.CATEGORY_ID]   = self.CATEGORY_OUTPUT_CONTROL
        cmdList[self.CMD_ID]        = self.CMD_SET_ACTIVE_PORTS
        cmdList[self.PARAMETER1]    = int(motorBits)
        self.sendCommand(cmdList)

    def setPower(self, powerLevel):
        cmdList                     = [0]*self.TX_PACKET_SIZE
        cmdList[self.ENDPOINT]      = self.ENDPOINT_ID
        cmdList[self.CATEGORY_ID]   = self.CATEGORY_OUTPUT_CONTROL
        cmdList[self.CMD_ID]        = self.CMD_SET_POWER
        cmdList[self.PARAMETER1]    = 0  # target motors = 0 = currently selected motors
        cmdList[self.PARAMETER2]    = int(powerLevel)>>8      # highbyte
        cmdList[self.PARAMETER3]    = int(powerLevel) & 0xff  # lowbyte

        self.sendCommand(cmdList)
        
    def setServoDuty(self, duty):
        cmdList                     = [0]*self.TX_PACKET_SIZE
        cmdList[self.ENDPOINT]      = self.ENDPOINT_ID
        cmdList[self.CATEGORY_ID]   = self.CATEGORY_OUTPUT_CONTROL
        cmdList[self.CMD_ID]        = self.CMD_SET_SERVO_DUTY
        cmdList[self.PARAMETER1]    = 0  # target motors = 0 = currently selected motors
        cmdList[self.PARAMETER2]    = int(duty)>>8      # highbyte
        cmdList[self.PARAMETER3]    = int(duty) & 0xff  # lowbyte

        self.sendCommand(cmdList)



    def motorToggleA(self):
        self.toggleMotor(0)
    def motorToggleB(self):
        self.toggleMotor(1)
    def motorToggleC(self):
        self.toggleMotor(2)
    def motorToggleD(self):
        self.toggleMotor(3)

    def toggleMotor(self, motorNumber):

        cmdList                     = [0]*self.TX_PACKET_SIZE
        cmdList[self.ENDPOINT]      = self.ENDPOINT_ID
        cmdList[self.CATEGORY_ID]   = self.CATEGORY_OUTPUT_CONTROL
        cmdList[self.CMD_ID]        = self.CMD_TOGGLE_ACTIVE_PORT
        cmdList[self.PARAMETER1]    = motorNumber
        self.sendCommand(cmdList)

    def ledControl(self, ledID, onOffState):
        cmdList                     = [0]*self.TX_PACKET_SIZE
        cmdList[self.ENDPOINT]      = self.ENDPOINT_ID
        cmdList[self.CATEGORY_ID]   = self.CATEGORY_OUTPUT_CONTROL
        cmdList[self.CMD_ID]        = self.CMD_LED_CONTROL
        cmdList[self.PARAMETER1]    = ledID   # 0 = the default user LED
        cmdList[self.PARAMETER2]    = onOffState  # 0 = off , 1 = on
        self.sendCommand(cmdList)

    def reboot(self):
        cmdList                     = [0]*self.TX_PACKET_SIZE
        cmdList[self.ENDPOINT]      = self.ENDPOINT_ID
        cmdList[self.CATEGORY_ID]   = self.CATEGORY_OUTPUT_CONTROL
        cmdList[self.CMD_ID]        = self.CMD_REBOOT
        self.sendCommand(cmdList)

    def syncRTC(self, dateTimeList):
        cmdList                     = [0]*self.TX_PACKET_SIZE
        cmdList[self.ENDPOINT]      = self.ENDPOINT_ID
        cmdList[self.CATEGORY_ID]   = self.CATEGORY_OUTPUT_CONTROL
        cmdList[self.CMD_ID]        = self.CMD_SYNC_RTC
        for i in range(len(dateTimeList)):
            cmdList[self.PARAMETER1 + i] = dateTimeList[i]

        self.sendCommand(cmdList)


    def readRTC(self):
        cmdList                     = [0]*self.TX_PACKET_SIZE
        cmdList[self.ENDPOINT]      = self.ENDPOINT_ID
        cmdList[self.CATEGORY_ID]   = self.CATEGORY_OUTPUT_CONTROL
        cmdList[self.CMD_ID]        = self.CMD_READ_RTC
        self.sendCommand(cmdList)


    def showShortText(self, text):
        cmdList                     = [0]*self.TX_PACKET_SIZE
        cmdList[self.ENDPOINT]      = self.ENDPOINT_ID
        cmdList[self.CATEGORY_ID]   = self.CATEGORY_OUTPUT_CONTROL
        cmdList[self.CMD_ID]        = self.CMD_SHOW_SHORT_TEXT
        i=0
        for c in text:
            cmdList[self.PARAMETER1 + i]    = ord(c)
            i+=1
        cmdList[self.PARAMETER1 + i]    = 0 # terminates the string

        self.sendCommand(cmdList)

    def showLongText(self, text):
        cmdList                     = [0]*self.TX_PACKET_SIZE
        cmdList[self.ENDPOINT]      = self.ENDPOINT_ID
        cmdList[self.CATEGORY_ID]   = self.CATEGORY_OUTPUT_CONTROL
        cmdList[self.CMD_ID]        = self.CMD_SHOW_LONG_TEXT
        i=0
        for c in text:
            cmdList[self.PARAMETER1 + i]    = ord(c)
            i+=1
        cmdList[self.PARAMETER1 + i]    = 0 # terminates the string

        self.sendCommand(cmdList)

    def LCDclearText(self):
        cmdList                     = [0]*self.TX_PACKET_SIZE
        cmdList[self.ENDPOINT]      = self.ENDPOINT_ID
        cmdList[self.CATEGORY_ID]   = self.CATEGORY_OUTPUT_CONTROL
        cmdList[self.CMD_ID]        = self.CMD_CLEAR_SCREEN

        self.sendCommand(cmdList)

    def voiceModuleControl(self, command, trackNumber=-1):
        cmdList                     = [0]*self.TX_PACKET_SIZE
        cmdList[self.ENDPOINT]      = self.ENDPOINT_ID
        cmdList[self.CATEGORY_ID]   = self.CATEGORY_OUTPUT_CONTROL

        if command.lower().strip() =="play":
            cmdList[self.CMD_ID]        = self.CMD_VOICE_PLAY_PAUSE
        elif command.lower().strip() =="nexttrack":
            cmdList[self.CMD_ID]        = self.CMD_VOICE_NEXT_TRACK
        elif command.lower().strip() =="prevtrack":
            cmdList[self.CMD_ID]        = self.CMD_VOICE_PREV_TRACK
        elif command.lower().strip() =="gototrack":
            cmdList[self.CMD_ID]        = self.CMD_VOICE_GOTO_TRACK
            cmdList[self.PARAMETER1]    = trackNumber
        elif command.lower().strip() =="erasetracks":
            cmdList[self.CMD_ID]        = self.CMD_VOICE_ERASE_ALL_TRACKS
        self.sendCommand(cmdList)



    def i2cWrite(self, i2cAddress, i2cRegisterIndex, i2cPayload):
        cmdList                     = [0]*self.TX_PACKET_SIZE
        cmdList[self.ENDPOINT]      = self.ENDPOINT_ID
        cmdList[self.CATEGORY_ID]   = self.CATEGORY_OUTPUT_CONTROL
        cmdList[self.CMD_ID]        = self.CMD_I2C_WRITE
        cmdList[self.PARAMETER1]    = i2cAddress
        cmdList[self.PARAMETER2]    = i2cRegisterIndex    
        cmdList[self.PARAMETER3]    = len(i2cPayload)
        for i in range(len(i2cPayload)):
            cmdList[self.PARAMETER4 + i] = i2cPayload[i]
        self.sendCommand(cmdList)

    def i2cRead(self, i2cAddress, i2cRegisterIndex, i2cReadLength):
        cmdList                     = [0]*self.TX_PACKET_SIZE
        cmdList[self.ENDPOINT]      = self.ENDPOINT_ID
        cmdList[self.CATEGORY_ID]   = self.CATEGORY_OUTPUT_CONTROL
        cmdList[self.CMD_ID]        = self.CMD_I2C_READ
        cmdList[self.PARAMETER1]    = i2cAddress
        cmdList[self.PARAMETER2]    = i2cRegisterIndex    
        cmdList[self.PARAMETER3]    = i2cReadLength
        self.sendCommand(cmdList)



    def rpiCameraControl(self, camera_on_state):
        cmdList                     = [0]*self.TX_PACKET_SIZE
        cmdList[self.ENDPOINT]      = self.ENDPOINT_ID
        cmdList[self.CATEGORY_ID]   = self.CATEGORY_RASPBERRY_PI_CONTROL
        cmdList[self.CMD_ID]        = self.RPI_CAMERA_CONTROL
        cmdList[self.PARAMETER1]    = camera_on_state  # 0 = off , 1 = on

        self.sendCommand(cmdList)

    def rpiFindFaceControl(self, find_face_state):
        cmdList                     = [0]*self.TX_PACKET_SIZE
        cmdList[self.ENDPOINT]      = self.ENDPOINT_ID
        cmdList[self.CATEGORY_ID]   = self.CATEGORY_RASPBERRY_PI_CONTROL
        cmdList[self.CMD_ID]        = self.RPI_FIND_FACE_CONTROL
        cmdList[self.PARAMETER1]    = find_face_state  # 0 = disable , 1 = enable

        self.sendCommand(cmdList)

    def rpiTakeSnapshot(self):
        cmdList                     = [0]*self.TX_PACKET_SIZE
        cmdList[self.ENDPOINT]      = self.ENDPOINT_ID
        cmdList[self.CATEGORY_ID]   = self.CATEGORY_RASPBERRY_PI_CONTROL
        cmdList[self.CMD_ID]        = self.RPI_TAKE_SNAPSHOT
        cmdList[self.PARAMETER1]    = 1  # 1 = save image, 0 = preview only

        self.sendCommand(cmdList)

    def rpiCameraPreview(self):
        cmdList                     = [0]*self.TX_PACKET_SIZE
        cmdList[self.ENDPOINT]      = self.ENDPOINT_ID
        cmdList[self.CATEGORY_ID]   = self.CATEGORY_RASPBERRY_PI_CONTROL
        cmdList[self.CMD_ID]        = self.RPI_TAKE_SNAPSHOT
        cmdList[self.PARAMETER1]    = 0  # 1 = save image, 0 = preview only

        self.sendCommand(cmdList)

    def rpiWifiConnect(self, ssid, password=None):
        cmdList                     = [0]*self.TX_PACKET_SIZE
        cmdList[self.ENDPOINT]      = self.ENDPOINT_ID
        cmdList[self.CATEGORY_ID]   = self.CATEGORY_RASPBERRY_PI_CONTROL
        cmdList[self.CMD_ID]        = self.RPI_WIFI_CONNECT
        if password is not None:
            parameterString = ssid + ',' + password
        else:
            parameterString = ssid + ','

        cmdList[self.PARAMETER1]    = len(parameterString)
        i = 0
        for c in parameterString:
            cmdList[self.PARAMETER2 + i] = ord(parameterString[i])
            i += 1

        self.sendCommand(cmdList)

    def rpiWifiDisonnect(self):
        cmdList                     = [0]*self.TX_PACKET_SIZE
        cmdList[self.ENDPOINT]      = self.ENDPOINT_ID
        cmdList[self.CATEGORY_ID]   = self.CATEGORY_RASPBERRY_PI_CONTROL
        cmdList[self.CMD_ID]        = self.RPI_WIFI_DISCONNECT
        self.sendCommand(cmdList)

    def rpiEmailConfig(self, email_user, email_password):
        cmdList                     = [0]*self.TX_PACKET_SIZE
        cmdList[self.ENDPOINT]      = self.ENDPOINT_ID
        cmdList[self.CATEGORY_ID]   = self.CATEGORY_RASPBERRY_PI_CONTROL
        cmdList[self.CMD_ID]        = self.RPI_EMAIL_CONFIG
        parameterString = email_user + ',' + email_password
        print (parameterString)
        cmdList[self.PARAMETER1]    = len(parameterString)
        i = 0
        for c in parameterString:
            cmdList[self.PARAMETER2 + i] = ord(parameterString[i])
            i += 1

        self.sendCommand(cmdList)

    def rpiEmailSend(self, email_recipient, email_subject, email_body):
        cmdList                     = [0]*self.TX_PACKET_SIZE
        cmdList[self.ENDPOINT]      = self.ENDPOINT_ID
        cmdList[self.CATEGORY_ID]   = self.CATEGORY_RASPBERRY_PI_CONTROL
        cmdList[self.CMD_ID]        = self.RPI_EMAIL_SEND
        parameterString = email_recipient + ',' +email_subject + ',' + email_body
        print (parameterString)
        cmdList[self.PARAMETER1]    = len(parameterString)
        i = 0
        for c in parameterString:
            cmdList[self.PARAMETER2 + i] = ord(parameterString[i])
            i += 1

        self.sendCommand(cmdList)

    def rpiSMSSend(self, sms_number, sms_message):
        cmdList                     = [0]*self.TX_PACKET_SIZE
        cmdList[self.ENDPOINT]      = self.ENDPOINT_ID
        cmdList[self.CATEGORY_ID]   = self.CATEGORY_RASPBERRY_PI_CONTROL
        cmdList[self.CMD_ID]        = self.RPI_SMS_SEND
        parameterString = sms_number + ',' +sms_message
        print (parameterString)
        cmdList[self.PARAMETER1]    = len(parameterString)
        i = 0
        for c in parameterString:
            cmdList[self.PARAMETER2 + i] = ord(parameterString[i])
            i += 1

        self.sendCommand(cmdList)

    def rpiSetRpiTxBuffer(self, index, value):
        cmdList                     = [0]*self.TX_PACKET_SIZE
        cmdList[self.ENDPOINT]      = self.ENDPOINT_ID
        cmdList[self.CATEGORY_ID]   = self.CATEGORY_RASPBERRY_PI_CONTROL
        cmdList[self.CMD_ID]        = self.RPI_SET_TX_BUFFER
        cmdList[self.PARAMETER1]    = index
        cmdList[self.PARAMETER2]    = value
        self.sendCommand(cmdList)

    def rpiClearScreenTappedFlag(self):
        RPI_SCREEN_TAP              = 20
        self.rpiSetRpiTxBuffer(RPI_SCREEN_TAP, 0)


    def rpiReboot(self):
        cmdList                     = [0]*self.TX_PACKET_SIZE
        cmdList[self.ENDPOINT]      = self.ENDPOINT_ID
        cmdList[self.CATEGORY_ID]   = self.CATEGORY_RASPBERRY_PI_CONTROL
        cmdList[self.CMD_ID]        = self.RPI_REBOOT
        self.sendCommand(cmdList)

    def rpiShutdown(self):
        cmdList                     = [0]*self.TX_PACKET_SIZE
        cmdList[self.ENDPOINT]      = self.ENDPOINT_ID
        cmdList[self.CATEGORY_ID]   = self.CATEGORY_RASPBERRY_PI_CONTROL
        cmdList[self.CMD_ID]        = self.RPI_SHUTDOWN
        self.sendCommand(cmdList)


# if __name__ == '__main__':
#     gogo = gogoTalk()
#     gogo.beep()

#     gogo.talkToMotor(0b1)
#     while (1):
#         gogo.setServoDuty(20)
#         time.sleep(1)
#         gogo.setServoDuty(40)
#         time.sleep(1)
