import heapq

class PriorityQueue:
    def __init__(self):
        self.que: List[Tuple[float, item]] = []
    
    def empty(self) -> bool:
        return len(self.que) == 0
    
    def put(self, item , priority: float):
        heapq.heappush(self.que, (priority, item))

    def get(self) :
        return heapq.heappop(self.que)[1]