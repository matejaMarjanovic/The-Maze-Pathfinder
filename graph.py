from collections import deque
from sortedcontainers import SortedDict

class Graph:
    def __init__(self, adjecencyList, heuristic):
        self.adjecencyList = adjecencyList
        self.marked = {}
        self.heuristic = heuristic
    
    def resetMarked(self):
        self.marked = {}
    
    def bestFirst(self, start, end):
        openList = [start]
        closedList = []
        g = {}
        g[start] = 0
        parent = {}
        parent[start] = None
        
        while len(openList) > 0:
            minVal = min([g[w] for w in openList])
            v = None
            for w in openList:
                if minVal == g[w]:
                    v = w
            
            if v == end:
                path = deque([])
                while parent[v] != None:
                    path.appendleft(v)
                    v = parent[v]
                path.appendleft(v)
                print "Best-First"
                return path
            for (w, weight) in self.adjecencyList[v]:
                if w not in openList and w not in closedList:
                    openList.append(w)
                    g[w] = g[v] + weight
                    parent[w] = v
                #elif g[w] > g[v] + weight:
                    #g[w] = g[v] + weight
                    #parent[w] = v
                    #if w in closedList:
                        #closedList.remove(w)
                        #openList.append(w)
            openList.remove(v)
            closedList.append(v)
        return []
            
    def DFS(self, start, end):
        self.marked[start] = True
        
        path = [start]
        
        step = 0
        while len(path) > 0:
            step += 1
            v = path[-1]
            
            if v == end:
                print "DFS"
                #print step
                return path
            
            noVisits = True
            for (w, weight) in self.adjecencyList[v]:
                if w not in self.marked:
                    path.append(w)
                    self.marked[w] = True
                    noVisits = False
                    break
            
            if noVisits == True:
                path.pop()
                
    def BFS(self, start, end):
        self.resetMarked()
        queue = deque([start])
        
        parent = {}
        self.marked[start] = True
        parent[start] = None
        
        step = 0
        while len(queue) > 0:
            step += 1
            v = queue.popleft()
            
            if v == end:
                path = []
                v = end
                while parent[v] != None:
                    path.append(v)
                    v = parent[v]
                
                path.append(v)
                print "BFS"
                #print step
                return list(path)[::-1]
            
            for (w, weight) in self.adjecencyList[v]:
                if w not in self.marked:
                    self.marked[w] = True
                    queue.append(w)
                    parent[w] = v
    
    def dijkstra(self, start, end):
        self.resetMarked()
        nodes = set(self.adjecencyList.keys())
        
        parent = {}
        parent[start] = None
        path = {}
        for v in self.adjecencyList.keys():
            path[v] = float('inf')
        path[start] = 0
        step = 0
        
        while len(self.marked) != len(path):
            step += 1
            # trazenje najblizeg cvora
            (min_node, min_weight) = min([(k, v) for (k, v) in path.items() if k not in self.marked], key=lambda t: t[1])
            
            # oznacavanje tog cvora
            self.marked[min_node] = True
            
            # azuriranje vrednosti njemu susednih cvorova
            for (node, weight) in self.adjecencyList[min_node]:
                if node not in self.marked and path[node] > weight + min_weight:
                    path[node] = weight + min_weight
                    parent[node] = min_node
        
        v = end
        reconstruction = deque([])
        
        while parent[v] != None:
            reconstruction.appendleft(v)
            v = parent[v]
        
        reconstruction.appendleft(v)
        
        print "dijkstra"
        #print step
        return list(reconstruction)

    def set_heuristic(self, H):
        self.H = H

    def h(self, v):
        return self.heuristic[v]


    def astar(self, start, end):
        g = {}
        g[start] = 0
        #openList = SortedDict({start : g[start]})
        openList = [start]
        closedList = {}

        
        parent = {}
        parent[start] = None
        
        while len(openList) > 0:
            #n = openList.keys()[-1]
            #n = min(openList.items(), key=lambda x: x([1]))
            n = None
            for v in openList:
                if n == None or g[v] + self.h(v) < g[n] + self.h(n):
                    n = v
            
            if n == None:
                print "Path not found..."
                return []
            
            if n == end:
                path = deque([])
                v = end
                while parent[v] != None:
                    path.appendleft(v)
                    v = parent[v]
                path.appendleft(v)
                
                print "A*"
                return list(path)
            
            for (w, weight) in self.adjecencyList[n]:
                if w not in openList and w not in closedList:
                    g[w] = g[n] + weight
                    openList.append(w)
                    parent[w] = n
                elif w in openList:
                    if g[w] > g[n] + weight:
                        g[w] = g[n] + weight
                        parent[w] = n
                        
            openList.remove(n)
            closedList[n] = True
        
        print "Path not found"
        return []
