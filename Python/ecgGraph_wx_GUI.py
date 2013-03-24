# need the following 2 lines of code before import wx
import wxversion
wxversion.select('2.8')
import wx

app = wx.PySimpleApp()  # Create a new app, don't redirect stdout/stderr to a window.

class GraphFrame(wx.Frame):
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
        
        self.panel = wx.Panel(self)
        
        #create sidebar
        self.sidebar = SideBar(self.panel, -1, "Sidebar", "1 bpm")
        
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
        
class SideBar(wx.Panel):
    def __init__(self, parent, ID, label, initval):
        wx.Panel.__init__(self, parent, ID)
        
        # declare sizer (container that arranges elements)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Add pause button
        self.paused = False
        self.pause_button = wx.Button(self, wx.ID_ANY, "Pause")
        self.Bind(wx.EVT_BUTTON, self.on_pause_button, self.pause_button)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_pause_button, self.pause_button)
        
        # declare elements
        self.elapsed_lbl = wx.StaticText(self, label="Time elapsed: ")
        self.elapsed = wx.StaticText(self, label="0 s")
        self.heartrate_lbl = wx.StaticText(self, label="Heart rate: ")
        self.heartrate = wx.StaticText(self, label=initval)
        
        # add elements to sizer
        sizer.Add(self.elapsed_lbl, 1, wx.EXPAND)
        sizer.Add(self.elapsed, 1, wx.EXPAND)
        sizer.Add(self.heartrate_lbl, 1, wx.EXPAND)
        sizer.Add(self.heartrate, 1, wx.EXPAND)
        
        self.SetSizer(sizer)
        self.SetAutoLayout(1)
        sizer.Fit(self)
        
    def on_pause_button(self, event):
        self.paused = not self.paused
    
    def on_update_pause_button(self, event):
        label = "Resume" if self.paused else "Pause"
        self.pause_button.SetLabel(label)
        

app.frame = GraphFrame(None, wx.ID_ANY, "Sonic Oxen")
app.MainLoop()