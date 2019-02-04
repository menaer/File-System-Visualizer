import wx, random
from MyFonts import LayerFont

class MyMainFrame(wx.Frame):
    def __init__(self, parent=None, ID=-1, pos=wx.DefaultPosition, title='FS Canvas'):
        self.size = wx.Size(640,670)
        wx.Frame.__init__(self, parent, ID, title, pos, self.size)

        # Add the search window
        self.win = SearchWin(self)
        self.win.SetBackgroundColour(wx.Colour(255,255,255))

        # Add a status and search bars
        self.mtdInitStatusBar()
        #self.sBar = MySearchBar(self.win)

        # Bind some events
        self.win.Bind(wx.EVT_PAINT, self.hdlOnPaint)

    # Event Handlers
    #-----------------------------------------------------------------------
    def hdlOnPaint(self, event):
        #self.win.Refresh(True)
        #gdc = self.GetDC(1)
        #self.sBar.draw(gdc)
        event.Skip()

    # Methods
    #-----------------------------------------------------------------------
    def GetDC(self, dctype):
        """ This method for simple creates and returns a paintDC or ClientDC
        upon request
        """
        #self.panel.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        if dctype == 1: dc = wx.PaintDC(self.win)
        else: dc = wx.ClientDC(self.win)

        gdc = wx.GraphicsContext.Create(dc)

        return gdc

    def mtdInitStatusBar(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-1, -2, -3])
        self.statusbar.SetStatusText('(')
        self.statusbar.SetStatusText('Current Pts: %s', 1)
        self.statusbar.SetStatusText('Line Count: %s', 2)


# ---------------------------------------------------------------------------

class SearchWin(wx.Panel):
    """ Base class for encapsulating all histograms.
        """

    def __init__(self, parent, pos=(0,0), style=wx.NO_BORDER, mgr=None):
        wx.Panel.__init__(self, parent, -1, pos=pos, style=style)

        # Add stuff
        self.sbar = MySearchBar(self)
        self.searchbox = wx.SearchCtrl(self, style=wx.TE_PROCESS_ENTER)

        # Bind events
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_SIZE, self.onSize)
        self.searchbox.Bind(wx.EVT_TEXT_ENTER, self.onEnter)

    # Event Handlers
    #-----------------------------------------------------------------------
    def onPaint(self, event):
        self.Refresh()
        psize = self.GetSizeTuple()
        self.adjustsearchbox(psize)
        dc = self.GetDC(1)
        self.sbar.draw(dc)
        event.Skip()

    def onSize(self, event):
        self.Refresh()
        event.Skip()

    def onEnter(self, evt):
        query = self.searchbox.Value
        msg = wx.MessageBox(query, 'Search Resquest', style=wx.OK|wx.CENTER)
        evt.Skip()

    def onFwd(evt):
        query = 'fwd'
        self.mgr.respond(query)

    def onBk(evt):
        query = 'back'
        self.mgr.respond(query)

    # Methods
    #-----------------------------------------------------------------------
    def adjustsearchbox(self, psize):
        w = 0.25 * psize[0]
        h = 0.40 * psize[1]
        self.searchbox.SetClientSize((w,h))

        x = (0.70 * psize[0])
        y = (0.30 * psize[1])
        self.searchbox.SetPosition(wx.Point(x,y))
        self.searchbox.SetFont(LayerFont())
        self.searchbox.SetWindowStyleFlag(wx.ALIGN_CENTER_VERTICAL)
        self.searchbox.Refresh()

    def GetDC(self, dctype):
        """ This method for simple creates and returns a paintDC or ClientDC
        upon request
        """
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        if dctype == 1: dc = wx.AutoBufferedPaintDC(self)
        else: dc = wx.ClientDC(self)

        return dc

# ---------------------------------------------------------------------------

class MySearchBar(object):
    def __init__(self, parent, mgr=None):
        self.parent = parent


    # Search bar Drawing Method
    # ============================
    def draw(self, dc):
        """ Draws this DrawingObject into our window.
            'dc' is the device context to use for drawing.
        """
        psize = self.parent.GetSizeTuple()

        # Setup the dimensions of the main bar
        # The main bar spans the width of the parent
        x1, y1 = 0, 0
        w1, h1, c1 = psize[0], psize[1], 0 # c1 is the intended curve
        rect = (x1, y1, h1, c1)

        # Define Gradient colours
        clr1 = wx.Color(59,59,59)
        clr2 = wx.Color(190,190,190)

        # Setup drawing tools
        dc.SetPen(wx.Pen('white', 10, wx.TRANSPARENT))
        dc.SetBrush(wx.Brush('gray', wx.SOLID))
        #br1 = gc.CreateLinearGradientBrush(x1,y1,x1,(y1+h1),clr1,clr2) # +5 ensures that gradient repetition does not show

        # Setup and draw the main horizontal bar
        #gc.SetBrush(br1)
        dc.DrawRoundedRectangle(x1, y1, w1, h1, c1)

#----------------------------------------------------------------------------

class MyApp(wx.App):
    def OnInit(self):
        '''This bit runs automatically when an instance of MyCanvasApp is born'''
        self.frame = MyMainFrame()
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True

def FnMain():
    '''Function creates instance of MySketchApp and call MainLoop'''
    App = MyApp(False, '')
    App.MainLoop()

if __name__ == '__main__':
    FnMain()