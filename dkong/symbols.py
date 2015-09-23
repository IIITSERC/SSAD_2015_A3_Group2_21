import pygame

RGB_WHITE = (255, 255, 255)
RGB_BLACK = (0, 0, 0)
move_d = {
        pygame.K_UP : (-1, 0),
        pygame.K_w : (-1, 0),
        pygame.K_DOWN: (1, 0),
        pygame.K_s: (1, 0),
        pygame.K_RIGHT: (0, 1),
        pygame.K_d: (0, 1),
        pygame.K_LEFT: (0, -1)
}
