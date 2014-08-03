
import wx

class CreateUserPopupWindow(wx.PopupWindow):
    def __init__(self, parent, user_name):
        super(CreateUserPopupWindow, self).__init__(parent)
        self.parent = parent
        self.user_name = user_name
        self.panel = wx.Panel(self, -1)
        self.box = wx.BoxSizer(wx.HORIZONTAL)
        textctrl_createquery = wx.TextCtrl(self.panel, -1, "Create new user\"" + user_name + "?\"")
        self.box.Add(textctrl_createquery)
        button_create = wx.Button(self.panel, -1, 'Create')
        self.Bind(wx.EVT_BUTTON, self.OnButtonCreateClicked, button_create)
        self.box.Add(button_create, 1)
        button_dismiss = wx.Button(self.panel, -1, 'Dismiss')
        self.Bind(wx.EVT_BUTTON, self.OnButtonDismissClicked, button_dismiss)
        self.box.Add(button_dismiss, 1)
        self.panel.SetSizer(self.box)
        self.Centre()

    def OnButtonCreateClicked(self, event):
        self.parent.create_user(self.user_name)
        self.Close()

    def OnButtonDismissClicked(self, event):
        self.Close()

class LoginFrame(wx.Frame):
    def __init__(self):
        self.no_ignore_OnTextChange = False
        
    def start(self, login):
        self.login = login
        self.app = wx.App(0)
        super(LoginFrame, self).__init__(None, title="Login, or create an account", size=(200,300))
        self.panel = wx.Panel(self, -1)
        self.box = wx.BoxSizer(wx.HORIZONTAL)
        self.cb = wx.ComboBox(self.panel, -1, 'User name', size=(100,100), style = wx.CB_SIMPLE | wx.CB_DROPDOWN)
        self.box.Add(self.cb)
        self.Bind(wx.EVT_TEXT, self.OnTextChanged, self.cb)
        button_login = wx.Button(self.panel, -1, 'Login')
        self.box.Add(button_login, 1)
        self.Bind(wx.EVT_BUTTON, self.OnButtonLoginClicked, button_login)
        button_quit = wx.Button(self.panel, -1, 'Quit')
        self.box.Add(button_quit, 1)
        self.Bind(wx.EVT_BUTTON, self.OnButtonQuitClicked, button_quit)
        self.panel.SetSizer(self.box)
        self.Centre()
        self.Show()
        self.app.MainLoop()

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
            
    def OnButtonLoginClicked(self, event):
        if self.cb.GetValue():
            if not self.login.set_user_name(self.cb.GetValue()):
                self.create_user_popupwindow = CreateUserPopupWindow(self, self.cb.GetValue())
                self.create_user_popupwindow.Show()
            else:
                self.Close()
                
    def OnButtonQuitClicked(self, event):
        self.Close()
    
    def create_user(self, user_name):
        self.login.create_user(user_name)
        self.Close()