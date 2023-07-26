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
            items += item.name + ", "
        items = items[:-2]
        return f'You are in {self.properties["PortrayalProperties"]}. Inside you see {items}. '

    def print_self_for_stable(self):
        items = ""
        for item in self.items:
            items += item.name + ", "
        items = items[:-2]
        return f'{self.properties["PortrayalProperties"]} with the following items inside: {items}. '


class Item:
    def __init__(self, name, isStatic):
        self.name = name
        self.properties = {}
        self.isStatic = isStatic

    def add_property(self, prop_name, prop_value):
        self.properties[prop_name] = prop_value

    def print_self(self):
        return f'{self.properties["PortrayalProperties"]}'

    def print_self_contains(self):
        items = ""
        for item in self.properties["ContainsProperties"]:
            items += item + ", "
        items = items[:-2]
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
            for gameworldItem in gameworld.items:
                if item == gameworldItem.name:
                    if not gameworldItem.isStatic:
                        self.inventory.append(item)
                        self.remove_item(item)
                        return "You picked up " + gameworldItem.name
                    else:
                        return "You cant do that"
        else:
            return "That item is not present in this room"

    def drop(self, item, gameworld):
        if item in self.inventory:
            self.inventory.remove(item)
            for gameworld_item in gameworld.items:
                if item == gameworld_item.name:
                    self.position.items.append(gameworld_item)
                    return "You dropped " + item + " in " + self.position.name
        return "You dont have that item"

    def use(self, item, gameworld):
        if item in self.inventory:
            for gameworld_item in gameworld.items:
                if gameworld_item.name == item:
                    if "ActivationProperties" in gameworld_item.properties:
                        action = gameworld_item.properties["ActivationProperties"]
                        if action.name == "HealAction":
                            self.inventory.remove(item)
                            self.health += action.amount
                            return "You used " + item + ". Your health is now " + str(self.health)
                    else:
                        return "That item cant be used"
        return "You dont have that item"

    def open(self, item, gameworld):
        if self.position.is_item_contained(item):
            for gameworldItem in gameworld.items:
                if item == gameworldItem.name:
                    if "ContainsProperties" in gameworldItem.properties:
                        for containItem in gameworldItem.properties["ContainsProperties"]:
                            for tempgameworlditem in gameworld.items:
                                if tempgameworlditem.name == containItem:
                                    self.position.items.append(tempgameworlditem)
                        self.remove_item(item)
                        return "You opened " + gameworldItem.name+""
                    else:
                        return "You cant do that"
        else:
            return "You cant do that"

    def move(self, direction, gameworld):
        if direction in self.position.doors:
            target_room = self.position.doors[direction]
            for region in gameworld.regions:
                if region.name == target_room:
                    if region.requirements is None:
                        self.position = region
                    elif region.requirements in self.inventory:
                        self.inventory.remove(region.requirements)
                        region.requirements = None
                        self.position = region
                    else:
                        return "Requirements not matched. You neeed a " + region.requirements, False
            return "You moved to " + self.position.name,True
        else:
            return "You can't go that way.", False

    def print_self(self):
        inventory = ""
        for item in self.inventory:
            inventory += item + ", "
        inventory = inventory[:-2]
        return f'{self.position.print_self()}Your backpack has {inventory}.'
