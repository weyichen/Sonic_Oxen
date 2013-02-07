import matplotlib
matplotlib.use('GTKAgg')
import matplotlib.pyplot as plt

import numpy
import serial

print "step 0"
ser = serial.Serial(2, timeout=2)
ser.setRTS(True)
ser.setRTS(False)

print "step 1"

line1, = plt.plot([], [])

plt.show()

print "step 3"
def extend(line, xval, yval):
	line1.set_xdata(numpy.append(line.get_xdata(), xval))
	line1.set_ydata(numpy.append(line.get_ydata(), yval))
	plt.draw()

print "step 4"

time = 0
while time < 1000:
	print str(time)
	height = ser.readline()
	print str(height)
	time += 1
	extend(line1, time, height )
ser.close