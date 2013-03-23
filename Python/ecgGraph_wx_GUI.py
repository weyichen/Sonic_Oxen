# need the following 2 lines of code before import wx
import wxversion
wxversion.select('2.8')
import wx

app = wx.PySimpleApp()  # Create a new app, don't redirect stdout/stderr to a window.

class GraphFrame(wx.Frame):
    def __init__(self, parent, ID, title):
        self.title = title
        wx.Frame.__init__(self, parent, ID, self.title, size = (200,100))
        self.CreateStatusBar() # A Statusbar in the bottom of the window

        # Setting up the menu.
        filemenu= wx.Menu()
        
        # wx.ID_ABOUT and wx.ID_EXIT are standard IDs provided by wxWidgets.
        filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        filemenu.AppendSeparator()
        filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")
        
        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
        
        self.panel = wx.Panel(self)
        # Add pause button
        self.paused = False
        self.pause_button = wx.Button(self.panel, wx.ID_ANY, "Pause")
        self.Bind(wx.EVT_BUTTON, self.on_pause_button, self.pause_button)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_pause_button, self.pause_button)
        #Add timer
        wx.clock = wx.StaticText(self.panel, wx.ID_ANY, "00:00")
        
        # Display
        self.Show(True)
        
    def on_pause_button(self, event):
        self.paused = not self.paused
    
    def on_update_pause_button(self, event):
        label = "Resume" if self.paused else "Pause"
        self.pause_button.SetLabel(label)

app.frame = GraphFrame(None, wx.ID_ANY, "Sonic Oxen")
app.MainLoop()