import pygame

BLACK = (0, 0, 0)


class Rana(object):
    counter = 0
    size = 10
    borderSize = 3
    moving = False
    speed = 5
    offset = 0
    rows = 0
    sowSize = 0
    maxRowSize = 9
    centralSup = 0
    gridList = []

    def __init__(self, color, empty=False):
        self.id = Rana.counter
        Rana.counter += 1
        self.color = color
        self.selected = False
        self.empty = empty
        self.pos = []

        if color == 0:
            self.image = pygame.image.load("files\green_frog.png")
        else:
            self.image = pygame.image.load("files\purple_frog.png")

    def draw(self, screen):
        if not self.empty:
            add = 0
            if Rana.centralSup != 0:
                add = 1
            if self.pos[0] < Rana.offset:
                # print(f"1 --> {self.id}, {self.pos}")
                screen.blit(
                    self.image, (self.pos[0] + Rana.borderSize, self.pos[1] - Rana.borderSize))
                screen.blit(
                    self.image, (Rana.size * (Rana.rowSize + add) + self.pos[0] + Rana.borderSize, self.pos[1] - Rana.size - Rana.borderSize))
            elif self.pos[0] > Rana.offset + Rana.size * (Rana.rowSize + add - 1):
                # print(f"2 --> {self.id}, {self.pos}")
                screen.blit(
                    self.image, (self.pos[0] + Rana.borderSize, self.pos[1] - Rana.borderSize))
                screen.blit(
                    self.image, ((self.pos[0] - Rana.size * (Rana.rowSize + add - 1)) - Rana.size + Rana.borderSize, self.pos[1] + Rana.size - Rana.borderSize))
            else:
                # print(f"3 --> {self.id}, {self.pos}")
                screen.blit(
                    self.image, (self.pos[0] + Rana.borderSize, self.pos[1] - Rana.borderSize))

    def update(self):
        if self.selected and not self.empty:
            if self.color == 1:
                self.pos[0] += Rana.speed
                if self.pos[0] >= Rana.gridList[self.id][0] and self.pos[1] >= Rana.gridList[self.id][1]:
                    self.pos = [Rana.gridList[self.id]
                                [0], Rana.gridList[self.id][1]]
                    Rana.moving = False
                    self.selected = False
                add = 0
                if Rana.centralSup != 0:
                    add = 1
                if self.pos[0] >= Rana.size * (Rana.rowSize + add) + Rana.offset:
                    self.pos = [Rana.offset, self.pos[1] + Rana.size]
            else:
                self.pos[0] -= Rana.speed
                if self.pos[0] <= Rana.gridList[self.id][0] and self.pos[1] <= Rana.gridList[self.id][1]:
                    self.pos = [Rana.gridList[self.id]
                                [0], Rana.gridList[self.id][1]]
                    Rana.moving = False
                    self.selected = False
                elif self.pos[0] <= -Rana.size + Rana.offset:
                    add = 0
                    if Rana.centralSup != 0:
                        add = 1
                    self.pos = [self.pos[0] + Rana.size *
                                (Rana.rowSize + add), self.pos[1] - Rana.size]

    @staticmethod
    def initRows(width, height):
        Rana.rows = (Rana.counter // (Rana.maxRowSize + 1)) + 1
        if Rana.rows % 2 == 0:
            Rana.rows += 1
        Rana.rowSize = Rana.counter // Rana.rows
        Rana.centralSup = Rana.counter - Rana.rows * Rana.rowSize
        centralAdd = 0
        if Rana.centralSup != 0:
            centralAdd = 1
        Rana.size = width // (Rana.rowSize + centralAdd)
        if Rana.size * Rana.rows > height:
            Rana.size = height // Rana.rows
        Rana.offset = (width - (Rana.size * (Rana.rowSize + centralAdd))) // 2

    def smooth(self):
        self.image = pygame.transform.smoothscale(
            self.image, (Rana.size - 2 * Rana.borderSize, Rana.size + 2 * Rana.borderSize))
