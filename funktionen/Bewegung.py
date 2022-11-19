#Import der Python Module
import RPi.GPIO as GPIO
import time
from threading import Timer, Lock

#Variablen definieren
PIR_Sensor = 24
LIFT = 23
LAUFZEIT = 5
timer = 0

mutex = Lock()

#GPIOs mit GPIO-Nummer ansprechen
GPIO.setmode(GPIO.BCM)

#Ein- und Ausgaenge definieren
GPIO.setup(PIR_Sensor, GPIO.IN)
GPIO.setup(LIFT, GPIO.OUT)
GPIO.output(LIFT, True)

print("Das Programm wurde gestartet.")
    
#Einfahren
def einfahren():
    mutex.acquire()
    print("Down")
    GPIO.output(LIFT, True)
    global timer
    timer = 0
    mutex.release()

    #Ausfahren
def rausfahren(PIR_Sensor):
    mutex.acquire()
    global timer
    print("UP")
    if timer == 0:
        GPIO.output(LIFT, False)
    else:
        timer.cancel()
    timer = Timer(20.0,einfahren)
    timer.start()
    mutex.release()

#Hauptprogramm starten
if __name__ == "__main__":
    try:
        #Sobald eine Bewegung erkannt wurde, fuehre die Funktion aus.
        GPIO.add_event_detect(PIR_Sensor, GPIO.RISING, callback=rausfahren)
        while True:
            time.sleep(1)
        
    #Programm beenden mit Strg + c
    except KeyboardInterrupt:
        print ("Das Programm wurde beendet.")
        GPIO.cleanup()