from gameInterpeter import parse_dsl
from gui import App
import sys


if __name__ == '__main__':
    parse_dsl("gameWorldDSL.tx", "simpleGame.game")
    # App()
