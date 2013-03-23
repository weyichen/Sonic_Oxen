import matplotlib.pylab as plt
import numpy
import serial
import time
from collections import deque
import threading

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

fig.show()

# capture background of the figure
backgrounds = [fig.canvas.copy_from_bbox(ax.bbox) for ax in axes]

fig.canvas.draw()

# Make a convenient zipped list for simultaneous access
items = zip(lines, axes, backgrounds)

# array to read in 4 bytes at a time
data = deque()
on = True

class serial_reader_thread(threading.Thread):
    def __init__(self, threadID, data):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.data = data
    def run(self):
        self.ser = serial.Serial(3, baudrate=57600, timeout=1)
        while on:
            if self.ser.inWaiting() > 4:
                dataLock.acquire()
                data.append(bytearray(4))
                self.ser.readinto(data[-1])
                dataLock.release()
        print "Data:", len(data)
        print "Serial:", self.ser.inWaiting()
        self.ser.close()

# Open serial connection
dataLock = threading.Lock()
loader = serial_reader_thread(1, data)
loader.start()

t = 0
pos = 0

tstart = time.time()
while t < 10000:

    if len(data) > channels:
        for i in range(channels):
            dataLock.acquire()
            bytes = data.popleft()
            dataLock.release()
            # construct y value
            height = (bytes[0] << 24) + (bytes[1] << 16) + (bytes[2] << 8) + bytes[3]
            
            # convert to signed long
            if (height >= 0x80000000):
                height = height - 0x100000000
                
            samples[pos,i] = numpy.long(height)

        pos += 1
        if (pos == BUF_LEN):
            pos = 0
            
        t += 1
        
    if (t % 5) == 0:
        for j, (line, ax, background) in enumerate(items):
                fig.canvas.restore_region(background)
                line.set_ydata(samples[:,j])
                ax.draw_artist(line)
                fig.canvas.blit(ax.bbox)

on = False