import pygame as pg
"""
This class is intended for handling the following:
    Enemy
    Enemy behavior
"""
class Spider(pg.Surface):
    def __init__(self, name, camera=None, offset=None):
        self.name = name
    
    def state(self):
        ...

    def followState(self):
        ...
    
    def avoidState(self):
        ...
