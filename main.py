from graph import Graph
import json
import sys

def createHeuristic(the_maze):
    heuristic = {}
    the_map = the_maze["map"]
    end = the_maze["end"].split('_')
    (end_i, end_j) = (int(end[0]), int(end[1]))
    
    n = the_maze['n']
    m = the_maze['m']
    
    for i in range(n):
        for j in range(m):
            heuristic["%d_%d" % (i, j)] = abs(end_i - i) + abs(end_j - j)
    return heuristic
        
def print_map(the_maze, path):
    n = the_maze['n']
    m = the_maze['m']
    start = the_maze["start"]
    end = the_maze["end"]
    the_map = the_maze["map"]
    for i in range(n):
        for j in range(m):
            elStr = ("%d_%d" % (i, j))
            if elStr == end:
                print "e",
            elif elStr == start:
                print "s",
            elif elStr in path:
                print "p",
            elif elStr in the_map:
                print " ",
            else:
                print "*",
        print
        
def loadJsonFile(text, fileName):
    jsonObj = {}
    jsonObj["map"] = {}
    
    n = len(text) - 1
    m = len(text[0])
    jsonObj["n"] = n
    jsonObj["m"] = m
    
    for i in range(n):
        for j in range(m):
            if text[i][j] == 's':
                jsonObj["start"] = "%d_%d" % (i, j)
                jsonObj["map"]["%d_%d" % (i, j)] = []
                if text[i+1][j] != '*':
                    jsonObj["map"]["%d_%d" % (i, j)].append(["%d_%d" % (i+1, j), 1])
                if text[i-1][j] != '*':
                    jsonObj["map"]["%d_%d" % (i, j)].append(["%d_%d" % (i-1, j), 1])
                if text[i][j+1] != '*':
                    jsonObj["map"]["%d_%d" % (i, j)].append(["%d_%d" % (i, j+1), 1])
                if text[i][j-1] != '*':
                    jsonObj["map"]["%d_%d" % (i, j)].append(["%d_%d" % (i, j-1), 1])
            elif text[i][j] == 'e':
                jsonObj["end"] = "%d_%d" % (i, j)
                jsonObj["map"]["%d_%d" % (i, j)] = []
            elif text[i][j] == ' ':
                jsonObj["map"]["%d_%d" % (i, j)] = []
                if text[i+1][j] != '*':
                    jsonObj["map"]["%d_%d" % (i, j)].append(["%d_%d" % (i+1, j), 1])
                if text[i-1][j] != '*':
                    jsonObj["map"]["%d_%d" % (i, j)].append(["%d_%d" % (i-1, j), 1])
                if text[i][j+1] != '*':
                    jsonObj["map"]["%d_%d" % (i, j)].append(["%d_%d" % (i, j+1), 1])
                if text[i][j-1] != '*':
                    jsonObj["map"]["%d_%d" % (i, j)].append(["%d_%d" % (i, j-1), 1])
    with open(fileName, "w") as f:
        json.dump(jsonObj, f)

def main():
    
    try:
        with open(sys.argv[1], "r") as lavTxt:
            text = lavTxt.read().split("\n")
            loadJsonFile(text, "maze.json")
            with open("maze.json", "r") as lavJson:
                the_maze = json.load(lavJson)
    except IOError:
        sys.exit("Failed loading file")
        
    
    the_map = the_maze["map"]
    heuristic = createHeuristic(the_maze)
    g = Graph(the_map, heuristic)
    start = the_maze["start"]
    end = the_maze["end"]
    
    pathBestFirst = g.bestFirst(start, end)
    print len(pathBestFirst)
    pathAStar = g.astar(start, end)
    print len(pathAStar)

    print_map(the_maze, pathBestFirst)
    print "###########################################"
    print "###########################################"
    print_map(the_maze, pathAStar)
    
if __name__ == "__main__":
    main()
