#!/usr/bin/env python
import time
import serial
import codecs
 
commandsmondo = {
  "poweron": "5b00100001",
  "poweroff": "5b00100000",
  "hdmi1": "5b00101000",
  "hdmi2": "5b00101001",
  "vga": "5b00101003",
  "ypbpr": "5b00101006",
  "av": "5b00101008",
  "dp1": "5b00101009",
  "getpoweron":""
}
#gibt eine Serielle Schnittstelle zurück
def getSerial():
        return serial.Serial(
                port='/dev/ttyUSB1', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1
        )

#Nimmt eine Liste aus Keys aus dem commandsmondo Dictionary
#und führt diese nacheinander aus
def runCmds(cmds):
        #hole eine Serielle Schnittstelle
        ser = getSerial()
        #für jeden command "x" in cmds
        for schluesselwort in cmds:
                # wenn commando = sleep, warte 10s
                if schluesselwort == "sleep":
                        time.sleep(10)
                        continue
                #hole das Kommando aus dem Dictionary  
                cmd=commandsmondo.get(schluesselwort)
                # printe einmal den command + den Text des commandsmondo
                print(schluesselwort, cmd)
                #wenn das Kommando nicht gefunden wurde
                if cmd == None:
                        #gehe zum nächsten Kommando
                        continue
                #führe Kommando aus
                ser.write(str.encode(commandsmondo.get(schluesselwort) + "\r"))
                #printe die Rückmeldung
                print(ser.read(64))
                #schlafe 4 Sekunden
                time.sleep(4)
        #schließe die Serielle Schnittstelle
        ser.close()





         
if __name__ == "__main__":
        
        runCmds(["poweroff", "sleep", "sleep", "poweron", "hdmi1", "dp1"])
        ser = getSerial()
        while 1:
                x = input()
                t = commandsmondo.get(x)
                if(t == None):
                        print("fehler")
                        continue
                
                ser.write(str.encode(t + "\r"))
                print(ser.read(64))