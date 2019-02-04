import wx, calendar
from DbManager2 import DBManager, SizeNavMgr

class FormFiche(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1,"Title", size=wx.Size(800,250))
        #scroll=wx.ScrolledWindow(self,-1)

        # Add a panel
        self.panel = wx.Panel(self, -1)
        # Initialize variables
        self.initializevars()

        # Add controls
        self.addcontrols()

        # Bind events
        self.bindevents()

        # Get the data for the current level and display it
        data = self.smgr.respond(self.query)
        self.datectrl.SetLabel(str(data))

        # Show the frame
        self.Show(1)
        self.mgr

# ------------------------------------------------------
# Event managers
    def onGo(self, evt):
        query = 'fwd'
        data = self.smgr.respond(query)
        self.datectrl.SetLabel(str(data))
        evt.Skip()

    def onBack(self, evt):
        query = 'back'
        data = self.smgr.respond(query)
        self.datectrl.SetLabel(str(data))
        evt.Skip()

    def onEnter(self, evt):
        query = self.inputctrl.Value
        data = self.smgr.respond(query)
        self.datectrl.SetLabel(str(data))
        self.inputctrl.SetLabel('Enter Another...')
        evt.Skip()

# -------------------------------------------------------
# Methods

    def initializevars(self):
        self.mgr = DBManager('Magee.db')
        self.smgr = SizeNavMgr(self, self.mgr)
        self.query = 0
        self.level = 0

    def addcontrols(self):
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)

        self.bkbutton = wx.Button(self.panel, id=1000, label='Back')
        self.gobutton = wx.Button(self.panel, id=1001, label='Go')
        self.datectrl = wx.TextCtrl(self.panel, id=1002, size=(750,50))
        self.inputctrl = wx.SearchCtrl(self.panel, id=1003, size=(750,50), style=wx.TE_PROCESS_ENTER)

        sizer1.Add(self.inputctrl, flag=wx.ALIGN_CENTER)
        sizer1.Add(self.datectrl, flag=wx.ALIGN_CENTER)
        sizer1.Add(sizer2, flag=wx.ALIGN_CENTER)
        sizer2.Add(self.bkbutton, flag=wx.ALIGN_CENTER)
        sizer2.Add(self.gobutton, flag=wx.ALIGN_CENTER)

        self.panel.SetSizer(sizer1)

    def bindevents(self):
        self.gobutton.Bind(wx.EVT_BUTTON, self.onGo)
        self.bkbutton.Bind(wx.EVT_BUTTON, self.onBack)
        self.inputctrl.Bind(wx.EVT_TEXT_ENTER, self.onEnter)

if __name__ == '__main__':
    try: del myapp
    except: pass
    myapp=wx.PySimpleApp()
    FormFiche()
    myapp.MainLoop()