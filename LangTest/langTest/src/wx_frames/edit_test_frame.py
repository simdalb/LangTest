
import wx
import logging
from common import found_status
from common import item_list_bounds_status

class ShowSimilarResultsPopupWindow(wx.Frame):
    def __init__(self, parent):
        self.logprefix = "ShowSimilarResultsPopupWindow"
        super(ShowSimilarResultsPopupWindow, self).__init__(parent, size=(300, 160))

    def start(self, ret_list, german_value, english_value):
        logging.info("{0}:{1}: start".format(self.logprefix, "start"))
        self.german_value = german_value
        self.english_value = english_value
        self.Bind(wx.EVT_CLOSE, self.when_closed)
        self.SetBackgroundColour('WHITE')
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(wx.StaticText(self, label="    ", style=wx.ALIGN_CENTER), flag=wx.CENTER)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        self.button_to_test_name = dict()
        (the_found_status, values) = ret_list[0]
        self.addFoundResultList(vbox2, the_found_status, values)
        if len(ret_list) == 2:
            (the_found_status, values) = ret_list[1]
            self.addFoundTestList(vbox2, the_found_status, values)
        hbox.Add(vbox2)
        hbox.Add(wx.StaticText(self, label="    ", style=wx.ALIGN_CENTER), flag=wx.CENTER)
        vbox.Add(hbox)
        vbox.AddSpacer(20)
        button_OK = wx.Button(self, -1, 'OK')
        self.Bind(wx.EVT_BUTTON, self.OnButtonOKClicked, button_OK)
        vbox.Add(button_OK, 1, flag=wx.CENTER)
        vbox.AddSpacer(20)
        self.SetSizerAndFit(vbox)
        self.Centre()
        self.Raise()
        self.MakeModal(True)
        self.Show()

    def addFoundResultList(self, vbox, the_found_status, values):
        if not the_found_status == found_status.FoundStatus.DE_FOUND:
            vbox.Add(wx.StaticText(self, id=-1, label="\nThe German expression", style=wx.ALIGN_CENTER), flag=wx.CENTER)
            vbox.Add(wx.StaticText(self, id=-1, label="'" + self.german_value + "'", style=wx.ALIGN_CENTER), flag=wx.CENTER)
        else:
            vbox.Add(wx.StaticText(self, id=-1, label="\nThe English expression", style=wx.ALIGN_CENTER), flag=wx.CENTER)
            vbox.Add(wx.StaticText(self, id=-1, label="'" + self.english_value + "'", style=wx.ALIGN_CENTER), flag=wx.CENTER)
        vbox.Add(wx.StaticText(self, id=-1, label="has been found in other places in this test.", style=wx.ALIGN_CENTER), flag=wx.CENTER)
        grid = wx.FlexGridSizer(len(values) + 2, 1, hgap=50)
        if not the_found_status == found_status.FoundStatus.DE_FOUND:
            grid.Add(wx.StaticText(self, id=-1, label="\nEnglish translations", style=wx.ALIGN_CENTER))
        else:
            grid.Add(wx.StaticText(self, id=-1, label="\nGerman translations", style=wx.ALIGN_CENTER))
        grid.Add(wx.StaticText(self, id=-1, style=wx.ALIGN_CENTER))
        for value in values:
            logging.info("{0}:{1}: value: {2}".format(self.logprefix, "addFoundResultList", value))
            grid.Add(wx.StaticText(self, id=-1, label=value, style=wx.ALIGN_CENTER))
        vbox.Add(grid, flag=wx.CENTER)

    def OnButtonOKClicked(self, event):
        logging.info("{0}:{1}: user clicked close".format(self.logprefix, "OnButtonCancelClicked"))
        self.Unbind(wx.EVT_CLOSE)
        self.MakeModal(False)
        self.Close()

    def when_closed(self, event):
        logging.info("{0}:{1}: user clicked close".format(self.logprefix, "when_closed"))
        self.Unbind(wx.EVT_CLOSE)
        self.MakeModal(False)
        self.Close()

