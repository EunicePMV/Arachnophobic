import pygame as pg
"""
This class is intended for handling the following:
    Offsetting camera (Movement)
    Player behavior
    Win Condition
"""
class Player(pg.Surface):
    def __init__(self, name, camera=None, offset=None):
        self.name = name