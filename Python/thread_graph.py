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

# A class that reads from the serial port using an isolated thread
class serial_reader_thread(threading.Thread):
    # Cookie-cutter __init__ function; nothing special
    def __init__(self, threadID, data):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.data = data
    def run(self):
        self.ser = serial.Serial(7, baudrate=57600, timeout=1)
        time.sleep(2)
        self.ser.write("Begin!")
        # Run until turned off
        while on:
            # Read bytes in chunks of meaningful size
            if self.ser.inWaiting() > 4:
                # Don't read and write data simultaneously; acquire lock
                dataLock.acquire()
                data.append(bytearray(4))
                self.ser.readinto(data[-1])
                dataLock.release()
        # Print status and close port on exit
        dataLock.acquire()
        print "Data:", len(data)
        dataLock.release()
        print "Serial:", self.ser.inWaiting()
        self.ser.close()

# Lock Access to data
dataLock = threading.Lock()
# Make sure to make a new thread each time program is turned on!
# Once a thread finishes running, it cannot be restarted.
# Each new thread will reopen the serial port and close it upon completion.
loader = serial_reader_thread(1, data)
loader.start()

t = 0
pos = 0

tstart = time.time()
while t < 1000:

    if len(data) > channels:
        for i in range(channels):
            # Don't read and write data simultaneously; acquire lock
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

# Close serial port reader
on = False