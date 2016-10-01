from rubik import RubikCube
from node import Node
import heapq

class Agent:
    def isGoal(state):
        if state == []:
            return True
     
        return all([ row[1:] == row[:-1] and row == state[0][0] for row in state[0] ]) and Agent.isGoal(state[1:])

    def heuristic1(state):
        if state == []:
            return 0

        return (0 if all([ row[1:] == row[:-1] and row == state[0][0] for row in state[0] ]) else 1) + Agent.heuristic1(state[1:])

    def search(startCube):
        node = Node(startCube,0,Agent.heuristic1(startCube.state),None,None)
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
                
                child = Node( childCube, node.cost+1, Agent.heuristic1(childCube.state), (x[0], x[1]), node)

                if child.cube.state not in explored and child not in frontier:
                    heapq.heappush(frontier, child)

                elif child in frontier:
                    i = frontier.index(child)
                    if frontier[i].cost > child.cost:
                        frontier.remove(frontier[i])
                        heapq.heapify(frontier)
                        heapq.heappush(frontier, child)
