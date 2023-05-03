"""
This class is intended for handling the following:
    pathfinding
    optimal path list
"""
import math
from typing import List

class Vec2():
    def __init__(self, x: float|int = None, y: float|int = None):
        self.x = x
        self.y = y

    def compareTo(self, vector) -> bool:
        return self.x == vector.x and self.y == vector.y

    def reverseCoord(self):
        self.x = self.x ^ self.y
        self.y = self.x ^ self.y
        self.x = self.x ^ self.y
        return self

    def __repr__(self):
        return f'({self.x}, {self.y})'
    
raw = True
Paths = True
class Cell():
    def __init__(self, position: Vec2):
        self.position = position
        self.f, self.g, self.h = 0, 0, 0
        #f(n) is the total cost the path
        #g(n) is the cost of path
        #h(n) is the estimated cost of path
        self.neighbors: List[Cell] = [] 
        self.wall: bool = False #indicates if cell is walkable or not
        self.prev: Cell = None  #Is the previously walked cell if is part of optimal path

    def add_neighbors(self, grid, cols, rows):
        #Add Straight Directions
        if self.position.x < cols - 1:
            self.neighbors.append(grid[self.position.x+1][self.position.y])
        if self.position.x > 0:
            self.neighbors.append(grid[self.position.x-1][self.position.y])
        if self.position.y < rows - 1:
            self.neighbors.append(grid[self.position.x][self.position.y+1])
        if self.position.y > 0:
            self.neighbors.append(grid[self.position.x][self.position.y-1])
        #Add Diagonal Directions
        if self.position.x < cols - 1 and self.position.y < rows - 1:
            self.neighbors.append(grid[self.position.x+1][self.position.y+1])
        if self.position.x < cols - 1 and self.position.y > 0:
            self.neighbors.append(grid[self.position.x+1][self.position.y-1])
        if self.position.x > 0 and self.position.y < rows - 1:
            self.neighbors.append(grid[self.position.x-1][self.position.y+1])
        if self.position.x > 0 and self.position.y > 0:
            self.neighbors.append(grid[self.position.x-1][self.position.y-1])
    
    def __repr__(self):
        if Paths:
            return f'({self.position.x}, {self.position.y})'
        elif raw:
            return f'({self.position.x}, {self.position.y}): {len(self.neighbors)}'
        else:
            return f'({self.position.x+1}, {self.position.y+1}): {len(self.neighbors)}'
    
class AStarPathfinding():
    def __init__(self, map: List[List[int] | str], wall: str | List[int]):
        self.paths:     List[Vec2]          = [] #List of generated paths
        self.closeSet:  List[Cell]          = [] #List of explored Cells
        self.openSet:   List[Cell]          = [] #Cells discovered but not explored
        self.grid:      List[List[Cell]]    = [] #List of Cells
        self.start = None       #Start Cell
        self.end = None         #End cell
        self.map = map          #Map
        self.wall = wall        #List of walls
        self.limiter = 1000    #Amount of cells to be explored
    
    def generateCells(self):
        #Add cells to grid
        for x in range(len(self.map)):
            rows: List[Cell] = []
            for y in range(len(self.map[x])):
                rows.append(Cell(Vec2(x, y)))
                if self.map[x][y] in wall:
                    rows[y].wall = True
            self.grid.append(rows)

        #Add neigbours to cells instead of searching inside the algorithm
        for x in range(len(self.grid)):
            for y in range(len(self.grid[x])):
                self.grid[x][y].add_neighbors(self.grid, len(self.map), len(self.map[x]))

    def updateMap(self, map: List[List[str | int]], wall: str | List[int]):
        self.map = map
        self.wall = wall
        self.grid = []
        self.generateCells()

    def reset(self):
        self.paths = []
        self.closeSet = []
        self.openSet = [] 
        self.start = None 
        self.end = None
        for x in range(len(self.grid)):
            for y in range(len(self.grid[x])):
                self.grid[x][y].g, self.grid[x][y].f, self.grid[x][y].h,self.grid[x][y].prev = 0, 0, 0, None
    
    def searchPath(self, start: Vec2, end : Vec2):
        self.reset()
        try:
            self.start = start
            self.end = end
            if len(self.grid) <= 0:
                error = "Cells must be available before generating a path"
                raise ValueError(f'\033[91m{error}\033[0m')
            
            limiter = 0
            finished = False
            self.openSet.append(self.grid[start.x][start.y])
            while (len(self.openSet) > 0 and limiter < self.limiter) and not finished:
                limiter += 1
                selected_cell = 0
                for i in range(len(self.openSet)):
                    if self.openSet[i].f < self.openSet[selected_cell].f:
                        selected_cell = i

                current = self.openSet[selected_cell]
                if current.position.compareTo(self.end):
                    temp_current = current
                    while temp_current.prev:
                        self.paths.append(temp_current.prev.position.reverseCoord())
                        temp_current = temp_current.prev 
                    if not finished:
                        finished = True
                    
                if not finished:
                    self.openSet.remove(current)
                    self.closeSet.append(current)

                    for neighbor in current.neighbors:
                        if neighbor in self.closeSet or neighbor.wall:
                            continue
                        g = current.g + 1

                        newPath = False
                        if neighbor in self.openSet:
                            if g < neighbor.g:
                                neighbor.g = g
                                newPath = True
                        else:
                            neighbor.g = g
                            newPath = True
                            self.openSet.append(neighbor)
                        
                        if newPath:
                            neighbor.h = self.heuristics(neighbor, end)
                            neighbor.f = neighbor.g + neighbor.h
                            neighbor.prev = current
            if len(self.paths) == 0:
                return []
            self.paths.reverse()
            self.paths.append(self.end.reverseCoord())
            return self.paths
        except ValueError as error:
            print(error)

    def heuristics(self, cell: Cell, end: Vec2):
        return math.sqrt((cell.position.x - end.x)**2 + abs(cell.position.y - end.y)**2)

map = ["aaaaaaaaaa",
       "acccbaaaaa",
       "cacccaaaaa",
       "bbabbaaaaa",
       "aaabbaaaaa",
       "aaaabaaaaa"]

#Vectors work in ROWS as x and COLS as y
#basically map[5][9] = Vec2(5, 9)
#but position in CARTESIAN COORDINATE = (9, 5)
#So if position of tile is x = 10, y = 15
#Vec2 = (15, 10) : Corresponding to tile[y][x]
#This is because x is the column, y is the row

#Vec2   = List System
#paths  = Coordinates System

start = Vec2(0, 0)
end = Vec2(5, 9)
wall = "bc"

#Starts the pathfinding instance
aStar = AStarPathfinding(map, wall)
#generate the cells
aStar.generateCells()
#returns the path in coordinate system
print(aStar.searchPath(start, Vec2(3, 9)))
print(aStar.searchPath(Vec2(0, 9), Vec2(2, 1)))
print(aStar.searchPath(start, end))
print(aStar.searchPath(start, end)) #Recycling is not allowed
print(aStar.searchPath(start, end))
print(aStar.searchPath(start, Vec2(2, 9)))
print(aStar.searchPath(start, Vec2(3, 9)))
print(aStar.searchPath(Vec2(1, 9), Vec2(2, 3))) # CANT

#has a bug here, will be looked in to
print(aStar.searchPath(Vec2(2, 9), Vec2(2, 1)))

map[2] = "cacacaaaaa" #Change Vec(2, 3) {also know as map[2][3] in coordinates it is x=3, y=2}

aStar.updateMap(map, wall)
print(aStar.searchPath(Vec2(1, 9), Vec2(2, 3))) # CAN