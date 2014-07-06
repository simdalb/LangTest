
import wx
from wx_frames import login_frame

class UIFactoryWXPython:
	def __init__(self):
		pass
	
	def create_login_UI(self):
		return login_frame.LoginFrame()
		