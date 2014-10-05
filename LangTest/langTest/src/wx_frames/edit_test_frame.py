
import wx
import logging
import string
from common import found_status

class InformNoEmptyFieldsPopupWindow(wx.Frame):
    def __init__(self, parent):
        self.logprefix = "InformNoEmptyFieldsPopupWindow"
        super(InformNoEmptyFieldsPopupWindow, self).__init__(parent, size=(300, 160))

    def start(self):
        logging.info("{0}:{1}: start".format(self.logprefix, "start"))
        self.Bind(wx.EVT_CLOSE, self.when_closed)
        self.SetBackgroundColour('WHITE')
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.AddSpacer(30)
        hbox.Add(wx.StaticText(self, id=-1, label="\nFields may not be empty\n", style=wx.ALIGN_CENTER), flag=wx.CENTER)
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

class InformItemExistsPopupWindow(wx.Frame):
    def __init__(self, parent):
        self.logprefix = "InformItemExistsPopupWindow"
        super(InformItemExistsPopupWindow, self).__init__(parent, size=(300, 160))

    def start(self, found_test_name, current_test_name):
        logging.info("{0}:{1}: start".format(self.logprefix, "start"))
        self.Bind(wx.EVT_CLOSE, self.when_closed)
        self.SetBackgroundColour('WHITE')
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(wx.StaticText(self, label="    ", style=wx.ALIGN_CENTER), flag=wx.CENTER)
        if found_test_name == current_test_name:
            hbox.Add(wx.StaticText(self, label="\nThis item already exists in this test\n", style=wx.ALIGN_CENTER), flag=wx.CENTER)
        else:
            hbox.Add(wx.StaticText(self, label="\nThis item already exists in test '" + found_test_name + "'\n", style=wx.ALIGN_CENTER), flag=wx.CENTER)
        hbox.Add(wx.StaticText(self, label="    ", style=wx.ALIGN_CENTER), flag=wx.CENTER)
        vbox.Add(hbox)
        vbox.AddSpacer(30)
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

