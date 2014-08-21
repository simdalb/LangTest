
import login_frame

class UIFactoryWXPython:
	def __init__(self):
		pass
	
	def create_login_UI(self):
		return login_frame.LoginFrame()
		
	def create_CreateUserPopupWindow(self, parent):
		return login_frame.CreateUserPopupWindow(parent)