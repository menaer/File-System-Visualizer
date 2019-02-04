import wx, wx.aui, MyGUIUtils
from DbManager import DBManager, dateNavMgr, sizeNavMgr
from Histogram_Module import DateWindow, SizeWindow, VizWindow
from Results_Module import ListWindow
from Search_Module import SearchBar

#---------------------------------------------------------------------------

class MainPanel(wx.Panel):
    def __init__(self, parent=None, ID=-1, pos=wx.DefaultPosition, size=(0,0), style=wx.TAB_TRAVERSAL|wx.NO_BORDER, mgr=None):
        wx.Panel.__init__(self, parent, ID, pos, size, style)
        self.snav = sizeNavMgr(parent=self, mgr=mgr)
        self.dnav = dateNavMgr(parent=self, mgr=mgr)
        self.SetBackgroundColour(wx.Colour(128,128,128))
        #self.SetBackgroundColour('white')
        mainwinsizer = wx.BoxSizer(wx.VERTICAL)

        # This is where all the three windows are added
        # i.e. The search, visuzlization and results windows
        self.searchwin = self.AddSearchWindow(None)

        # Add a panel that is split into 2
        # Viz and tag panel
        self.subbook = self.AddSubBook([self.dnav, self.snav])
        #self.subbook = self.AddSubBook([self.dnav])
        #self.subbook = self.AddSubBook([self.snav])
        self.resultwin = self.AddResultsWindow(None)

        mainwinsizer.Add(self.searchwin, 0, wx.EXPAND | wx.ALL | wx.ALIGN_CENTER, 3)
        mainwinsizer.Add(self.subbook, 6, wx.EXPAND | wx.ALL | wx.ALIGN_CENTER, 3)
        mainwinsizer.Add(self.resultwin, 3, wx.EXPAND | wx.ALL | wx.ALIGN_CENTER, 3)
        self.SetSizer(mainwinsizer)

        # Start the engines (tell all navigators to respond)
        self.dnav.respond(0)
        self.snav.respond(0)

    def AddSearchWindow(self, mgr):
        window = SearchBar.SearchWin(self)

        # Add some buttons to the window
        #sizer = wx.BoxSizer(wx.HORIZONTAL)
        #bkbutton = wx.Button(window, id=1000, label='Back')
        #fwdbutton = wx.Button(window, id=1001, label='Forward')
        #sizer.Add(bkbutton, flag=wx.ALIGN_CENTER)
        #sizer.Add(fwdbutton, flag=wx.ALIGN_CENTER)

        def onFwd(evt):
            query = 'fwd'
            self.mgr.respond(query)

        def onBk(evt):
            query = 'back'
            self.mgr.respond(query)

        # Bind events
        #bkbutton.Bind(wx.EVT_BUTTON, onBk)
        #fwdbutton.Bind(wx.EVT_BUTTON, onFwd)

        #window.SetSizer(sizer)
        return window

    def AddSubBook(self, navs):
        #book = SubBook(self, -1, navs=navs)
        win = MiddlePanel(self, -1, navs=navs)
        return win

    def AddResultsWindow(self, mgr):
        window = ListWindow.VirtualList(self)
        window.SetBackgroundColour(wx.Colour(255,255,255))
        return window

#---------------------------------------------------------------------------

class DateSizePanel(wx.Panel):
    def __init__(self, parent=None, ID=-1, pos=wx.DefaultPosition, size=(0,0),
                    style=wx.TAB_TRAVERSAL|wx.NO_BORDER, navs=None, wtype=None):
        wx.Panel.__init__(self, parent, ID, pos, size, style)

        # Create the different navigators here
        #self.SetBackgroundColour(wx.Colour(255,255,255))
        self.SetBackgroundColour('pink')

        # Add a sizer here for the panel instance (hope this work as a notebook page)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # This is where the date and size windows are added
        # i.e. determine which one to use then create it
        if wtype == 's':
            self.win = VizWindow.VizWin(self, mgr=navs[1])
        else:
            self.win = VizWindow.VizWin(self, mgr=navs[0])

        # Stick it in the sizer
        sizer.Add(self.win, 1, wx.EXPAND | wx.ALL | wx.ALIGN_CENTER, 3)
        self.SetSizer(sizer)

#---------------------------------------------------------------------------

