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
        self.solution = Agent.idaStarMain(self.initCube)
        assert self.solution != None, "No solution"
        self.timeElapsed = time.clock() - t0
        self.moves = len(self.solution)

if __name__ == "__main__":

    init = RubikCube(3)
    n = int( input("Randomize by how many moves? ") )
    init.randomize(n)
    print(init)
    pidaStar = Problem(init)
    
    pidaStar.solve()
    print("Time: {}s".format("%.3f"%pidaStar.timeElapsed))
    print("Moves: {}".format(pidaStar.moves))
    print("{}\n".format(pidaStar.solution))
