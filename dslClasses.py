class GameWorld:
    def __init__(self):
        self.regions = []
        self.items = []
        self.player = None
        self.start_position = None
        self.final_position = None

    def set_start_position(self, region):
        self.start_position = region

    def set_final_position(self, region):
        self.final_position = region


class Region:
    def __init__(self, name):
        self.name = name
        self.properties = {}

    def add_property(self, prop_name, prop_value):
        self.properties[prop_name] = prop_value


class Item:
    def __init__(self, name):
        self.name = name
        self.properties = {}

    def add_property(self, prop_name, prop_value):
        self.properties[prop_name] = prop_value


class Player:
    def __init__(self, name):
        self.name = name
        self.properties = {}

    def add_property(self, prop_name, prop_value):
        self.properties[prop_name] = prop_value
