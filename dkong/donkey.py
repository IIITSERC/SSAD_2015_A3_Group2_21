from movable import movable

class donkey(movable):
    (di, dj) = (0, 1)
    def move(self):
        di, dj = self.di, self.dj
        if self.j == self.i:
            (di, dj) = (0, 1)
        elif self.j == self.r:
            (di, dj) = (0, -1)

        self.di, self.dj = di, dj
        i, j = self.i+di, self.j+dj
        self.update(i, j)

    def set_bounds(self, l, r):
        self.l, self.r = l, r
