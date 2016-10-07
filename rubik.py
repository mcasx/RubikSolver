import random
import copy

class Cubie:
    def __init__(self, x,y,z,cx = None,cy = None,cz = None):
        self.x = x
        self.y = y
        self.z = z
        self.cx = cx
        self.cy = cy
        self.cz = cz

    def __eq__(self,other):
        return (self.x, self.y, self.z, self.cx, self.cy, self.cz) == (other.x, other.y, other.z, other.cx, other.cy, other.cz)

    def __str__(self):
        return '(' + str(self.x) + ',' + str(self.y) + ',' + str(self.z) + '), cx = ' + str(self.cx or 'None') + ', cy = ' + str(self.cy or 'None') + ', cz = ' + str(self.cz or 'None')

class RubikCube:
    def __init__(self,state = None):
        if state != None:
            self.state = copy.deepcopy(state)
        else:
            #Centers
            self.state = [ Cubie(0,0,1, cz = 'W'), Cubie(-1,0,0, cx = 'O'), Cubie(1,0,0, cx = 'R'), Cubie(0,0,-1, cz = 'B'), Cubie(0,1,0, cy = 'Y'), Cubie(0,-1,0, cy = 'G')]
            #Top Corners
            self.state += [ Cubie(-1,1,1, cx = 'O', cy = 'Y', cz = 'W'), Cubie(1,1,1, cx = 'R', cy = 'Y', cz = 'W'), Cubie(-1,-1,1, cx = 'O', cy = 'G', cz = 'W'), Cubie(1,-1,1, cx = 'R', cy = 'G', cz = 'W') ]
            #Bottom Corners
            self.state += [ Cubie(-1,1,-1, cx = 'O', cy = 'Y', cz = 'B'), Cubie(1,1,-1, cx = 'R', cy = 'Y', cz = 'B'), Cubie(-1,-1,-1, cx = 'O', cy = 'G', cz = 'B'), Cubie(1,-1,-1, cx = 'R', cy = 'G', cz = 'B') ]
            #Top Edges
            self.state += [ Cubie(-1,0,1, cx = 'O', cz = 'W'), Cubie(0,1,1, cy = 'Y', cz = 'W'), Cubie(1,0,1, cx = 'R', cz = 'W'), Cubie(0,-1,1, cy = 'G', cz = 'W') ]
            #Middle Edges
            self.state += [ Cubie(-1,1,0, cx = 'O', cy = 'Y'), Cubie(1,1,0, cx = 'R', cy = 'Y'), Cubie(1,-1,0, cx = 'R', cy = 'G'), Cubie(-1,-1,0, cx = 'O', cy = 'G') ]
            #Bottom Edges
            self.state += [ Cubie(-1,0,-1, cx = 'O', cz = 'B'), Cubie(0,1,-1, cy = 'Y', cz = 'B'), Cubie(1,0,-1, cx = 'R', cz = 'B'), Cubie(0,-1,-1, cy = 'G', cz = 'B') ]
            

    def __eq__(self,other):
       return all( [ x[0] == x[1] for x in zip( self.state, other.state  )  ] )

    #direction = 1 for clockwise rotation, -1 for ccw rotation
    def rotate(self,face,direction):
        assert face in ('F','L','R','B','U','D')
        if face == 'F':
            for cubie in [ x for x in self.state if x.y == -1 ]:
                cubie.x, cubie.z, cubie.cx, cubie.cz = direction*cubie.z, -1*direction*cubie.x, cubie.cz, cubie.cx
        if face == 'L':
            for cubie in [ x for x in self.state if x.x == -1 ]:
                cubie.y, cubie.z, cubie.cy, cubie.cz = -1*direction*cubie.z, direction*cubie.y, cubie.cz, cubie.cy
        if face == 'R':
            for cubie in [ x for x in self.state if x.x == 1 ]:
                cubie.y, cubie.z, cubie.cy, cubie.cz = -1*direction*cubie.z, direction*cubie.y, cubie.cz, cubie.cy
        if face == 'B':
            for cubie in [ x for x in self.state if x.y == 1 ]:
                cubie.x, cubie.z, cubie.cx, cubie.cz = direction*cubie.z, -1*direction*cubie.x, cubie.cz, cubie.cx
        if face == 'U':
            for cubie in [ x for x in self.state if x.z == 1 ]:
                cubie.x, cubie.y, cubie.cx, cubie.cy = direction*cubie.y, -1*direction*cubie.x, cubie.cy, cubie.cx
        if face == 'D':
            for cubie in [ x for x in self.state if x.z == -1 ]:
                cubie.x, cubie.y, cubie.cx, cubie.cy = direction*cubie.y, -1*direction*cubie.x, cubie.cy, cubie.cx

    def randomize(self,n):
        actions = self.getActions()
        while n>0:
            i = random.randrange(len(actions))
            self.rotate(actions[i][0],actions[i][1])
            n -= 1

    def getActions(self):
        actions = [ (x,y) for x in ('F','L','R','B','U','D') for y in (-1,1)]
        return actions


    def __str__(self):
        s = ' '*4 + '-'*5 + '\n'
        for i in (1,0,-1):
            s += ' '*4 + '|' + ''.join([ x.cz for x in sorted(self.state,key=lambda x: x.x) if x.z == 1 and x.y == i ]) + '|\n'

        s += '-' + '-'*15 + '-\n'
        for i in (1,0,-1):
            s += '|' + ''.join([ x.cx for x in sorted(self.state,key=lambda x: x.y,reverse=True) if x.x == -1 and x.z == i ]) + '|' + ''.join([ x.cy for x in sorted(self.state,key=lambda x: x.x) if x.y == -1 and x.z == i ]) + '|' + ''.join([ x.cx for x in sorted(self.state,key=lambda x: x.y) if x.x == 1 and x.z == i ]) + '|' + ''.join([ x.cy for x in sorted(self.state,key=lambda x: x.x) if x.y == 1 and x.z == i ]) + '|\n'
        
        s += '-' + '-'*15 + '-\n'
        for i in (-1,0,1):
            s += ' '*4 + '|' + ''.join([ x.cz for x in sorted(self.state,key=lambda x: x.x) if x.z == -1 and x.y == i ]) + '|\n'
       
        s += ' '*4 + '-'*5 + '\n'

        return s