class SelectOtherTestPopupWindow(wx.Frame):
    def __init__(self, parent):
        self.logprefix = "InformItemExistsPopupWindow"
        super(SelectOtherTestPopupWindow, self).__init__(parent, size=(300, 160))

    def start(self, ret_list, parent):
        logging.info("{0}:{1}: start".format(self.logprefix, "start"))
        self.parent = parent
        self.Bind(wx.EVT_CLOSE, self.when_closed)
        self.SetBackgroundColour('WHITE')
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(wx.StaticText(self, label="    ", style=wx.ALIGN_CENTER), flag=wx.CENTER)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        (found_status, found_test_name_to_values, self.german_value, self.english_value) = ret_list[0]
        self.button_to_test_name = dict()
        if found_status == found_status.FoundStatus.DE_FOUND:
            vbox2.Add(wx.StaticText(self, id=-1, label="\nThe German expression", style=wx.ALIGN_CENTER), flag=wx.CENTER)
            vbox2.Add(wx.StaticText(self, id=-1, label="'" + self.german_value + "'", style=wx.ALIGN_CENTER), flag=wx.CENTER)
            vbox2.Add(wx.StaticText(self, id=-1, label="\nhas been found elsewhere. Please choose a test to append your item to.", style=wx.ALIGN_CENTER), flag=wx.CENTER)
            grid = wx.FlexGridSizer(len(found_test_name_to_values), 3)
            grid.Add(wx.StaticText(self, id=-1, label="\nTest name", style=wx.ALIGN_CENTER))
            grid.Add(wx.StaticText(self, id=-1, label="\nEnglish translations", style=wx.ALIGN_CENTER))
            grid.Add(wx.StaticText(self, id=-1, style=wx.ALIGN_CENTER))
            for test_name in found_test_name_to_values:
                grid.Add(wx.StaticText(self, id=-1, label=test_name, style=wx.ALIGN_CENTER))
                found_values = found_test_name_to_values[test_name]
                found_values_string = string()
                for found_value in found_values:
                    found_values_string += "'" + found_value + "'\n"
                grid.Add(wx.StaticText(self, id=-1, label=found_values_string, style=wx.ALIGN_CENTER))
                button_append = wx.Button(self, -1, 'Append')
                self.Bind(wx.EVT_BUTTON, self.OnButtonAppendClicked, button_append)
                self.button_to_test_name[button_append] = test_name
            vbox2.Add(grid)
        if len(ret_list) == 2:
            (found_status, found_test_name_to_values, self.german_value, self.english_value) = ret_list[1]
            if found_status == found_status.FoundStatus.EN_FOUND:
                vbox2.Add(wx.StaticText(self, id=-1, label="\nThe English expression", style=wx.ALIGN_CENTER), flag=wx.CENTER)
                vbox2.Add(wx.StaticText(self, id=-1, label="'" + self.english_value + "'", style=wx.ALIGN_CENTER), flag=wx.CENTER)
                vbox2.Add(wx.StaticText(self, id=-1, label="\nhas been found elsewhere. Please choose a test to append your item to.", style=wx.ALIGN_CENTER), flag=wx.CENTER)
                grid = wx.FlexGridSizer(len(found_test_name_to_values), 3)
                grid.Add(wx.StaticText(self, id=-1, label="\nTest name", style=wx.ALIGN_CENTER))
                grid.Add(wx.StaticText(self, id=-1, label="\nGerman translations", style=wx.ALIGN_CENTER))
                grid.Add(wx.StaticText(self, id=-1, style=wx.ALIGN_CENTER))
                for test_name in found_test_name_to_values:
                    grid.Add(wx.StaticText(self, id=-1, label=test_name, style=wx.ALIGN_CENTER))
                    found_values = found_test_name_to_values[test_name]
                    found_values_string = string()
                    for found_value in found_values:
                        found_values_string += "'" + found_value + "'\n"
                    grid.Add(wx.StaticText(self, id=-1, label=found_values_string, style=wx.ALIGN_CENTER))
                    button_append = wx.Button(self, -1, 'Append')
                    self.Bind(wx.EVT_BUTTON, self.OnButtonAppendClicked, button_append)
                    self.button_to_test_name[id(button_append)] = test_name
                    grid.Add(button_append)
                vbox2.Add(grid)
        hbox.Add(vbox2)
        hbox.Add(wx.StaticText(self, label="    ", style=wx.ALIGN_CENTER), flag=wx.CENTER)
        vbox.Add(hbox)
        vbox.AddSpacer(30)
        button_ok = wx.Button(self, -1, 'OK')
        self.Bind(wx.EVT_BUTTON, self.OnButtonOKClicked, button_ok)
        vbox.Add(button_ok, 1, flag=wx.CENTER)
        vbox.Add(wx.StaticText(self, style=wx.ALIGN_CENTER), flag=wx.CENTER)
        self.SetSizerAndFit(vbox)
        self.Centre()
        self.Raise()
        self.MakeModal(True)
        self.Show()
        
    def OnButtonAppendClicked(self, event):
        self.parent.append_item_to_other_test(self.button_to_test_name[id(event.GetEventObject())], self.german_value, self.english_value)

    def OnButtonOKClicked(self, event):
        logging.info("{0}:{1}: user clicked OK".format(self.logprefix, "OnButtonOKClicked"))
        self.Unbind(wx.EVT_CLOSE)
        self.MakeModal(False)
        self.Close()
        
    def when_closed(self, event):
        logging.info("{0}:{1}: user clicked close".format(self.logprefix, "when_closed"))
        self.OnButtonOKClicked(event)

