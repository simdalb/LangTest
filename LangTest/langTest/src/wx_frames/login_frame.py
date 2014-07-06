
import wx

class LoginFrame(wx.Frame):
    def __init__(self):
        self.clear_on_text_changed = False
        self.app = wx.App(0)
        super(LoginFrame, self).__init__(None, title="Login", size=(200,100))
        panel = wx.Panel(self, -1)
        box = wx.BoxSizer(wx.HORIZONTAL)
        self.cb = wx.ComboBox(panel, -1, 'User name', style = wx.CB_DROPDOWN)
        self.cb.SetEditable(True)
        box.Add(self.cb)
        self.Bind(wx.EVT_TEXT, self.OnTextChanged, self.cb) 
        button = wx.Button(panel, -1, 'Login')
        box.Add(button, 1 )
        panel.SetSizer(box)
        self.Centre()
        
    def start(self, login):
        self.login = login
        self.Show()
        self.app.MainLoop()
        
    def ask_if_new_user(self, user_name):
        return True
    
    def OnTextChanged(self, event):
        if not self.clear_on_text_changed:
            self.clear_on_text_changed = True
            self.text_ctrl = self.cb.GetValue()
            self.cb.Clear()
            self.cb.SetValue(self.text_ctrl)
            for item in self.login.receive_partial_text(event.GetString()):
                self.cb.Append(item)
            self.cb.SetInsertionPointEnd()
            self.cb.Popup()
        else:
            self.clear_on_text_changed = False
    
    def close(self):
        self.Close()