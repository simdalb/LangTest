
import wx
import logging

class InformUserExistsPopupWindow(wx.Frame):
    def __init__(self, parent):
        self.logprefix = "InformUserExistsPopupWindow"
        super(InformUserExistsPopupWindow, self).__init__(parent, size=(300, 160))

    def start(self, user_name):
        logging.info("{0}:{1}: start".format(self.logprefix, "start"))
        self.Bind(wx.EVT_CLOSE, self.when_closed)
        self.SetBackgroundColour('WHITE')
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.AddSpacer(30)
        hbox.Add(wx.StaticText(self, id=-1, label="\nUser name \"" + user_name + "\" already exists,\nplease choose a different user name\n", style=wx.ALIGN_CENTER), flag=wx.CENTER)
        hbox.AddSpacer(30)
        vbox.Add(hbox)
        button_ok = wx.Button(self, -1, 'OK')
        self.Bind(wx.EVT_BUTTON, self.OnButtonOKClicked, button_ok)
        vbox.Add(button_ok, 1, flag=wx.CENTER)
        vbox.Add(wx.StaticText(self, style=wx.ALIGN_CENTER), flag=wx.CENTER)
        self.SetSizerAndFit(vbox)
        self.Centre()
        self.Raise()
        self.MakeModal(True)
        self.Show()

    def OnButtonOKClicked(self, event):
        logging.info("{0}:{1}: user clicked OK".format(self.logprefix, "OnButtonOKClicked"))
        self.Unbind(wx.EVT_CLOSE)
        self.MakeModal(False)
        self.Close()
        
    def when_closed(self, event):
        logging.info("{0}:{1}: user clicked close".format(self.logprefix, "when_closed"))
        self.OnButtonOKClicked(event)

class CreateUserPopupWindow(wx.Frame):
    def __init__(self, parent):
        self.logprefix = "CreateUserPopupWindow"
        super(CreateUserPopupWindow, self).__init__(parent, size=(400, 160))

    def start(self, user_name, parent):
        logging.info("{0}:{1}: start".format(self.logprefix, "start"))
        self.parent = parent
        self.user_name = user_name
        self.Bind(wx.EVT_CLOSE, self.when_closed)
        self.SetBackgroundColour('WHITE')
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(wx.StaticText(self, id=-1, label="\nCreate new user \"" + user_name + "\"?\n", style=wx.ALIGN_CENTER), flag=wx.CENTER)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.AddSpacer(20)
        button_create = wx.Button(self, -1, 'Create\nand login')
        self.Bind(wx.EVT_BUTTON, self.OnButtonCreateClicked, button_create)
        hbox.Add(button_create, 1)
        hbox.AddSpacer(20)
        button_dismiss = wx.Button(self, -1, 'Dismiss')
        self.Bind(wx.EVT_BUTTON, self.OnButtonDismissClicked, button_dismiss)
        hbox.Add(button_dismiss, 1)
        hbox.AddSpacer(20)
        box.Add(hbox, flag=wx.CENTER)
        box.Add(wx.StaticText(self, style=wx.ALIGN_CENTER), flag=wx.CENTER)
        self.SetSizerAndFit(box)
        self.Centre()
        self.Raise()
        self.MakeModal(True)
        self.Show()

    def OnButtonCreateClicked(self, event):
        logging.info("{0}:{1}: creating user name: {2}".format(self.logprefix, "OnButtonCreateClicked", self.user_name))
        self.MakeModal(False)
        self.Hide()
        self.parent.create_user(self.user_name)
        self.Close()

    def OnButtonDismissClicked(self, event):
        logging.info("{0}:{1}: user clicked dismiss".format(self.logprefix, "OnButtonDismissClicked"))
        self.Unbind(wx.EVT_CLOSE)
        self.MakeModal(False)
        self.Close()
        
    def when_closed(self, event):
        logging.info("{0}:{1}: user clicked close".format(self.logprefix, "when_closed"))
        self.OnButtonDismissClicked(event)

class LoginFrame(wx.Frame):
    def __init__(self):
        self.logprefix = "LoginFrame"
        super(LoginFrame, self).__init__(None, title="Language test", size=(300, 300))

    def start(self, login):
        logging.info("{0}:{1}: start".format(self.logprefix, "start"))
        self.login = login
        self.Bind(wx.EVT_CLOSE, self.when_closed)
        self.SetBackgroundColour('WHITE')
        vbox = wx.BoxSizer(wx.VERTICAL)
        users = login.get_users()
        logging.info("{0}:{1}: found {2} users".format(self.logprefix, "start", len(users)))
        if users:
            vbox.Add(wx.StaticText(self, label='\nDouble click your user name to login:\n'), flag=wx.CENTER)
            user_list_box = wx.ListBox(self, choices=users)
            self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnListItemDClicked, user_list_box)
            vbox.Add(user_list_box, 1, flag=wx.CENTER)
        vbox.Add(wx.StaticText(self, label='\nCreate a new user:\n'), flag=wx.CENTER)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.input_create_user = wx.TextCtrl(self)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnButtonCreateClicked, self.input_create_user)
        hbox.Add(self.input_create_user, 1)
        hbox.AddSpacer(20)
        button_create = wx.Button(self, -1, 'Create')
        self.Bind(wx.EVT_BUTTON, self.OnButtonCreateClicked, button_create)
        hbox.Add(button_create, 1)
        vbox.Add(hbox, flag=wx.CENTER)
        vbox.AddSpacer(60)
        button_quit = wx.Button(self, -1, 'Quit')
        self.Bind(wx.EVT_BUTTON, self.OnButtonQuitClicked, button_quit)
        grid = wx.GridSizer(1, 3)
        grid.Add(wx.StaticText(self), flag=wx.CENTER)
        grid.Add(button_quit, 1, flag=wx.CENTER)
        vbox.Add(grid, flag=wx.CENTER)
        vbox.Add(wx.StaticText(self), flag=wx.CENTER)
        self.SetSizerAndFit(vbox)
        self.Centre()
        self.Show()

    def OnListItemDClicked(self, event):
        logging.info("{0}:{1}: user clicked string: {2}".format(self.logprefix, "OnListItemDClicked", event.GetString()))
        self.Unbind(wx.EVT_CLOSE)
        self.Hide()
        self.login.set_user_name(event.GetString())
        self.Close()

    def OnButtonCreateClicked(self, event):
        value = self.input_create_user.GetValue()
        if value:
            if not self.login.user_exists(value):
                logging.info("{0}:{1}: user name: {2} does not exist".format(self.logprefix, "OnButtonCreateClicked", value))
                self.login.prompt_new_user(value)
            else:
                logging.info("{0}:{1}: user name: {2} exists".format(self.logprefix, "OnButtonCreateClicked", value))
                self.login.inform_user_exists(value)

    def OnButtonQuitClicked(self, event):
        logging.info("{0}:{1}: user clicked quit".format(self.logprefix, "OnButtonQuitClicked"))
        self.Unbind(wx.EVT_CLOSE)
        self.Hide()
        self.login.quit()
        self.Close()

    def when_closed(self, event):
        logging.info("{0}:{1}: user clicked close".format(self.logprefix, "when_closed"))
        self.OnButtonQuitClicked(event)

    def finish(self):
        logging.info("{0}:{1}: finish".format(self.logprefix, "finish"))
        self.Unbind(wx.EVT_CLOSE)
        self.Close()
