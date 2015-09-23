from movable import movable
from random import *

class fireball(movable):
    downstairs = False
    def move(self):
        sh = self.G.space_h
        d = lambda x : 2*(x%(2*sh)==sh-1)-1
        B = self.G.board
        pi, pj = self.i, self.j
        if self.on_ground() and B[pi+1][pj]=='X':
            i, j = pi, pj+d(pi)
        elif self.nothing_beneath() or B[pi][pj]=='H':
            i, j = pi+1, pj
        else:
            i, j = pi+1, pj
            if randint(0, 2):
                i, j = pi, pj+d(pi)
        if B[i][j] == 'X':
            return False
        self.update(i, j)
        return True
