
import wx

class LoginFrame(wx.Frame):
    def __init__(self):
        self.app = wx.App(0)
        super(LoginFrame, self).__init__(None, title="Login", size=(200,100))
        panel = wx.Panel(self, -1)
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(wx.Button(panel, -1, 'Login'), 1 )
        panel.SetSizer(box)
        self.Centre()
        
    def start(self):
        self.Show()
        self.app.MainLoop()
        
    def ask_if_new_user(self, user_name):
        return True
    
    def close(self):
        self.Close()