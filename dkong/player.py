from movable import movable
from symbols import move_d
import pygame

class player(movable):
    score = 0
    lives = 3
    in_air = False
    jumping = False
    jump_h = 3
    
    def kill(self):
        if self.lives <= 0:
            return True
        self.lives -= 1
        i, j = self.G.M-2, 1
        self.update(i, j)
        self.G.update_lives(self.lives)
        self.G.pause_status = True
        self.G.update_status("Lost life. Press C to continue")
        return False
    
    def collect_coins(self, i, j):
        self.G.board[i][j] = ' '
        self.score += 5
        self.G.update_score(self.score)


    def move(self, (di, dj)):
        G = self.G
        B = G.board
        pi, pj = self.i, self.j
        i, j = self.i + di, self.j + dj

        if B[i][j] == 'X':
            return False

        # Players moves
        # right, valid, left, valid, if not x or h beneath, free fall
        # up, valid if on stair, down valid if on stair, or above stair
        direction = (di, dj)
        up = (-1, 0)
        down = (1, 0)
        right = (0, 1)
        left = (0, -1)

        if B[i][j] == 'C':
            self.collect_coins(i, j)

        if direction == up:
            if (B[pi][pj] == 'H'):
                self.update(i, j)
            elif self.jumping:
                self.update(i, j)

        elif direction == left or direction == right:
            self.update(i, j)

        elif direction == down and B[pi+1][pj] in ['H', ' ']:
            self.update(i, j)

        else:
            return False

        return True

    def tryJump(self, jump):
        P = self
        if  P.jumping:
            if jump > 0:
                jump = jump - 1
                P.move(move_d[pygame.K_UP])
            elif jump>-self.jump_h:
                jump = jump - 1
                P.move(move_d[pygame.K_DOWN])
            elif jump==-self.jump_h:
                P.jumping = False
                jump = 0
        return jump


