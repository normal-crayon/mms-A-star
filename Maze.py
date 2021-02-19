import API
import itertools
import sys

from Direction import Direction
from Mouse import Mouse 


mouse= Mouse(0, 0, Direction.NORTH)
class Maze:
    def __init__(self, width, height):
        # Initialize walls
        self.mouse= Mouse(0, 0, Direction.NORTH)
        self.start= (0,0)
        self.weights: Dict[mouse.getPosition(), float] = {}
        self.pos = {(0,0)}
        self.point = {(7,7)}
        positions = itertools.product(range(width), range(height))
        self.walls = {p: set() for p in positions}
        for position in self.walls:
            x, y = position
            if x == 0:
                self.setWall(position, Direction.WEST)
            if y == 0:
                self.setWall(position, Direction.SOUTH)
            if x == width - 1:
                self.setWall(position, Direction.EAST)
            if y == height - 1:
                self.setWall(position, Direction.NORTH)

        # Calculate center
        x = width // 2
        y = height // 2
        self.center = {(x, y)}
        if width % 2 == 0:
            self.center.add((x - 1, y))
        if height % 2 == 0:
            self.center.add((x, y - 1))
        if height % 2 == 0 and width % 2 == 0:
            self.center.add((x - 1, y - 1))

    def contains(self, position):
        return position in self.walls

    def inCenter(self, position):
        return position in self.center

    def getWall(self, position, direction):
        return direction in self.walls[position]

    def inStart(self, position):
        return position in self.pos

    def setWall(self, position, direction):
        self.walls[position].add(direction)
        API.setWall(*position, direction.value)
    
    def inPos(self, position):
        return position in self.point
    
    def getStart(self):
        return self.start
    
    def getEnd(self):
        return self.center
    
    def cost(self, fro_node: mouse.getPosition(), to_node: mouse.getPosition()):
        return self.weights.get(to_node, 1)
