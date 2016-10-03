from rubik import RubikCube
from node import Node
import heapq
from functools import reduce
import math

class Agent:
    def isGoal(state):
        if state == []:
            return True
     
        return all([ row[1:] == row[:-1] and row == state[0][0] for row in state[0] ]) and Agent.isGoal(state[1:])

    def heuristic(state):
        values = [Agent.heuristic1(state)/4, Agent.heuristic2(state)/4 ]
        return reduce(lambda x,y: x if x > y else y, values, values[0])

    #Number of corners cubies displaced
    def heuristic1(state):
        #Top cubies
        #upper left
        lst = [ state[0][0][0] == state[0][1][1] and state[5][0][2] == state[5][1][1] and state[1][0][0] == state[1][1][1] ]
        #upper right 
        lst += [ state[0][0][2] == state[0][1][1] and state[5][0][0] == state[5][1][1] and state[3][0][2] == state[3][1][1] ]
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
        lst += [ state[4][2][0] == state[4][1][1] and state[5][2][2] == state[5][1][1] and state[1][2][0] == state[1][1][1] ]
        #lower right
        lst += [ state[4][2][2] == state[4][1][1] and state[5][2][0] == state[5][1][1] and state[3][2][2] == state[3][1][1] ]
        return lst.count(False)

    #Number of edges displaced
    def heuristic2(state):
        #Top cubies
        lst = [ state[0][0][1] == state[0][1][1] and state[5][2][1] == state[5][1][1] ]
        lst += [ state[0][1][0] == state[0][1][1] and state[1][0][1] == state[1][1][1] ]
        lst += [ state[0][1][2] == state[0][1][1] and state[3][0][1] == state[3][1][1] ]
        lst += [ state[0][2][1] == state[0][1][1] and state[2][0][1] == state[2][1][1] ]
        #Side cubies
        lst += [ state[1][1][0] == state[1][1][1] and state[5][1][0] == state[5][1][1] ]
        lst += [ state[1][1][2] == state[1][1][1] and state[2][1][0] == state[2][1][1] ]
        lst += [ state[3][1][0] == state[3][1][1] and state[2][1][2] == state[2][2][1] ]
        lst += [ state[3][1][2] == state[3][1][1] and state[5][1][2] == state[5][1][1] ]
        #Bottom cubies
        lst += [ state[4][0][1] == state[4][1][1] and state[2][2][1] == state[2][1][1] ]
        lst += [ state[4][1][0] == state[4][1][1] and state[1][2][1] == state[1][1][1] ]
        lst += [ state[4][1][2] == state[4][1][1] and state[3][2][1] == state[3][1][1] ]
        lst += [ state[4][2][1] == state[4][1][1] and state[5][0][1] == state[5][1][1] ]

        return lst.count(False)

    def idaStarMain(startCube):
        node = Node(startCube,0,Agent.heuristic(startCube.state),None,None)
        bound = node.totalCost
        while bound < math.inf:
            bound = Agent.idaStar(node,bound)
            if type(bound) is Node:
                return bound.getPath()

        return None


    def idaStar(node,bound):
        if Agent.isGoal(node.cube.state):
            return node

        fn = math.inf
        for x in node.cube.getActions():
            childCube = RubikCube(state = node.cube.state)
            if x[0] in ('up','down','left','right'):
                childCube.move(x[0], x[1])
            else:
                childCube.rotate(x[1])
            
            child = Node( childCube, node.cost+1, Agent.heuristic(childCube.state), (x[0], x[1]), node)
            if child.totalCost <= bound:
                m = Agent.idaStar(child,bound)
                if type(m) is Node:
                    return m
                fn = m if m < fn else fn

            else:
                fn = child.totalCost if child.totalCost < fn else fn

        return fn
