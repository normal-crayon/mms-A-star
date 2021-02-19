import API
import sys
import collections
import heapq as h
from Direction import Direction
from Maze import Maze
from Mouse import Mouse
from astar_class import PriorityQueue
from short import Graph
from math import sqrt

def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()

def main():
    g= Graph(16*16)
    maze = Maze(API.mazeWidth(), API.mazeHeight())
    mouse = Mouse(0, 0, Direction.NORTH)
    while not maze.inCenter(mouse.getPosition()):
        updateWalls(maze, mouse)
        moveOneCell(maze, mouse, g, 1000)
    log(g.getGraph())
    #API.ackReset()
    while not maze.inStart(mouse.getPosition()):
        updateWalls(maze, mouse)
        moveBack(maze, mouse, g, 1000)
    while not maze.inCenter(mouse.getPosition()):
        updateWalls(maze, mouse)
        moveOneCell(maze, mouse, g, 1000)
    

def updateWalls(maze, mouse):
    position = mouse.getPosition()
    direction = mouse.getDirection()
    if API.wallFront():
        maze.setWall(position, direction)
    if API.wallLeft():
        maze.setWall(position, direction.turnLeft())
    if API.wallRight():
        maze.setWall(position, direction.turnRight())


def moveOneCell(maze, mouse, g, weight):
    w= weight
    currentX, currentY = mouse.getPosition()
    nextX, nextY= getNextCell(maze, mouse, w)
    g.addEdge((currentX, currentY),(nextX, nextY), 1)
    if nextX < currentX:
        nextDirection = Direction.WEST
    if nextY < currentY:
        nextDirection = Direction.SOUTH
    if nextX > currentX:
        nextDirection = Direction.EAST
    if nextY > currentY:
        nextDirection = Direction.NORTH

    # Turn and move to the next cell
    currentDirection = mouse.getDirection()
    if currentDirection.turnLeft() == nextDirection:
        mouse.turnLeft()
    elif currentDirection.turnRight() == nextDirection:
        mouse.turnRight()
    elif currentDirection != nextDirection:
        mouse.turnAround()
    mouse.moveForward()

def getNextCell(maze, mouse, w):
    frontier= PriorityQueue()
    initial= mouse.getPosition()
    frontier.put(initial, 0)
    anc= {}
    center= (7,7)
    cost_so_far ={}
    anc[initial]= None
    cost_so_far[initial]= 0

    while not frontier.empty():
        current = frontier.get()

        if current == center:
                break
        for direction in Direction:
            neighbor= getNeighbor(current, direction)
            
            if not maze.contains(neighbor):
                continue
            if maze.getWall(current, direction):
                continue
            if neighbor in anc:
                continue
            new_cost= cost_so_far[current] + maze.cost(current, neighbor)
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority= new_cost + w*heuristic(neighbor, center)
                frontier.put(neighbor, priority)
                anc[neighbor] = current
                x, y= current
                API.setText(x, y, priority)
                #flood[x][y]= priority
                if maze.inCenter(neighbor):
                    center = neighbor
    #return anc
    position = center
    while anc[position]!= initial:
        position= anc[position]
    #x, y= position
    #API.setText(x, y, priority)
    return position



def getNeighbor(current, direction):
    x, y = current
    if direction == Direction.NORTH:
        y += 1
    if direction == Direction.EAST:
        x += 1
    if direction == Direction.SOUTH:
        y -= 1
    if direction == Direction.WEST:
        x -= 1
    return (x, y)

def heuristic(neighbor, center):
    x1, y1 = neighbor
    x2, y2 = center
    return abs(x1-x2) + abs(y1-y2)
    

#def findShort(maze, mouse, g):
    
#------------------------------------------------------------------------


def moveBack(maze, mouse, g, weight):
    # Compute the next direction
    w = weight
    currentX, currentY = mouse.getPosition()
    nextX, nextY = getBackCell(maze, mouse, w)
    if nextX < currentX:
        nextDirection = Direction.WEST
    if nextY < currentY:
        nextDirection = Direction.SOUTH
    if nextX > currentX:
        nextDirection = Direction.EAST
    if nextY > currentY:
        nextDirection = Direction.NORTH

    # Turn and move to the next cell
    currentDirection = mouse.getDirection()
    if currentDirection.turnLeft() == nextDirection:
        mouse.turnLeft()
    elif currentDirection.turnRight() == nextDirection:
        mouse.turnRight()
    elif currentDirection != nextDirection:
        mouse.turnAround()
    mouse.moveForward()

def getBackCell(maze, mouse, w):
    frontier= PriorityQueue()
    initial= mouse.getPosition()
    frontier.put(initial, 0)
    #global flood
    anc= {}
    center= (0,0)
    cost_so_far= {}
    anc[initial]= None
    cost_so_far[initial]= 0

    while not frontier.empty():
        current = frontier.get()

        if current == center:
            break
        for direction in Direction:
            neighbor= getNeighbor(current, direction)
            
            if not maze.contains(neighbor):
                continue
            if maze.getWall(current, direction):
                continue
            if neighbor in anc:
                continue
            new_cost= cost_so_far[current] + maze.cost(current, neighbor)
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority= new_cost + w*heuristic(neighbor, center)
                frontier.put(neighbor, priority)
                anc[neighbor] = current
                x, y= current
                API.setText(x, y, priority)
                #flood[x][y]= priority
                #if maze.inCenter(neighbor):
                #    center = neighbor

    position = center
    while anc[position]!= initial:
        position= anc[position]
    return position 


if __name__ == "__main__":
    main()
