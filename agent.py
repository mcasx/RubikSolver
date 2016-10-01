from rubik import RubikCube
from node import Node
import heapq
from functools import reduce

class Agent:
    def isGoal(state):
        if state == []:
            return True
     
        return all([ row[1:] == row[:-1] and row == state[0][0] for row in state[0] ]) and Agent.isGoal(state[1:])

    def heuristic(state):
        values = [ Agent.heuristic1(state), Agent.heuristic2(state) ]
        return reduce(lambda x,y: x if x > y else y, values, values[0])

    #Number of faces unsolved
    def heuristic1(state):
        if state == []:
            return 0

        return (0 if all([ row[1:] == row[:-1] and row == state[0][0] for row in state[0] ]) else 1) + Agent.heuristic1(state[1:])

    #Number of corners cubies displaced
    def heuristic2(state):
        #Top cubies
        #upper left
        lst = [ state[0][0][0] == state[0][1][1] and state[5][2][0] == state[5][1][1] and state[1][0][0] == state[1][1][1] ]
        #upper right 
        lst += [ state[0][0][2] == state[0][1][1] and state[5][2][2] == state[5][1][1] and state[3][2][0] == state[3][1][1] ]
        #lower left
        lst += [ state[0][2][0] == state[0][1][1] and state[2][0][0] == state[2][1][1] and state[1][0][2] == state[1][1][1] ]
        #lower right
        lst += [ state[0][2][2] == state[0][1][1] and state [2][0][2] == state[2][1][1] and state[3][0][0] == state[3][1][1] ]

        #Bottom cubies
        #upper left
        lst += [ state[4][0][0] == state[4][1][1] and state[2][2][0] == state[2][1][1] and state[1][2][2] == state[1][1][1] ]
        #upper right
        lst += [ state[4][0][2] == state[4][1][1] and state[2][2][2] == state[2][1][1] and state[3][2][0] == state[3][1][1] ]
        #lower left
        lst += [ state[4][2][0] == state[4][1][1] and state[5][0][0] == state[5][1][1] and state[1][2][0] == state[1][1][1] ]
        #lower right
        lst += [ state[4][2][2] == state[4][1][1] and state[5][2][0] == state[5][1][1] and state[3][2][2] == state[3][1][1] ]

        return lst.count(False)

    def search(startCube):
        node = Node(startCube,0,Agent.heuristic(startCube.state),None,None)
        frontier = []
        heapq.heappush(frontier, node)
        explored = []
        
        while True:
            if frontier == []:
                return None

            node = heapq.heappop(frontier)
            if Agent.isGoal(node.cube.state):
                return node.getPath()
           
            if node.cube.state not in explored:
                explored += [node.cube.state]

            for x in node.cube.getActions():
                childCube = RubikCube(state = node.cube.state)
                if x[0] in ('up','down','left','right'):
                    childCube.move(x[0], x[1])
                else:
                    childCube.rotate(x[1])
                
                child = Node( childCube, node.cost+1, Agent.heuristic(childCube.state), (x[0], x[1]), node)

                if child.cube.state not in explored and child not in frontier:
                    heapq.heappush(frontier, child)

                elif child in frontier:
                    i = frontier.index(child)
                    if frontier[i].cost > child.cost:
                        frontier.remove(frontier[i])
                        heapq.heapify(frontier)
                        heapq.heappush(frontier, child)
