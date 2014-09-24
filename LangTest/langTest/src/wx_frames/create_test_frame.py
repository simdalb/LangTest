
import wx
import logging

class CreateTestFrame(wx.Frame):
    def __init__(self, parent):
        self.logprefix = "CreateTestFrame"
        super(CreateTestFrame, self).__init__(parent, size=(300, 160))
    
    def start(self, user_name):
        logging.info("{0}:{1}: start".format(self.logprefix, "start"))
        self.SetBackgroundColour('WHITE')