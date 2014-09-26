
import logging

class Menu:
    def __init__(self, manager, UI_factory):
        self.logprefix = "Login"
        logging.info("{0}:{1}:".format(self.logprefix, "__init__"))
        self.manager = manager
        self.UI_factory = UI_factory
        self.menu_UI = UI_factory.create_menu_UI()

    def start(self):
        self.menu_UI.start(self)

    def work_test(self):
        self.manager.do_test()

    def create_test(self):
        self.manager.do_create()

    def see_stats(self):
        self.manager.do_stats()
