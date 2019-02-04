import wx, wx.aui, MyGUIUtils, gc
from DataManager import DBManager
from SizeNavigator import sizeNavMgr
from DateNavigator import dateNavMgr
from Histogram_Module import VizWindow
from Results_Module import ListWindow
from Search_Module import ButtonBar
from Panels import MainPanel, VizPanel, MiddlePanel, SubBook

#---------------------------------------------------------------------------

class MyMainFrame(wx.Frame):
    def __init__(self, parent=None, ID=-1, pos=wx.DefaultPosition, title='FSCanvas - Bright Anaekwe - 2010'):
        #size = (1200,750)
        size = (1000,650)
        wx.Frame.__init__(self, parent, ID, title, pos, size)

        # Add objects: database manager and notebook
        self.initializetools()

        # Add a menu bar
        self.addmenubar()

    def initializetools(self):
        gc.disable()
        self.mgr = DBManager(self, 'InvIndex.db')

        # Add a status bar
        self.initstatusbar(self.mgr)

        panel = MainPanel(self, pos=(0,0), mgr=self.mgr)

    def initstatusbar(self, mgr):
        self.statusbar = self.CreateStatusBar()
        mgr.sbar = self.statusbar
        self.statusbar.SetFieldsCount(1)

    def addmenubar(self):
        mbar = ('&File','&Tools','&Help') # My mod - define menu bar items in a tuple
        mbaritems = (['Open', 'Save', 'Print'],['Options'],['FSCanvas Help', 'About FSCanvas']) # My mod - define menu items in a tuple
        mbardetails = () # My mod - define menu details in a list

        menubar = MyGUIUtils.FnMenuBar(mbar,mbaritems)
        self.SetMenuBar(menubar)

#----------------------------------------------------------------------

class FSApp(wx.App):
    def OnInit(self):
        '''This bit runs automatically when an instance of MyCanvasApp is born'''
        self.frame = MyMainFrame()
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True

#----------------------------------------------------------------------

def FnMain():
    '''Function creates instance of MySketchApp and call MainLoop'''
    App = FSApp(False, '')
    App.MainLoop()

if __name__ == '__main__':
    FnMain()