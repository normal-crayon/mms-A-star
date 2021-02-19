import API
import collections
import sys
import numpy as np
from Direction import Direction
from Maze import Maze
from Mouse import Mouse
from time import sleep

path = []
def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()

def main():
    maze = Maze(API.mazeWidth(), API.mazeHeight())
    mouse = Mouse(0, 0, Direction.NORTH)
    while not maze.inCenter(mouse.getPosition()):
        #log(mouse.getPosition())
        updateWalls(maze, mouse)
        moveOneCell(maze, mouse)
        path.append(mouse.getPosition())
    log("Done!")
    log("Going back")
    '''while not maze.inStart(mouse.getPosition()):
        log(mouse.getPosition())
        updateWalls(maze, mouse)
        moveBack(maze, mouse)
        path.append(mouse.getPosition())'''
    

def updateWalls(maze, mouse):
    position = mouse.getPosition()
    direction = mouse.getDirection()
    if API.wallFront():
        maze.setWall(position, direction)
    if API.wallLeft():
        maze.setWall(position, direction.turnLeft())
    if API.wallRight():
        maze.setWall(position, direction.turnRight())


def moveOneCell(maze, mouse):
    currentX, currentY = mouse.getPosition()
    nextX, nextY = getNextCell(maze, mouse)
    if nextX < currentX:
        nextDirection = Direction.WEST
    if nextY < currentY:
        nextDirection = Direction.SOUTH
    if nextX > currentX:
        nextDirection = Direction.EAST
    if nextY > currentY:
        nextDirection = Direction.NORTH

    currentDirection = mouse.getDirection()
    if currentDirection.turnLeft() == nextDirection:
        mouse.turnLeft()
    elif currentDirection.turnRight() == nextDirection:
        mouse.turnRight()
    elif currentDirection != nextDirection:
        mouse.turnAround()
    mouse.moveForward()


def getNextCell(maze, mouse):
    initial = mouse.getPosition()
    center = None
    ancestors = {}
    queue = collections.deque([initial])
    while queue:
        current = queue.popleft()
        for direction in Direction:
            neighbor = getNeighbor(current, direction)
            # If the neighbor is out of bounds, skip
            if not maze.contains(neighbor):
                continue
            # If the neighbor is blocked by wall, skip
            if maze.getWall(current, direction):
                continue
            # If the neighbor is already discovered, skip
            if neighbor in ancestors:
                continue
            # Add the neighbor to queue and update ancestors
            queue.append(neighbor)
            ancestors[neighbor] = current
            if maze.inCenter(neighbor):
                center = neighbor
        # If a center cell was found, stop searching
        if center:
            break

    # Walk backwards from the center
    position = center
    while ancestors[position] != initial:
        position = ancestors[position]
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

def goBack(maze, mouse):
    initial= mouse.getPosition()
    start= None
    anc={}
    q= collections.deque([initial])
    while q:
        current = q.popleft()
        for direction in Direction:
            neighbor= getNeighbor(current, direction)

            if not maze.contains(neighbor):
                continue
            if maze.getWall(current, direction):
                continue
            if neighbor in anc:
                continue
            q. append(neighbor)
            anc[neighbor]= current
            if maze.inStart(neighbor):
                start= neighbor
            
        if start:
            break
        
    position= start
    while anc[position]!= initial:
        position= anc[position]
    return position

def goTo(maze, mouse):
    initial= mouse.getPosition()
    start= None
    anc={}
    q= collections.deque([initial])
    while q:
        current = q.popleft()
        for direction in Direction:
            neighbor= getNeighbor(current, direction)

            if not maze.contains(neighbor):
                continue
            if maze.getWall(current, direction):
                continue
            if neighbor in anc:
                continue
            q. append(neighbor)
            anc[neighbor]= current
            if maze.inPos(neighbor):
                start= neighbor
            
        if start:
            break
        
    position= start
    while anc[position]!= initial:
        position= anc[position]
    return position
#go back
def moveBack(maze, mouse):
    # Compute the next direction
    currentX, currentY = mouse.getPosition()
    nextX, nextY = goBack(maze, mouse)
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

#goto
def moveTo(maze, mouse):
    # Compute the next direction
    currentX, currentY = mouse.getPosition()
    nextX, nextY = goTo(maze, mouse)
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

if __name__ == "__main__":
    main()
    '''log(tocenter)
    log(tostart[::-1])
    np.save('toCenter', tocenter)
    np.save('toStart', tostart)'''