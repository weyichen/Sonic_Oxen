# need the following 2 lines of code before import wx
import wxversion
wxversion.select('2.8')
import wx

# imports for matplotlib and serial
import os
import pprint
import random
import sys
import matplotlib
matplotlib.use('WXAgg')
import matplotlib.pylab as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar
import numpy as np
import pylab as pyl
import serial
import time
import ctypes
import multiprocessing as mp
from scipy.signal import butter, lfilter

# Initialize dsp filter
filter_on = True
fs = 150
nyq = 0.5 * fs
lowcut = 0.5
highcut = 50
low = lowcut / nyq
high = highcut / nyq
order = 3
b, a = butter(order, [low, high], btype='band')

class MainFrame(wx.Frame):
    def __init__(self, parent, ID, title):
        self.title = title
        wx.Frame.__init__(self, parent, ID, self.title)

        # Setting up the menu.
        filemenu= wx.Menu()
        # wx.ID_ABOUT and wx.ID_EXIT are standard IDs provided by wxWidgets.
        menuOpen = filemenu.Append(wx.ID_OPEN, "&Open"," Open an existing ECG file")
        menuSave = filemenu.Append(wx.ID_SAVE, "&Save"," Save as an ECG file")
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        filemenu.AppendSeparator()
        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")
        
        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
        
        # Open file dialog
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        # Save file dialog
        self.Bind(wx.EVT_MENU, self.OnSave, menuSave)
        
        # About dialog
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        
        # Create the main panel which contains the graphing elements
        self.main_panel = MainPanel(self)
        
        # A Statusbar in the bottom of the window
        self.CreateStatusBar()
        
        # Display (always last step)
        self.Show(True)
        
    def OnOpen(self,e):
        """ Open a file"""
        self.dirname = ''
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname, self.filename), 'r')
            self.control.SetValue(f.read())
            f.close()
        dlg.Destroy()

    def OnSave(self,e):
        """ Save a file"""
        self.dirname = ''
        dlg = wx.FileDialog(self, "Save file", self.dirname, "", "*.*", wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname, self.filename), 'r')
            self.control.SetValue(f.read())
            f.close()
        dlg.Destroy()
        
    def OnAbout(self, event):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog(self, "A small text editor", "About Sample Editor", wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.
        
    def OnExit(self,e):
        self.main_panel.exit()
        self.Close(True)  # Close the frame.

class MainPanel(wx.Panel):
# this class contains the GUI elements for graphing, and the logic for setting up and updating the graph, plus a sidebar
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        # this will contain all elements in this class
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # "interactive mode" off
        # if on, figure is redrawn every time it is updated, such as setting data in the extend() method
        plt.ioff()
        
        # graph figure parameters
        global BUF_LEN, FRAME_LEN, timestep, period, height, channels
        BUF_LEN = 100
        FRAME_LEN = BUF_LEN * 0.2
        timestep = 1
        period = BUF_LEN * timestep
        height = 10000000
        channels = 8
        dpi = 100
        g_width = 3.2
        g_length = 1.8
        
        global Vpp
        Vpp = np.zeros(channels + 1)

        styles = ['r-', 'g-', 'y-', 'm-', 'r-', 'r-', 'g-', 'y-', 'm-', 'r-', 'r-', 'g-']
        
        global times, raw_samples, samples
        times = np.arange(0, period, timestep) # X values
        raw_samples = mp.Array(ctypes.c_longlong, BUF_LEN * channels)
        samples = np.ctypeslib.as_array(raw_samples.get_obj())
        samples = samples.reshape(BUF_LEN, channels) # Y values
        
        # save initial background of all graphing canvas, for use when updating graphs
        # place data, axes, and backgrounds of matplotlib figures in lists for easy acces to handles later
        figs = []
        lines = []
        axes = []
        backgrounds = []
        
        #change size of graph axes labels
        matplotlib.rc('font', size='10')
        
        #-----------------BEGIN GRAPHS------------------
        
        # create a 3 by 4 grid of ECG lead graphs
        graphGrid = wx.GridBagSizer(hgap=5, vgap=10)
        # Create a custom label formatter for y-axis labels
        y_label_formatter = matplotlib.ticker.FuncFormatter(self.rescale_voltage_labels)
        x_label_formatter = matplotlib.ticker.FuncFormatter(self.rescale_time_labels)
        
        # Create titles
        titles = ["Limb 1", "Limb 2", "Limb 3", "Precordial 1", "Precordial 2", "Precordial 3", \
                "Precordial 4", "Precordial 5", "Precordial 6"]
        
        # create all plots and place them in the graph grid
        for i in range (channels + 1):
            # create label for graph and add it to grid
            label = wx.StaticText(self, label=titles[i])
            graphGrid.Add(label, pos=((i*2)%6, i/3))
        
            # initialize graph figure and add it to grid
            grafig = Figure((g_width, g_length), dpi) 
            axis = grafig.add_subplot(111)
            axis.set_axis_bgcolor('black')
            axis.get_yaxis().set_major_formatter(y_label_formatter)
            axis.get_xaxis().set_major_formatter(x_label_formatter)
            y = samples[:,0]
            line = axis.plot(times[:-2*FRAME_LEN], y[FRAME_LEN:-FRAME_LEN], styles[i], animated=True)
            axis.set_ylim(-height, height)
            axis.set_xlim(-timestep, period - 2 * FRAME_LEN + timestep)
            
            canvas = FigCanvas(self, -1, grafig)
            graphGrid.Add(canvas, pos=((i*2+1)%6, i/3))
            
            # We need to draw the canvas before we start animating
            grafig.canvas.draw()
            
            # add figure elements to the appropriate list
            figs.append(grafig);
            lines.extend(line)
            axes.append(axis);
            backgrounds.append(grafig.canvas.copy_from_bbox(axis.bbox))
            
        #-----------------BEGIN DATA STUFF------------------
        # Lock Access to data
        global calc_ctrl
        calc_ctrl = mp.Queue()
        global sample_count
        sample_count = mp.Value(ctypes.c_longlong, 0, lock = False)
        self.calc = calculator_thread(raw_samples, BUF_LEN, channels, calc_ctrl, sample_count)
        
        # Make a convenient zipped list for simultaneous access
        self.items = zip(figs, lines, axes, backgrounds)
        self.pos = 0;
        
        #-----------------BEGIN SIDEBAR-----------------
        
        # Sidebar with buttons and vitals data
        sideBar = wx.GridBagSizer(vgap=5)
        
        # add pause button
        self.paused = False
        self.pause_button = wx.Button(self, wx.ID_ANY, "Pause")
        self.reset_button = wx.Button(self, wx.ID_ANY, "Reset")
        self.Bind(wx.EVT_BUTTON, self.on_pause_button, self.pause_button)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_pause_button, self.pause_button)
        
        self.Bind(wx.EVT_BUTTON, self.on_reset_button, self.reset_button)
        
        # add vitals information
        self.elapsed_lbl = wx.StaticText(self, label="Time elapsed: ")
        self.elapsed = wx.StaticText(self, label="00:00:00")
        self.sampling_rate_lbl = wx.StaticText(self, label="Approximate Sampling Rate (Hz)")
        self.sampling_rate = wx.StaticText(self, label="0")
        self.Vpp_lbl = wx.StaticText(self, label="Peak to Peak Amplitudes")
        self.Vpp = wx.StaticText(self, label="[]")
        #self.heartrate_lbl = wx.StaticText(self, label="Heart rate: ")
        #self.heartrate = wx.StaticText(self, label="1 bpm")
        
        # add sidebar elements to grid
        sideBar.Add(self.pause_button, pos=(0,0))
        sideBar.Add(self.reset_button, pos=(1,0))
        sideBar.Add(self.elapsed_lbl, pos=(2,0))
        sideBar.Add(self.elapsed, pos=(3,0))
        sideBar.Add(self.sampling_rate_lbl, pos=(4,0))
        sideBar.Add(self.sampling_rate, pos=(5,0))
        sideBar.Add(self.Vpp_lbl, pos=(6,0))
        sideBar.Add(self.Vpp, pos=(7,0))
        #sideBar.Add(self.heartrate_lbl, pos=(3,0))
        #sideBar.Add(self.heartrate, pos=(4,0))
        
        #-----------------ENDOF SIDEBAR-----------------
         
        # add graph grid and sidebar to sizer, and add that to the panel
        mainSizer.Add(graphGrid, 0, wx.ALL, 5)
        mainSizer.Add(sideBar, 0, 0, wx.CENTER)
        self.SetAutoLayout(1)
        self.SetSizerAndFit(mainSizer)
        
        # show panel (always last step)
        parent.Show(True)
        self.Show(True)
        
        # Begin timer and helper threads
        self.calc.start()
        
        self.redraw_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_redraw_timer, self.redraw_timer)        
        self.redraw_timer.Start(10)
        
        self.t_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_time, self.t_timer)
        self.t_timer.Start(10000)
        time.clock()
        
    def rescale_voltage_labels(self, x, p):
        return "%.1f" % (x * 3000 / 0x800000)
        
    def rescale_time_labels(self, x, p):
        return "%.1f" % (x / fs)
    
    def exit(self):
        self.paused = True
        calc_ctrl.put("Exit!")
    
    def update_time(self, event):
        elapsed_t = time.clock()
        hr = str(int(elapsed_t / 3600))
        min = str(int((elapsed_t / 60) % 60))
        sec = str(int(elapsed_t % 60))
        l = ':'.join([hr,min,sec])
        self.elapsed.SetLabel(l)
        self.sampling_rate.SetLabel(str(float(sample_count.value) / elapsed_t))
        self.Vpp.SetLabel(str(Vpp * 3300 / 0x800000))
    
    def on_redraw_timer(self, event):
        global Vpp
        if not self.paused:
            # get and update graph at each position in the grid
            for j, (fig, line, ax, background) in enumerate(self.items):
                fig.canvas.restore_region(background)
                if (j == 0):
                    slice = -1 * samples[:,j]
                elif (j == 1):
                    slice = samples[:,j]
                elif (j == 2):
                    slice = samples[:,0] + samples[:,1]
                else:
                    slice = samples[:, j - 1]
                if filter_on:
                    y = lfilter(b, a, slice)
                else:
                    y = slice
                y -= np.mean(y)
                Vpp[j] = np.ptp(y)
                line.set_ydata(y[FRAME_LEN:-FRAME_LEN])
                ax.draw_artist(line)
                fig.canvas.blit(ax.bbox)
    
    def on_pause_button(self, event):
        self.paused = not self.paused
        if self.paused:
            self.redraw_timer.Stop()
        else:
            self.redraw_timer.Start(10)
            
    def on_update_pause_button(self, event):
        label = "Resume" if self.paused else "Pause"
        self.pause_button.SetLabel(label)
            
    def on_reset_button(self, event):
        calc_ctrl.put('-')
        calc_ctrl.put('+')

