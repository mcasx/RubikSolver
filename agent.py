from rubik import RubikCube
from node import Node
import heapq
import math
import itertools

class Agent:
    def isGoal(state):
        top = [ cubie.cz for cubie in state if cubie.z == 1 ]
        left = [ cubie.cx for cubie in state if cubie.x == -1 ]
        face = [ cubie.cy for cubie in state if cubie.y == -1 ]
        right = [ cubie.cx for cubie in state if cubie.x == 1 ]
        bottom = [ cubie.cz for cubie in state if cubie.z == -1 ]
        back = [ cubie.cy for cubie in state if cubie.y == 1 ]

        return top[1:] == top[:-1] and left[1:] == left[:-1] and face[1:] == face[:-1] and right[1:] == right[:-1] and bottom[1:] == bottom[:-1] and back[1:] == back[:-1] 

    def manhattan_Dist3D(cubie):
        if (cubie.cx,cubie.cy,cubie.cz) in itertools.permutations(['O','Y','W']):
            return abs(cubie.x+1) + abs(cubie.y-1) + abs(cubie.z-1)
        if (cubie.cx,cubie.cy,cubie.cz) in itertools.permutations(['R','Y','W']):
            return abs(cubie.x-1) + abs(cubie.y-1) + abs(cubie.z-1)
        if (cubie.cx,cubie.cy,cubie.cz) in itertools.permutations(['O','G','W']):
            return abs(cubie.x+1) + abs(cubie.y+1) + abs(cubie.z-1)
        if (cubie.cx,cubie.cy,cubie.cz) in itertools.permutations(['R','G','W']):
            return abs(cubie.x-1) + abs(cubie.y+1) + abs(cubie.z-1)
        
        if (cubie.cx,cubie.cy,cubie.cz) in itertools.permutations(['O','Y','B']):
            return abs(cubie.x+1) + abs(cubie.y-1) + abs(cubie.z+1)
        if (cubie.cx,cubie.cy,cubie.cz) in itertools.permutations(['R','Y','B']):
            return abs(cubie.x-1) + abs(cubie.y-1) + abs(cubie.z+1)
        if (cubie.cx,cubie.cy,cubie.cz) in itertools.permutations(['O','G','B']):
            return abs(cubie.x+1) + abs(cubie.y+1) + abs(cubie.z+1)
        if (cubie.cx,cubie.cy,cubie.cz) in itertools.permutations(['R','G','B']):
            return abs(cubie.x-1) + abs(cubie.y+1) + abs(cubie.z+1)
        
        if (cubie.cx,cubie.cy,cubie.cz) in itertools.permutations(['O','W',None]):
            return abs(cubie.x+1) + abs(cubie.y) + abs(cubie.z-1)
        if (cubie.cx,cubie.cy,cubie.cz) in itertools.permutations(['Y','W',None]):
            return abs(cubie.x) + abs(cubie.y-1) + abs(cubie.z-1)
        if (cubie.cx,cubie.cy,cubie.cz) in itertools.permutations(['R','W',None]):
            return abs(cubie.x-1) + abs(cubie.y) + abs(cubie.z-1)
        if (cubie.cx,cubie.cy,cubie.cz) in itertools.permutations(['G','W',None]):
            return abs(cubie.x) + abs(cubie.y+1) + abs(cubie.z-1)
        
        if (cubie.cx,cubie.cy,cubie.cz) in itertools.permutations(['O','Y',None]):
            return abs(cubie.x+1) + abs(cubie.y-1) + abs(cubie.z)
        if (cubie.cx,cubie.cy,cubie.cz) in itertools.permutations(['R','Y',None]):
            return abs(cubie.x-1) + abs(cubie.y-1) + abs(cubie.z)
        if (cubie.cx,cubie.cy,cubie.cz) in itertools.permutations(['R','G',None]):
            return abs(cubie.x-1) + abs(cubie.y+1) + abs(cubie.z)
        if (cubie.cx,cubie.cy,cubie.cz) in itertools.permutations(['O','G',None]):
            return abs(cubie.x+1) + abs(cubie.y+1) + abs(cubie.z)
        
        if (cubie.cx,cubie.cy,cubie.cz) in itertools.permutations(['O','B',None]):
            return abs(cubie.x+1) + abs(cubie.y) + abs(cubie.z+1)
        if (cubie.cx,cubie.cy,cubie.cz) in itertools.permutations(['Y','B',None]):
            return abs(cubie.x) + abs(cubie.y-1) + abs(cubie.z+1)
        if (cubie.cx,cubie.cy,cubie.cz) in itertools.permutations(['R','B',None]):
            return abs(cubie.x-1) + abs(cubie.y) + abs(cubie.z+1)
        if (cubie.cx,cubie.cy,cubie.cz) in itertools.permutations(['G','B',None]):
            return abs(cubie.x) + abs(cubie.y+1) + abs(cubie.z+1)

    def heuristic(state):
        values = [Agent.heuristic1(state), Agent.heuristic2(state) ]
        return values[0] if values[0] > values[1] else values[1]

    #Number of corners cubies displaced
    def heuristic1(state):
        return sum([ Agent.manhattan_Dist3D(state[i]) for i in range(6,14) ])/4

    #Number of edges displaced
    def heuristic2(state):
        return sum([ Agent.manhattan_Dist3D(state[i]) for i in range(14,26) ])/4

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
            childCube.rotate(x[0],x[1])
            child = Node( childCube, node.cost+1, Agent.heuristic(childCube.state), (x[0], x[1]), node)
            if child.totalCost <= bound:
                m = Agent.idaStar(child,bound)
                if type(m) is Node:
                    return m
                fn = m if m < fn else fn

            else:
                fn = child.totalCost if child.totalCost < fn else fn

        return fn
