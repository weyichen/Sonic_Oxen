from pylab import *
import numpy
import serial
from time import *
from collections import deque

# "interactive mode" off
# if on, figure is redrawn every time it is updated, such as setting data in the extend() method
ioff()

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
lines = []

# create 5 subplots, and set their axes limits
for i in range(channels):
    subplot(321+i)
    lines.extend(plot(times, samples[:,i]))
    lines[i].axes.set_ylim(-height, height)
    lines[i].axes.set_xlim(-timestep, period + timestep)

# with interactive mode off, we must call show
# block = False is an experimental argument    which enables shown figure to be edited
show(block = False)

# Update graph to extend data lines
def extend():
    for i in range(channels):
        # lines[i].set_xdata(times)
        lines[i].set_ydata(samples[:,i])

time = 0
pos = 0

# Open serial connection
ser = serial.Serial(2, baudrate=57600, timeout=1)
ser.setRTS(True) #?
ser.setRTS(False) #?

# array to read in 4 bytes at a time
data = deque()
# amount of time in seconds to plot
while time < 2000:
    
    # plot 5 channels, up to 4-byte integers (long)
    while ser.inWaiting() > 4:
        data.append(bytearray(4))
        ser.readinto(data[-1])

    if len(data) > channels:
        for i in range(channels):
            bytes = data.popleft()
            # construct y value
            height = (bytes[0] << 24) + (bytes[1] << 16) + (bytes[2] << 8) + bytes[3]
            
            # convert to signed long
            if (height >= 0x80000000):
                height = height - 0x100000000
                
            samples[pos,i] = numpy.long(height)

        if (time % 5 == 0):
            extend()
            draw() # with ioff(), figure is only updated when draw() is called

        pos = (pos + 1)
        if (pos == BUF_LEN):
            pos = 0
            #times = times + period
            
        time += 1

print ser.inWaiting()
print len(data)
ser.close
