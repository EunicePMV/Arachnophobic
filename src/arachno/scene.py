import pygame as pg
import sys
from arachno.constants import *

is_playing = True

"""
For initializing pygame and calling main function
"""
def start():
    pg.init()
    main()

"""
Main function, dont have to be edited
"""
def main():
    preProcess()
    while True:
        preEvents(SCREEN, CLOCK)
        events(SCREEN, CLOCK)
        postEvents(SCREEN, CLOCK)

"""
This is for loading
"""
def preProcess(*l, **d):
    ...

"""
This is tasks that will occur before the event if any
"""
def preEvents(s, c, *l, **d):
    PLAYER.name = "world"

"""
This is where events will occur
"""
def events(s, c, *l, **d):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

"""
This is for tasks that occurs after event handling
"""
def postEvents(s, c, **d):
    s.fill(WHITE)
    c.tick(60)
    pg.display.update()

