from rubik import RubikCube
from node import Node
from agent import Agent
import time

class Problem:
    def __init__(self,initCube,t):
        self.initCube = initCube
        self.t = t
        self.moves = 0
        self.timeElapsed = 0.0
        self.solution = []

    def solve(self):
        t0 = time.clock()
        if self.t == 0:
            self.solution = Agent.aStar(self.initCube)
        elif self.t == 1:
            self.solution = Agent.idaStarMain(self.initCube)
        assert self.solution != None, "No solution"
        self.timeElapsed = time.clock() - t0
        self.moves = len(self.solution)

if __name__ == "__main__":

    init = RubikCube(3)
    n = int( input("Randomize by how many moves? ") )
    init.randomize(n)
    print(init)
    paStar = Problem(init,0)
    pidaStar = Problem(init,1)
    
    pidaStar.solve()
    print("----idaStar----")
    print("Time: {}s".format("%.3f"%pidaStar.timeElapsed))
    print("Moves: {}".format(pidaStar.moves))
    print(pidaStar.solution)
    
    paStar.solve()
    print("\n----aStar----")
    print("Time: {}s".format("%.3f"%paStar.timeElapsed))
    print("Moves: {}".format(paStar.moves))
    print("{}\n".format(paStar.solution))

