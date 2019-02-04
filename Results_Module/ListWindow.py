import wx
from MyFonts import LayerFont

class MyMainFrame(wx.Frame):
    def __init__(self, parent=None, ID=-1, pos=wx.DefaultPosition, title='Blank GUI (Do not overwrite skeleton)'):
        size = (700,400)
        wx.Frame.__init__(self, parent, ID, title, pos, size)
        self.list = VirtualList(self)
       	self.list.SetItemTextColour(10, 'Red')

class MySketchApp(wx.App):
    def OnInit(self):
        '''This bit runs automatically when an instance of MyCanvasApp is born'''
        self.frame = MyMainFrame()
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True

def FnMain():
    '''Function creates instance of MySketchApp and call MainLoop'''
    App = MySketchApp(True, '')
    App.MainLoop()

#----------------------------------------------------------------------

class VirtualList(wx.ListCtrl):
    def __init__(self, parent, pos=(0,0), mgr=None):
        wx.ListCtrl.__init__(self, parent, -1, pos=pos, style=wx.LC_REPORT|wx.LC_VIRTUAL)

        # Add this window to the manager
        mgr.rstpanel = self
        self.mgr = mgr

        # Add tooltip
        self.addtooltips()

        # Setup the image list
        self.setupimagelist()

        # Insert columns
        self.insertcolumns()

        # Define attributes
        self.initattributes()

        # Bind some events
        self.bindevents()

# -------------------------------------------------------
# Event Handlers
    def OnItemSelected(self, event):
        self.currentItem = event.m_itemIndex
        print 'Selected %d' %self.currentItem
        event.Skip()

    def OnItemActivated(self, event):
        self.currentItem = event.m_itemIndex
        print 'Double clicked %d' %self.currentItem
        event.Skip()

    def OnItemDeselected(self, event):
        event.Skip()

# -------------------------------------------------------
# Methods

    def reload(self, data, ranks=None):

        if ranks:
            ndata = [(ranks[i], data[i]) for i in range(len(ranks))]
            ndata.sort(reverse=True)
        else:
            ndata = data

        self.data = ndata
        self.ranks = ranks
        self.SetItemCount(len(self.data))
        #self.SetItemFont(3, self.font)
        self.Refresh()

    def insertcolumns(self):
        # File-id column
        self.InsertColumn(0,"ID")
        self.SetColumnWidth(0,0)

        # Filename column
        self.InsertColumn(1,"Filename")
        self.SetColumnWidth(1,150)

        # Location column
        self.InsertColumn(2,"Location")
        self.SetColumnWidth(2,300)

        # File-type column
        self.InsertColumn(3,"Type")
        self.SetColumnWidth(3,50)

        # File-size column
        self.InsertColumn(4,"Size")
        self.SetColumnWidth(3,50)

    def setupimagelist(self):
        #self.il = wx.ImageList(16, 16)
        #self.idx1 = self.il.Add(images.getSmilesBitmap())
        #self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        pass

    def addtooltips(self):
        self.SetToolTip(wx.ToolTip('WIP'))

    def bindevents(self):
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected)

    def initattributes(self):
        self.SetItemCount(0)
        self.font = LayerFont()

        # Set item attributes
        self.attr = wx.ListItemAttr()
        #self.attr.SetFont(LayerFont())
        #self.attr.SetTextColour('black')

    #def getColumnText(self, index, col):
        #item = self.GetItem(index, col)
        #return item.GetText()

    def OnGetItemText(self, item, col):
        if self.ranks: file = self.data[item][1]
        else: file = self.data[item]
        #if self.ranks: columns = {0:'Rank Here', 1:file[2], 2:file[1], 3:file[3], 4:file[4]}
        #else: columns = {0:file[0], 1:file[2], 2:file[1], 3:file[3], 4:file[4]}
        columns = {0:file[0], 1:file[2], 2:file[1], 3:file[4], 4:file[6]}
        return str(columns[col])

    def OnGetItemImage(self, item):
        return -1

    def OnGetItemAttr(self, item):
        return self.attr

if __name__ == '__main__':
    FnMain()