class EditTestFrame(wx.Frame):
    def __init__(self):
        self.logprefix = "EditTestFrame"
        super(EditTestFrame, self).__init__(None, title="Language test", size=(300, 800))

    def start(self, editTest):
        logging.info("{0}:{1}: start".format(self.logprefix, "start"))
        self.editTest = editTest
        self.Bind(wx.EVT_CLOSE, self.when_closed)
        self.SetBackgroundColour('WHITE')
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(wx.StaticText(self, label='\nView and edit items:\n'), flag=wx.CENTER)
        grid = wx.FlexGridSizer(2, 4, hgap=20)
        self.firstEditStaticText = wx.StaticText(self)
        self.secondEditStaticText = wx.StaticText(self)
        self.button_switch = wx.Button(self, -1)
        self.Bind(wx.EVT_BUTTON, self.OnDeToEnSwitch, self.button_switch)
        if self.editTest.getDeToEn():
            self.firstEditStaticText.SetLabel('\nGerman:\n')
            self.secondEditStaticText.SetLabel('\nEnglish:\n')
            self.button_switch.SetLabel('Switch to\nEnglish to German')
        else:
            self.firstEditStaticText.SetLabel('\nEnglish:\n')
            self.secondEditStaticText.SetLabel('\nGerman:\n')
            self.button_switch.SetLabel('Switch to\nGerman to English')
        grid.Add(self.firstEditStaticText, flag=wx.CENTER)
        grid.Add(self.secondEditStaticText, flag=wx.CENTER)
        grid.Add(self.button_switch)
        grid.Add(wx.StaticText(self))
        self.firstEditText = wx.TextCtrl(self, size=(250, 50), style = wx.TE_MULTILINE)
        self.secondEditText = wx.TextCtrl(self, size=(250, 50), style = wx.TE_MULTILINE)
        self.button_next_item = wx.Button(self, -1, label='Show first item')
        self.button_previous_item = wx.Button(self, -1, label='Show previous item')
        grid.Add(self.firstEditText, flag=wx.CENTER)
        grid.Add(self.secondEditText, flag=wx.CENTER)
        grid.Add(self.button_next_item, flag=wx.CENTER)
        grid.Add(self.button_previous_item, flag=wx.CENTER)
        vbox.Add(grid, flag=wx.CENTER)
        vbox.Add(wx.StaticText(self, label='\nSearch for an item in the test:\n'), flag=wx.CENTER)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.input_search_term = wx.TextCtrl(self)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnButtonSearchClicked, self.input_search_term)
        hbox.Add(self.input_search_term, 1)
        hbox.AddSpacer(20)
        self.button_search = wx.Button(self, -1, 'Search')
        self.Bind(wx.EVT_BUTTON, self.OnButtonSearchClicked, self.button_search)
        hbox.Add(self.button_search, 1)
        vbox.Add(hbox, flag=wx.CENTER)
        vbox.Add(wx.StaticText(self, label='\nAppend an item to the test:\n'), flag=wx.CENTER)
        grid2 = wx.FlexGridSizer(2, 4, hgap=20)
        self.firstAppendStaticText = wx.StaticText(self)
        self.secondAppendStaticText = wx.StaticText(self)
        self.button_switch2 = wx.Button(self, -1)
        self.Bind(wx.EVT_BUTTON, self.OnDeToEnSwitch, self.button_switch2)
        if self.editTest.getDeToEn():
            self.firstAppendStaticText.SetLabel('\nGerman:\n')
            self.secondAppendStaticText.SetLabel('\nEnglish:\n')
            self.button_switch2.SetLabel('Switch to\nEnglish to German')
        else:
            self.firstAppendStaticText.SetLabel('\nEnglish:\n')
            self.secondAppendStaticText.SetLabel('\nGerman:\n')
            self.button_switch2.SetLabel('Switch to\nGerman to English')
        grid2.Add(self.firstAppendStaticText, flag=wx.CENTER)
        grid2.Add(self.secondAppendStaticText, flag=wx.CENTER)
        grid2.Add(self.button_switch2)
        grid2.Add(wx.StaticText(self), flag=wx.CENTER)
        self.firstAppendText = wx.TextCtrl(self, size=(250, 50), style = wx.TE_MULTILINE)
        self.secondAppendText = wx.TextCtrl(self, size=(250, 50), style = wx.TE_MULTILINE)
        self.button_append_item = wx.Button(self, -1, label='Append')
        self.Bind(wx.EVT_BUTTON, self.OnAppendClick, self.button_append_item)
        grid2.Add(self.firstAppendText, flag=wx.CENTER)
        grid2.Add(self.secondAppendText, flag=wx.CENTER)
        grid2.Add(self.button_append_item, flag=wx.CENTER)
        self.nItems_text = wx.StaticText(self, 
                                         label='Number of items\n      in test: {0}\n'.format(self.editTest.getNumberOfItems()), 
                                         style=wx.ALIGN_LEFT)
        grid2.Add(self.nItems_text, flag=wx.ALIGN_LEFT)
        vbox.Add(grid2, flag=wx.CENTER)
        vbox.Add(wx.StaticText(self, label='\nMultiple item operations:\n'), flag=wx.CENTER)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.button_import = wx.Button(self, -1, 'Import from file')
        self.button_export = wx.Button(self, -1, 'Export to file')
        self.button_clear = wx.Button(self, -1, 'Clear test')
        hbox2.Add((270,-1))
        hbox2.Add(self.button_import, flag=wx.CENTER)
        hbox2.Add((30,-1))
        hbox2.Add(self.button_export, flag=wx.CENTER)
        hbox2.Add((30,-1))
        hbox2.Add(self.button_clear, flag=wx.CENTER)
        hbox2.Add((270,-1))
        vbox.Add(hbox2, flag=wx.ALIGN_CENTER)
        vbox.AddSpacer(60)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        button_quit = wx.Button(self, -1, 'Quit')
        self.Bind(wx.EVT_BUTTON, self.OnButtonQuitClicked, button_quit)
        self.button_start_test = wx.Button(self, -1, 'Start test')
        button_test_selection = wx.Button(self, -1, '<< Back\nto login')
        self.Bind(wx.EVT_BUTTON, self.OnButtonTestSelectionClicked, button_test_selection)
        hbox3.AddSpacer(30)
        hbox3.Add(button_test_selection, 1)
        hbox3.AddSpacer(60)
        hbox3.Add(self.button_start_test, 1)
        hbox3.AddSpacer(60)
        hbox3.Add(button_quit, 1)
        hbox3.AddSpacer(30)
        vbox.Add(hbox3, flag=wx.CENTER)
        vbox.AddSpacer(30)
        self.fully_enabled = True
        if not self.editTest.getNumberOfItems():
            self.firstEditText.Disable()
            self.secondEditText.Disable()
            self.button_switch.Disable()
            self.button_next_item.Disable()
            self.button_previous_item.Disable()
            self.input_search_term.Disable()
            self.button_search.Disable()
            self.button_export.Disable()
            self.button_clear.Disable()
            self.button_start_test.Disable()
            self.fully_enabled = False
        self.SetSizerAndFit(vbox)
        self.Centre()
        self.Show()

    def OnAppendClick(self, event):
        firstAppendTextValue = self.firstAppendText.GetValue()
        secondAppendTextValue = self.secondAppendText.GetValue()
        if not firstAppendTextValue or not secondAppendTextValue:
            self.editTest.inform_no_empty_fields()
        else:
            ret_list = self.editTest.append_item(firstAppendTextValue, secondAppendTextValue)
            the_found_status = ret_list[0][0]
            logging.info("{0}:{1}: found status: {2}".format(self.logprefix, "OnAppendClick", the_found_status))
            if the_found_status == found_status.FoundStatus.NONE_FOUND:
                if not self.fully_enabled:
                    self.firstEditText.Enable()
                    self.secondEditText.Enable()
                    self.button_switch.Enable()
                    self.button_next_item.Enable()
                    self.button_previous_item.Enable()
                    self.input_search_term.Enable()
                    self.button_search.Enable()
                    self.button_export.Enable()
                    self.button_clear.Enable()
                    self.button_start_test.Enable()
                    self.fully_enabled = True
                logging.info("{0}:{1}: Number of items: {2}".format(self.logprefix, "OnAppendClick", self.editTest.getNumberOfItems()))
                self.nItems_text.SetLabel('Number of items\n      in test: {0}\n'.format(self.editTest.getNumberOfItems()))
                self.firstAppendText.Clear()
                self.secondAppendText.Clear()
            elif the_found_status == found_status.FoundStatus.BOTH_FOUND:
                found_test_name = ret_list[0][1].keys()[0]
                self.editTest.inform_item_exists(found_test_name)
            else:
                self.editTest.select_other_test(ret_list)

    def OnDeToEnSwitch(self, event):
        self.editTest.switchDeToEn()
        if self.editTest.getDeToEn():
            logging.info("{0}:{1}: DeToEn: {2}".format(self.logprefix, "OnDeToEnSwitch", "True"))
            self.button_switch.SetLabel('Switch to\nEnglish to German')
            self.button_switch2.SetLabel('Switch to\nEnglish to German')
            self.firstEditStaticText.SetLabel('\nGerman:\n')
            self.secondEditStaticText.SetLabel('\nEnglish:\n')
            self.firstAppendStaticText.SetLabel('\nGerman:\n')
            self.secondAppendStaticText.SetLabel('\nEnglish:\n')
        else:
            logging.info("{0}:{1}: DeToEn: {2}".format(self.logprefix, "OnDeToEnSwitch", "False"))
            self.button_switch.SetLabel('Switch to\nGerman to English')
            self.button_switch2.SetLabel('Switch to\nGerman to English')
            self.firstEditStaticText.SetLabel('\nEnglish:\n')
            self.secondEditStaticText.SetLabel('\nGerman:\n')
            self.firstAppendStaticText.SetLabel('\nEnglish:\n')
            self.secondAppendStaticText.SetLabel('\nGerman:\n')
        firstAppendTextValue = self.firstAppendText.GetValue()
        self.firstAppendText.SetValue(self.secondAppendText.GetValue())
        self.secondAppendText.SetValue(firstAppendTextValue)
        
    def OnButtonSearchClicked(self, event):
        logging.info("{0}:{1}: user clicked search".format(self.logprefix, "OnButtonSearchClicked"))

    def OnButtonQuitClicked(self, event):
        logging.info("{0}:{1}: user clicked quit".format(self.logprefix, "OnButtonQuitClicked"))
        self.Unbind(wx.EVT_CLOSE)
        self.Hide()
        self.editTest.quit()
        self.Close()

    def OnButtonTestSelectionClicked(self, event):
        logging.info("{0}:{1}: user clicked back to login".format(self.logprefix, "OnButtonTestSelectionClicked"))
        self.Unbind(wx.EVT_CLOSE)
        self.Hide()
        self.editTest.back_to_test_selection()
        self.Close()
    
    def when_closed(self, event):
        logging.info("{0}:{1}: user clicked close".format(self.logprefix, "when_closed"))
        self.OnButtonQuitClicked(event)
