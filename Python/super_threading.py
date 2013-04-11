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

# Status variables
on = True

# Lock access to data streams
dataLock = threading.Lock()
sampleLock = threading.Lock()
timeLock = threading.Lock()

# A class that reads from the serial port using an isolated thread
class serial_reader_thread(threading.Thread):
    # Cookie-cutter __init__ function; nothing special
    def __init__(self, threadID, data, calc):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.data = data
        self.calc = calc
    def run(self):
        self.ser = serial.Serial(4, baudrate=57600, timeout=1)
        time.sleep(5)
        self.ser.write("Begin!")
        # Run until turned off
        while self.calc.go():
            # Read bytes in chunks of meaningful size
            if self.ser.inWaiting() > 4:
                # Don't read and write data simultaneously; acquire lock
                b = bytearray(4)
                self.ser.readinto(b)
                dataLock.acquire()
                data.append(b)
                dataLock.release()
        # Print status and close port on exit
        self.ser.write("Stop!")
        dataLock.acquire()
        print "Data:", len(data)
        print "Serial:", self.ser.inWaiting()
        dataLock.release()
        self.ser.close()

# A class that calculates data on an isolated thread
class calculator_thread(threading.Thread):
    # Cookie-cutter __init__ function; nothing special
    def __init__(self, threadID, data):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.data = data
        self.t = 0
    def go(self):
        timeLock.acquire()
        yes = (self.t < 1000000)
        timeLock.release()
        return yes
    def run(self):
        self.pos = 0
        # This t is a global variable shared with display
        while (self.go()):
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
                    
                    height = numpy.long(height)
                    sampleLock.acquire()
                    samples[self.pos,i] = height
                    sampleLock.release()

                self.pos += 1
                if (self.pos == BUF_LEN):
                    self.pos = 0
                
                timeLock.acquire()
                self.t += 1
                timeLock.release()
        # Print status and close reader on exit
        dataLock.acquire()
        print "Data:", len(data)
        dataLock.release()

# A class that updates the graph on an isolated thread
class display_thread(threading.Thread):
    # Cookie-cutter __init__ function; nothing special
    def __init__(self, threadID, calculator):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.calc = calculator
    def run(self):
        # Runs until the calculator is finished
        while (self.calc.go()):
            for j, (line, ax, background) in enumerate(items):
                fig.canvas.restore_region(background)
                sampleLock.acquire()
                line.set_ydata(samples[:,j])
                sampleLock.release()
                ax.draw_artist(line)
                fig.canvas.blit(ax.bbox)
        # Print status on exit
        dataLock.acquire()
        print "Data:", len(data)
        dataLock.release()

# A parent thread that controls the others
calc = calculator_thread(2, data)
calc.start()

# Make sure to make a new thread each time program is turned on!
# Once a thread finishes running, it cannot be restarted.
# Each new thread will reopen the serial port and close it upon completion.
loader = serial_reader_thread(1, data, calc)
loader.start()

gui = display_thread(3, calc)
gui.start()