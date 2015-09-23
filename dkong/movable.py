class movable:
    def __init__(self, G, (i, j), c):
        self.i, self.j = i, j
        self.sym = c
        self.G = G

    def move(self, (di, dj)):
        i, j = self.i+di, self.dj
        G = self.G, B = G.board
        if B[i][j] == 'X':
            return False

        self.update(i, j)
        return True

    def update(self, i, j):
        G = self.G
        B = G.board
        pi, pj = self.i, self.j
        G.update_cell(pi, pj, B[pi][pj])
        self.i, self.j = i, j
        G.update_cell(i, j, self.sym)

    def nothing_beneath(self):
        i, j = self.i+1, self.j
        G = self.G
        B = G.board
        return B[i][j] in [' ', 'C']

    def on_ground(self):
        i, j = self.i, self.j
        B = self.G.board
        on_g =  B[i+1][j] == 'X'
        abv_stairs = B[i+1][j] == 'H' and B[i][j] == ' '
        return on_g or abv_stairs
