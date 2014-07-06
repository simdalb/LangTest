
import wx

class LoginFrame(wx.Frame):
    def __init__(self):
        self.no_ignore_OnTextChange = False
        self.app = wx.App(0)
        super(LoginFrame, self).__init__(None, title="Login", size=(200,300))
        self.panel = wx.Panel(self, -1)
        self.box = wx.BoxSizer(wx.HORIZONTAL)
        self.cb = wx.ComboBox(self.panel, -1, 'User name', size=(100,100), style = wx.CB_SIMPLE | wx.CB_DROPDOWN)
        self.box.Add(self.cb)
        self.Bind(wx.EVT_TEXT, self.OnTextChanged, self.cb) 
        button = wx.Button(self.panel, -1, 'Login')
        self.box.Add(button, 1 )
        self.panel.SetSizer(self.box)
        self.Centre()
        
    def start(self, login):
        self.login = login
        self.Show()
        self.app.MainLoop()
        
    def ask_if_new_user(self, user_name):
        return True
    
    def OnTextChanged(self, event):
        if not self.no_ignore_OnTextChange:
            self.text_ctrl = self.cb.GetValue()
            self.cb.Clear()
            self.no_ignore_OnTextChange = True
            self.cb.SetValue(self.text_ctrl)
            for item in self.login.receive_partial_text(event.GetString()):
                self.cb.Append(item)
            self.cb.SetInsertionPointEnd()
            self.panel.SetSizer(self.box)
        else:
            self.no_ignore_OnTextChange = False
    
    def close(self):
        self.Close()