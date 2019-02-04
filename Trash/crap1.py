import wx
try:
    import wx.lib.buttonpanel as bp
except:
    import wx.lib.agw.buttonpanel as bp

class MyFrame(wx.Frame):

    def __init__(self, parent, id=-1, title="ButtonPanel", pos=wx.DefaultPosition,
                 size=(800, 600), style=wx.DEFAULT_FRAME_STYLE):

        wx.Frame.__init__(self, parent, id, title, pos, size, style)

        mainPanel = wx.Panel(self, -1)
        self.logtext = wx.TextCtrl(mainPanel, -1, "", style=wx.TE_MULTILINE)

        vSizer = wx.BoxSizer(wx.VERTICAL)
        mainPanel.SetSizer(vSizer)

        #alignment = BP_ALIGN_RIGHT

        titleBar = bp.ButtonPanel(mainPanel, -1, "A Simple Test & Demo")

        btn1 = bp.ButtonInfo(titleBar, wx.NewId(), wx.Bitmap("png4.png", wx.BITMAP_TYPE_PNG))
        titleBar.AddButton(btn1)
        #self.Bind(wx.EVT_BUTTON, self.OnButton, btn1)

        btn2 = bp.ButtonInfo(titleBar, wx.NewId(), wx.Bitmap("png3.png", wx.BITMAP_TYPE_PNG))
        titleBar.AddButton(btn2)
        #self.Bind(wx.EVT_BUTTON, self.OnButton, btn2)

        btn3 = bp.ButtonInfo(titleBar, wx.NewId(), wx.Bitmap("png2.png", wx.BITMAP_TYPE_PNG))
        titleBar.AddButton(btn3)
        #self.Bind(wx.EVT_BUTTON, self.OnButton, btn3)

        btn4 = bp.ButtonInfo(titleBar, wx.NewId(), wx.Bitmap("png1.png", wx.BITMAP_TYPE_PNG))
        titleBar.AddButton(btn4)
        #self.Bind(wx.EVT_BUTTON, self.OnButton, btn4)

        vSizer.Add(titleBar, 0, wx.EXPAND)
        vSizer.Add((20, 20))
        vSizer.Add(self.logtext, 1, wx.EXPAND|wx.ALL, 5)

        titleBar.DoLayout()
        vSizer.Layout()

# our normal wxApp-derived class, as usual

app = wx.PySimpleApp()

frame = MyFrame(None)
app.SetTopWindow(frame)
frame.Show()

app.MainLoop()
