#Import der Python Module
import RPi.GPIO as GPIO
import pins
import time
from threading import  Lock

#Variablen definieren



# Wer darf gerade arbeiten
mutex = Lock()

#GPIOs mit GPIO-Nummer ansprechen
GPIO.setmode(GPIO.BCM)

#Ein- und Ausgaenge definieren
GPIO.setup(pins.PIR_Sensor, GPIO.IN)
GPIO.setup(pins.UP, GPIO.OUT)
GPIO.setup(pins.DOWN, GPIO.OUT)
GPIO.output(pins.UP, True)
GPIO.output(pins.DOWN, True)

#Setup Lichtsensor
GPIO.setup(pins.LICHT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print("Das Programm wurde gestartet.")


#richtungen
# 0 = stehen
# 1 = runter
# 2 = hoch
def bewegung(richtung = 0):
    return
    mutex.acquire()
    
       
    if richtung == 1:
        GPIO.output(pins.UP, True)
        time.sleep(0.2)
        GPIO.output(pins.DOWN, False)
    elif richtung == 2:
        GPIO.output(pins.DOWN, True)
        time.sleep(0.2)
        GPIO.output(pins.UP, False)
    else:
        GPIO.output(pins.UP, True)
        GPIO.output(pins.DOWN, True)

    mutex.release()


def shutdown():
    GPIO.cleanup()


