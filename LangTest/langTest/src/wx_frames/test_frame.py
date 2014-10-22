
import wx
import logging

class TestFrame(wx.Frame):
    def __init__(self):
        self.logprefix = "TestFrame"
        super(TestFrame, self).__init__(None, title="Language test", size=(300, 300))

    def start(self, test):
        logging.info("{0}:{1}: start".format(self.logprefix, "start"))
        self.test = test
        self.Bind(wx.EVT_CLOSE, self.when_closed)
        self.SetBackgroundColour('WHITE')
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox_info = wx.BoxSizer(wx.HORIZONTAL)
        hbox_info.Add(wx.StaticText(self, label='\n                                          '), flag=wx.CENTER)
        hbox_info.Add(wx.StaticText(self, label='\nTest:  ' + self.test.getTestName()), flag=wx.CENTER)
        hbox_info.Add(wx.StaticText(self, label='\n                                   '), flag=wx.CENTER)
        self.nItems_text = wx.StaticText(self, label='\nNumber of items: {0}'.format(self.test.getNumberOfItems()))
        hbox_info.Add(self.nItems_text, flag=wx.CENTER)
        hbox_info.Add(wx.StaticText(self, label='\n                                   '), flag=wx.CENTER)
        hbox_info.Add(wx.StaticText(self, label='\nUser:  ' + self.test.getUserName()), flag=wx.CENTER)
        hbox_info.Add(wx.StaticText(self, label='\n                                          '), flag=wx.CENTER)
        vbox.Add(hbox_info, flag=wx.CENTER)
        vbox.AddSpacer(60)
        grid = wx.FlexGridSizer(2, 3, hgap=20)
        firstStaticText = wx.StaticText(self)
        secondStaticText = wx.StaticText(self)
        if self.test.getDeToEn():
            firstStaticText.SetLabel('\nGerman:\n')
            secondStaticText.SetLabel('\nEnglish:\n')
        else:
            firstStaticText.SetLabel('\nEnglish:\n')
            secondStaticText.SetLabel('\nGerman:\n')
        grid.Add(firstStaticText, flag=wx.CENTER)
        grid.Add(secondStaticText, flag=wx.CENTER)
        grid.Add(wx.StaticText(self, label=''), flag=wx.CENTER)
        self.firstEditText = wx.TextCtrl(self, size=(250, 50), style = wx.TE_MULTILINE)
        self.secondEditText = wx.TextCtrl(self, size=(250, 50), style = wx.TE_MULTILINE)
        grid.Add(self.firstEditText, flag=wx.CENTER)
        grid.Add(self.secondEditText, flag=wx.CENTER)
        self.Bind(wx.EVT_TEXT, self.OnFirstEditTextChanged, self.firstEditText)
        self.Bind(wx.EVT_TEXT, self.OnSecondEditTextChanged, self.secondEditText)
        grid2 = wx.FlexGridSizer(2, 2, hgap=10, vgap=10)
        self.button_submit = wx.Button(self, -1, label='Submit')
        self.Bind(wx.EVT_BUTTON, self.OnButtonSubmitClicked, self.button_submit)
        self.button_save = wx.Button(self, -1, label='Save')
        self.Bind(wx.EVT_BUTTON, self.OnButtonSaveClicked, self.button_save)
        self.button_skip = wx.Button(self, -1, label='Skip')
        self.Bind(wx.EVT_BUTTON, self.OnButtonSkipClicked, self.button_skip)
        self.button_view_answer = wx.Button(self, -1, label='View answer')
        self.Bind(wx.EVT_BUTTON, self.OnButtonViewAnswerClicked, self.button_view_answer)
        grid2.Add(self.button_submit, flag=wx.CENTER)
        grid2.Add(self.button_save, flag=wx.CENTER)
        grid2.Add(self.button_skip, flag=wx.CENTER)
        grid2.Add(self.button_view_answer, flag=wx.CENTER)
        grid.Add(grid2, flag=wx.CENTER)
        vbox.Add(grid, flag=wx.CENTER)
        self.wrongRightText = wx.StaticText(self)
        vbox.Add(self.wrongRightText, flag=wx.CENTER)
        vbox.AddSpacer(60)
        self.previousItemStaticText = wx.StaticText(self, label="Correct answer to previous question:")
        vbox.Add(self.previousItemStaticText, flag=wx.CENTER)
        vbox.Add(wx.StaticText(self), flag=wx.CENTER)
        self.previousItemText = wx.StaticText(self, label="(Answer will be placed here)")
        vbox.Add(self.previousItemText, flag=wx.CENTER)
        vbox.Add(wx.StaticText(self), flag=wx.CENTER)
        self.button_edit = wx.Button(self, -1, label='Edit')
        self.Bind(wx.EVT_BUTTON, self.OnButtonEditClicked, self.button_edit)
        vbox.Add(self.button_edit, flag=wx.CENTER)
        vbox.AddSpacer(60)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(wx.StaticText(self, label='\n                                          '), flag=wx.CENTER)
        grid3 = wx.FlexGridSizer(2, 2, hgap=60, vgap=10)
        self.numberRightText = wx.StaticText(self, label="Correct answers:    ")
        grid3.Add(self.numberRightText, flag=wx.CENTER)
        self.numberWrongText = wx.StaticText(self, label="Wrong answers:    ")
        grid3.Add(self.numberWrongText, flag=wx.CENTER)
        self.numberAnsweredText = wx.StaticText(self, label="Questions answered:    ")
        grid3.Add(self.numberAnsweredText, flag=wx.CENTER)
        self.numberRemainingText = wx.StaticText(self, label="Remaining answers:    ")
        grid3.Add(self.numberRemainingText, flag=wx.CENTER)
        hbox.Add(grid3, flag=wx.CENTER)
        hbox.Add(wx.StaticText(self, label='\n                                          '), flag=wx.CENTER)
        vbox.Add(hbox, flag=wx.CENTER)
        vbox.AddSpacer(60)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        button_quit = wx.Button(self, -1, 'Quit')
        self.Bind(wx.EVT_BUTTON, self.OnButtonQuitClicked, button_quit)
        button_edit_test = wx.Button(self, -1, '<< Back to\n test editing')
        self.Bind(wx.EVT_BUTTON, self.OnButtonEditTestClicked, button_edit_test)
        hbox3.AddSpacer(30)
        hbox3.Add(button_edit_test, 1, flag=wx.CENTER)
        hbox3.AddSpacer(60)
        hbox3.Add(button_quit, 1, flag=wx.CENTER)
        hbox3.AddSpacer(30)
        vbox.Add(hbox3, flag=wx.CENTER)
        vbox.AddSpacer(60)
        self.SetSizerAndFit(vbox)
        self.Centre()
        self.Show()
        
    def OnButtonEditTestClicked(self, event):
        self.Unbind(wx.EVT_CLOSE)
        self.Hide()
        self.test.back_to_edit_test()
        self.Close()
        
    def OnButtonQuitClicked(self, event):
        logging.info("{0}:{1}: user clicked quit".format(self.logprefix, "OnButtonQuitClicked"))
        self.Unbind(wx.EVT_CLOSE)
        self.Hide()
        self.test.quit()
        self.Close()

    def OnFirstEditTextChanged(self, event):
        pass

    def OnSecondEditTextChanged(self, event):
        pass

    def OnButtonEditClicked(self, event):
        pass
        
    def OnButtonViewAnswerClicked(self, event):
        pass
        
    def OnButtonSkipClicked(self, event):
        pass
        
    def OnButtonSaveClicked(self, event):
        pass
        
    def OnButtonSubmitClicked(self, event):
        pass
        
    def when_closed(self, event):
        logging.info("{0}:{1}: user clicked close".format(self.logprefix, "when_closed"))
        self.OnButtonQuitClicked(event)

    def OnButtonQuitClicked(self, event):
        logging.info("{0}:{1}: user clicked quit".format(self.logprefix, "OnButtonQuitClicked"))
        self.Unbind(wx.EVT_CLOSE)
        self.Hide()
        self.test.quit()
        self.Close()

    def OnButtonTestSelectionClicked(self, event):
        logging.info("{0}:{1}: user clicked back to test selection".format(self.logprefix, "OnButtonTestSelectionClicked"))
        self.Unbind(wx.EVT_CLOSE)
        self.Hide()
        self.test.back_to_test_selection()
        self.Close()
    