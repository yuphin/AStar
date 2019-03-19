from queue import PriorityQueue
import heapq
import timeit
from copy import deepcopy
outDict = {}
# Read and parse the file => (coordX,coordY)


class Node:
    def __init__(self, state, emptyCoord, g):
        global outDict
        self.state = state
        self.deleted = 0
        self.emptyCoord = emptyCoord
        self.g = g
        self.parent = None
        self.pathCost = calculateH(self.state, outDict) + self.g

    def __eq__(self, other):
        return self.pathCost == other.pathCost

    def __lt__(self, other):
        return self.pathCost < other.pathCost


def readFile(outDict):
    out = 0
    coord = ()
    input = ()
    output = ()
    numLineInp = 0
    with open('input.txt') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped:
                out = 1
                numLineInp += 1
                continue
            if not out:
                for j, num in enumerate(stripped.split()):
                    if num == '0':
                        coord = (i, j)
                    input += (int(num),)
                numLineInp += 1
            else:
                for j, num in enumerate(stripped.split()):
                    output += (int(num),)
                    outDict[int(num)] = (i-numLineInp, j)
    return (input,output,coord)
# Generate possible actions(u,d,l,r) w.r.t coordinates => [string]


def generateActions(emptyCoord):
    actions = []
    i, j = emptyCoord
    if j == 0:
        actions.append('r')
    elif j == 1:
        actions.extend(['l', 'r'])
    else:
        actions.append('l')
    if i == 0:
        actions.append('d')
    elif i == 1:
        actions.extend(['u', 'd'])
    else:
        actions.append('u')

    return actions
# Apply the action => (newCoordx,newCoordy,newState)
def applyAction(node, action):
    i, j = node.emptyCoord
    if not action:
        return node
    newState = list(node.state)
    if action == 'd':
        newState[(i+1)*3 +j ], newState[i*3 +j] = newState[i*3 +j], newState[(i+1)*3 +j ]
        return Node(tuple(newState), (i + 1, j), node.g + 1)
    elif action == 'u':
        newState[(i-1)*3+ j], newState[i*3 +j] = newState[i*3 +j], newState[(i-1)*3+ j]
        return Node(tuple(newState), (i - 1, j), node.g + 1)
    elif action == 'r':
        newState[i*3 + j+1], newState[i*3 +j] = newState[i*3 +j], newState[i*3 + j+1]
        return Node(tuple(newState), (i, j + 1), node.g + 1)
    elif action == 'l':
        newState[i*3 + j-1], newState[i*3 +j] = newState[i*3 +j], newState[i*3 + j-1]
        return Node(tuple(newState), (i, j - 1), node.g + 1)
    return node
#Calculate heuristics
def calculateH(state, outDict):
    heur = 0
    for idx, num in enumerate(state):
        i = idx // 3
        j = idx % 3
        if num != 0:
            heur += abs(outDict[num][0] - i) + abs(outDict[num][1] - j)
    return heur


def stateInFrontier(state, frontierDict):
   return frontierDict.get(state)

def stateInExplored(state, explored):
   return explored.get(state)

def A_star(initNode):
    frontier = []
    explored = {}
    frontierDict = {}
    heapq.heappush(frontier, initNode)
    while frontier:
        node = heapq.heappop(frontier)
        if node.deleted:
            continue
        if node.pathCost == node.g:
            printStates(node)
            return
        explored[node.state] = 1
        for action in generateActions(node.emptyCoord):
            child = applyAction(node, action)
            frontierRef = stateInFrontier(child.state, frontierDict)
            if not (frontierRef or stateInExplored(child.state, explored)):
                heapq.heappush(frontier, child)
                frontierDict[child.state] = child
                child.parent = node
            elif frontierRef and frontierRef.pathCost > child.pathCost:
                frontierRef.deleted = 1
                heapq.heappush(frontier,child)
                child.parent = node
                frontierDict[child.state] = child
    return 'fail'

def fLimitedDFS(node,limit,path):
    if node.pathCost == node.g:
        return (0,node)
    elif node.pathCost > limit:
        return (1,node.pathCost)
    else:
        cutoff = 9999999
        for action in generateActions(node.emptyCoord):
            child = applyAction(node, action)
            if not path.get(child.state):
                child.parent = node
                path[child.state] =1
                result = fLimitedDFS(child,limit,path)
                if result[0]:
                    cutoff = result[1]
                elif result != 'fail':
                    return result
                path.pop(child.state)
        return (1,cutoff)
def IDA_star(node):
    limit = node.pathCost
    #print("Calling dfs with ", limit)
    path = {}
    while True:
        #print("Calling dfs with ", limit)
        path.clear()
        path[node.state] = 1
        result = fLimitedDFS(node,limit,path)
        if result == 'fail':
            return 'fail'
        elif result[0] ==0:
            printStates(result[1],True)
            return
        if result[1] > 31:
            return 'fail'
        else:
            limit = result[1]
            #print("Calling dfs with ",limit)
def printState(state,f):
    for i in range(3):
        for j in range(3):
            if j != 2:
                f.write("%d " % state[i*3+j])
            else:
                f.write("%d" % state[i*3+j])
        f.write('\n')
    f.write('\n')

def printStates(node,idastar = False):
    lst = []
    f = None
    if idastar:
        f = open("outputIDA.txt", "w+")
    else:
        f = open("outputA.txt", "w+")
    while node.parent:
        lst.append(node.state)
        node = node.parent
    for state in reversed(lst):
        printState(state,f)
    f.close()

def main():
    global outDict
    start = timeit.default_timer()
    input,output,emptyCoord = readFile(outDict)
    A_star(Node(input, emptyCoord, 0))
    stop = timeit.default_timer()
    print('A* Time: ', stop - start)
    start = timeit.default_timer()
    IDA_star(Node(input, emptyCoord, 0))
    stop = timeit.default_timer()
    print('IDA* Time: ', stop - start)

if __name__ == '__main__':
    main()
