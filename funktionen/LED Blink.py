from gpiozero import LED
from time import sleep

green = LED(23)
zahl = 0
while vzahl<10:
    zahl = zahl +1
    gr.on()
    sleep(1)
    green.off()
    sleep(1)