
import wx

class PreviewFrame(wx.Frame):
    def __init__(self, preview, test):
        self.preview = preview
        titlename = test.testname + " - preview"
        wx.Frame.__init__(self, None, title=titlename, size=(200,100))