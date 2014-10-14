
import login_frame
import test_selection_frame
import edit_test_frame
import wx

class UIFactoryWXPython:
	def __init__(self):
		pass

	def create_login_UI(self):
		return login_frame.LoginFrame()

	def create_CreateUserPopupWindow(self, parent):
		return login_frame.CreateUserPopupWindow(parent)

	def create_InformUserExistsPopupWindow(self, parent):
		return login_frame.InformUserExistsPopupWindow(parent)

	def create_test_selection_UI(self):
		return test_selection_frame.TestSelectionFrame()

	def create_CreateTestPopupWindow(self, parent):
		return test_selection_frame.CreateTestPopupWindow(parent)

	def create_InformTestExistsPopupWindow(self, parent):
		return test_selection_frame.InformTestExistsPopupWindow(parent)

	def create_edit_test_UI(self):
		return edit_test_frame.EditTestFrame()
	
	def create_SelectOtherTestPopupWindow(self, parent):
		return edit_test_frame.SelectOtherTestPopupWindow(parent)

	def create_InformItemExistsPopupWindow(self, parent):
		return edit_test_frame.InformItemExistsPopupWindow(parent)

	def create_InformNoEmptyFieldsPopupWindow(self, parent):
		return edit_test_frame.InformNoEmptyFieldsPopupWindow(parent)
	
	def create_PromptDeleteTestPopupWindow(self, parent):
		return edit_test_frame.PromptDeleteTestPopupWindow(parent)
	
	def create_SelectItemPopupWindow(self, parent):
		return edit_test_frame.SelectItemPopupWindow(parent)
	
	def create_SelectTestPopupWindow(self, parent):
		return edit_test_frame.SelectTestPopupWindow(parent)
	
	def create_ShowSimilarResultsPopupWindow(self, parent):
		return edit_test_frame.ShowSimilarResultsPopupWindow(parent)
	
	def getPathForImportFileDialog(self, parent):
		openFileDialog = wx.FileDialog(parent, style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
		openFileDialog.ShowModal()
		path = openFileDialog.GetPath()
		openFileDialog.Destroy()
		return path
	
	def getPathForExportFileDialog(self, parent):
		openFileDialog = wx.FileDialog(parent, style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
		openFileDialog.ShowModal()
		path = openFileDialog.GetPath()
		openFileDialog.Destroy()
		return path
	