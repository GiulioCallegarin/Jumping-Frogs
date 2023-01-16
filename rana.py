import pygame

BLACK = (0, 0, 0)


class Rana(object):
    classID = 0
    size = 10
    borderSize = 3
    moving = False
    speed = 5
    offset = 0

    def __init__(self, color, pos, empty=False):
        self.id = Rana.classID
        Rana.classID += 1
        self.color = color
        self.selected = False
        self.pos = [pos[0], pos[1]]
        self.empty = empty

        if color == 0:
            self.image = pygame.image.load("files\green_frog.png")
        else:
            self.image = pygame.image.load("files\purple_frog.png")

        self.image = pygame.transform.smoothscale(
            self.image, (Rana.size - 2 * Rana.borderSize, Rana.size + 2 * Rana.borderSize))

    def draw(self, screen):
        if not self.empty:
            global size
            screen.blit(
                self.image, (self.pos[0] + Rana.borderSize + self.offset, self.pos[1] - Rana.borderSize))

    def update(self):
        if self.selected and not self.empty:
            if self.color == 1:
                self.pos[0] += Rana.speed
                if self.pos[0] >= Rana.size * self.id + self.offset:
                    Rana.moving = False
                    self.selected = False
            else:
                self.pos[0] -= Rana.speed
                if self.pos[0] <= Rana.size * self.id + self.offset:
                    Rana.moving = False
                    self.selected = False
