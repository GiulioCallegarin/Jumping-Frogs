import pygame
from rana import Rana

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 800

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
display = pygame.display.set_caption("RANE BUFFE")
clock = pygame.time.Clock()

FROG_NUMBER = 4
Rana.size = SCREEN_WIDTH // (FROG_NUMBER * 2 + 1)
yPos = SCREEN_HEIGHT / 2 - Rana.size / 2
offset = (SCREEN_WIDTH - Rana.size * (FROG_NUMBER * 2 + 1)) // 2
Rana.offset = offset
frogList = []


def init():
    for i in range(FROG_NUMBER * 2 + 1):
        if i == FROG_NUMBER:
            frogList.append(Rana(-1, [Rana.size * i, yPos], True))
        elif i < FROG_NUMBER:
            frogList.append(Rana(1, [Rana.size * i, yPos]))
        else:
            frogList.append(Rana(0, [Rana.size * i, yPos]))


def swap(idxA, idxB):
    frogList[idxA], frogList[idxB] = frogList[idxB], frogList[idxA]
    frogList[idxA].id, frogList[idxB].id = frogList[idxB].id, frogList[idxA].id


def draw():
    for i in range(FROG_NUMBER * 2 + 1):
        pygame.draw.rect(
            screen, BLACK, (Rana.size * i + offset, yPos, Rana.size, Rana.size), Rana.borderSize)
        frogList[i].draw(screen)


def overlap():
    if pygame.mouse.get_pos()[1] > yPos and pygame.mouse.get_pos()[1] < yPos + Rana.size:
        for i in range(FROG_NUMBER * 2 + 1):
            if pygame.mouse.get_pos()[0] > Rana.size * i + offset and pygame.mouse.get_pos()[0] < Rana.size * i + Rana.size + offset:
                return i
    return -1


def update():
    for i in range(FROG_NUMBER * 2 + 1):
        frogList[i].update()


def handle(event: pygame.event.Event):
    if event.type == pygame.QUIT:
        pygame.quit()
    elif event.type == pygame.MOUSEBUTTONDOWN and not Rana.moving:
        if event.button == 1:
            idx = overlap()
            try:
                if frogList[idx].color == 1 and (frogList[idx + 1].empty or (frogList[idx + 1].color == 0 and frogList[idx + 2].empty)):
                    print(idx)
                    Rana.moving = True
                    frogList[idx].selected = True
                    if frogList[idx + 1].empty:
                        swap(idx, idx + 1)
                    else:
                        swap(idx, idx + 2)
                elif frogList[idx].color == 0 and (frogList[idx - 1].empty or (frogList[idx - 1].color == 1 and frogList[idx - 2].empty)):
                    print(idx)
                    Rana.moving = True
                    frogList[idx].selected = True
                    if frogList[idx - 1].empty:
                        swap(idx, idx - 1)
                    else:
                        swap(idx, idx - 2)
            except:
                print("Out of bound")


init()
while True:
    for event in pygame.event.get():
        handle(event)

    screen.fill(WHITE)
    update()
    draw()
    pygame.display.update()
    clock.tick(60)
