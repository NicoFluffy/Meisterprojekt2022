#-*- coding: utf-8 -*-
import serial, time
# https://www.electronicwings.com/raspberry-pi/raspberry-pi-uart-communication-using-python-and-c

class rpi_rs232:
    def __init__(self, baud=9600, rpi_port="ttyS0"):
        self.baud = int(baud)
        self.rpi_port = str(rpi_port)
    
    def send_data(self, command, type="raw"):
        ser = serial.Serial("/dev/{}".format(self.rpi_port), self.baud)
        if type == "RAW":
            ser.write(command)
        ser.close()
    