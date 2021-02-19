def dijkstra(maze, mouse):
    frontier= PrioriyQueue()
    initial= mouse.getPosition()
    anc= {}
    center= {(7,7)}
    cost_so_far= {}
    anc[initial]= None
    cost_so_far[initial]= 0

    while not frontier.empty():
        current = frontier.get()

        if current == maze.getEnd():
            break
        
        for direction in Direction:
            neighbor= getNeighbor(current, direction)
            
            if not maze.contains(neighbor):
                continue
            if maze.getWall(current, direction):
                continue
            
            new_cost= cost_so_far[current] + maze.cost(current, neighbor)
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority= new_cost
                frontier.put(neighbor, priority)
                anc[neighbor] = current
    position = maze.getEnd()
    while anc[position]!= initial:
        position= anc[position]
    return position