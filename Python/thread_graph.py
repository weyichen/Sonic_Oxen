import matplotlib.pylab as plt
import numpy
import serial
import time
from collections import deque
import threading
from scipy.signal import butter, lfilter

fs = 1000
nyq = 0.5 * fs
lowcut = 2
highcut = 50
low = lowcut / nyq
high = highcut / nyq
b, a = butter(5, [low, high], btype='band')

# "interactive mode" off
# if on, figure is redrawn every time it is updated, such as setting data in the extend() method
plt.ioff()

BUF_LEN = 300 # Length of data buffer
FRAME_LEN = 0.1*BUF_LEN
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
    y = samples[:,i]
    lines.extend(axes[i].plot(times[:-2*FRAME_LEN], y[FRAME_LEN:-FRAME_LEN], styles[i], animated=True))
    lines[i].axes.set_ylim(-height, height)
    lines[i].axes.set_xlim(-timestep, period - 2 * FRAME_LEN + timestep)

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
        self.ser = serial.Serial(4, baudrate=57600, timeout=1)
        self.ser.flushInput()
        self.ser.setRTS(False)
        time.sleep(0.5)
        self.ser.setRTS(True)
        while (self.ser.inWaiting() == 0):
            self.ser.write("Begin!x")
            print "Trying"
            time.sleep(0.2)
        # Run until turned off
        while on:
            # Read bytes in chunks of meaningful size
            if self.ser.inWaiting() > 4:
                b = bytearray(4)
                self.ser.readinto(b)
                # Don't read and write data simultaneously; acquire lock
                dataLock.acquire()
                data.append(b)
                dataLock.release()
        # Print status and close port on exit
        dataLock.acquire()
        print "Data:", len(data)
        dataLock.release()
        print "Serial:", self.ser.inWaiting()
        while (self.ser.inWaiting()):
            self.ser.write("Stop!")
            self.ser.flushInput()
            time.sleep(0.5)
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

#tstart = time.time()
while t < 1000:
    dataLock.acquire()
    packages = len(data)
    dataLock.release()
    if packages > channels:
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
                y = lfilter(b,a,samples[:,j])
                line.set_ydata(y[FRAME_LEN:-FRAME_LEN])
                ax.draw_artist(line)
                fig.canvas.blit(ax.bbox)

# Close serial port reader
on = False