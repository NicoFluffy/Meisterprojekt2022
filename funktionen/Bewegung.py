#Import der Python Module
import RPi.GPIO as GPIO
import time
from threading import Timer, Lock

#Variablen definieren
PIR_Sensor = 24
UP = 23
DOWN = 25
LAUFZEIT = 5
timer = 0

mutex = Lock()

#GPIOs mit GPIO-Nummer ansprechen
GPIO.setmode(GPIO.BCM)

#Ein- und Ausgaenge definieren
GPIO.setup(PIR_Sensor, GPIO.IN)
GPIO.setup(UP, GPIO.OUT)
GPIO.setup(DOWN, GPIO.OUT)
GPIO.output(UP, True)
GPIO.output(DOWN, True)

print("Das Programm wurde gestartet.")

Cooldown = 0
    
#Einfahren
def einfahren():
    mutex.acquire()
    print("Down")    
    GPIO.output(UP,True) 
    time.sleep(1)    
    GPIO.output(DOWN,False)
    time.sleep(30)
    global Cooldown
    Cooldown = time.time()
    GPIO.output(DOWN,True)
    global timer
    timer = 0
    mutex.release()

    #Ausfahren
def rausfahren(PIR_Sensor):
    mutex.acquire()
    global Cooldown
    now = time.time()
    if now < Cooldown+60*2:
        print("still Cooldown")
        mutex.release()
        return

    global timer
    print("UP")
    if timer == 0:
        GPIO.output(DOWN,True) 
        time.sleep(1)    
        GPIO.output(UP,False)
        time.sleep(30)
        GPIO.output(UP,True)
    else:
        timer.cancel()
    timer = Timer(30.0,einfahren)
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