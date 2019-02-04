import wx, random
from MyFonts import LayerFont

class DateArtist(object):
    """ This function reads data from the database for level 1 in the drill-down
            and draws the rectangle objects using the data retrieved.

            The level 1 artist draws three layers as 2-Tuples of rect coordinates
            i.e. (lyr1, lyr2) = (concept layer, attribute layer)

            Each layer has the following properties:
                'pos'           The position of the layer within the window.
                'size'          The size of the layer within the window.
                'pColor'        Colour of the layer's outline.
                'fColor'        Colour of the layer's interior.
                'lSize'         Thickness of the layer's outline.
                'pSize'         Size of the parent window
                """

    def __init__(self, pSize=wx.Point(0,0)):
        self.stack = {}
        pass

    def scaledata(self, pSize, datadict):
        ''' The method accepts a dictionary of data and scales the values
            to 70% of the height of the parent window'''

        scale = 0.75 * pSize[1]
        minimum = 0.03 * scale

        scaleddata = datadict.copy()
        total = float(max(scaleddata.values()))
        for datum in scaleddata:
            value = 0
            if total: value = (scaleddata[datum]/total) * scale
            if value <= minimum and value != 0: value = minimum
            scaleddata[datum] = value
        return scaleddata

    def draw(self, dc, pSize, data, mouseover, label, level):

        # Empty vessels
        self.stack.clear()

        # Scale the data first
        self.sdata = self.scaledata(pSize, data)

        # Get dimensions
        base = 0.09 * pSize[1]
        x = 0.05 * pSize[0]
        y = pSize[1]
        startpos = wx.Point(x,y)

        # clear the device context
        dc.Clear() # This limits clear to EVT_PAINT calls only and thus eliminates all the flicker
                        # during hovering. i.e. Clear() causes flicker when called severally
                        # Also neccessary bcos Clear() in ClientDC is not white. Two birds killed !!!

        dc.SetPen(wx.Pen(wx.Colour(222,222,222), width=0.5, style=wx.SOLID))
        top, bottom = 0, pSize[1]
        start, stop = 0, pSize[0]
        for line in range(top, bottom, 30):
            dc.DrawLine(start,line,stop,line)       #Grid lines

        #-----------------------------------------------------------------------
        # Draw Layer One: i.e. Currently selected level (height=7.5%, width=100% of parent's)
        #-----------------------------------------------------------------------
        w, h = pSize[0], (-1 * base)  # -1 inverts the Y axis
        x, y = 0, startpos.y
        rect = (x, y, w, h)
        dc = self.setupDrawTools(dc, 1)
        dc.SetFont(LayerFont())
        dc.DrawRoundedRectangleRect(rect, 0)
        label = label[0] + ': ' + label[1]
        dc.DrawLabel(label, rect, alignment=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, indexAccel=-1)

        # save coords and update startpos with the new coords
        x, y = startpos
        newx, newy = x, y+h
        startpos = wx.Point(newx, newy)


        for datum in self.sdata:

            #-------------------------------------------------------------------
            # Draw Layer Two: The labelled base for the bars
            #-------------------------------------------------------------------
            # Get details of the bar
            name = str(datum)
            value = self.sdata[datum]

            w = (0.900 * pSize[0])/len(self.sdata)
            h = (-1 * base)
            x, y = startpos
            rect = (x, y, w, h)

            dc = self.setupDrawTools(dc, 1)
            dc.SetFont(LayerFont())
            dc.DrawRoundedRectangleRect(rect, 2)
            dc.DrawLabel(name, rect, alignment=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, indexAccel=-1)

            # save coords for use in next pair
            newx, newy = (x + w), y

            #-------------------------------------------------------------------
            # Draw Layer Three: The bar itself
            #-------------------------------------------------------------------
            # Draw the attribute layer in pair
            pos = wx.Point(startpos.x,startpos.y+h) # Position relative to layer 1 in pair
            h = value * -1
            x, y = pos.x, pos.y
            rect = (x, y, w, h) # uses same width as base

            # Check for hover and change color by passing a different color number to setupDrawTools
            if name == str(mouseover):
                dc = self.setupDrawTools(dc, 3, level)
            else:
                dc = self.setupDrawTools(dc, 2, level)
            dc.DrawRoundedRectangleRect(rect, 2)

            # Store this rectangle in a dictionary for mouseover checks
            self.stack[name] = rect

            # update startpos with the new coords
            startpos = wx.Point(newx, newy)

        #-----------------------------------------------------------------------
        # Draw Side Bars
        #-----------------------------------------------------------------------
        #w, h = pSize[0], (-1 * pSize[1])  # -1 inverts the Y axis
        #w = 100
        #h = 100
        #x, y = 0, 0
        #rect = (x, y, w, h)
        #dc = self.setupDrawTools(dc, 4)
        #dc.DrawRoundedRectangleRect(rect, 4)


    def constructRect(self, size=(0,0), pos=(0,0)):
            # Construct the rectangle and reverse the y axis
            w, h = size.width, -1 * size.height
            rect = (w, h)
            return rect


    def setupDrawTools(self, dc, bar, lvl=-1):
            # Setup the pen and brush
            colorDict = {1:wx.Colour(128,128,128), 3:wx.Colour(247,158,9),
                        2:wx.Colour(255,127,127)}

            if bar==2:
                pColor, fColor, lSize = wx.Colour(255,255,255), colorDict[bar], 0.5
            elif bar==4:
                pColor, fColor, lSize = wx.Colour(255,255,255), wx.Colour('yellow'), 4
            else: pColor, fColor, lSize = wx.Colour(255,255,255), colorDict[bar], 0.5

            dc.SetPen(wx.Pen(pColor, lSize, wx.SOLID))
            dc.SetBrush(wx.Brush(fColor, wx.SOLID))
            dc.SetTextForeground('white')
            return dc


    # Selection Methods
    # =======================
    def containsPoint(self, pos=(0,0)):
        """ Returns True if this stack contains the given point. This will be used
            to determine if the user is over a bar in the current histogram.
        """

        stack = self.stack.copy()
        x0, y0 = pos # The cordinates of the mouse pointer
        for rectangle in stack:
            rect = stack[rectangle]

            # Note: rect = (x,y,w,h) and rectangle = name
            x1, y1 = int(rect[0]), int(rect[1])
            x2, y2 = int(x1 + rect[2]), int(y1 + rect[3])
            if x0 in range(x1, x2+1) and y0 in range(y2, y1+1): return True, rectangle

        return False, None


if __name__ == '__main__':
    art = DateArtist((0,0))