class SelectTestPopupWindow(wx.Frame):
    def __init__(self, parent):
        self.logprefix = "SelectTestPopupWindow"
        super(SelectTestPopupWindow, self).__init__(parent, size=(300, 160))

    def start(self, test_list, parent):
        logging.info("{0}:{1}: start".format(self.logprefix, "start"))
        self.test_list = test_list
        self.parent = parent
        self.Bind(wx.EVT_CLOSE, self.when_closed)
        self.SetBackgroundColour('WHITE')
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(wx.StaticText(self, label="    ", style=wx.ALIGN_CENTER), flag=wx.CENTER)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox2.Add(wx.StaticText(self, id=-1, label="\nPlease choose a test to move this item to", style=wx.ALIGN_CENTER), flag=wx.CENTER)
        grid = wx.FlexGridSizer(len(test_list) + 1, 3, hgap=50, vgap=10)
        grid.Add(wx.StaticText(self, id=-1, label="Test name", style=wx.ALIGN_CENTER))
        grid.Add(wx.StaticText(self, id=-1, label="Number of items", style=wx.ALIGN_CENTER))
        grid.Add(wx.StaticText(self, id=-1, style=wx.ALIGN_CENTER))
        self.button_to_test_id = dict()
        for test_details in test_list:
            grid.Add(wx.StaticText(self, id=-1, label="  " + test_details[1], style=wx.ALIGN_CENTER))
            grid.Add(wx.StaticText(self, id=-1, label="  " + str(test_details[2]), style=wx.ALIGN_CENTER))
            button_append = wx.Button(self, -1, 'Move')
            self.Bind(wx.EVT_BUTTON, self.OnButtonMoveClicked, button_append)
            logging.info("{0}:{1}: append button has id: {2}".format(self.logprefix, "start", id(button_append)))
            self.button_to_test_id[id(button_append)] = test_details[0]
            grid.Add(button_append)
        vbox2.Add(grid, flag=wx.CENTER)
        hbox.Add(vbox2)
        hbox.Add(wx.StaticText(self, label="    ", style=wx.ALIGN_CENTER), flag=wx.CENTER)
        vbox.Add(hbox)
        vbox.AddSpacer(20)
        button_cancel = wx.Button(self, -1, 'Cancel')
        self.Bind(wx.EVT_BUTTON, self.OnButtonCancelClicked, button_cancel)
        vbox.Add(button_cancel, 1, flag=wx.CENTER)
        vbox.AddSpacer(20)
        self.SetSizerAndFit(vbox)
        self.Centre()
        self.Raise()
        self.MakeModal(True)
        self.Show()

    def OnButtonMoveClicked(self, event):
        logging.info("{0}:{1}: append button with id: {2} was clicked".format(self.logprefix, 
                                                                              "OnButtonAppendClicked", 
                                                                              id(event.GetEventObject())))
        self.parent.move_item_to_other_test(self.button_to_test_id[id(event.GetEventObject())])
        self.Unbind(wx.EVT_CLOSE)
        self.MakeModal(False)
        self.Close()
        
    def OnButtonCancelClicked(self, event):
        logging.info("{0}:{1}: user clicked cancel".format(self.logprefix, "OnButtonCancelClicked"))
        self.Unbind(wx.EVT_CLOSE)
        self.MakeModal(False)
        self.Close()
        
    def when_closed(self, event):
        logging.info("{0}:{1}: user clicked close".format(self.logprefix, "when_closed"))
        self.OnButtonCancelClicked(event)

class SelectItemPopupWindow(wx.Frame):
    def __init__(self, parent):
        self.logprefix = "SelectItemPopupWindow"
        super(SelectItemPopupWindow, self).__init__(parent, size=(300, 160))

    def start(self, matches, parent):
        logging.info("{0}:{1}: start".format(self.logprefix, "start"))
        self.parent = parent
        self.matches = matches
        self.Bind(wx.EVT_CLOSE, self.when_closed)
        self.SetBackgroundColour('WHITE')
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(wx.StaticText(self, label='    '), flag=wx.CENTER)
        vbox = wx.BoxSizer(wx.VERTICAL)
        logging.info("{0}:{1}: found {2} matches".format(self.logprefix, "start", len(matches)))
        if matches:
            match_list = []
            for match in matches:
                match_list.append(match[1] + " | " + match[2])
            vbox.Add(wx.StaticText(self, label='\nDouble click a match:\n'), flag=wx.CENTER)
            match_list_box = wx.ListBox(self, choices=match_list)
            self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnListItemDClicked, match_list_box)
            vbox.Add(match_list_box, 1, flag=wx.CENTER)
            vbox.Add(wx.StaticText(self, style=wx.ALIGN_CENTER), flag=wx.CENTER)
            button_cancel = wx.Button(self, -1, 'Cancel')
            self.Bind(wx.EVT_BUTTON, self.OnButtonCancelClicked, button_cancel)
            vbox.Add(button_cancel, flag=wx.CENTER)
        else:
            vbox.Add(wx.StaticText(self, label='\nNo results found\n'), flag=wx.CENTER)
            button_OK = wx.Button(self, -1, 'OK')
            self.Bind(wx.EVT_BUTTON, self.OnButtonCancelClicked, button_OK)
            vbox.Add(button_OK, 1, flag=wx.CENTER)
        vbox.Add(wx.StaticText(self, style=wx.ALIGN_CENTER), flag=wx.CENTER)
        hbox.Add(vbox, flag=wx.CENTER)
        hbox.Add(wx.StaticText(self, label='    '), flag=wx.CENTER)
        self.SetSizerAndFit(hbox)
        self.Centre()
        self.Raise()
        self.MakeModal(True)
        self.Show()

    def OnListItemDClicked(self, event):
        logging.info("{0}:{1}: user clicked string: {2}".format(self.logprefix, "OnListItemDClicked", event.GetString()))
        questionId = self.matches[event.GetSelection()][0]
        self.Unbind(wx.EVT_CLOSE)
        self.MakeModal(False)
        self.parent.set_question(questionId)
        self.Close()

    def OnButtonCancelClicked(self, event):
        logging.info("{0}:{1}: user clicked cancel".format(self.logprefix, "OnButtonCancelClicked"))
        self.Unbind(wx.EVT_CLOSE)
        self.MakeModal(False)
        self.Close()

    def when_closed(self, event):
        logging.info("{0}:{1}: user clicked close".format(self.logprefix, "when_closed"))
        self.OnButtonCancelClicked(event)

