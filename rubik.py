import random
from copy import deepcopy

class RubikCube:
    def __init__(self,size = 3,state = None):
        self.TOP = 0
        self.LEFT = 1
        self.FACE = 2
        self.RIGHT = 3
        self.BOTTOM = 4
        self.BACK = 5
        if state:
            self.size = len(state[0])
            self.state = list(state)
        else:
            assert size >= 0, "Size has to be positive"
            self.size = size
            self.state = [\
                [ [0]*size for y in range(size) ],\
                [ [1]*size for y in range(size) ],\
                [ [2]*size for y in range(size) ],\
                [ [3]*size for y in range(size) ],\
                [ [4]*size for y in range(size) ],\
                [ [5]*size for y in range(size) ] ]

    def __cwQuarterTurn(self,face):
        temp = [ [-1]*self.size for y in range(self.size) ]
        for i in range(self.size):
                for j in range(self.size):
                    temp[i][j] = face[j][i]

        return temp
    
    def __ccwQuarterTurn(self,face):
        temp = [ [-1]*self.size for y in range(self.size) ]
        for i in range(self.size):
                for j in range(self.size):
                    temp[i][j] = face[j][self.size-1-i]

        return temp
 
    def rotate(self,direction):
        assert direction == 'up' or direction == 'down' or direction == 'left' or direction == 'right', "Wrong direction: {}".format(direction)
        if direction == 'up':
            top = self.state[self.FACE][:]
            left = self.__ccwQuarterTurn(self.state[self.LEFT][:])
            face = self.state[self.BOTTOM][:]
            right = self.__cwQuarterTurn(self.state[self.RIGHT][:])
            bottom = self.state[self.BACK][:]
            bottom = self.__cwQuarterTurn(bottom[:])
            bottom = self.__cwQuarterTurn(bottom[:])
            back = self.state[self.TOP][:]
            back = self.__cwQuarterTurn(back[:])
            back = self.__cwQuarterTurn(back[:])

        elif direction == 'down':
            top = self.state[self.BACK][:]
            top = self.__cwQuarterTurn(top[:])
            top = self.__cwQuarterTurn(top[:])
            left = self.__cwQuarterTurn(self.state[self.LEFT][:])
            face = self.state[self.TOP][:]
            right = self.__ccwQuarterTurn(self.state[self.RIGHT][:])
            bottom = self.state[self.FACE][:]
            back = self.state[self.BOTTOM][:]
            back = self.__cwQuarterTurn(back[:])
            back = self.__cwQuarterTurn(back[:])
             
        elif direction == 'left':
            top = self.__cwQuarterTurn(self.state[self.TOP][:])
            left = self.state[self.FACE][:]
            face = self.state[self.RIGHT][:]
            right = self.state[self.BACK][:]
            bottom = self.__ccwQuarterTurn(self.state[self.BOTTOM][:])
            back = self.state[self.LEFT][:]

        elif direction == 'right':
            top = self.__ccwQuarterTurn(self.state[self.TOP][:])
            left = self.state[self.BACK][:]
            face = self.state[self.LEFT][:]
            right = self.state[self.FACE][:]
            bottom = self.__cwQuarterTurn(self.state[self.BOTTOM][:])
            back = self.state[self.RIGHT][:]

        self.state[self.TOP]  = top
        self.state[self.LEFT]  = left
        self.state[self.FACE]  = face
        self.state[self.RIGHT]  = right
        self.state[self.BOTTOM]  = bottom
        self.state[self.BACK]  = back

    def move(self, direction, rowcolumn):
        assert direction == 'up' or direction == 'down' or direction == 'left' or direction == 'right', "Wrong direction: {}".format(direction)
        assert rowcolumn >=0 and rowcolumn < self.size, "Invalid row/column number: {}".format(rowcolumn)

        top = deepcopy(self.state[self.TOP])
        left = deepcopy(self.state[self.LEFT])
        face = deepcopy(self.state[self.FACE])
        right = deepcopy(self.state[self.RIGHT])
        bottom = deepcopy(self.state[self.BOTTOM])
        back = deepcopy(self.state[self.BACK])

        if direction == 'up': 
            for i in range(self.size):
                top[i][rowcolumn] = self.state[self.FACE][i][rowcolumn]
                face[i][rowcolumn] = self.state[self.BOTTOM][i][rowcolumn]
                bottom[i][rowcolumn] = self.state[self.BACK][i][rowcolumn]
                bottom = self.__cwQuarterTurn(bottom[:])
                bottom = self.__cwQuarterTurn(bottom[:])
                back[i][rowcolumn] = self.state[self.TOP][i][rowcolumn]
                back = self.__cwQuarterTurn(back[:])
                back = self.__cwQuarterTurn(back[:])

            if rowcolumn == 0:
                left = self.__ccwQuarterTurn(left)

            if rowcolumn == self.size - 1:
                right = self.__cwQuarterTurn(right)

        if direction == 'down':
            for i in range(self.size):
                top[i][rowcolumn] = self.state[self.BACK][i][rowcolumn]
                top = self.__cwQuarterTurn(top[:])
                top = self.__cwQuarterTurn(top[:])
                face[i][rowcolumn] = self.state[self.TOP][i][rowcolumn] 
                bottom[i][rowcolumn] = self.state[self.FACE][i][rowcolumn] 
                back[i][rowcolumn] = self.state[self.BOTTOM][i][rowcolumn]
                back = self.__cwQuarterTurn(back[:])
                back = self.__cwQuarterTurn(back[:])


            if rowcolumn == 0:
                left = self.__cwQuarterTurn(left)

            if rowcolumn == self.size - 1:
                right = self.__ccwQuarterTurn(right)
            
        if direction == 'left':
            left[rowcolumn] = self.state[self.FACE][rowcolumn][:]
            face[rowcolumn] = self.state[self.RIGHT][rowcolumn][:]
            right[rowcolumn] = self.state[self.BACK][rowcolumn][:]
            back[rowcolumn] = self.state[self.LEFT][rowcolumn][:]

            if rowcolumn == 0:
                top = self.__cwQuarterTurn(top)

            if rowcolumn == self.size - 1:
                bottom = self.__ccwQuarterTurn(bottom)

        if direction == 'right':
            left[rowcolumn] = self.state[self.BACK][rowcolumn][:]
            face[rowcolumn] = self.state[self.LEFT][rowcolumn][:]
            right[rowcolumn] = self.state[self.FACE][rowcolumn][:]
            back[rowcolumn] = self.state[self.RIGHT][rowcolumn][:]

            if rowcolumn == 0:
                top = self.__ccwQuarterTurn(top)

            if rowcolumn == self.size - 1:
                bottom = self.__cwQuarterTurn(bottom)

        self.state[self.TOP]  = top
        self.state[self.LEFT]  = left
        self.state[self.FACE]  = face
        self.state[self.RIGHT]  = right
        self.state[self.BOTTOM]  = bottom
        self.state[self.BACK]  = back


    def randomize(self,n):
        actions = self.getActions()
        while n>0:
            i = random.randrange(len(actions))
            if actions[i][0] in ('up','down','left','right'):
                self.move(actions[i][0],actions[i][1])
            else:
                self.rotate(actions[i][1])
            n -= 1

    def getActions(self):
        actions = [ ('up', x) for x in range(self.size) ]
        actions += [ ('down', x) for x in range(self.size) ]
        actions += [ ('left', x) for x in range(self.size) ]
        actions += [ ('right', x) for x in range(self.size) ]
        actions += [ ('rotate','up'), ('rotate','down'), ('rotate','left'),('rotate','right') ]
        return actions


    def __str__(self):
        s = ' '*(self.size+1) + '-' + '-'*self.size + '-' + '\n'
        for i in range(self.size):
            s += ' '*(self.size+1) + '|' + ''.join([str(x) for x in self.state[self.TOP][i]]) + '|\n'

        s += '-' + '-'*(self.size*4+3) + '-\n'
        for i in range(self.size):
            s += '|' + ''.join([str(x) for x in self.state[self.LEFT][i]]) + '|' + ''.join([str(x) for x in self.state[self.FACE][i]]) + '|' + ''.join([str(x) for x in self.state[self.RIGHT][i]]) + '|' + ''.join([str(x) for x in self.state[self.BACK][i]]) + '|\n'
        
        s += '-' + '-'*(self.size*4+3) + '-\n'
        for i in range(self.size):
            s += ' '*(self.size+1) + '|' + ''.join([str(x) for x in self.state[self.BOTTOM][i]]) + '|\n'
       
        s += ' '*(self.size+1) + '-' + '-'*self.size + '-' + '\n'

        return s


