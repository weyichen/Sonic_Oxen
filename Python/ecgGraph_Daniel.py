import matplotlib
matplotlib.use('GTKAgg')
import matplotlib.pyplot as plt

import numpy
import serial
from time import sleep
import traceback

ser = serial.Serial(3, baudrate=9600, timeout=1)
ser.setRTS(True)
ser.setRTS(False)

fig = plt.figure()

ax = fig.add_subplot(111)

line1, = ax.plot([], [], animated=True, lw=2, label="value")

fig.show()

def extend(line, xval, yval):
    line1.set_xdata(numpy.append(line.get_xdata(), xval))
    line1.set_ydata(numpy.append(line.get_ydata(), yval))
    #Draw the lines
    """
    try:
        ax.draw_artist(line1)
        ax.canvas.draw()
    except AssertionError:
        pass
        """

time = 0

while time < 50:
	while ser.inWaiting() < 2:
		sleep(0.01)
	bytes = ser.read(2)
	height = ord(bytes[0]) << 8 + ord(bytes[1])
	print time, height
	extend(line1, time, height)
	time += 1

fig.show()
try:
        ax.draw_artist(line1)
        ax.canvas.draw()
except AssertionError:
    print "AssertionError"
    traceback.print_exc()
    print line1.get_xdata()
    print line1.get_ydata()
    #pass

ser.close