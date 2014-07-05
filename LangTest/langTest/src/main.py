
import manager
import data_factory_SQL
import UI_factory_wxPython

def main():
    manager_wx_sql = manager.Manager(UI_factory_wxPython.UIFactoryWXPython(), data_factory_SQL.DataFactorySQL());
    manager_wx_sql.do_login();
    
if __name__ == "__main__":
    main()