# Read and parse the file => (coordX,coordY)
def readFile(input,output):
    out = 0
    coord = ()
    with open('input.txt') as f:
        lines = f.readlines()
        for i,line in enumerate(lines):
            stripped = line.strip()
            if not stripped:
                out = 1
                continue
            if not out:
                inner = []
                for j,num in enumerate(stripped.split()):
                    if num == '0':
                        coord = (i,j)
                    inner.append(int(num))
                input.append(inner)
            else:
                output.append([int(n) for n in stripped.split()])
    return coord
# Generate possible actions(u,d,l,r) w.r.t coordinates => [string]
def generateActions(emptyCoord):
    actions = []
    i,j = emptyCoord
    if i == 0:
        actions.append('r')
    elif i == 1:
        actions.extend(['l','r'])
    else:
        actions.append('l')
    if j == 0:
        actions.append('d')
    elif j == 1:
        actions.extend(['u','d'])
    else:
        actions.append('u')

    return actions
# Apply the action => (newCoordx,newCoordy,newState)
def applyAction(state,action,emptyCoord):
    i, j = emptyCoord
    if not action:
        return (i,j,state)
    newState = [[i for i in row] for row in state]
    if action == 'd':
        newState[i+1][j],newState[i][j] = newState[i][j],newState[i+1][j]
        return (i+1,j,newState)
    elif action == 'u':
        newState[i-1][j],newState[i][j] = newState[i][j],newState[i-1][j]
        return (i-1,j,newState)
    elif action == 'r':
        newState[i][j+1],newState[i][j] = newState[i][j],newState[i][j+1]
        return (i,j+1,newState)
    elif action == 'l':
        newState[i][j-1],newState[i][j] = newState[i][j],newState[i][j-1]
        return (i,j-1,newState)
    return  (i,j,state)
def main():
    input = []
    output = []
    emptyCoord = readFile(input, output)
if __name__ == '__main__':
    main()