class MiddlePanel(wx.Panel):
    def __init__(self, parent=None, ID=-1, pos=wx.DefaultPosition, size=(0,0),
                    style=wx.TAB_TRAVERSAL|wx.NO_BORDER, navs=None, wtype=None):
        wx.Panel.__init__(self, parent, ID, pos, size, style)

        # Create the different navigators here
        #self.SetBackgroundColour(wx.Colour(255,255,255))
        self.SetBackgroundColour('red')

        # Add a sizer here for the panel instance (hope this work as a notebook page)
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        # This is where the date and size windows are added
        # i.e. determine which one to use then create it
        self.subbook = SubBook(self, -1, navs=navs)

        greenpanel = wx.Panel(self, -1)
        greenpanel.SetBackgroundColour('green')

        # Stick it in the sizer
        sizer.Add(self.subbook, 3, wx.EXPAND | wx.ALL | wx.ALIGN_CENTER, 3)
        sizer.Add(greenpanel, 1, wx.EXPAND | wx.ALL | wx.ALIGN_CENTER, 3)
        self.SetSizer(sizer)

#----------------------------------------------------------------------

class SubBook(wx.aui.AuiNotebook):
    def __init__(self, parent, id, navs=None):
        wx.aui.AuiNotebook.__init__(self, parent, id, size=(21,21), style=wx.BK_TOP)

        # Initialize variables and set dimensions
        sty, color = self.initializeVars()

        # Add the windows
        self.dpanel = DateSizePanel(self, pos=(0,0), navs=navs)
        self.AddPage(self.dpanel, "Browse by Date")

        self.spanel = DateSizePanel(self, pos=(0,0), navs=navs, wtype='s')
        self.AddPage(self.spanel, "Browse by Size")

    def initializeVars(self):
        self.SetTabCtrlHeight(30)
        style = wx.RAISED_BORDER
        color = wx.Colour(224,234,245)
        return style, color

    def addWindows(self, sty, color, mgr):
        pass

#----------------------------------------------------------------------

class NBook(wx.aui.AuiNotebook):
    def __init__(self, parent, id, mgr=None):
        wx.aui.AuiNotebook.__init__(self, parent, id, size=(21,21), style=wx.BK_TOP)

        # Initialize variables and set dimensions
        sty, color = self.initializeVars()

        # Add the windows
        #mgr = DBManager('Bright.db')
        #Brightpanel = MainPanel(self, pos=(0,0), mgr=mgr)
        #self.AddPage(Brightpanel, "Bright A.")

        mgr = DBManager('Khoi.db')
        Khoipanel = MainPanel(self, pos=(0,0), mgr=mgr)
        self.AddPage(Khoipanel, "Khoi Nguyen")

        #mgr = DBManager('Magee.db')
        #Mageepanel = MainPanel(self, pos=(0,0), mgr=mgr)
        #self.AddPage(Mageepanel, "Dr Magee")

    def initializeVars(self):
        self.SetTabCtrlHeight(50)
        style = wx.RAISED_BORDER
        color = wx.Colour(224,234,245)
        return style, color

    def addWindows(self, sty, color, mgr):
        pass

#----------------------------------------------------------------------

class MyMainFrame(wx.Frame):
    def __init__(self, parent=None, ID=-1, pos=wx.DefaultPosition, title='FSCanvas - Bright Anaekwe - 2010'):
        size = (900,750)
        wx.Frame.__init__(self, parent, ID, title, pos, size)

        # Add objects: database manager and notebook
        self.initializetools()

        # Add a menu bar
        self.addmenubar()

        # Add a status bar
        self.initstatusbar()

    def initializetools(self):
        # Notebook to hold various visualization windows
        self.nbook = NBook(self, -1)

    def initstatusbar(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(1)
        self.statusbar.SetStatusText('')

    def addmenubar(self):
        mbar = ('&File','&Tools','&Help') #My mod - define menu bar items in a tuple
        mbaritems = (['Open', 'Save', 'Print'],['Options'],['FSCanvas Help', 'About FSCanvas']) #My mod - define menu items in a tuple
        mbardetails = () #My mod - define menu details in a list

        menubar = MyGUIUtils.FnMenuBar(mbar,mbaritems)
        self.SetMenuBar(menubar)

#----------------------------------------------------------------------

class MySketchApp(wx.App):
    def OnInit(self):
        '''This bit runs automatically when an instance of MyCanvasApp is born'''
        self.frame = MyMainFrame()
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True

#----------------------------------------------------------------------

def FnMain():
    '''Function creates instance of MySketchApp and call MainLoop'''
    App = MySketchApp(False, '')
    App.MainLoop()

if __name__ == '__main__':
    FnMain()