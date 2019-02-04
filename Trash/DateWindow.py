import wx, random
from Artist import DateArtist as artist
#from DateNavigator import DateNavigator

# ---------------------------------------------------------------------------

class DateWin(wx.Panel):
    """ Base class for encapsulating all histograms.
        """

    def __init__(self, parent, pos=(0,0), style=wx.NO_BORDER, mgr=None):
        wx.Panel.__init__(self, parent, -1, pos=pos, style=style)

        # Initialize variables
        self.initializevars()

        # Add the main tools and init variables
        self.initializeTools(mgr)

        # Bind some events
        self.bindevents()

# -------------------------------------------------------
# Event Handlers
    def hdlOnMotion(self, event):
        attrSelect = False
        # Get the mouse position
        self.MousePos = event.GetPositionTuple()

        # Check if that position fall within a histogram
        contains, name = self.artist.containsPoint(self.MousePos)
        if contains and self.mouseover==False:
            self.mouseover = True
            self.mouseoverloc = name
            self.reload(self.data, self.level)
        if contains and self.mouseover==True and self.mouseoverloc!=name:
            self.mouseover = True
            self.mouseoverloc = name
            self.reload(self.data, self.level)
        elif not contains and self.mouseover == True:
            self.mouseover = False
            self.mouseoverloc = -1
            self.reload(self.data, self.level)
        else:
            self.reload(self.data, self.level)

        event.Skip()

    def hdlOnClick(self, event):
        # Get the mouse position
        self.MousePos = event.GetPositionTuple()

        # Check if that position fall within a histogram
        # if it does, tell the navigator to respond
        contains, self.query = self.artist.containsPoint(self.MousePos)
        if contains:
            print self.query
            self.navigator.respond(self.query)
        else:
            pass
        event.Skip()

    def hdlOnPaint(self, event):
        self.size = self.GetSize() # Size of the parent window
        self.Refresh()

        # Get a dc and use it to draw whatever data you currently have
        dc = self.GetDC(self, 1, self.size)
        name, level = self.mouseoverloc, self.level
        self.artist.draw(dc, self.size, self.data, name, level)

        # Draw the cross hairs after everything else is finished
        x, y = self.MousePos
        self.DrawCrossHair(x, y, dc)
        event.Skip()

    def hdlOnSize(self, event):
        self.Refresh()
        event.Skip()

# -------------------------------------------------------
# Methods
    def reload(self, data, level):
        self.data = data
        self.level = level
        self.Refresh()

    def GetDC(self, parent, dctype, pSize):
        """ This method for simple creates and returns an 'auto buffered' paintDC
        upon request data from the database for level 1 in the drill-down
        """
        parent.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        if dctype == 1: dc = wx.AutoBufferedPaintDC(parent)
        else: dc = wx.ClientDC(parent)
        return dc

    def initializeTools(self, mgr):
        # Create a database manager to get and hold the master data
        self.navigator = mgr
        self.artist = artist(self.size)

    def bindevents(self):
        self.Bind(wx.EVT_PAINT, self.hdlOnPaint)
        self.Bind(wx.EVT_SIZE, self.hdlOnSize)
        self.Bind(wx.EVT_MOTION, self.hdlOnMotion)
        self.Bind(wx.EVT_LEFT_DOWN, self.hdlOnClick)

    def initializevars(self):
        self.attr = -1
        self.firstpass = True
        self.lineSize = 3
        self.level = -1
        self.query = 0
        self.SetBackgroundColour('pink')
        self.size = self.GetSize()
        self.data = None
        self.mouseover = False
        self.mouseoverloc = -1
        self.MousePos = (-1,-1)

    def DrawCrossHair(self, a, b, dc):
        dc.SetPen(wx.Pen(wx.Colour(100, 100, 100), 1, wx.DOT))
        dc.CrossHair(a, b)

#---------------------------------------------------------------------------
#if __name__ == '__main__':
#    color = wx.Colour(224,234,245)
#    win = DateWin(None, color)