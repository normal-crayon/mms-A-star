from collections import defaultdict

class Graph:
    def __init__(self, vertices):
        self.v= vertices 
        self.graph= defaultdict(list)

    def addEdge(self, u, v, w):
        if w==1:
            self.graph[u].append(v)
        else:
            self.graph[u].append(self.v)
            self.graph[self.v].append(v)
            self.v= self.v + 1
    def getGraph(self):
        return self.graph


#def findShort(maze, mouse, anc):
    