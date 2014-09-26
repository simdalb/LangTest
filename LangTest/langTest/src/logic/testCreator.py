
import logging

class TestCreator:
    def __init__(self, manager, UI_factory):
        self.logprefix = "TestCreator"
        logging.info("{0}:{1}: start".format(self.logprefix, "__init__"))
        self.manager = manager
        self.UI_factory = UI_factory
        self.test_creator_UI = UI_factory.create_test_creator_UI()

    def start(self):
        self.test_creator_UI.start(self)
