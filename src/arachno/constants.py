"""
This class is intended for global constants:
    Font
    Music (if any)
    Clock
"""
from arachno.screen import Screen
from arachno.player import Player

import pygame as pg

PLAYER = Player("hello")
SCREEN = Screen(500, 500, "Hello World!").screen
CLOCK = pg.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
