
import login_frame
import menu_frame
import create_test_frame
import test_selection_frame

class UIFactoryWXPython:
	def __init__(self):
		pass
	
	def create_login_UI(self):
		return login_frame.LoginFrame()
		
	def create_CreateUserPopupWindow(self, parent):
		return login_frame.CreateUserPopupWindow(parent)
	
	def create_InformUserExistsPopupWindow(self, parent):
		return login_frame.InformUserExistsPopupWindow(parent)
	
	def create_menu_UI(self):
		return menu_frame.MenuFrame()
	
	def create_test_creator_UI(self):
		return create_test_frame.CreateTestFrame()
	
	def create_test_selection_UI(self):
		return test_selection_frame.TestSelectionFrame()
	
	def create_CreateTestPopupWindow(self, parent):
		return test_selection_frame.CreateTestPopupWindow(parent)
	
	def create_InformTestExistsPopupWindow(self, parent):
		return test_selection_frame.InformTestExistsPopupWindow(parent)
	