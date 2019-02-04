import wx, random
from Artist import DateArtist as artist
from MyFonts import BigFont, MediumFont

# ---------------------------------------------------------------------------

class VizWin(wx.Panel):
    """ Base class for encapsulating all histograms.
        """

    def __init__(self, parent, pos=(0,0), style=wx.NO_BORDER, nav=None):
        wx.Panel.__init__(self, parent, -1, pos=pos, style=style)

        # Initialize variables
        self.initializevars()

        # Add the main tools and init variables
        self.initializeTools(nav)

        # Bind some events
        self.bindevents()

# -------------------------------------------------------
# Event Handlers
    def hdlOnMotion(self, event):
        # Get the mouse position
        self.MousePos = event.GetPositionTuple()

        # Check if that position fall within a histogram
        contains, name = self.artist.containsPoint(self.MousePos)
        if contains and self.mouseover==False: # Going in
            self.mouseover = True
            self.mouseoverloc = name
        elif contains and self.mouseover==True and self.mouseoverloc!=name: # Still in but now a different bar
            self.mouseover = True
            self.mouseoverloc = name
        elif not contains and self.mouseover == True: # Going out
            self.mouseover = False
            self.mouseoverloc = -1
        elif contains and self.mouseover == True and self.mouseoverloc == name:
            pass # no need to do anything.
        else:
            self.mouseoverloc = -1
            #Print 'Viz window: Just hovering and repainting .....'

        self.Refresh()
        event.Skip()

    def hdlOnClick(self, event):

        # Get the mouse position
        self.MousePos = event.GetPositionTuple()

        # Check if that position fall within a histogram
        # if it does, tell the navigator to respond
        contains, name = self.artist.containsPoint(self.MousePos)
        if contains:
            print '\nViz Window: New Bar Selected', name
            self.navigator.respond(name)
        else:
            pass

        event.Skip()

    def hdlOnPaint(self, event):
        self.size = self.GetSize() # Size of the parent window
        self.Refresh() # Note to self - please do not ever remove this refresh to avoid "window over" issues

        # Get a dc and use it to draw whatever data you currently have
        dc = self.GetDC(self, 1, self.size)
        name, level, label = self.mouseoverloc, self.level, self.labels[self.level]
        self.artist.draw(dc, self.size, self.data, name, label, level)

        # Draw the cross hairs after everything else is finished
        x, y = self.MousePos
        self.drawCrossHair(x, y, dc)

        #ndc = wx.BufferedPaintDC(self)
        #dc = wx.GCDC(ndc)
        if (self.navigator.type == 's' or self.navigator.type == 't') and self.rdown:
            self.drawmultiselect(x, y, dc)
        else:
            contains, name = self.artist.containsPoint(self.MousePos) # this call overcomes a wierd clash btw motion, click and paint over name
            if contains:
                self.drawTooltip(x, y, dc, self.size, name)
                myCursor= wx.StockCursor(wx.CURSOR_HAND)
                self.navigator.mgr.parent.SetCursor(myCursor)
            else:
                myCursor= wx.StockCursor(wx.CURSOR_ARROW)
                self.navigator.mgr.parent.SetCursor(myCursor)

        event.Skip()

    def hdlOnSize(self, event):
        self.Refresh()
        event.Skip()

    def hdlOnRDown(self, event):
        self.rdown = True

        # Get the mouse position
        self.RMousePos = event.GetPositionTuple()

        print 'VizWin: Right mousedown = ', self.rdown
        event.Skip()

    def hdlOnRUp(self, event):
        self.rdown = False
        print 'VizWin: Right mousedown = ', self.rdown
        event.Skip()