# A class that calculates data on an isolated thread
class calculator_thread(mp.Process):
    # Cookie-cutter __init__ function; nothing special
    def __init__(self, raw_samples, BUF_LEN, channels, cmds, sample_count):
        mp.Process.__init__(self)
        self.raw_samples = raw_samples
        self.channels = channels
        self.BUF_LEN = BUF_LEN
        self.cmds = cmds
        self.sample_count = sample_count
        self.paused = False
        self.on = True
    def reset(self):
        # Print status and close port on exit
        self.paused = True
        # Make extra super sure we reset the Arduino
        while (self.ser.inWaiting()):
            self.ser.write("Stop!x")
            self.ser.flushInput()
            time.sleep(1)
        time.sleep(1)
        while (self.ser.inWaiting()):
            self.ser.write("Stop!x")
            self.ser.flushInput()
            time.sleep(1)
        time.sleep(1)
        while (self.ser.inWaiting()):
            self.ser.write("Stop!x")
            self.ser.flushInput()
            time.sleep(1)
        print "Serial:", self.ser.inWaiting()
    def ready(self):
        self.paused = False
        while (not self.ser.inWaiting()):
            self.ser.write("Begin!x")
            time.sleep(0.5)
    def run(self):
        self.pos = 0
        self.channel = 0
        
        samples = np.ctypeslib.as_array(self.raw_samples.get_obj())
        samples = samples.reshape(self.BUF_LEN, self.channels)
        
        self.ser = serial.Serial(6, baudrate=57600, timeout=1)
        self.ser.flushInput()
        self.reset()
        self.ready()
        ctrl_bytes = bytearray(3)
        bytes = bytearray(3 * self.channels)
        # Run until turned off
        while self.on:
            # Read and execute control commands from main process
            if not self.cmds.empty():
                cmd = self.cmds.get()
                if cmd == '+':
                    self.ready()
                elif cmd == '-':
                    self.reset()
                elif cmd == "Exit!":
                    self.on = False
                else:
                    print cmd
            # While on, continuously empty serial port
            if not self.paused:
                # Read bytes in chunks of meaningful size
                if self.ser.inWaiting() > 27:
                    self.ser.readinto(ctrl_bytes)
                    
                    if (ctrl_bytes[0] == 192 and ctrl_bytes[1] == 0 and ctrl_bytes[2] == 0):
                        self.ser.readinto(bytes)
                        for channel in range(self.channels):
                            offset = 3 * channel
                            height = (bytes[offset] << 16) + (bytes[offset + 1] << 8) + bytes[offset + 2]
                                
                            # convert to signed long
                            if (height >= 0x800000): # = 2^23
                                height = height - 0x1000000 # = 2^24
                            
                            height = np.long(height)
                            samples[self.pos, channel] = height

                        self.pos += 1
                        self.sample_count.value += 1
                        if self.pos == self.BUF_LEN:
                            self.pos = 0
                            
                    else:
                        shift = bytearray(1)
                        self.ser.readinto(shift)
        
# global graph variables
# array to read in 4 bytes at a time

if __name__ == '__main__':
    # Make sure to make a new thread each time program is turned on!
    # Once a thread finishes running, it cannot be restarted.
    # Each new thread will reopen the serial port and close it upon completion.

    app = wx.App(False)
    frame = MainFrame(None, wx.ID_ANY, "Sonic Oxen")
    app.MainLoop()