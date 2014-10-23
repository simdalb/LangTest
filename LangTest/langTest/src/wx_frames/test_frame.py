
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
        hbox_info.Add(wx.StaticText(self, label='\n                               '), flag=wx.CENTER)
        hbox_info.Add(wx.StaticText(self, label='\nTest:  ' + self.test.getTestName()), flag=wx.CENTER)
        hbox_info.Add(wx.StaticText(self, label='\n                                   '), flag=wx.CENTER)
        self.nItems_text = wx.StaticText(self, label='\nNumber of items: {0}'.format(self.test.getNumberOfItems()))
        hbox_info.Add(self.nItems_text, flag=wx.CENTER)
        hbox_info.Add(wx.StaticText(self, label='\n                                   '), flag=wx.CENTER)
        hbox_info.Add(wx.StaticText(self, label='\nUser:  ' + self.test.getUserName()), flag=wx.CENTER)
        hbox_info.Add(wx.StaticText(self, label='\n                               '), flag=wx.CENTER)
        vbox.Add(hbox_info, flag=wx.CENTER)
        vbox.AddSpacer(30)
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
        grid.Add(wx.StaticText(self), flag=wx.CENTER)
        self.firstEditText = wx.TextCtrl(self, size=(250, 50), style = wx.TE_MULTILINE)
        self.secondEditText = wx.TextCtrl(self, size=(250, 50), style = wx.TE_MULTILINE)
        self.firstEditText.SetEditable(False)
        grid.Add(self.firstEditText, flag=wx.CENTER)
        grid.Add(self.secondEditText, flag=wx.CENTER)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnSecondEditTextEntered, self.secondEditText)
        self.button_submit = wx.Button(self, -1, label='Submit')
        self.Bind(wx.EVT_BUTTON, self.OnButtonSubmitClicked, self.button_submit)
        grid.Add(self.button_submit, flag=wx.CENTER)
        vbox.Add(grid, flag=wx.CENTER)
        self.wrongRightText = wx.StaticText(self)
        vbox.Add(self.wrongRightText, flag=wx.LEFT)
        vbox.AddSpacer(30)
        self.previousItemStaticText = wx.StaticText(self, label="Previous question and correct answer:")
        vbox.Add(self.previousItemStaticText, flag=wx.CENTER)
        vbox.AddSpacer(10)
        self.previousItemText = wx.StaticText(self, style=wx.ALIGN_CENTER)
        vbox.Add(self.previousItemText, flag=wx.ALIGN_CENTER)
        vbox.AddSpacer(10)
        self.button_edit = wx.Button(self, -1, label='Edit')
        self.Bind(wx.EVT_BUTTON, self.OnButtonEditClicked, self.button_edit)
        vbox.Add(self.button_edit, flag=wx.CENTER)
        vbox.AddSpacer(30)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(wx.StaticText(self, label='\n                                          '), flag=wx.CENTER)
        grid3 = wx.FlexGridSizer(2, 2, hgap=60, vgap=10)
        self.numberRightText = wx.StaticText(self, label="Correct answers: " + self.get_number_with_padding(0))
        grid3.Add(self.numberRightText, flag=wx.CENTER)
        self.numberWrongText = wx.StaticText(self, label="Wrong answers: " + self.get_number_with_padding(0))
        grid3.Add(self.numberWrongText, flag=wx.CENTER)
        self.numberAnsweredText = wx.StaticText(self, label="Questions answered: " + self.get_number_with_padding(0))
        grid3.Add(self.numberAnsweredText, flag=wx.CENTER)
        self.numberRemainingText = wx.StaticText(self, label="Remaining answers: " + self.get_number_with_padding(self.test.getNumberOfItems()))
        grid3.Add(self.numberRemainingText, flag=wx.CENTER)
        hbox.Add(grid3, flag=wx.CENTER)
        hbox.Add(wx.StaticText(self, label='\n                                          '), flag=wx.CENTER)
        vbox.Add(hbox, flag=wx.CENTER)
        vbox.AddSpacer(30)
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
        vbox.AddSpacer(30)
        self.button_edit.Disable()
        self.firstEditText.SetValue(self.test.getNextQuestion())
        self.secondEditText.SetFocus()
        self.SetSizerAndFit(vbox)
        self.Centre()
        self.Show()
        self.previousItemText.SetLabel("(Answer will be placed here)")
        self.previousItemText.Center()
        
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
        
    def handle_submitted_answer(self, answer):
        (score, wrong, done, remaining, correct, item) = self.test.update_results(answer)
        logging.info("{0}:{1}: correct: {2}".format(self.logprefix, "handle_submitted_answer", correct))
        self.numberRightText.SetLabel("Correct answers: " + self.get_number_with_padding(score))
        self.numberWrongText.SetLabel("Wrong answers: " + self.get_number_with_padding(wrong))
        self.numberAnsweredText.SetLabel("Questions answered: " + self.get_number_with_padding(done))
        self.numberRemainingText.SetLabel("Remaining answers: " + self.get_number_with_padding(remaining))
        if correct:
            self.wrongRightText.SetLabel("                    Correct")
        else:
            self.wrongRightText.SetLabel("                    The answer '" + answer + "' is wrong")
        self.previousItemText.SetLabel(item)
        self.previousItemText.Center()
        if not self.button_edit.IsEnabled():
            self.button_edit.Enable()
        self.firstEditText.SetValue(self.test.getNextQuestion())
        self.secondEditText.Clear()
        self.secondEditText.SetFocus()
        
    def get_number_with_padding(self, number):
        if number < 10:
            return "  " + str(number)
        elif number < 100:
            return " " + str(number)
        else:
            return str(number)

    def OnSecondEditTextEntered(self, event):
        self.handle_submitted_answer(self.secondEditText.GetValue())

    def OnButtonEditClicked(self, event):
        pass

    def OnButtonSubmitClicked(self, event):
        self.handle_submitted_answer(self.secondEditText.GetValue())
        
    def when_closed(self, event):
        logging.info("{0}:{1}: user clicked close".format(self.logprefix, "when_closed"))
        self.OnButtonQuitClicked(event)

    def OnButtonTestSelectionClicked(self, event):
        logging.info("{0}:{1}: user clicked back to test selection".format(self.logprefix, "OnButtonTestSelectionClicked"))
        self.Unbind(wx.EVT_CLOSE)
        self.Hide()
        self.test.back_to_test_selection()
        self.Close()
    