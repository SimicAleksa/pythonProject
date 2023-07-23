from dslClasses import GameWorld, Region, Item, Player
from textx import metamodel_from_file
from os.path import join, dirname


class UnlockAction:
    def __init__(self, name, direction, target, price):
        self.name = name
        self.direction = direction
        self.target = target
        self.price = price


class HealAction:
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount


class UnlockAction:
    def __init__(self, name, direction, target, price):
        self.name = name
        self.direction = direction
        self.target = target
        self.price = price


def parse_dsl(dsl_path, game_path):
    # Load the metamodel from the DSL grammar
    this_folder = dirname(__file__)
    dsl_mm = metamodel_from_file(join(this_folder, dsl_path))

    # Parse the DSL file and create the GameWorld
    model = dsl_mm.model_from_file(join(this_folder, game_path))

    game_world = GameWorld()

    # Create regions
    for region_def in model.regions:
        region = Region(region_def.name)
        properties(region, region_def)
        game_world.regions.append(region)

    # Create items
    for item_def in model.items:
        item = Item(item_def.name)
        properties(item, item_def)
        game_world.items.append(item)

    # Create player
    player_def = model.player
    player = Player(player_def.name)
    properties(player, player_def)
    game_world.player = player

    # Set start and final positions
    game_world.set_start_position(model.start_position.name)
    game_world.set_final_position(model.final_position.name)

    return game_world


def properties(obj, obj_def):
    for prop in obj_def.properties:
        prop_name = prop.__class__.__name__
        if prop_name == "PortrayalProperties":
            prop_value = prop.portrayal
        elif prop_name == "ContainsProperties":
            prop_value = []
            for item in prop.contains:
                prop_value.append(item.name)
        elif prop_name == "ActivationProperties":
            action_name = prop.action.__class__.__name__
            if action_name == "UnlockAction":
                prop_value = UnlockAction(action_name, prop.action.direction, prop.action.target, prop.action.price)
            elif action_name == "HealAction":
                prop_value = HealAction(action_name, prop.action.amount)
        elif prop_name == "HealthProperties":
            prop_value = prop.health
        elif prop_name == "ScoreProperties":
            prop_value = prop.score
        elif prop_name == "InventoryProperties":
            prop_value = []
            for item in prop.inventory:
                prop_value.append(item.name)
        elif prop_name == "PositionProperties":
            prop_value = prop.position.name

        obj.add_property(prop_name, prop_value)
