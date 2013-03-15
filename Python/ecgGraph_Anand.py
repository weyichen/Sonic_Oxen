from pylab import *
import numpy
import serial
from time import *

ion() # "interactive mode" on

# Length of data buffer
BUF_LEN = 128

# Time between samples
timestep = 1

# Period of 1 draw cycle
period = BUF_LEN * timestep

# Expected sample value range
height = 2000000

# X values
times = numpy.arange(0, period, timestep)

channels = 5
# Y values
samples = numpy.zeros([BUF_LEN, channels])

lines = plot(times, samples)
for i in range(channels) :
    lines[i].axes.set_ylim(-height, height)
    lines[i].axes.set_xlim(-timestep, period + timestep)

# Update graph to extend data lines
def extend(pos):
    for i in range(channels):
        lines[i].set_xdata(times)
        lines[i].set_ydata(samples[:,i])

time = 0
pos = 0

# Open serial connection
ser = serial.Serial(2, baudrate=57600, timeout=1)
ser.setRTS(True) #?
ser.setRTS(False) #?

while time < 5000:
    
    # plot 5 channels, up to 4-byte integers (long)
    if ser.inWaiting() > 20:        
        for i in range(channels):
            bytes = ser.read(4)
            height = (ord(bytes[0]) << 24) + (ord(bytes[1]) << 16) + (ord(bytes[2]) << 8) + ord(bytes[3])
            
            # convert to signed long
            if (height >= 0x80000000):
                height = height - 0x100000000
                
            samples[pos, i] = numpy.long(height)

        if (time % 2 == 0):
            extend(pos)

        pos = (pos + 1)
        if (pos == BUF_LEN):
            pos = 0
            #times = times + period
            
        draw()
        time += 1

print ser.inWaiting()
ser.close