class PromptDeleteTestPopupWindow(wx.Frame):
    def __init__(self, parent):
        self.logprefix = "PromptDeleteTestPopupWindow"
        super(PromptDeleteTestPopupWindow, self).__init__(parent, size=(300, 160))

    def start(self, test_name, parent):
        logging.info("{0}:{1}: start".format(self.logprefix, "start"))
        self.parent = parent
        self.Bind(wx.EVT_CLOSE, self.when_closed)
        self.SetBackgroundColour('WHITE')
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.AddSpacer(30)
        hbox.Add(wx.StaticText(self, id=-1, label="\nReally delete test '" + test_name + "' ?", style=wx.ALIGN_CENTER), flag=wx.CENTER)
        hbox.AddSpacer(30)
        vbox.Add(hbox, flag=wx.CENTER)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.AddSpacer(30)
        hbox2.Add(wx.StaticText(self, id=-1, label="\nThis operation cannot be undone\n", style=wx.ALIGN_CENTER), flag=wx.CENTER)
        hbox2.AddSpacer(30)
        vbox.Add(hbox2, flag=wx.CENTER)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        button_delete = wx.Button(self, -1, 'Delete test')
        self.Bind(wx.EVT_BUTTON, self.OnButtonDeleteTestClicked, button_delete)
        hbox3.Add(button_delete, 1, flag=wx.CENTER)
        hbox3.AddSpacer(30)
        button_cancel = wx.Button(self, -1, 'Cancel')
        self.Bind(wx.EVT_BUTTON, self.OnButtonCancelClicked, button_cancel)
        hbox3.Add(button_cancel, 1, flag=wx.CENTER)
        vbox.Add(hbox3, flag=wx.CENTER)
        vbox.Add(wx.StaticText(self, style=wx.ALIGN_CENTER), flag=wx.CENTER)
        self.SetSizerAndFit(vbox)
        self.Centre()
        self.Raise()
        self.MakeModal(True)
        self.Show()

    def OnButtonDeleteTestClicked(self, event):
        logging.info("{0}:{1}: user clicked delete".format(self.logprefix, "OnButtonDeleteTestClicked"))
        self.parent.delete_test()
        self.Unbind(wx.EVT_CLOSE)
        self.MakeModal(False)
        self.Close()
        
    def OnButtonCancelClicked(self, event):
        logging.info("{0}:{1}: user clicked cancel".format(self.logprefix, "OnButtonCancelClicked"))
        self.Unbind(wx.EVT_CLOSE)
        self.MakeModal(False)
        self.Close()
        
    def when_closed(self, event):
        logging.info("{0}:{1}: user clicked close".format(self.logprefix, "when_closed"))
        self.OnButtonCancelClicked(event)

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

    def start(self, found_test_name, current_test_name, firstAppendTextValue, secondAppendTextValue):
        logging.info("{0}:{1}: start".format(self.logprefix, "start"))
        self.Bind(wx.EVT_CLOSE, self.when_closed)
        self.SetBackgroundColour('WHITE')
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(wx.StaticText(self, label="    ", style=wx.ALIGN_CENTER), flag=wx.CENTER)
        if found_test_name == current_test_name:
            hbox.Add(wx.StaticText(self, label="\nThe item '" + firstAppendTextValue + " | " + secondAppendTextValue + "' already exists in this test\n", style=wx.ALIGN_CENTER), flag=wx.CENTER)
        else:
            hbox.Add(wx.StaticText(self, label="\nThe item '" + firstAppendTextValue + " | " + secondAppendTextValue + "' already exists in test '" + found_test_name + "'\n", style=wx.ALIGN_CENTER), flag=wx.CENTER)
        hbox.Add(wx.StaticText(self, label="    ", style=wx.ALIGN_CENTER), flag=wx.CENTER)
        vbox.Add(hbox)
        vbox.AddSpacer(20)
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
        self.logprefix = "SelectOtherTestPopupWindow"
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
        self.button_to_test_name = dict()
        (the_found_status, found_test_name_to_values, self.german_value, self.english_value) = ret_list[0]
        self.addFoundTestList(vbox2, the_found_status, found_test_name_to_values)
        if len(ret_list) == 2:
            (the_found_status, found_test_name_to_values, self.german_value, self.english_value) = ret_list[1]
            self.addFoundTestList(vbox2, the_found_status, found_test_name_to_values)
        hbox.Add(vbox2)
        hbox.Add(wx.StaticText(self, label="    ", style=wx.ALIGN_CENTER), flag=wx.CENTER)
        vbox.Add(hbox)
        vbox.AddSpacer(20)
        button_cancel = wx.Button(self, -1, 'Cancel')
        self.Bind(wx.EVT_BUTTON, self.OnButtonCancelClicked, button_cancel)
        vbox.Add(button_cancel, 1, flag=wx.CENTER)
        vbox.AddSpacer(20)
        self.SetSizerAndFit(vbox)
        self.Centre()
        self.Raise()
        self.MakeModal(True)
        self.Show()
        
    def addFoundTestList(self, vbox, the_found_status, found_test_name_to_values):
        if the_found_status == found_status.FoundStatus.DE_FOUND:
            vbox.Add(wx.StaticText(self, id=-1, label="\nThe German expression", style=wx.ALIGN_CENTER), flag=wx.CENTER)
            vbox.Add(wx.StaticText(self, id=-1, label="'" + self.german_value + "'", style=wx.ALIGN_CENTER), flag=wx.CENTER)
        else:
            vbox.Add(wx.StaticText(self, id=-1, label="\nThe English expression", style=wx.ALIGN_CENTER), flag=wx.CENTER)
            vbox.Add(wx.StaticText(self, id=-1, label="'" + self.english_value + "'", style=wx.ALIGN_CENTER), flag=wx.CENTER)
        vbox.Add(wx.StaticText(self, id=-1, label="has been found elsewhere. Please choose a test to append your item to.", style=wx.ALIGN_CENTER), flag=wx.CENTER)
        grid = wx.FlexGridSizer(len(found_test_name_to_values) + 1, 3, hgap=50, vgap=10)
        grid.Add(wx.StaticText(self, id=-1, label="\nTest name", style=wx.ALIGN_CENTER))
        if the_found_status == found_status.FoundStatus.DE_FOUND:
            grid.Add(wx.StaticText(self, id=-1, label="\nEnglish translations", style=wx.ALIGN_CENTER))
        else:
            grid.Add(wx.StaticText(self, id=-1, label="\nGerman translations", style=wx.ALIGN_CENTER))
        grid.Add(wx.StaticText(self, id=-1, label="\n", style=wx.ALIGN_CENTER))
        for test_name in found_test_name_to_values:
            grid.Add(wx.StaticText(self, id=-1, label="  " + test_name, style=wx.ALIGN_CENTER))
            found_values = found_test_name_to_values[test_name]
            found_values_string = ""
            for found_value in found_values:
                found_values_string += "'" + found_value + "'\n"
            grid.Add(wx.StaticText(self, id=-1, label="  " + found_values_string, style=wx.ALIGN_CENTER))
            button_append = wx.Button(self, -1, 'Append')
            self.Bind(wx.EVT_BUTTON, self.OnButtonAppendClicked, button_append)
            logging.info("{0}:{1}: append button has id: {2}".format(self.logprefix, "start", id(button_append)))
            self.button_to_test_name[id(button_append)] = test_name
            grid.Add(button_append)
        vbox.Add(grid, flag=wx.CENTER)

    def OnButtonAppendClicked(self, event):
        logging.info("{0}:{1}: append button with id: {2} was clicked".format(self.logprefix, 
                                                                              "OnButtonAppendClicked", 
                                                                              id(event.GetEventObject())))
        self.parent.append_item_to_other_test(self.button_to_test_name[id(event.GetEventObject())], self.german_value, self.english_value)
        self.Unbind(wx.EVT_CLOSE)
        self.MakeModal(False)
        self.Close()
        
    def OnButtonCancelClicked(self, event):
        logging.info("{0}:{1}: user clicked close".format(self.logprefix, "OnButtonCancelClicked"))
        self.Unbind(wx.EVT_CLOSE)
        self.MakeModal(False)
        self.Close()

    def when_closed(self, event):
        logging.info("{0}:{1}: user clicked close".format(self.logprefix, "when_closed"))
        self.Unbind(wx.EVT_CLOSE)
        self.MakeModal(False)
        self.Close()

