"""
This class is intended for handling the following:
    pathfinding
    optimal path list
"""

class AStar():
    def __init__(self, start=None, end=None, map=None):
        self.path = None
    
    def h(self):
        ...