# -------------------------------------------------------
# Methods
    def reload(self, data, level, labels):
        self.data = data
        self.level = level
        self.labels = labels.copy()
        self.Refresh()

    def GetDC(self, parent, dctype, pSize):
        """ This method for simple creates and returns an 'auto buffered' paintDC
        upon request data from the database for level 1 in the drill-down
        """
        parent.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        if dctype == 1: ndc = wx.BufferedPaintDC(parent)
        else: ndc = wx.ClientDC(parent)
        dc = ndc
        return dc

    def initializeTools(self, nav):
        # Create a database manager to get and hold the master data
        self.navigator = nav
        self.artist = artist(self.size)

    def bindevents(self):
        self.Bind(wx.EVT_PAINT, self.hdlOnPaint)
        self.Bind(wx.EVT_SIZE, self.hdlOnSize)
        self.Bind(wx.EVT_MOTION, self.hdlOnMotion)
        self.Bind(wx.EVT_LEFT_UP, self.hdlOnClick)
        self.Bind(wx.EVT_RIGHT_DOWN, self.hdlOnRDown)
        self.Bind(wx.EVT_RIGHT_UP, self.hdlOnRUp)

    def initializevars(self):
        self.attr = -1
        self.firstpass = True
        self.lineSize = 3
        self.level = -1
        self.labels = []
        self.query = 0
        self.SetBackgroundColour('red')
        self.size = self.GetSize()
        self.data = None
        self.mouseover = False
        self.mouseoverloc = -1
        self.MousePos, self.RMousePos = (-1,-1), (-1,-1)
        self.rdown = False

    def drawCrossHair(self, a, b, dc):
        dc.SetPen(wx.Pen(wx.Colour(100, 100, 100), 1, wx.DOT))
        dc.CrossHair(a, b)

    def drawmultiselect(self, x, y, dc):
        pen = wx.Pen(wx.Colour(100,100,100), 2, wx.SOLID)
        brush = wx.Brush(wx.Colour(222,222,222,200))
        dc.SetPen(pen)
        dc.SetBrush(brush)

        x1, y1 = self.RMousePos[0], self.RMousePos[1]
        dc.SetTextForeground('blue')
        if x < x1: dc.DrawText('Multi-Select Activated', x, y-30)
        else: dc.DrawText('Multi-Select Activated', x, y-30)
        dc.DrawLine(x1, y1+10, x1, y1-10)
        dc.DrawLine(x1, y1, x, y)
        dc.DrawLine(x, y+10, x, y-10)

    def drawTooltip(self, x, y, dc, psize, name):
        # consider setting up a gdc using dc here
        pen = wx.Pen(wx.Colour(255,255,255), 2, wx.SOLID)
        pen.SetJoin(wx.JOIN_BEVEL)
        brush = wx.Brush(wx.Colour(222,222,222,200))
        dc.SetPen(pen)
        dc.SetBrush(brush)

        # Setup and draw the popup box
        w=0.1*psize[0]
        h=0.2*psize[1]
        polygon = [(x,y),(x+(0.05*w),y-(0.2*h)),(x+(0.5*w),y-(0.2*h)),
                    (x+(0.5*w),y-((0.2*h)+(h))), (x-(0.5*w),y-((0.2*h)+(h))),
                    (x-(0.5*w),y-(0.2*h)),(x-(0.05*w),y-(0.2*h))]
        #dc.DrawPolygon(polygon, fillStyle=wx.WINDING_RULE)

        # Setup and draw the text
        dc.SetTextForeground('blue')
        dc.SetFont(MediumFont())
        if name.isdigit(): name = int(name)

        try: # if the wierd clash (over name) btw motion, click and paint happens, this trap
                # will nullify it by preventing freeze and crash
            no_of_files = str(self.data[name])
            text = 'Histogram: ' + str(name) + '     ' + no_of_files + ' File(s)'
            dc.DrawText(text, 10, 10)
            #dc.DrawText(no_of_files + ' Files', 100, 120)
        except:
            print 'VizWindow: Error drawing tooltip and screen info...'

#---------------------------------------------------------------------------
#if __name__ == '__main__':
#    color = wx.Colour(224,234,245)
#    win = DateWin(None, color)
# tag cloud matrix
# matrix = a list of equal length lists for each line in the matrix