import math
"""
This class is intended for assigning a tile in a grid, for the use of a*
"""
class Spot:
    def __init__(self, col, row):
        self.x, self.y = col, row
        self.f, self.g, self.h = 0, 0, 0
        self.neighbors = []
        self.prev = None
        self.wall = False
        # if random.randint(0, 100) < 20:
        #     self.wall = True
    def heuristics(self, a, b):
        return math.sqrt((a.x - b.x)**2 + abs(a.y - b.y)**2)    
    # def show(self, win, col):
    #     if self.wall == True:
    #         col = (0, 0, 0)
    #     pygame.draw.rect(win, col, (self.x*w, self.y*h, w-1, h-1))
    
    def add_neighbors(self, grid, cols, rows):
        if self.x < cols - 1:
            self.neighbors.append(grid[self.x+1][self.y])
        if self.x > 0:
            self.neighbors.append(grid[self.x-1][self.y])
        if self.y < rows - 1:
            self.neighbors.append(grid[self.x][self.y+1])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y-1])
        #Add Diagonals
        if self.x < cols - 1 and self.y < rows - 1:
            self.neighbors.append(grid[self.x+1][self.y+1])
        if self.x < cols - 1 and self.y > 0:
            self.neighbors.append(grid[self.x+1][self.y-1])
        if self.x > 0 and self.y < rows - 1:
            self.neighbors.append(grid[self.x-1][self.y+1])
        if self.x > 0 and self.y > 0:
            self.neighbors.append(grid[self.x-1][self.y-1])
    