import pygame as pg
import csv, math, numpy as np
"""
This class is intended for handling the following:
    Canvas screen
    Overlay
    Masking of Flashlight
"""
class Screen(pg.Surface):
    def __init__(self, width: int, height: int, title: str):
        self.map = None
        self.screen = pg.display.set_mode((width, height))
        pg.display.set_caption(title)
    
    def loadMap(self):
        ...

    def overlay(self):
        ...
    
    def overlayMask(self):
        ...
    
    def cast_rays(self, player, MAP, step_angle, screen, HALF_FOV, CASTED_RAYS, MAX_DEPTH, TILE_SIZE, MAP_SIZE):
        player_angle = math.pi
        # define left most angle of FOV
        start_angle = player_angle - HALF_FOV

        # loop over casted rays
        for ray in range(CASTED_RAYS):
            # cast ray step by step
            for depth in range(MAX_DEPTH):
                # get ray target coordinates
                target_x = player.x - math.sin(start_angle) * depth
                target_y = player.y + math.cos(start_angle) * depth

                # covert target X, Y coordinate to map col, row
                col = int(target_x / TILE_SIZE)
                row = int(target_y / TILE_SIZE)

                # calculate map square index
                square = row * MAP_SIZE + col

                # ray hits the condition
                if MAP[square] == '#':
                    # highlight wall that has been hit by a casted ray
                    pg.draw.rect(screen, (0, 255, 0), (col * TILE_SIZE,
                                                        row * TILE_SIZE,
                                                        TILE_SIZE - 2,
                                                        TILE_SIZE - 2))

                    # draw casted ray
                    pg.draw.line(screen, (255, 255, 0), (player.x, player.y), (target_x, target_y))
                    break

            # increment angle by a single step
            start_angle += step_angle