
import wx

class CreateUserPopupWindow(wx.Frame):
    def __init__(self, parent):
        super(CreateUserPopupWindow, self).__init__(parent, size=(300, 160))
        
    def start(self, user_name, parent):
        self.parent = parent
        self.user_name = user_name
        self.SetBackgroundColour('WHITE')
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(wx.StaticText(self, id=-1, label="\nCreate new user\"" + user_name + "\"?\n", style=wx.ALIGN_CENTER), flag=wx.CENTER)
        grid_sizer = wx.GridSizer(1, 2, 10, 20)
        button_create = wx.Button(self, -1, 'Create')
        self.Bind(wx.EVT_BUTTON, self.OnButtonCreateClicked, button_create)
        grid_sizer.Add(button_create, 1)
        button_dismiss = wx.Button(self, -1, 'Dismiss')
        self.Bind(wx.EVT_BUTTON, self.OnButtonDismissClicked, button_dismiss)
        grid_sizer.Add(button_dismiss, 1)
        box.Add(grid_sizer, flag=wx.CENTER)
        self.SetSizer(box)
        self.Centre()
        self.Raise()
        self.Show()

    def OnButtonCreateClicked(self, event):
        self.parent.create_user(self.user_name)
        self.Close()

    def OnButtonDismissClicked(self, event):
        self.Close()

class LoginFrame(wx.Frame):
    def __init__(self):
        super(LoginFrame, self).__init__(None, title="Login, or create an account", size=(200,300))
        
    def start(self, login):
        self.no_ignore_OnTextChange = False
        self.login = login
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
                self.login.prompt_new_user(self.cb.GetValue())
            else:
                self.Close()
                
    def OnButtonQuitClicked(self, event):
        self.Close()
    
    def create_user(self, user_name):
        self.login.create_user(user_name)
        self.Close()