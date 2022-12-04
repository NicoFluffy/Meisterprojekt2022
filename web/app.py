from flask import Flask, render_template
import time
import serial
app = Flask(__name__)

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

def getSerial():
        return serial.Serial(
                port='/dev/ttyUSB0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
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




@app.route("/")
def home():
    buttons = [("Lokale-Präsentation","/rs232/hdmi1",0),("Videokonferenz (Zoom)","/Displayport",0),("Mute","/Mic Mute","btn-danger")]
    return render_template("home.html",buttons=buttons)

@app.route("/test")
def test():
    gustaf = ["nico", "marc", "Valerie"]
    return render_template("test.html",names=gustaf)

@app.route("/rs232/<command>")
def r232(command):
    cmds = []
    if command == "hdmi1":
        cmds = ["hdmi1"]
    elif command == "hdmi2":
        cmds = ["hdmi2"]
    
    if len(cmds) == 0:
        return ""
    
    runCmds(cmds)
    return "ok"