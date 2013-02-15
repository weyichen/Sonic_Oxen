from pylab import *
#import matplotlib.pyplot as plt
import numpy
import serial
from time import sleep

ser = serial.Serial(3, baudrate=115200, timeout=1)
ser.setRTS(True) #?
ser.setRTS(False) #?

ion() # "interactive mode" on

lines = plot([],[],[],[],[],[],[],[],[],[])
for i in range(5) :
    lines[i].axes.set_ylim(-2000000,2000000)

def extend(line, xval, yval):
    line.set_xdata(numpy.append(line.get_xdata(), xval))
    line.set_ydata(numpy.append(line.get_ydata(), numpy.long(yval)))
    line.axes.set_xlim(xval-50,xval+50)
    #Draw the lines
    #draw()

time = 0

while time < 200:
    
    # plot one channel, up to 16-bit integers
	# while ser.inWaiting() < 2:
		# sleep(0.01)
	# bytes = ser.read(2)
	# height = ord(bytes[0]) * 256 + ord(bytes[1])
	# print time, height
	# extend(line, time, height)
	# time += 1
    
    # plot 5 channels, up to 1-byte integers
    # while ser.inWaiting() < 5:
        # sleep(0.01)
        
    # for i in range(5):
        # byte = ser.read(1)
        # height = ord(byte)
        # extend(lines[i], time, height)
        
    # plot 5 channels, up to 4-byte integers (long)
    while ser.inWaiting() < 20:
        sleep(0.01)
        
    for i in range(5):
        bytes = ser.read(4)
        height = (ord(bytes[0]) << 24) + (ord(bytes[1]) << 16) + (ord(bytes[2]) << 8) + ord(bytes[3])
        
        # convert to signed long
        if (height >= 0x80000000):
            height = height - 0x100000000
        #print time, height
        extend(lines[i], time, height) 
    
    draw()
    time += 1

ser.close