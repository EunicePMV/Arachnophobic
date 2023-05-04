"""
This class is intended for handling the following:
pathfinding
optimal path list
"""
import math, queue
from typing import List
    
class Vec2():
    def __init__(self, x: float|int = None, y: float|int = None):
        self.x = x
        self.y = y

    def compareTo(self, vector) -> bool:
        return self.x == vector.x and self.y == vector.y

    def reverseCoord(self):
        x = self.x
        y = self.y
        return Vec2(y, x)

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
        self.grid:      List[List[Cell]]    = [] #List of Cells
        self.map = map          #Map
        self.wall = wall        #List of walls
        self.limiter = 100    #Amount of cells to be explored
    
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
    
    def resetCells(self):
        for x in range(len(self.grid)):
            for y in range(len(self.grid[x])):
                self.grid[x][y].g = 0
                self.grid[x][y].f = 0
                self.grid[x][y].h = 0
                self.grid[x][y].prev = None

    def getPathsAsQueue(self, paths: List[Vec2]) -> queue.Queue:
        queuePath = queue.Queue()
        for path in paths: queuePath.put(path)
        return queuePath

    def searchPath(self, start: Vec2, end : Vec2) -> List[Vec2]:
        paths:      List[Vec2] = [] #List of generated paths
        closeSet:   List[Cell] = [] #List of explored Cells
        openSet:    List[Cell] = [] #Cells discovered but not explored
        self.resetCells()
        try:
            if len(self.grid) <= 0:
                error = "Cells must be available before generating a path"
                raise ValueError(f'\033[91m{error}\033[0m')
            
            limiter = 0
            finished = False
            openSet.append(self.grid[start.x][start.y])
            while (len(openSet) > 0 and limiter < self.limiter) and not finished:
                limiter += 1
                selected_cell = 0
                for i in range(len(openSet)): #checks any unexplored discovered cell
                    if openSet[i].f < openSet[selected_cell].f: #if cell is cheaper than selected cell, swap
                        selected_cell = i

                current = openSet[selected_cell] #select the cheapest cell path

                if current.position.compareTo(end): #check if current cell is the end cell
                    temp_current = current
                    while temp_current.prev: #traverses back to start and records the path
                        limiter += 1
                        paths.append(temp_current.prev.position.reverseCoord())
                        temp_current = temp_current.prev 
                    if not finished:
                        self.resetCells() #resets the cell values for next search call
                        finished = True
                    
                if not finished:
                    openSet.remove(current) #since the current is going to be explored
                    closeSet.append(current) #it will be moved to closeSet (discovered and explored)

                    for neighbor in current.neighbors: #checks the neighbor cells of current cell being explored
                        if neighbor in closeSet or neighbor.wall: #if neighbor is explored and discoverd or is a wall
                            continue #pass
                        g = current.g + 1 #adds current g for the g of the next cells

                        newCell = False #the cell is not yet explored
                        if neighbor in openSet: #neighbor is discoverd and unexplored
                            if g < neighbor.g: #adjust the value of unexplored and discovered g to correct value
                                neighbor.g = g
                                newCell = True
                        else:
                            neighbor.g = g #adjust the value of unexplored and undiscovered g to correct value
                            newCell = True 
                            openSet.append(neighbor)
                        
                        if newCell:
                            neighbor.h = self.heuristics(neighbor, end)
                            neighbor.f = neighbor.g + neighbor.h
                            neighbor.prev = current

            if len(paths) == 0:
                return [None]
            elif limiter == self.limiter-1:
                return [False]
            paths.reverse()
            paths.append(end.reverseCoord())
            return paths
        except ValueError as error:
            print(error)

    def heuristics(self, cell: Cell, end: Vec2):
        return math.sqrt((cell.position.x - end.x)**2 + abs(cell.position.y - end.y)**2)
#18 * 64
map = ["bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
       "baaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaccaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
       "baaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaacacaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
       "baaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaacaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
       "baaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
       "baaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
       "baaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabaaaaaaaaaaaaaaaaaaaaaaaaaaa",
       "baaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
       "baaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
       "baaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
       "baaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
       "baaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
       "baaaaaaaaaaaaaaaaaaaaaaaaaaaaabaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
       "baaaaaaaaaaaaaaaaaaaaaaaabbbaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
       "baaaaaaaaaaaaaaaaaaaaaaaaaabaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
       "baaaaaaaaaaaaaaaaaaaaaaaaaabaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
       "baaaaaaaaaaaaaaaaaaaaaaabbbbaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
       "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
       ]

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

path = aStar.searchPath(start, end)
queuePath = aStar.getPathsAsQueue(path)