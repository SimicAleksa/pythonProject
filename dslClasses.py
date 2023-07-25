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
        self.doors = {}
        self.items = []
        self.requirements = None

    def add_requirements(self, requirement):
        self.requirements = requirement

    def remove_item(self, item):
        for region_item in self.items:
            if item == region_item.name:
                self.items.remove(region_item)

    def is_item_contained(self, item):
        for region_item in self.items:
            if item == region_item.name:
                return True
        return False

    def add_connection(self, direction, target_region):
        self.doors[direction] = target_region

    def add_property(self, prop_name, prop_value):
        self.properties[prop_name] = prop_value

    def print_self(self):
        items = ""
        for item in self.items:
            items += item.name + " "
        return f'{self.properties["PortrayalProperties"]}. Inside you see {items}'


class Item:
    def __init__(self, name):
        self.name = name
        self.properties = {}

    def add_property(self, prop_name, prop_value):
        self.properties[prop_name] = prop_value

    def use(self):
        pass

    def print_self(self):
        return f'{self.properties["PortrayalProperties"]}'

    def print_self_contains(self):
        items = ""
        for item in self.properties["ContainsProperties"]:
            items += item + " "
        return f'{self.properties["PortrayalProperties"]}. Inside you see {items}'


class Player:
    def __init__(self, name, start_position):
        self.name = name
        self.health = 100
        self.score = 0
        self.inventory = []
        self.position = start_position
        self.properties = {}

    def remove_item(self, item):
        for region_item in self.position.items:
            if item == region_item.name:
                self.position.items.remove(region_item)
                break

    def add_property(self, prop_name, prop_value):
        self.properties[prop_name] = prop_value

    def heal(self, amount):
        self.health += amount
        if amount > 0:
            return "You healed " + amount
        else:
            return "You took " + amount + " damage"

    def take(self, item, gameworld):
        if self.position.is_item_contained(item):
            if "door" in item: #TODO ovo treba prosiriti za zabranjeim stvarima za kupiti
                return "You cant do that"
            else:
                for gameworldItem in gameworld.items:
                    if item == gameworldItem.name:
                        self.inventory.append(item)
                        self.remove_item(item)
                        return "You picked up " + gameworldItem.name
        else:
            return "That item is not present in this room"

    def move(self, direction, gameworld):
        if direction in self.position.doors:
            target_room = self.position.doors[direction]
            for region in gameworld.regions:
                if region.name == target_room:
                    if region.requirements in self.inventory:
                        self.inventory.remove(region.requirements)
                        region.requirements = None
                        self.position = region
                    else:
                        return "Requirements not matched. You neeed a " + region.requirements
            return "You moved to " + self.position.name
        else:
            return "You can't go that way."

    def print_self(self):
        inventory = ""
        for item in self.inventory:
            inventory += item + " "
        return f'You find yourself currently in {self.properties["PositionProperties"]}. Your backpack has {inventory}'
