"""
This class is intended for global constants:
    Font
    Music (if any)
    Clock
"""
from arachno.screen import Screen
from arachno.player import Player

import pygame as pg
WIDTH = 500
HEIGHT = 500
TITLE = "Arachnophobic"

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

SIZE = (WIDTH, HEIGHT)
PLAYER = Player("hello")
SCREEN = Screen(SIZE, TITLE).screen
CLOCK = pg.time.Clock()