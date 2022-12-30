from flask import Flask, render_template
import time, threading
import serial
from flask_socketio import SocketIO
import atexit
from threading import Timer
import RPi.GPIO as GPIO

import bewegung
import pins

# Erstelle Flask APP mit SocketIO
app = Flask(__name__)
app.config['SECRET_KEY'] = 'superSecret!'
socketio = SocketIO(app)


# Ist PC verbunden?
pc = False
# Befehl den der PC noch zu starten hat
pcHasToDo = None

namespace_win = "/win"

#timer für Bewegungssensor
timer = 0
Cooldown = 10


@socketio.on('connect', namespace=namespace_win)
def test_connect():
    print('pc da')
    global pc 
    global pcHasToDo
    pc = True
    # Wenn der PC noch einen Befehl ausführen muss
    if pcHasToDo != None:
        #Rufe den Befehl auf
        cmd_pc(pcHasToDo)
        pcHasToDo = None


@socketio.on('disconnect', namespace=namespace_win)
def test_disconnect():
    print('pc weg')
    global pc
    pc = False

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
                time.sleep(0.5)
        #schließe die Serielle Schnittstelle
        ser.close()




@app.route("/")
def home():
    buttons = [("Lokale-Präsentation","/rs232/hdmi1",0),("Interner PC","/rs232/dp1",0),("Videokonferenz (Zoom)","/pc/zoom",0),("Videokonferenz (Teams)","/pc/teams",0),("Mute","/Mic Mute","btn-danger")]
    return render_template("home.html",buttons=buttons)

@app.route("/test")
def test():
    gustaf = ["nico", "marc", "Valerie"]
    return render_template("test.html",names=gustaf)

@app.route("/rs232/<command>")
def app_r232(command):
        print("hi app")
        return r232(command)


def r232(command):
    print("hi test")
    cmds = []
    if command == "hdmi1":
        cmds = ["poweron", "hdmi1"]
    elif command == "hdmi2":
        cmds = ["poweron", "hdmi2"]
    elif command == "dp1":
        cmds = ["poweron", "dp1"]
    elif command == "poweroff":
        cmds = ["poweroff"]
    if len(cmds) == 0:
        return ""
    print(cmds)
    runCmds(cmds)
    return "ok"


@app.route("/bewegung/<command>")
def bewege(command):
        bewegung.bewegung(int(command))
        return "ok"

@app.route("/pc/<command>")
def app_pc(command):
        print("pc app")
        return cmd_pc(command)


def cmd_pc(command):
        global pc
        print("pc cmd", pc)
        global pcHasToDo
        r232("dp1")
        #Falls der PC noch nicht verbunden ist
        if pc == False:
                print("pc nicht da")
                # Speichere Kommando
                pcHasToDo = command
                return "noch nicht ready"
        # sende Befehl an PC
        if command == "zoom":
                socketio.emit("message","zoom", namespace=namespace_win)
        elif command == "teams":
                socketio.emit("message", "teams",namespace=namespace_win)
        
        return "ok"


#Einfahren
def einfahren():
    r232("poweroff")
    bewegung.bewegung(1)
    time.sleep(30)
    bewegung.bewegung(0)
    global Cooldown
    Cooldown = time.time()
    global timer
    timer = 0

    #Ausfahren
def rausfahren(PIR_Sensor):
    global Cooldown
    now = time.time()
    if now < Cooldown+60*2:
        print("still Cooldown")
        return

    global timer
    print("UP")
    if timer == 0:
        r232("dp1")
        bewegung.bewegung(2)
    else:
        timer.cancel()
    timer = Timer(30.0,einfahren)
    timer.start()

def licht(channel):
    p = GPIO.input(pins.LICHT)
    if p == False:
    #hat licht
        print("habe licht")
    else: 
    #hat kein licht
        print("habe kein licht")


def delayLicht():
    while True:
        time.sleep(10)
        licht(0)
# Erstelle Thread für die Licht Überprüfung
lichtThread = threading.Thread(target=lambda: delayLicht())
lichtThread.start()

#starte Bewegungsensor
#GPIO.add_event_detect(pins.PIR_Sensor, GPIO.RISING, callback=rausfahren)


def OnExitApp():
        print("shutting down gpio")
        bewegung.shutdown()

atexit.register(OnExitApp)

licht(pins.LICHT)
licht(pins.LICHT)

if __name__ == '__main__':
    socketio.run(app)
