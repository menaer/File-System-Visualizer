import wx, wx.aui, MyGUIUtils
#from wx.lib.agw import aui
from DataManager import DBManager
from SizeNavigator import sizeNavMgr
from DateNavigator import dateNavMgr
from Histogram_Module import VizWindow
from Results_Module import ListWindow
from Search_Module import ButtonBar

#---------------------------------------------------------------------------
class MainPanel(wx.Panel):
    def __init__(self, parent=None, ID=-1, pos=wx.DefaultPosition, size=(0,0), style=wx.TAB_TRAVERSAL|wx.NO_BORDER, mgr=None):

        # Add this window to the manager
        mgr.mpanel = self
        self.mgr = mgr

        wx.Panel.__init__(self, parent, ID, pos, size, style)
        #self.SetBackgroundColour('white')
        #self.SetBackgroundColour(wx.Colour(128,128,128))

        # This is where all the three windows are added
        self.addWindows()

        # Arrange the windows
        self.arrangeWindows()

        # Start the engines (tell all navigators to respond)
        self.mgr.dnav.respond(0)
        #self.mgr.snav.respond(0)
        #self.mgr.tnav.respond(0)
        selection = self.mgr.selectionhistory[self.mgr.historypoint]
        self.mgr.rstpanel.reload(selection)
        self.mgr.sbar.SetStatusText("   No of files: %d" %len(selection))

        # Bind some events
        self.searchwin.Bind(wx.EVT_BUTTON, self.onButton)
        self.searchwin.Bind(wx.EVT_TEXT_ENTER, self.onEnter)

    #---------------------------------------------------------------------------
    # Event handlers
    def onButton(self, evt):
        if evt.GetId() == self.searchwin.bk: caller = 4
        elif evt.GetId() == self.searchwin.fw: caller = 5
        else: caller = 6

        self.mgr.updatenavs(caller)
        evt.Skip()

    def onEnter(self, evt):
        msg = self.searchwin.search.GetValue()

        # Get the current selection
        selection = self.mgr.selectionhistory[self.mgr.historypoint]

        # Call iteriselection on it
        self.mgr.iteriselection(selection, 7, msg) # 7 = Buttonbar's call-sign

        #self.searchwin.search.SetValue('')
        evt.Skip()

    #---------------------------------------------------------------------------
    # Methods
    def addWindows(self):
        # Add a search window
        self.searchwin = self.addSearchWindow()

        # Add the summary window
        #self.summarywin = self.addSummaryWindow()

        # Add visualization and tag cloud window pair
        self.subbook = self.addSubBook()

        # Add the results window
        self.resultwin = self.addResultsWindow()

    def arrangeWindows(self):
        mainwinsizer = wx.BoxSizer(wx.VERTICAL)
        mainwinsizer.Add(self.searchwin, 0, wx.EXPAND | wx.ALIGN_CENTER, 3)
        mainwinsizer.Add(self.subbook, 6, wx.EXPAND | wx.ALIGN_CENTER, 3)
        #mainwinsizer.Add(self.summarywin, 2, wx.EXPAND | wx.ALIGN_CENTER, 3)
        mainwinsizer.Add(self.resultwin, 2, wx.EXPAND | wx.ALIGN_CENTER, 3)
        self.SetSizer(mainwinsizer)

    def addSearchWindow(self):
        window = ButtonBar.NavWin(self, mgr=self.mgr)
        return window

    def addSummaryWindow(self):
        window = wx.Panel(self, -1,style=wx.BORDER_RAISED)
        window.SetBackgroundColour(wx.Colour(224,234,245))
        return window

    def addSubBook(self):
        win = MiddlePanel(self, -1, mgr=self.mgr)
        return win

    def addResultsWindow(self):
        window = ListWindow.VirtualList(self, mgr=self.mgr)
        window.SetBackgroundColour(wx.Colour(255,255,255))
        return window

#---------------------------------------------------------------------------

