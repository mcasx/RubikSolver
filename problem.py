from rubik import RubikCube
from node import Node
from agent import Agent
import time

class Problem:
    def __init__(self,initCube):
        self.initCube = initCube
        self.moves = 0
        self.timeElapsed = 0.0
        self.solution = []

    def solve(self):
        t0 = time.clock()
        self.solution = Agent.search(self.initCube)
        assert self.solution != None, "No solution"
        self.timeElapsed = time.clock() - t0
        self.moves = len(self.solution)

if __name__ == "__main__":

    s = int( input("Length of cube? ") )
    init = RubikCube(s)
    n = int( input("Randomize by how many moves? ") )
    init.randomize(n)
    print(init)
    p = Problem(init)
    p.solve()
    print("Time: {}s".format("%.3f"%p.timeElapsed))
    print("Moves: {}".format(p.moves))
    print(p.solution)