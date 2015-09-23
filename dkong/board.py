import pygame
from symbols import *
from random import *
from player import *
from donkey import *
from fireball import *

class board:
    """Game stats, graphics"""
    level = 1
    def __init__(self, M, N):
        self.N = N
        self.M = M

        #Pygame settings
        pygame.init()
        (self.cw, self.ch) = (30, 30)
        self.space_h = 5
        self.scr = pygame.display.set_mode((self.cw*(N), self.ch*(M+1)))
        self.clock = pygame.time.Clock()
        self.P = player(self, (self.M-1, 1), 'P')
        self.set_game()
        self.status = "New Game. Press C to start"
        self.listen()

    def set_game(self):
        self.board = [[' ' for i in range(self.N)] 
                        for j in range(self.M)]

        self.scr.fill(RGB_WHITE)
        self.generate_maze()
        self.draw_board()

        self.D = donkey(self, (self.space_h-1, 1), 'D')
        self.P.i, self.P.j = self.M-2, 1
        #Place player
        self.update_cell(self.M-2, 1, 'P')

        #Place donkey
        self.D.set_bounds(1, self.opening+3)
        self.update_cell(self.space_h-1, 4, 'D')

        self.update_lives(3)
        self.update_score(self.P.score)
        #Start Listening


    def check_collision_pair(self, a, b):
        return a.i == b.i and a.j == b.j

    def checkCollision(self, P, D, FB):
        dead = False
        for fb in FB:
            if self.check_collision_pair(P, fb):
                dead = P.kill()
                FB.remove(fb)
        if self.check_collision_pair(P, D):
            dead = P.kill()
        return dead


    def listen(self):
        game_over = False
        dead = False
        P = self.P
        FB = []
        jump = 0
        self.pause_status = False

        while not game_over:
            D = self.D
            for evt in pygame.event.get():
                if evt.type == pygame.QUIT:
                    game_over = True
            if not self.pause_status:
                if len(FB) < 3 and D.j == self.opening and (D.di, D.dj)==(0, 1):
                    FB.append(fireball(self, (D.i, D.j+1), 'F'))

                for fb in FB:
                    #ToDo, slow down this rate(?)
                    mv = fb.move()
                    if not mv:
                        self.update_cell(fb.i, fb.j, ' ')
                        FB.remove(fb)

                D.move()
                pygame.display.update()
                dead = dead or self.checkCollision(P, D, FB)
                jump = P.tryJump(jump)

                if P.nothing_beneath() and not P.jumping:
                    P.move(move_d[pygame.K_DOWN])

                dead = dead or self.checkCollision(P, D, FB)

            if evt.type == pygame.KEYDOWN:
                if self.pause_status == True:
                    if evt.key == pygame.K_c:
                        self.pause_status = False
                        self.update_status(" ")
                else:
                    try:
                        P.move(move_d[evt.key])
                    except(KeyError): 
                        if evt.key == pygame.K_SPACE and P.on_ground():
                            P.jumping = True
                            jump = P.jump_h
                        elif evt.key == pygame.K_ESCAPE:
                            self.pause_status = True
                            self.update_status("Game Paused. Press C to continue")


            if self.board[P.i][P.j] == 'Q':
                P.score += 50
                self.set_game()
                FB = []
                self.level += 1

            if dead:
                P.score = 0
                P.lives = 3
                self.set_game()
                self.update_status("New Game. Press C to start")
                self.update_score(P.score)
                self.update_lives(P.lives)
                dead = False
                self.pause_status = True


            pygame.display.update()
            self.clock.tick(20+self.level)
                

    def debug_board(self):
        for row in self.board:
            print ''.join(row)

    def set_pieces(self):
        # M rows, Levels of height 3 cells each.
        # (empty_cells, walls) = (3k, k+1)
        # 4k = M - 1, k = (M-1)/4
        # Assert M-1 has to be a multiple of 4
        k = (self.M-1)/self.space_h

        # Create rectangular boxes for each levels
        for i in range(k+1):
            for j in range(self.N):
                self.board[(self.space_h*i)][j] = 'X';

        for i in range(self.M):
            self.board[i][0] = 'X'
            self.board[i][self.N-1] = 'X'


        # Princess.
        self.board[1][8] = 'X'
        self.board[1][8+20-1] = 'X'
        self.board[1][8+1] = 'Q'
        for i in range(2,3):
            for j in range(8, 8+20):
                self.board[i][j] = 'X'
        self.opening = randint(8+15, 8+20-2);
        for i in range(2, self.space_h):
            self.board[i][self.opening] = 'H'


    def break_walls(self):
        k = (self.M-1)/self.space_h;
        # (left, right) = (0, 1)
        # for walls to be aligned properly, 
        # assert k = odd.
        break_at = 1
        for i in range(1, k):
            j = break_at*(self.N-3)+1
            for breaks in range(2):
                self.board[self.space_h*i][j] = ' '
                j = j - (2*break_at - 1)
            break_at = not break_at

    def add_stairs(self):
        # For each pair of horizontal adjacent walls
        # Pick random(1, 2) stairs
        # Break random(0, 1) stairs
        # Assert stairs don't start/end at empty cells
        # Easy, only choose cells [3, N-4)
        k = (self.M-1)/self.space_h;
        for s_ in range(k-1):
            s = self.M - 1 - self.space_h*s_
            stairs = randint(1, 2)
            broken_stairs = randint(0, 1)

            #ToDo: improve stair algorithm
            for stair in range(stairs):
                j = randint(4, self.N-5)
                #Construct stairs up
                for i_ in range(1,self.space_h+1):
                    i = s - i_
                    self.board[i][j] = 'H'

            #ToDo: Break a few stairs
    def place_coins(self):
        count = 16
        while count:
            i, j = randint(1, self.M-2), randint(1, self.N-1)
            if self.board[i][j] not in ['X', 'H', 'Q', 'P'] \
                    and (i, j) is not (self.M-1, 1):
                self.board[i][j] = 'C'
                count = count - 1
        return

    def generate_maze(self):
        self.set_pieces()
        self.break_walls()
        self.add_stairs()
        self.place_coins()
        
    def update_cell(self, i, j, text):
        P = (self.cw/2*(2*j+1), self.ch/2*(2*i+1))
        self.print_rect(text, P, RGB_BLACK, RGB_WHITE)

    def print_rect(self, text, c, fg, bg):
        scr = self.scr 
        font = pygame.font.Font("Monaco.ttf", 24)
        fo = font.render(text, True, fg, bg)
        frect = fo.get_rect()
        frect.center = c
        scr.blit(fo, frect)

    def draw_board(self):
        """Function redraws the board"""
        for i in range(self.M):
            for j in range(self.N):
                text = self.board[i][j]
                P = (self.cw/2*(2*j+1), self.ch/2*(2*i+1))
                self.print_rect(text, P, RGB_BLACK, RGB_WHITE)
        
        pygame.display.update()

    def update_score(self, s):
        text = "Score: "+str(s)
        i, j = self.M, self.N-5
        P = (self.cw/2*(2*j+1), self.ch/2*(2*i+1))
        self.print_rect(text, P, RGB_BLACK, RGB_WHITE)
        pygame.display.update()
    
    def update_status(self, status):
        t = len(self.status)
        self.status = status
        i, j = self.M, self.N - 20
        P = (self.cw/2*(2*j+1), self.ch/2*(2*i+1))
        self.print_rect(" "*t, P, RGB_BLACK, RGB_WHITE)
        self.print_rect(status, P, RGB_BLACK, RGB_WHITE)
        pygame.display.update()

    def update_lives(self, lives):
        i, j = self.M, 2
        P = (self.cw/2*(2*j+1), self.ch/2*(2*i+1))
        self.print_rect("Lives: "+str(lives), P, RGB_BLACK, RGB_WHITE)
        pygame.display.update()
