from dslClasses import GameWorld, Region, Item, Player
from gui import App
from textx import metamodel_from_file
import sys
from os.path import join, dirname


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
        for prop in region_def.properties:
            prop_name = prop.__class__.__name__
            if prop_name == "PortrayalProperties":
                prop_value = prop.portrayal
            if prop_name == "ContainsProperties":
                prop_value = []
                for item in prop.contains:
                    prop_value.append(item.name)
            region.add_property(prop_name, prop_value)
        game_world.regions.append(region)

    # Create items
    for item_def in model.items:
        item = Item(item_def.name)
        for prop in item_def.properties:
            prop_name = list(prop.keys())[0]
            prop_value = prop[prop_name]
            item.add_property(prop_name, prop_value)
        game_world.items.append(item)

    # Create player
    player_def = model.player
    game_world.player = Player(player_def.name)
    for prop in player_def.properties:
        prop_name = list(prop.keys())[0]
        prop_value = prop[prop_name]
        game_world.player.add_property(prop_name, prop_value)

    # Set start and final positions
    game_world.set_start_position(model.start_position[0])
    game_world.set_final_position(model.final_position[0])

    return game_world


if __name__ == '__main__':
    # App()
    parse_dsl("gameWorldDSL.tx", "simpleGame.game")