class VizPanel(wx.Panel):
    def __init__(self, parent=None, ID=-1, pos=wx.DefaultPosition, size=(0,0),
                    style=wx.TAB_TRAVERSAL|wx.NO_BORDER, mgr=None, wtype=None):
        wx.Panel.__init__(self, parent, ID, pos, size, style)

        # Add this window to the manager
        mgr.vizpanel = self
        self.mgr = mgr

        self.SetBackgroundColour('white')

        # Add a sizer here for the panel instance (hope this work as a notebook page)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # This is where the date and size windows are added
        # i.e. determine which one to use then create it
        if wtype == 's':
            self.win = VizWindow.VizWin(self, nav=self.mgr.snav)
        elif wtype == 't':
            self.win = VizWindow.VizWin(self, nav=self.mgr.tnav)
        else:
            self.win = VizWindow.VizWin(self, nav=self.mgr.dnav)

        # Stick it in the sizer
        sizer.Add(self.win, 1, wx.EXPAND | wx.ALIGN_CENTER, 3)
        self.SetSizer(sizer)

#---------------------------------------------------------------------------

class MiddlePanel(wx.Panel):
    def __init__(self, parent=None, ID=-1, pos=wx.DefaultPosition, size=(0,0),
                    style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER, mgr=None, wtype=None):
        wx.Panel.__init__(self, parent, ID, pos, size, style)

        # Add this window to the manager
        mgr.mdlpanel = self
        self.mgr = mgr

        #self.SetBackgroundColour(wx.Colour(128,128,128))
        #self.SetBackgroundColour('white')

        # Add a sizer here for the panel instance (hope this work as a notebook page)
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        # This is where the date and size windows are added
        # i.e. determine which one to use then create it
        self.subbook = SubBook(self, -1, mgr=self.mgr)

        # Add the tagcloud window
        self.sidebar = SideBar(self)

        #self.tagcloud.SetBackgroundColour('gray')

        # Stick all into the sizer
        sizer.Add(self.subbook, 3, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 0)
        sizer.Add(self.sidebar, 0, wx.EXPAND | wx.ALIGN_CENTER |wx.ALL, 5)

        self.SetSizer(sizer)

#----------------------------------------------------------------------

class SubBook(wx.aui.AuiNotebook):
    def __init__(self, parent, id, mgr=None):
        wx.aui.AuiNotebook.__init__(self, parent, id, size=(21,21), style=wx.BK_TOP|wx.NO_BORDER)

        # Add this window to the manager
        mgr.sbook = self
        self.mgr = mgr

        # Initialize variables and set dimensions
        sty, color = self.initializeVars()

        # Add the windows
        self.dpanel = VizPanel(self, pos=(0,0), mgr=self.mgr)
        self.AddPage(self.dpanel, "Browse by Date-Modified")

        self.spanel = VizPanel(self, pos=(0,0), mgr=self.mgr, wtype='s')
        self.AddPage(self.spanel, "Browse by File-Size")

        self.tpanel = VizPanel(self, pos=(0,0), mgr=self.mgr, wtype='t')
        self.AddPage(self.tpanel, "Browse by File-Type")

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

