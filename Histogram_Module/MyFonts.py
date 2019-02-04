import wx

class LayerFont(wx.Font):
    def __init__(self, pointSize=9, family=wx.FONTFAMILY_DECORATIVE, style=wx.FONTSTYLE_NORMAL,
                    weight=wx.FONTWEIGHT_NORMAL, underline=False, face='Calibri', encoding=wx.FONTENCODING_DEFAULT):
        wx.Font.__init__(self, pointSize, family, style, weight, underline, face, encoding)
        pass

class Header(wx.Font):
    def __init__(self, pointSize=9, family=wx.FONTFAMILY_DECORATIVE, style=wx.FONTSTYLE_NORMAL,
                    weight=wx.FONTWEIGHT_NORMAL, underline=False, face='Calibri', encoding=wx.FONTENCODING_DEFAULT):
        wx.Font.__init__(self, pointSize, family, style, weight, underline, face, encoding)
        pass

class MediumFont(wx.Font):
    def __init__(self, pointSize=10, family=wx.FONTFAMILY_DECORATIVE, style=wx.FONTSTYLE_NORMAL,
                    weight=wx.FONTWEIGHT_NORMAL, underline=False, face='Lucida Console', encoding=wx.FONTENCODING_DEFAULT):
        wx.Font.__init__(self, pointSize, family, style, weight, underline, face, encoding)
        pass

class BigFont(wx.Font):
    def __init__(self, pointSize=24, family=wx.FONTFAMILY_DECORATIVE, style=wx.FONTSTYLE_NORMAL,
                    weight=wx.FONTWEIGHT_NORMAL, underline=False, face='Calibri', encoding=wx.FONTENCODING_DEFAULT):
        wx.Font.__init__(self, pointSize, family, style, weight, underline, face, encoding)
        pass