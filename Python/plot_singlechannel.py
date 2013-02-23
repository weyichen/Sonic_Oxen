from pylab import *
import numpy
import serial
from time import sleep

ser = serial.Serial(4, baudrate=57600, timeout=1)
ser.setRTS(True) #?
ser.setRTS(False) #?

ion() # "interactive mode" on

lines = plot([],[])
for i in range(5) :
    lines[i].axes.set_ylim(-1000,1000)

def extend(line, xval, yval):
    line.set_xdata(numpy.append(line.get_xdata(), xval))
    line.set_ydata(numpy.append(line.get_ydata(), numpy.long(yval)))
    line.axes.set_xlim(xval-50,xval+50)
    #Draw the lines
    #draw()

time = 0

while time < 700:
    
    # plot one channel, up to 16-bit integers
	while ser.inWaiting() < 2:
		sleep(0.01)
	bytes = ser.read(2)
	height = ord(bytes[0]) * 256 + ord(bytes[1])
    
    # convert height to signed int
    if (height >=
    
	print time, height
	extend(lines, time, height)
        
    draw()
    time += 1

ser.close