
import manager
from data_sql import data_sql_manager
from wx_frames import UI_factory_wxPython

def main():
    manager_wx_sql = manager.Manager(UI_factory_wxPython.UIFactoryWXPython(), data_sql_manager.DataSQLManager());
    manager_wx_sql.do_login();
    
if __name__ == "__main__":
    main()