class SideBar(wx.Panel):
    def __init__(self, parent=None, ID=-1, pos=wx.DefaultPosition, size=wx.DefaultSize,
                    style=wx.TAB_TRAVERSAL|wx.NO_BORDER, navs=None, wtype=None):
        wx.Panel.__init__(self, parent, ID, pos, size, style)

        # Create the different navigators here
        self.SetBackgroundColour(wx.Colour(255,255,255))

        # Add a sizer here for the panel instance (hope this work as a notebook page)
        self.terms = [('active','decide'),('church','faint'),('milk', 'season'),('wish', 'image'),
                        ('reader','pebble'),('divide','sweep'),('thwart','razor'),('blaze','crave'),
                        ('truant','axial'),('mention','zoomify')]


        topsizer = wx.BoxSizer(wx.VERTICAL)
        bothsizer = wx.BoxSizer(wx.HORIZONTAL)
        # -----------------------------------------------------
        lsizer = wx.BoxSizer(wx.VERTICAL)
        rsizer = wx.BoxSizer(wx.VERTICAL)
        for term, occurs in self.terms:
            button1 = wx.Button(self, -1,term)
            button1.SetBackgroundColour('white')
            button2 = wx.Button(self, -1, str(occurs))
            button2.SetBackgroundColour('white')
            lsizer.Add(button1, 1, wx.EXPAND)
            rsizer.Add(button2, 1, wx.EXPAND)

        #-------------------------------------------------------------------------------
        # WIP: a toolbar for the tagcloud window
        bar1 = wx.Panel(self, -1)
        bar1.SetBackgroundColour(wx.Colour(222,222,222))
        #-------------------------------------------------------------------------------
        bothsizer.Add(lsizer, 1, wx.EXPAND)
        bothsizer.Add(rsizer, 1, wx.EXPAND)
        topsizer.Add(bar1, 0, wx.EXPAND|wx.ALIGN_CENTER, 5)
        topsizer.Add(bothsizer, 1, wx.EXPAND)
        #-------------------------------------------------------


        bottomsizer = wx.BoxSizer(wx.VERTICAL)
        #-------------------------------------------------------------------------------
        # WIP: a toolbar for the tagcloud window
        bar2 = wx.Panel(self, -1)
        bar2.SetBackgroundColour(wx.Colour(222,222,222))
        #-------------------------------------------------------------------------------
        datebox = wx.StaticBox(self, -1, "Date Modified")
        dbsizer = wx.StaticBoxSizer(datebox, wx.VERTICAL)
        self.dlabel = wx.StaticText(self, -1,"All" )
        dbsizer.Add(self.dlabel, 0, wx.ALIGN_CENTER)

        sizebox = wx.StaticBox(self, -1, "Size Range")
        sbsizer = wx.StaticBoxSizer(sizebox, wx.VERTICAL)
        self.slabel = wx.StaticText(self, -1,"All" )
        sbsizer.Add(self.slabel, 0, wx.ALIGN_CENTER)

        typebox = wx.StaticBox(self, -1, "File Type")
        tbsizer = wx.StaticBoxSizer(typebox, wx.VERTICAL)
        self.tlabel = wx.StaticText(self, -1,"All" )
        tbsizer.Add(self.tlabel, 0, wx.ALIGN_CENTER)

        kwbox = wx.StaticBox(self, -1, "Keyword(s)")
        kbsizer = wx.StaticBoxSizer(kwbox, wx.VERTICAL)
        self.klabel = wx.StaticText(self, -1,"None" )
        kbsizer.Add(self.klabel, 0, wx.ALIGN_CENTER)

        bottomsizer.Add(bar2, 0, wx.EXPAND | wx.ALIGN_CENTER, 5)
        bottomsizer.Add(dbsizer, 1, wx.EXPAND|wx.ALL, 5)
        bottomsizer.Add(sbsizer, 1, wx.EXPAND|wx.ALL, 5)
        bottomsizer.Add(tbsizer, 1, wx.EXPAND|wx.ALL, 5)
        bottomsizer.Add(kbsizer, 1, wx.EXPAND|wx.ALL, 5)
        #-------------------------------------------------------------------------------

        mainsizer = wx.BoxSizer(wx.VERTICAL)
        mainsizer.Add(bottomsizer, 1, wx.EXPAND, 5)
        mainsizer.Add(topsizer, 1, wx.EXPAND, 5)
        self.SetSizer(mainsizer)

        font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL)
        head1 = wx.StaticText(bar2, -1, 'Current Filters', size=(100,20))
        head2 = wx.StaticText(bar1, -1, 'Tag Cloud', size=(100,20))
        head1.SetFont(font)
        head2.SetFont(font)
#----------------------------------------------------------------------


