
import manager
from data_sql import data_sql_manager
from wx_frames import UI_factory_wxPython
import wx

def main():
    app = wx.App(False)
    dataSQLManager = data_sql_manager.DataSQLManager()
    manager_wx_sql = manager.Manager(UI_factory_wxPython.UIFactoryWXPython(), dataSQLManager);
    manager_wx_sql.do_login();
    app.MainLoop()
    
if __name__ == "__main__":
    main()
