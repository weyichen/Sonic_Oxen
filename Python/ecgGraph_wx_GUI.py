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
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar
import numpy as np
import pylab as pyl
import serial
import time
from collections import deque

class MainFrame(wx.Frame):
    def __init__(self, parent, ID, title):
        self.title = title
        wx.Frame.__init__(self, parent, ID, self.title, size = (200,100))

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
        
        #create sidebar
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
        self.Close(True)  # Close the frame.

class MainPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # 4x3 grid of all 12 ECG leads
        pyl.ioff()
        
        # graph figure parameters
        BUF_LEN = 128
        timestep = 1
        period = BUF_LEN * timestep
        height = 2000000
        channels = 12
        styles = ['r-', 'g-', 'y-', 'm-', 'k-', 'r-', 'g-', 'y-', 'm-', 'k-', 'r-', 'g-']
        
        # X values
        times = np.arange(0, period, timestep)
        # Y values
        samples = np.zeros([BUF_LEN, channels])

        self.lines = []
        
        self.fig = Figure((9.0, 12.0), dpi=100)
        self.lines.extend(self.fig.add_subplot(1,1,1))
        
        #for i in range (channels):
            
        
        # self.fig, self.axes = pyl.subplots(nrows=4, ncols=3)
        # for i in range(channels):
            # self.lines.extend(self.axes[i/3][i%3].plot(times, samples[:,i], styles[i], animated=True))
            # self.lines[i].axes.set_ylim(-height, height)
            # self.lines[i].axes.set_xlim(-timestep, period + timestep)
        # self.fig = Figure((3.0, 3.0), dpi=self.dpi)
        self.fig.show()
        
        # Let's capture the background of the figure
        #self.backgrounds = [self.fig.canvas.copy_from_bbox(ax.bbox) for ax in self.axes]

        # We need to draw the canvas before we start animating...
        self.fig.canvas.draw()
        
        # Make a convenient zipped list for simultaneous access
        #self.items = zip(self.lines, self.axes, self.backgrounds)
        
        graphGrid = wx.GridBagSizer(hgap=5, vgap=5)
        
        # self.init_plot()
        # self.lead1 = FigCanvas(self, -1, self.fig)
        # graphGrid.Add(self.lead1, pos=(1,0))
        
        # self.init_plot()
        # self.lead2 = FigCanvas(self, -1, self.fig)
        # graphGrid.Add(self.lead2, pos=(1,1))
        # self.init_plot()
        # self.lead6 = FigCanvas(self, -1, self.fig)
        # graphGrid.Add(self.lead6, pos=(3,2))
        # self.init_plot()
        # self.lead7 = FigCanvas(self, -1, self.fig)
        # graphGrid.Add(self.lead7, pos=(5,0))
        # self.init_plot()
        # self.lead10 = FigCanvas(self, -1, self.fig)
        # graphGrid.Add(self.lead10, pos=(7,0))
        
        # lead1_lbl = wx.StaticText(self, label="Lead 1")
        # lead2_lbl = wx.StaticText(self, label="Lead 2")
        # lead3_lbl = wx.StaticText(self, label="Lead 3")
        # lead4_lbl = wx.StaticText(self, label="Lead 4")
        # lead5_lbl = wx.StaticText(self, label="Lead 5")
        # lead6_lbl = wx.StaticText(self, label="Lead 6")
        # lead7_lbl = wx.StaticText(self, label="Lead 7")
        # lead8_lbl = wx.StaticText(self, label="Lead 8")
        # lead9_lbl = wx.StaticText(self, label="Lead 9")
        # lead10_lbl = wx.StaticText(self, label="Lead 10")
        # lead11_lbl = wx.StaticText(self, label="Lead 11")
        # lead12_lbl = wx.StaticText(self, label="Lead 12")
        # graphGrid.Add(lead1_lbl, pos=(0,0))
        # graphGrid.Add(lead2_lbl, pos=(0,1))
        # graphGrid.Add(lead3_lbl, pos=(0,2))
        # graphGrid.Add(lead4_lbl, pos=(2,0))
        # graphGrid.Add(lead5_lbl, pos=(2,1))
        # graphGrid.Add(lead6_lbl, pos=(2,2))
        # graphGrid.Add(lead7_lbl, pos=(4,0))
        # graphGrid.Add(lead8_lbl, pos=(4,1))
        # graphGrid.Add(lead9_lbl, pos=(4,2))
        # graphGrid.Add(lead10_lbl, pos=(6,0))
        # graphGrid.Add(lead11_lbl, pos=(6,1))
        # graphGrid.Add(lead12_lbl, pos=(6,2))
        
        # sidebar with buttons and vitals data
        sideGrid = wx.GridBagSizer(vgap=5)
        
        # add pause button
        self.paused = False
        self.pause_button = wx.Button(self, wx.ID_ANY, "Pause")
        self.Bind(wx.EVT_BUTTON, self.on_pause_button, self.pause_button)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_pause_button, self.pause_button)
        
        # add vitals information
        self.elapsed_lbl = wx.StaticText(self, label="Time elapsed: ")
        self.elapsed = wx.StaticText(self, label="0 s")
        self.heartrate_lbl = wx.StaticText(self, label="Heart rate: ")
        self.heartrate = wx.StaticText(self, label="1 bpm")
        
        # add sidebar elements to grid
        sideGrid.Add(self.pause_button, pos=(0,0))
        sideGrid.Add(self.elapsed_lbl, pos=(1,0))
        sideGrid.Add(self.elapsed, pos=(2,0))
        sideGrid.Add(self.heartrate_lbl, pos=(3,0))
        sideGrid.Add(self.heartrate, pos=(4,0))
        
        mainSizer.Add(graphGrid, 0, wx.ALL, 5)
        mainSizer.Add(sideGrid, 0, 0, wx.CENTER)
        self.SetAutoLayout(1)
        self.SetSizerAndFit(mainSizer)
        
        self.Show(True)
        
    def on_pause_button(self, event):
        self.paused = not self.paused
    
    def on_update_pause_button(self, event):
        label = "Resume" if self.paused else "Pause"
        self.pause_button.SetLabel(label)
    
    def init_plot(self, width=3.2, length=1.8):
        self.dpi = 100
        self.fig = Figure((width, length), dpi=self.dpi)
        #self.plot = plot(
        
app = wx.App(False)
frame = MainFrame(None, wx.ID_ANY, "Sonic Oxen")
frame.Show()
app.MainLoop()