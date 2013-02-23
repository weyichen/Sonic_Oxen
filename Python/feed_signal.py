from pylab import *
import numpy
import serial
from time import sleep

ser = serial.Serial(4, baudrate=57600, timeout=1)
ser.setRTS(True) #?
ser.setRTS(False) #?

with open(ecgfile, 'rU') as f:
    for line in f:
        upper = float(line) >> 8
        
        ser.write(line);
    