class EditTestFrame(wx.Frame):
    def __init__(self):
        self.logprefix = "EditTestFrame"
        super(EditTestFrame, self).__init__(None, title="Language test", size=(300, 800))

    def start(self, editTest):
        logging.info("{0}:{1}: start".format(self.logprefix, "start"))
        self.editTest = editTest
        self.ignore_edit_text_changed = 0
        self.Bind(wx.EVT_CLOSE, self.when_closed)
        self.SetBackgroundColour('WHITE')
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox_info = wx.BoxSizer(wx.HORIZONTAL)
        hbox_info.Add(wx.StaticText(self, label='\nTest:  ' + self.editTest.getTestName()), flag=wx.CENTER)
        hbox_info.Add(wx.StaticText(self, label='\n                                               '), flag=wx.CENTER)
        self.nItems_text = wx.StaticText(self, label='\nNumber of items: {0}'.format(self.editTest.getNumberOfItems()))
        hbox_info.Add(self.nItems_text, flag=wx.CENTER)
        hbox_info.Add(wx.StaticText(self, label='\n                                               '), flag=wx.CENTER)
        hbox_info.Add(wx.StaticText(self, label='\n                                               '), flag=wx.CENTER)
        hbox_info.Add(wx.StaticText(self, label='\nUser:  ' + self.editTest.getUserName()), flag=wx.CENTER)
        vbox.Add(hbox_info, flag=wx.CENTER)
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
        grid.Add(self.button_switch, flag=wx.CENTER)
        grid.Add(wx.StaticText(self), flag=wx.CENTER)
        self.firstEditText = wx.TextCtrl(self, size=(250, 50), style = wx.TE_MULTILINE)
        self.secondEditText = wx.TextCtrl(self, size=(250, 50), style = wx.TE_MULTILINE)
        self.Bind(wx.EVT_TEXT, self.OnEditTextChanged, self.firstEditText)
        self.Bind(wx.EVT_TEXT, self.OnEditTextChanged, self.secondEditText)
        grid.Add(self.firstEditText, flag=wx.CENTER)
        grid.Add(self.secondEditText, flag=wx.CENTER)
        grid2 = wx.FlexGridSizer(2, 3, hgap=10, vgap=10)
        self.button_next_item = wx.Button(self, -1, label='Show first item')
        self.Bind(wx.EVT_BUTTON, self.OnButtonNextClicked, self.button_next_item)
        self.nextItemButtonLabelSet = False
        self.button_previous_item = wx.Button(self, -1, label='Show previous item')
        self.Bind(wx.EVT_BUTTON, self.OnButtonPreviousClicked, self.button_previous_item)
        self.itemNumber_text = wx.StaticText(self, label='', style=wx.ALIGN_LEFT)
        self.button_delete_item = wx.Button(self, -1, label='Delete item')
        self.Bind(wx.EVT_BUTTON, self.OnButtonDeleteItemClicked, self.button_delete_item)
        self.button_save_item = wx.Button(self, -1, label='Save modified item')
        self.Bind(wx.EVT_BUTTON, self.OnButtonSaveClicked, self.button_save_item)
        self.button_shift_item = wx.Button(self, -1, label='Move item\nto another test')
        self.Bind(wx.EVT_BUTTON, self.OnButtonMoveItemClicked, self.button_shift_item)
        grid2.Add(self.button_next_item, flag=wx.CENTER)
        grid2.Add(self.button_previous_item, flag=wx.CENTER)
        grid2.Add(self.itemNumber_text, flag=wx.CENTER)
        grid2.Add(self.button_save_item, flag=wx.CENTER)
        grid2.Add(self.button_shift_item, flag=wx.CENTER)
        grid2.Add(self.button_delete_item, flag=wx.CENTER)
        grid.Add(grid2, flag=wx.CENTER)
        vbox.Add(grid, flag=wx.CENTER)
        vbox.Add(wx.StaticText(self, label='\nSearch for an item in the test:\n'), flag=wx.CENTER)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.input_search_term = wx.TextCtrl(self)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnButtonSearchClicked, self.input_search_term)
        hbox.Add(self.input_search_term, 1, flag=wx.CENTER)
        hbox.AddSpacer(20)
        self.button_search = wx.Button(self, -1, 'Search')
        self.Bind(wx.EVT_BUTTON, self.OnButtonSearchClicked, self.button_search)
        hbox.Add(self.button_search, 1, flag=wx.CENTER)
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
        grid2.Add(self.button_switch2, flag=wx.CENTER)
        grid2.Add(wx.StaticText(self), flag=wx.CENTER)
        self.firstAppendText = wx.TextCtrl(self, size=(250, 50), style = wx.TE_MULTILINE)
        self.secondAppendText = wx.TextCtrl(self, size=(250, 50), style = wx.TE_MULTILINE)
        self.button_append_item = wx.Button(self, -1, label='Append')
        self.Bind(wx.EVT_BUTTON, self.OnAppendClick, self.button_append_item)
        grid2.Add(self.firstAppendText, flag=wx.CENTER)
        grid2.Add(self.secondAppendText, flag=wx.CENTER)
        grid2.Add(self.button_append_item, flag=wx.CENTER)
        grid2.Add(wx.StaticText(self, style=wx.ALIGN_LEFT), flag=wx.ALIGN_LEFT)
        vbox.Add(grid2, flag=wx.CENTER)
        vbox.Add(wx.StaticText(self, label='\nMultiple item operations:\n'), flag=wx.CENTER)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        button_import = wx.Button(self, -1, 'Import from file')
        self.Bind(wx.EVT_BUTTON, self.OnButtonImportClicked, button_import)
        self.button_export = wx.Button(self, -1, 'Export to file')
        self.Bind(wx.EVT_BUTTON, self.OnButtonExportClicked, self.button_export)
        button_delete = wx.Button(self, -1, 'Delete test')
        self.Bind(wx.EVT_BUTTON, self.OnButtonDeleteTestClicked, button_delete)
        hbox2.Add((340,-1))
        hbox2.Add(button_import, flag=wx.CENTER)
        hbox2.Add((30,-1))
        hbox2.Add(self.button_export, flag=wx.CENTER)
        hbox2.Add((30,-1))
        hbox2.Add(button_delete, flag=wx.CENTER)
        hbox2.Add((340,-1))
        vbox.Add(hbox2, flag=wx.ALIGN_CENTER)
        vbox.AddSpacer(60)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        button_quit = wx.Button(self, -1, 'Quit')
        self.Bind(wx.EVT_BUTTON, self.OnButtonQuitClicked, button_quit)
        self.button_start_test = wx.Button(self, -1, 'Start test')
        self.Bind(wx.EVT_BUTTON, self.OnButtonStartTestClicked, self.button_start_test)
        button_test_selection = wx.Button(self, -1, '<< Back to\n test selection')
        self.Bind(wx.EVT_BUTTON, self.OnButtonTestSelectionClicked, button_test_selection)
        hbox3.AddSpacer(30)
        hbox3.Add(button_test_selection, 1, flag=wx.CENTER)
        hbox3.AddSpacer(60)
        hbox3.Add(self.button_start_test, 1, flag=wx.CENTER)
        hbox3.AddSpacer(60)
        hbox3.Add(button_quit, 1, flag=wx.CENTER)
        hbox3.AddSpacer(30)
        vbox.Add(hbox3, flag=wx.CENTER)
        vbox.AddSpacer(30)
        self.fully_enabled = True
        self.button_previous_item.Disable()
        self.button_save_item.Disable()
        self.button_shift_item.Disable()
        self.button_delete_item.Disable()
        self.firstEditText.Disable()
        self.secondEditText.Disable()
        if self.editTest.get_number_of_tests() < 2:
            self.button_shift_item.Disable()
        if not self.editTest.getNumberOfItems():
            self.button_next_item.Disable()
            self.input_search_term.Disable()
            self.button_search.Disable()
            self.button_export.Disable()
            self.button_start_test.Disable()
            self.fully_enabled = False
        self.SetSizerAndFit(vbox)
        self.Centre()
        self.Show()
        
    def OnButtonStartTestClicked(self, event):
        self.Unbind(wx.EVT_CLOSE)
        self.Hide()
        self.editTest.start_test()
        self.Close()
        
    def OnButtonMoveItemClicked(self, event):
        self.editTest.move_current_item()
        logging.info("{0}:{1}: number of items is now: {2}".format(self.logprefix, "OnButtonMoveItemClicked", self.editTest.getNumberOfItems()))
        self.setNumberItemsText()
        
    def OnButtonDeleteItemClicked(self, event):
        self.editTest.delete_current_item()
        if self.editTest.getNumberOfItems() == 0:
            self.input_search_term.Disable()
            self.button_search.Disable()
        self.setNumberItemsText()
        
    def OnEditTextChanged(self, event):
        if not self.ignore_edit_text_changed == 0:
            logging.info("{0}:{1}: ignore_edit_text_changed: {2}, will now be decremented".format(self.logprefix, "OnEditTextChanged", self.ignore_edit_text_changed))
            self.ignore_edit_text_changed -= 1
        else:
            logging.info("{0}:{1}:".format(self.logprefix, "OnEditTextChanged"))
            self.button_save_item.Enable()
        
    def OnButtonSaveClicked(self, event):
        ret_list = self.editTest.modify_question(self.firstEditText.GetValue(), self.secondEditText.GetValue())
        the_found_status = ret_list[0][0]
        logging.info("{0}:{1}: found status: {2}".format(self.logprefix, "OnAppendClick", the_found_status))
        if the_found_status == found_status.FoundStatus.NONE_FOUND:
            self.button_save_item.Disable()
        else:
            self.process_ret_list(ret_list)
        
    def OnButtonPreviousClicked(self, event):
        logging.info("{0}:{1}:".format(self.logprefix, "OnButtonPreviousClicked"))
        self.button_save_item.Disable()
        (itemFirst, itemSecond) = self.editTest.getPreviousItem()
        self.ignore_edit_text_changed = 2
        self.firstEditText.SetValue(itemFirst)
        self.secondEditText.SetValue(itemSecond)
        self.setButtonsOnPrevious()
        self.setNumberItemsText()
        
    def setButtonsOnPrevious(self):
        if not self.editTest.isNotFirstItem():
            logging.info("{0}:{1}: beginning reached".format(self.logprefix, "setButtonsOnPrevious"))
            self.button_previous_item.Disable()
        if not self.button_next_item.IsEnabled():
            self.button_next_item.Enable()
        
    def OnButtonNextClicked(self, event):
        logging.info("{0}:{1}:".format(self.logprefix, "OnButtonNextClicked"))
        self.button_save_item.Disable()
        (is_end, itemFirst, itemSecond) = self.editTest.getNextItem()
        logging.info("{0}:{1}: is_end: {2}".format(self.logprefix, "OnButtonNextClicked", is_end))
        firstEditTextIsEnabled = self.firstEditText.Enabled
        logging.info("{0}:{1}: firstEditTextIsEnabled: {2}, isNotFirstItem: {3}".format(self.logprefix, "OnButtonNextClicked", firstEditTextIsEnabled, self.editTest.isNotFirstItem()))
        self.ignore_edit_text_changed = 2
        self.firstEditText.SetValue(itemFirst)
        self.secondEditText.SetValue(itemSecond)
        self.setButtonsOnNext(is_end)
        self.setNumberItemsText()
        
    def setButtonsOnNext(self, is_end):
        if self.editTest.isNotFirstItem():
            logging.info("{0}:{1}: enabling previous item buttons".format(self.logprefix, "setButtonsOnNext"))
            if not self.nextItemButtonLabelSet:
                self.button_next_item.SetLabel("Show next item")
                self.nextItemButtonLabelSet = True
            self.button_previous_item.Enable()
        if not self.firstEditText.Enabled:
            logging.info("{0}:{1}: enabling other buttons".format(self.logprefix, "setButtonsOnNext"))
            if not self.nextItemButtonLabelSet:
                self.button_next_item.SetLabel("Show next item")
                self.nextItemButtonLabelSet = True
            self.button_shift_item.Enable()
            self.button_delete_item.Enable()
            self.firstEditText.Enable()
            self.secondEditText.Enable()
        if is_end:
            self.button_next_item.Disable()
            
    def set_item(self, is_end, itemFirst, itemSecond):
        self.Raise()
        self.button_save_item.Disable()
        self.ignore_edit_text_changed = 2
        self.firstEditText.SetValue(itemFirst)
        self.secondEditText.SetValue(itemSecond)
        self.setButtonsOnPrevious()
        self.setButtonsOnNext(is_end)
        self.setNumberItemsText()
        
    def OnButtonExportClicked(self, event):
        path = self.editTest.export_test()
        logging.info("{0}:{1}: user entered path: {2}".format(self.logprefix, "OnButtonExportClicked", path))
        self.editTest.write_to_file(path)
        
    def OnButtonImportClicked(self, event):
        path = self.editTest.import_test()
        logging.info("{0}:{1}: user entered path: {2}".format(self.logprefix, "OnButtonImportClicked", path))
        self.editTest.parse_file(path)
        if self.editTest.getNumberOfItems() > 0:
            self.input_search_term.Enable()
            self.button_search.Enable()
        self.setNumberItemsText()
        
    def OnButtonDeleteTestClicked(self, event):
        self.editTest.prompt_delete_test()

    def OnAppendClick(self, event):
        firstAppendTextValue = self.firstAppendText.GetValue()
        secondAppendTextValue = self.secondAppendText.GetValue()
        if not firstAppendTextValue or not secondAppendTextValue:
            self.editTest.inform_no_empty_fields()
        else:
            ret_list = self.editTest.append_item(firstAppendTextValue, secondAppendTextValue)
            the_found_status = ret_list[0][0]
            if the_found_status == found_status.FoundStatus.NONE_FOUND:
                if not self.fully_enabled:
                    self.button_switch.Enable()
                    self.input_search_term.Enable()
                    self.button_search.Enable()
                    self.button_export.Enable()
                    self.button_start_test.Enable()
                    self.fully_enabled = True
                logging.info("{0}:{1}: Number of items: {2}".format(self.logprefix, "OnAppendClick", self.editTest.getNumberOfItems()))
                self.setNumberItemsText()
                self.clearAppendText()
                if not self.button_next_item.IsEnabled():
                    self.button_next_item.Enable()
            else:
                self.process_ret_list(ret_list)
        if self.editTest.getNumberOfItems() > 0:
            self.input_search_term.Enable()
            self.button_search.Enable()
            
    def process_ret_list(self, ret_list):
        the_found_status = ret_list[0][0]
        logging.info("{0}:{1}: found status: {2}".format(self.logprefix, "OnAppendClick", the_found_status))
        if the_found_status == found_status.FoundStatus.BOTH_FOUND:
            found_test_name = ret_list[0][1].keys()[0]
            if self.editTest.getDeToEn():
                self.editTest.inform_item_exists(found_test_name, ret_list[0][2], ret_list[0][3])
            else:
                self.editTest.inform_item_exists(found_test_name, ret_list[0][3], ret_list[0][2])
        else:
            self.editTest.select_other_test(ret_list)
            
    def setNumberItemsText(self):
        if self.editTest.getItemNumber() > 0 and self.editTest.getNumberOfItems() > 0:
            self.itemNumber_text.SetLabel('Item number {0}\n'.format(self.editTest.getItemNumber()))
        else:
            self.itemNumber_text.SetLabel('')
        self.nItems_text.SetLabel('\nNumber of items: {0}'.format(self.editTest.getNumberOfItems()))
            
    def setNewEditTextAfterDelete(self, theItemListBoundsStatus):
        self.setNumberItemsText()
        self.ignore_edit_text_changed = 2
        if not theItemListBoundsStatus == item_list_bounds_status.ItemListBoundsStatus.EMPTY:
            logging.info("{0}:{1}: list is not empty".format(self.logprefix, "setNewEditTextAfterDelete"))
            item = self.editTest.getCurrentItem()
            self.firstEditText.SetValue(item[0])
            self.secondEditText.SetValue(item[1])
        else:
            logging.info("{0}:{1}: list is empty".format(self.logprefix, "setNewEditTextAfterDelete"))
            self.firstEditText.Clear()
            self.secondEditText.Clear()
            self.firstEditText.Disable()
            self.secondEditText.Disable()
        if theItemListBoundsStatus == item_list_bounds_status.ItemListBoundsStatus.BOTH:
            self.button_previous_item.Disable()
            self.button_next_item.Disable()
        elif theItemListBoundsStatus == item_list_bounds_status.ItemListBoundsStatus.EMPTY:
            self.button_previous_item.Disable()
            self.button_next_item.SetLabel("Show first item")
            self.nextItemButtonLabelSet = False
            self.button_next_item.Disable()
            self.button_shift_item.Disable()
            self.button_delete_item.Disable()
            self.input_search_term.Disable()
            self.button_search.Disable()
        elif theItemListBoundsStatus == item_list_bounds_status.ItemListBoundsStatus.END:
            self.button_previous_item.Enable()
            self.button_next_item.Disable()
        elif theItemListBoundsStatus == item_list_bounds_status.ItemListBoundsStatus.BEGIN:
            self.button_previous_item.Disable()
            self.button_next_item.Enable()
        elif theItemListBoundsStatus == item_list_bounds_status.ItemListBoundsStatus.NEITHER:
            self.button_previous_item.Enable()
            self.button_next_item.Enable()
                
    def clearAppendText(self):
        self.firstAppendText.Clear()
        self.secondAppendText.Clear()

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
        self.ignore_edit_text_changed = 2
        firstEditTextValue = self.firstEditText.GetValue()
        self.firstEditText.SetValue(self.secondEditText.GetValue())
        self.secondEditText.SetValue(firstEditTextValue)
        
    def OnButtonSearchClicked(self, event):
        logging.info("{0}:{1}: user clicked search for {2}".format(self.logprefix, "OnButtonSearchClicked", self.input_search_term.GetValue()))
        self.editTest.searchExpression(self.input_search_term.GetValue())

    def OnButtonQuitClicked(self, event):
        logging.info("{0}:{1}: user clicked quit".format(self.logprefix, "OnButtonQuitClicked"))
        self.Unbind(wx.EVT_CLOSE)
        self.Hide()
        self.editTest.quit()
        self.Close()

    def OnButtonTestSelectionClicked(self, event):
        logging.info("{0}:{1}: user clicked back to test selection".format(self.logprefix, "OnButtonTestSelectionClicked"))
        self.goBackToTestSelection()
        
    def goBackToTestSelection(self):
        self.Unbind(wx.EVT_CLOSE)
        self.Hide()
        self.editTest.back_to_test_selection()
        self.Close()
    
    def when_closed(self, event):
        logging.info("{0}:{1}: user clicked close".format(self.logprefix, "when_closed"))
        self.OnButtonQuitClicked(event)
