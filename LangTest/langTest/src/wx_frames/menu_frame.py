
import wx
import logging

class MenuFrame(wx.Frame):
    def __init__(self):
        self.logprefix = "MenuFrame"
        super(MenuFrame, self).__init__(None, title="Language test", size=(500, 500))
        
    def start(self, menu):
        logging.info("{0}:{1}: start".format(self.logprefix, "start"))
        self.menu = menu
        self.SetBackgroundColour('WHITE')
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(wx.StaticText(self, label='\nChoose an option:\n'), flag=wx.CENTER)
        hlWorkTest = wx.HyperlinkCtrl(self, label='\nWork on a test\n')
        self.Bind(wx.EVT_HYPERLINK, self.OnHlWorkTest, hlWorkTest)
        vbox.Add(hlWorkTest, flag=wx.CENTER)
        hlCreateTest = wx.HyperlinkCtrl(self, label='\nCreate a test\n')
        self.Bind(wx.EVT_HYPERLINK, self.OnHlCreateTest, hlCreateTest)
        vbox.Add(hlCreateTest, flag=wx.CENTER)
        hlSeeStats = wx.HyperlinkCtrl(self, label='\nSee statistics\n')
        self.Bind(wx.EVT_HYPERLINK, self.OnHlSeeStats, hlSeeStats)
        vbox.Add(hlSeeStats, flag=wx.CENTER)
        vbox.Add(wx.StaticText(self), flag=wx.CENTER)
        self.SetSizerAndFit(vbox)
        self.Centre()
        self.Show()

    def OnHlWorkTest(self, event):
        logging.info("{0}:{1}: ".format(self.logprefix, "OnHlWorkTest"))
        self.Hide()
        self.menu.work_test()
        self.Close()

    def OnHlCreateTest(self, event):
        logging.info("{0}:{1}: ".format(self.logprefix, "OnHlCreateTest"))
        self.Hide()
        self.menu.create_test()
        self.Close()

    def OnHlSeeStats(self, event):
        logging.info("{0}:{1}: ".format(self.logprefix, "OnHlSeeStats"))
        self.Hide()
        self.menu.see_stats()
        self.Close()
