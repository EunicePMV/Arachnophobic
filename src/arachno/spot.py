"""
This class is intended for assigning a tile in a grid, for the use of a*
"""
class Spot():
    def __init__(self, row, col, total_rows):
        self.x, self.y = row, col
        self.f, self.g, self.h = 0, 0, 0
        self.neighbors = []
        self.prev = None
        self.wall = False

    def update_neighbors(self, grid):
        ...

    def get_pos(self):
	    return self.row, self.col
    
    