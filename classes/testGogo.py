
class testGogo:

    def process1(self):
        print("Gogo complete ledOn ")

    def process2(self):
        print("Gogo complete beep")

    def processNone(self):
        print("Gogo complete none!!!!")

    def processCommand(self, command):
        print('command ' + command)
        command = command.split('::')
        # del command[0]
        print ("command[0] : "+command[0])
        if (command == "onOff"):
            self.process1()  # 0 = the default user led, 1 = 0n
        elif (command == "beep"):
            self.process2()
        else :
            self.processNone()