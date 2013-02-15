import matplotlib.pyplot as plt
import numpy
import serial
import traceback
from time import sleep
from pylab import *

ion()

ser = serial.Serial(3, baudrate=9600, timeout=1)
ser.setRTS(True)
ser.setRTS(False)

x = arange(0,10,500)            # x-array
y = [0] * len(x)
line, = plot(x,y)

def extend(yval) :
    #line.set_xdata(numpy.append(line.get_xdata(), xval))
    #line.set_ydata(numpy.append(line.get_ydata(), yval))
    line.set_ydata(numpy.append(line.get_ydata()[1:], yval))
    draw()
    
for time in range(200) :
    while ser.inWaiting() < 2: # 2 bytes per 16-bit integer
        sleep(.001)
    bytes = ser.read(2)
    height = ord(bytes[0]) * 256 + ord(bytes[1])
    #print time, height
    extend(height)

#plt.canvas.draw()
#plt.show()

ser.close()
    