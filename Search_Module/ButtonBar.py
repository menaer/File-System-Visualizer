import wx, random
from MyFonts import LayerFont
try:
    import wx.lib.buttonpanel as bp
except:
    import wx.lib.agw.buttonpanel as bp

class MyMainFrame(wx.Frame):
    def __init__(self, parent=None, ID=-1, pos=wx.DefaultPosition, title='FS Canvas'):
        self.size = wx.Size(640,670)
        wx.Frame.__init__(self, parent, ID, title, pos, self.size)

        # Add the search
        self.win = NavWin(self)

        # Add a status and search bars
        self.mtdInitStatusBar()

        # Bind some events
        self.win.Bind(wx.EVT_PAINT, self.hdlOnPaint)

    # Event Handlers
    #-----------------------------------------------------------------------
    def hdlOnPaint(self, event):
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

class NavWin(wx.Panel):
    """ Base class for encapsulating all histograms.
        """

    def __init__(self, parent, pos=(0,0), style=wx.BORDER_SUNKEN, mgr=None):
        wx.Panel.__init__(self, parent, -1, pos=pos, style=style)
        self.SetBackgroundColour('white')

        #mgr.srchpanel = self
        #self.mgr = mgr

        vSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vSizer)

        # Add stuff
        self.bar = bp.ButtonPanel(self, -1,
                    alignment=bp.BP_ALIGN_LEFT, style=bp.BP_USE_GRADIENT|bp.BP_GRADIENT_VERTICAL)

        self.setupbar(self.bar)

        vSizer.Add(self.bar, 0, wx.EXPAND)

        self.bar.DoLayout()
        vSizer.Layout()

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

    def setupbar(self, bar):

        kind = wx.ITEM_CHECK
        btnbk = bp.ButtonInfo(bar, 100, wx.Bitmap("png2b.png", wx.BITMAP_TYPE_PNG), text='Back')
        btnfw = bp.ButtonInfo(bar, 101, wx.Bitmap("png1b.png", wx.BITMAP_TYPE_PNG), text='Forward')
        btnrst = bp.ButtonInfo(bar, 101, wx.Bitmap("png3b.png", wx.BITMAP_TYPE_PNG), text='Reset')
        self.bk = btnbk.GetId()
        self.fw = btnfw.GetId()
        self.search = wx.SearchCtrl(bar, style=wx.TE_PROCESS_ENTER, size=(200,-1))
        self.search.ShowCancelButton(True)

        bar.AddButton(btnbk)
        bar.AddSeparator() # Make it look nice
        bar.AddButton(btnfw)
        bar.AddSeparator() # Make it look nice
        bar.AddButton(btnrst)
        bar.AddSeparator() # Make it look nice
        self.bar.AddSpacer(size=(700,50), flag=wx.EXPAND)
        bar.AddControl(self.search)

        # trying to set the different colors
        bpArt = bar.GetBPArt()
        bpArt.SetColor(bp.BP_BORDER_COLOR, wx.Colour(0,0,0))
        bpArt.SetColor(bp.BP_GRADIENT_COLOR_FROM, wx.Colour(0,0,0))
        bpArt.SetColor(bp.BP_GRADIENT_COLOR_TO, wx.Colour(128,128,128))
        bpArt.SetColor(bp.BP_BUTTONTEXT_COLOR, wx.Colour(255,255,255))
        bpArt.SetColor(bp.BP_SEPARATOR_COLOR, bp.BrightenColour(wx.Colour(128, 128, 128), 0.85))
        bpArt.SetColor(bp.BP_SELECTION_BRUSH_COLOR, wx.Color(128, 128, 128))
        bpArt.SetColor(bp.BP_SELECTION_PEN_COLOR, wx.Color(128, 128, 128))
        bpArt.SetMetric(bp.BP_BORDER_SIZE, 3)
        bpArt.SetMetric(bp.BP_SEPARATOR_SIZE, 30)
        bpArt.SetMetric(bp.BP_MARGINS_SIZE, wx.Size(10,10))
        bpArt.SetFont(bp.BP_TEXT_FONT,LayerFont())

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