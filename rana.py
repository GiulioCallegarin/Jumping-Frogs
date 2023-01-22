import pygame

BLACK = (0, 0, 0)


class Rana(object):
    counter = 0  # Numero di Rane create
    size = 0  # Dimensioni a schermo
    borderSize = 3  # Usato per centrare l'immagine
    moving = False  # Blocco, non si può spostare un'altra rana durante il movimento
    speed = 5
    offset = 0  # Per centrare allo schermo
    rows = 0
    sowSize = 0
    maxRowSize = 9
    centralSup = 0
    # Lista di posizioni (per la griglia e per controllare l'allineamento)
    gridList = []

    def __init__(self, color, empty=False):
        self.id = Rana.counter
        Rana.counter += 1
        self.color = color  # Tipo 0 verso sinistra, 1 verso destra
        self.selected = False  # In movimento
        self.empty = empty  # Rana vuota, solo per comodità
        self.pos = []

        if color == 0:  # Si muove verso sinistra
            self.image = pygame.image.load("files\green_frog.png")
        else:  # Si muove verso destra
            self.image = pygame.image.load("files\purple_frog.png")

    def draw(self, screen):  # Disegna sullo schermo
        if not self.empty:
            add = 0
            if Rana.centralSup != 0:
                add = 1

            # Se ci sono più righe e si deve spostare da una all'altra (verso sinistra)
            if self.pos[0] < Rana.offset:
                # print(f"1 --> {self.id}, {self.pos}")
                screen.blit(
                    self.image, (self.pos[0] + Rana.borderSize, self.pos[1] - Rana.borderSize))
                screen.blit(
                    self.image, (Rana.size * (Rana.rowSize + add) + self.pos[0] + Rana.borderSize, self.pos[1] - Rana.size - Rana.borderSize))

            # Se ci sono più righe e si deve spostare da una all'altra (verso destra)
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

    def update(self):  # Aggiorna la posizione delle rane selezionate
        if self.selected and not self.empty:
            if self.color == 1:  # Verso sinistra
                self.pos[0] += Rana.speed

                # Raggiunta la nuova posizione
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
            else:  # Verso destra
                self.pos[0] -= Rana.speed

                # Raggiunta la nuova posizione
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
    # Inizializza tutti i valori statici in base alle dimensioni dello schermo ed il numero di rane
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

    def smooth(self):  # Ridimensiona l'immagine alle nuove dimensioni
        self.image = pygame.transform.smoothscale(
            self.image, (Rana.size - 2 * Rana.borderSize, Rana.size + 2 * Rana.borderSize))
