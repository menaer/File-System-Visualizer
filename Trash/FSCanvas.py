import wx, wx.aui, MyGUIUtils
from DataManager import DBManager
from SizeNavigator import sizeNavMgr
from DateNavigator import dateNavMgr
from Histogram_Module import DateWindow, SizeWindow, VizWindow
from Results_Module import ListWindow
from Search_Module import SearchBar, ButtonBar

#---------------------------------------------------------------------------
class MainPanel(wx.Panel):
    def __init__(self, parent=None, ID=-1, pos=wx.DefaultPosition, size=(0,0), style=wx.TAB_TRAVERSAL|wx.NO_BORDER, mgr=None):
        wx.Panel.__init__(self, parent, ID, pos, size, style)
        mgr.snav = sizeNavMgr(parent=self, mgr=mgr)
        mgr.dnav = dateNavMgr(parent=self, mgr=mgr)
        self.SetBackgroundColour(wx.Colour(210,208,200))

        # This is where all the three windows are added
        self.addWindows(datenav=self.dnav, sizenav=self.snav)

        # Arrange the windows
        self.arrangeWindows()

        # Start the engines (tell all navigators to respond)
        mgr.dnav.respond(0)
        mgr.snav.respond(0)

        # Bind some events
        self.searchwin.Bind(wx.EVT_BUTTON, self.onButton)

    #---------------------------------------------------------------------------
    # Event handlers
    def onButton(self, evt):
        if evt.GetId() == self.searchwin.bk: msg = 'back'
        elif evt.GetId() == self.searchwin.fw: msg = 'fwd'
        else: msg = 'rst'
        self.dnav.respond(msg)
        #msg = wx.MessageBox('You clicked the %s button' %msg, style=wx.OK)
        evt.Skip()

    #---------------------------------------------------------------------------
    # Methods
    def addWindows(self, datenav, sizenav):
        # Add a search window
        self.searchwin = self.addSearchWindow(None)

        # Add the summary window
        self.summarywin = self.addSummaryWindow(None)

        # Add visualization and tag cloud window pair
        self.subbook = self.addSubBook([datenav, sizenav])

        # Add the results window
        self.resultwin = self.addResultsWindow(None)

    def arrangeWindows(self):
        mainwinsizer = wx.BoxSizer(wx.VERTICAL)
        mainwinsizer.Add(self.searchwin, 0, wx.EXPAND | wx.ALL | wx.ALIGN_CENTER, 3)
        mainwinsizer.Add(self.summarywin, 1, wx.EXPAND | wx.ALL | wx.ALIGN_CENTER, 3)
        mainwinsizer.Add(self.subbook, 6, wx.EXPAND | wx.ALL | wx.ALIGN_CENTER, 3)
        mainwinsizer.Add(self.resultwin, 3, wx.EXPAND | wx.ALL | wx.ALIGN_CENTER, 3)
        self.SetSizer(mainwinsizer)

    def addSearchWindow(self, mgr):
        window = ButtonBar.NavWin(self)
        return window

    def addSummaryWindow(self, mgr):
        window = wx.Panel(self, -1,style=wx.BORDER_RAISED)
        window.SetBackgroundColour(wx.Colour(224,234,245))
        return window

    def addSubBook(self, navs):
        #book = SubBook(self, -1, navs=navs)
        win = MiddlePanel(self, -1, navs=navs)
        return win

    def addResultsWindow(self, mgr):
        window = ListWindow.VirtualList(self)
        window.SetBackgroundColour(wx.Colour(255,255,255))
        return window

#---------------------------------------------------------------------------

class DateSizePanel(wx.Panel):
    def __init__(self, parent=None, ID=-1, pos=wx.DefaultPosition, size=(0,0),
                    style=wx.TAB_TRAVERSAL|wx.NO_BORDER, navs=None, wtype=None):
        wx.Panel.__init__(self, parent, ID, pos, size, style)

        self.SetBackgroundColour('white')

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
                    style=wx.TAB_TRAVERSAL|wx.RAISED_BORDER, navs=None, wtype=None):
        wx.Panel.__init__(self, parent, ID, pos, size, style)

        # Create the different navigators here
        #self.SetBackgroundColour(wx.Colour(128,128,128))
        self.SetBackgroundColour('black')

        # Add a sizer here for the panel instance (hope this work as a notebook page)
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        # This is where the date and size windows are added
        # i.e. determine which one to use then create it
        self.subbook = SubBook(self, -1, navs=navs)

        # Add the tagcloud window
        self.tagcloud = wx.Panel(self, -1,style=wx.NO_BORDER)
        self.tagcloud.SetBackgroundColour('white')

        # ------------------------------------------------
        # WIP: a toolbar for the tagcloud window
        bar = wx.ToolBar(self.tagcloud, style=wx.TB_FLAT)
        bar.AddLabelTool(100, "Test", wx.ArtProvider_GetBitmap(wx.ART_QUESTION))
        bar.AddLabelTool(200, "Test", wx.ArtProvider_GetBitmap(wx.ART_QUESTION))
        bar.AddLabelTool(300, "Test", wx.ArtProvider_GetBitmap(wx.ART_QUESTION))
        bar.Realize()
        tagsizer = wx.BoxSizer(wx.VERTICAL)
        tagsizer.Add(bar, 0, wx.EXPAND | wx.ALL | wx.ALIGN_CENTER, 3)
        tagsizer.Add(wx.Panel(self.tagcloud, -1), wx.EXPAND | wx.ALL | wx.ALIGN_CENTER, 3)
        self.tagcloud.SetSizer(tagsizer)
        # ------------------------------------------------

        # Stick all into the sizer
        sizer.Add(self.subbook, 3, wx.EXPAND | wx.ALL | wx.ALIGN_CENTER, 3)
        sizer.Add(self.tagcloud, 1, wx.EXPAND | wx.ALL | wx.ALIGN_CENTER, 3)
        self.SetSizer(sizer)

#----------------------------------------------------------------------

class SubBook(wx.aui.AuiNotebook):
    def __init__(self, parent, id, navs=None):
        wx.aui.AuiNotebook.__init__(self, parent, id, size=(21,21), style=wx.BK_TOP|wx.NO_BORDER)

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

    def refreshBook(self, data, level):
        self.dpanel.win.reload(data, level)
        self.spanel.win.reload(data, level)

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
        #self.nbook = NBook(self, -1)
        mgr = DBManager('Bright.db')
        Khoipanel = MainPanel(self, pos=(0,0), mgr=mgr)
        #self.AddPage(Khoipanel, "Khoi Nguyen")

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