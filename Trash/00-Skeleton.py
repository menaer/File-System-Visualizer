import wx

class MyMainFrame(wx.Frame):
    def __init__(self, parent=None, ID=-1, pos=wx.DefaultPosition, title='Blank GUI (Do not overwrite skeleton)'):
        size = (700,400)
        wx.Frame.__init__(self, parent, ID, title, pos, size)
        self.panel = ButtonPanel(self, -1)

class MySketchApp(wx.App):
    def OnInit(self):
        '''This bit runs automatically when an instance of MyCanvasApp is born'''
        self.frame = MyMainFrame()
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True

#---------------------------------------------------------------------------

class ButtonPanel(wx.Panel):
    def __init__(self, parent=None, ID=-1, pos=wx.DefaultPosition, size=(0,0),
                    style=wx.TAB_TRAVERSAL|wx.NO_BORDER, navs=None, wtype=None):
        wx.Panel.__init__(self, parent, ID, pos, size, style)

        # Create the different navigators here
        #self.SetBackgroundColour(wx.Colour(255,255,255))
        self.SetBackgroundColour('pink')

        # Add a sizer here for the panel instance (hope this work as a notebook page)
        self.terms = [('beans',12),('fish',8),('milk', 24),('wish', 29),
                        ('shopping',5),('cake',17),('bread',39),('pie',4),
                        ('shopping',5),('cake',17),('bread',39),('pie',4),
                        ('shopping',5),('cake',17),('bread',39),('pie',4),
                        ('shopping',5),('cake',17),('bread',39),('pie',4),
                        ('shopping',5),('cake',17),('bread',39),('pie',4),
                        ('shopping',5),('cake',17),('bread',39),('pie',4),
                        ('shopping',5),('cake',17),('bread',39),('pie',4),
                        ('shopping',5),('cake',17),('bread',39),('pie',4),
                        ('shopping',5),('cake',17),('bread',39),('pie',4),
                        ('shopping',5),('cake',17),('bread',39),('pie',4),
                        ('shopping',5),('cake',17),('bread',39),('pie',4)]

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        gsizer = wx.GridSizer(1000,2,0,0)
        #sizer = wx.FlexGridSizer(0,2,0,0)
        for term, occurs in self.terms:
            button = wx.Panel(self, -1,name=term)
            button.SetBackgroundColour('red')
            label = wx.Panel(self,-1,name=str(occurs))
            gsizer.Add(button, 1, wx.ALIGN_CENTRE|wx.EXPAND, 5)
            gsizer.Add(label, 1, wx.ALIGN_CENTRE|wx.EXPAND, 5)

        # This is where the date and size windows are added
        # i.e. determine which one to use then create it
        #pinkpanel = wx.Panel(self, -1)
        #pinkpanel.SetBackgroundColour('pink')
        #greenpanel = wx.Panel(self, -1)
        #greenpanel.SetBackgroundColour('green')

        # Stick it in the sizer
        #sizer.Add(pinkpanel, 3, wx.EXPAND | wx.ALL | wx.ALIGN_CENTER, 3)
        #sizer.Add(greenpanel, 1, wx.EXPAND | wx.ALL | wx.ALIGN_CENTER, 3)
        sizer.Add(gsizer, 1, wx.EXPAND)
        self.SetSizer(sizer)




#----------------------------------------------------------------------

def FnMain():
    '''Function creates instance of MySketchApp and call MainLoop'''
    App = MySketchApp(True, 'Output.log')
    App.MainLoop()

if __name__ == '__main__':
    FnMain()