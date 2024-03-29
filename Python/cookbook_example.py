from pylab import *
import time

ion() # "interactive mode" on

tstart = time.time()               # for profiling
x = arange(0,2*pi,0.01)            # x-array
line, = plot(x,sin(x))

for i in arange(1,200):
    line.set_ydata(sin(x+i/10.0))  # update the data
    if (i % 3) == 0 : 
        draw()                         # redraw the canvas

print 'FPS:' , 200/(time.time()-tstart)