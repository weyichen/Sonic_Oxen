import matplotlib.pylab as plt
import numpy
import serial
import time
from collections import deque

# "interactive mode" off
# if on, figure is redrawn every time it is updated, such as setting data in the extend() method
plt.ioff()

BUF_LEN = 128 # Length of data buffer
timestep = 1 # Time between samples
period = BUF_LEN * timestep # Period of 1 draw cycle
height = 2000000 # Expected sample value range

# X value (time)
times = numpy.arange(0, period, timestep)

channels = 5
# Y values
samples = numpy.zeros([BUF_LEN, channels])
lines = []

styles = ['r-', 'g-', 'y-', 'm-', 'k-']

# create 5 subplots and set their axes limits
fig, axes = plt.subplots(nrows=channels)    
for i in range(channels):
    lines.extend(axes[i].plot(times, samples[:,i], styles[i], animated=True))
    lines[i].axes.set_ylim(-height, height)
    lines[i].axes.set_xlim(-timestep, period + timestep)
    
# capture background of the figure
backgrounds = [fig.canvas.copy_from_bbox(ax.bbox) for ax in axes]

fig.show()
fig.canvas.draw()


# Open serial connection
ser = serial.Serial(2, baudrate=57600, timeout=1)
ser.setRTS(True) #?
ser.setRTS(False) #?

# array to read in 4 bytes at a time
data = deque()

t = 0
pos = 0

tstart = time.time()
while t < 2000:
    
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

        items = enumerate(zip(lines, axes, backgrounds), start=1)
        for j, (line, ax, background) in items:
            fig.canvas.restore_region(background)
            line.set_ydata(samples[:,j-1])
            ax.draw_artist(line)
            fig.canvas.blit(ax.bbox)

        pos += 1
        if (pos == BUF_LEN):
            pos = 0
            
        t += 1

print ser.inWaiting()
print len(data)
ser.close
