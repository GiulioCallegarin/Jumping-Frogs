import time
import pygame
from rana import Rana

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
display = pygame.display.set_caption("RANE BUFFE")
clock = pygame.time.Clock()

frogList = []

################################################################# SETTINGS #################################################################
FROG_NUMBER = 11  # OF EACH COLOR (+ 1)
FRAMERATE = 120  # HZ
SPEED = 5  # FROG SPEED
############################################################################################################################################


def smooth():
    for i in range(len(frogList)):
        frogList[i].smooth()


def initPos():
    gridList = []
    Rana.initRows(SCREEN_WIDTH, SCREEN_HEIGHT)
    smooth()
    botShortRows = (Rana.rows - Rana.centralSup) // 2
    topShortRows = (Rana.rows - Rana.centralSup) - botShortRows
    yPos = SCREEN_HEIGHT // 2 - Rana.size // 2 - \
        (Rana.size * (Rana.rows - 1) // 2)
    counter = 0
    add = 0
    if Rana.centralSup != 0:
        add = 1
    print(f"add {add}")
    print(f"Size {len(frogList)}")
    print(f"Counter {Rana.counter}")
    print(f"Rows {Rana.rows}")
    print(f"RowSize {Rana.rowSize}")
    print(f"Central {Rana.centralSup}")
    print(f"top {topShortRows}")
    print(f"bot {botShortRows}")
    print(f"RanaSize {Rana.size}")
    print(f"yPos {yPos}")
    for i in range(topShortRows):
        for j in range(Rana.rowSize):
            frogList[counter].pos = [Rana.offset + Rana.size * (j + add), yPos]
            gridList.append([frogList[counter].pos[0],
                            frogList[counter].pos[1]])
            counter += 1
            print(f"1, Riga {i}, counter {counter-1}")
        yPos += Rana.size
    for i in range(topShortRows, Rana.rows - botShortRows):
        for j in range(Rana.rowSize + add):
            frogList[counter].pos = [Rana.offset + Rana.size * j, yPos]
            gridList.append([frogList[counter].pos[0],
                            frogList[counter].pos[1]])
            counter += 1
            print(f"2, Riga {i}, counter {counter-1}")
        yPos += Rana.size
    for i in range(botShortRows):
        for j in range(Rana.rowSize):
            frogList[counter].pos = [Rana.offset + Rana.size * j, yPos]
            gridList.append([frogList[counter].pos[0],
                            frogList[counter].pos[1]])
            counter += 1
            print(f"3, Riga {i}, counter {counter-1}")
        yPos += Rana.size

    for i in range(len(gridList)):
        print(f"{gridList[i][0]}, {gridList[i][1]}")

    Rana.gridList = gridList


def init():
    Rana.speed = SPEED
    for i in range(FROG_NUMBER * 2 + 1):
        if i == FROG_NUMBER:
            frogList.append(Rana(-1, True))
        elif i < FROG_NUMBER:
            frogList.append(Rana(1))
        else:
            frogList.append(Rana(0))
    initPos()


def swap(idxA, idxB):
    print(f"{frogList[idxA].id}, {frogList[idxB].id}")
    frogList[idxA], frogList[idxB] = frogList[idxB], frogList[idxA]
    frogList[idxA].id, frogList[idxB].id = frogList[idxB].id, frogList[idxA].id


def draw():
    for i in range(len(Rana.gridList)):
        pygame.draw.rect(
            screen, BLACK, (Rana.gridList[i][0], Rana.gridList[i][1], Rana.size, Rana.size), Rana.borderSize)
        # print("draw")
        frogList[i].draw(screen)


def overlap():
    for i in range(len(frogList)):
        if (pygame.mouse.get_pos()[0] > frogList[i].pos[0] and pygame.mouse.get_pos()[0] < frogList[i].pos[0] + Rana.size) and (pygame.mouse.get_pos()[1] > frogList[i].pos[1] and pygame.mouse.get_pos()[1] < frogList[i].pos[1] + Rana.size):
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
                print(f"idx --> {idx}")
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


def moveLeft():
    for i in range(len(frogList)):
        if frogList[len(frogList) - 1 - i].color == 0:
            try:
                if frogList[len(frogList) - 2 - i].empty == True or (frogList[len(frogList) - 2 - i].color == 1 and frogList[len(frogList) - 3 - i].empty == True):
                    print(f"moving Left {len(frogList) - 1 - i}")
                    Rana.moving = True
                    frogList[len(frogList) - 1 - i].selected = True
                    if frogList[len(frogList) - 2 - i].empty:
                        swap(len(frogList) - 1 - i, len(frogList) - 2 - i)
                    else:
                        swap(len(frogList) - 1 - i, len(frogList) - 3 - i)
                    return
            except:
                print("Out of range moveLeft")


def moveRight():
    for i in range(len(frogList)):
        if frogList[i].color == 1:
            try:
                if frogList[i + 1].empty == True or (frogList[i + 1].color == 0 and frogList[i + 2].empty == True):
                    print(f"moving right {i}")
                    Rana.moving = True
                    frogList[i].selected = True
                    if frogList[i + 1].empty:
                        swap(i, i + 1)
                    else:
                        swap(i, i + 2)
                    return
            except:
                print("Out of range moveRight")


def complete(vars):
    global FROG_NUMBER
    left = vars[0]
    reaching = vars[1]
    idx = vars[2]
    ascending = vars[3]
    maxCount = vars[4]
    done = vars[5]

    # print(f"Vars {vars}, frogs {FROG_NUMBER}")

    if maxCount == 0:
        if left:
            moveLeft()
            idx += 1
            if idx >= reaching:
                if ascending:
                    reaching += 1
                    idx = 0
                    left = False
                    if reaching >= FROG_NUMBER:
                        reaching -= 1
                        maxCount = 1
                        ascending = False
                else:
                    reaching -= 1
                    idx = 0
                    left = False
                    if reaching <= 0:
                        done = True
        else:
            moveRight()
            idx += 1
            if idx >= reaching:
                if ascending:
                    reaching += 1
                    idx = 0
                    left = True
                    if reaching >= FROG_NUMBER:
                        reaching -= 1
                        maxCount = 1
                        ascending = False
                else:
                    reaching -= 1
                    idx = 0
                    left = True
                    if reaching <= 0:
                        done = True
    else:
        if left:
            moveLeft()
            idx += 1
            if idx >= FROG_NUMBER:
                idx = 0
                left = False
                maxCount = (maxCount + 1) % 4
        else:
            moveRight()
            idx += 1
            if idx >= FROG_NUMBER:
                idx = 0
                left = True
                maxCount = (maxCount + 1) % 4
    vars[0] = left
    vars[1] = reaching
    vars[2] = idx
    vars[3] = ascending
    vars[4] = maxCount
    vars[5] = done


def fillBorders():
    pygame.draw.rect(screen, WHITE, (0, 0, Rana.offset, SCREEN_HEIGHT))
    add = 0
    if Rana.centralSup != 0:
        add = 1
    startPoint = Rana.offset + Rana.size * (Rana.rowSize + add)
    pygame.draw.rect(screen, WHITE, (startPoint, 0,
                     SCREEN_WIDTH - startPoint, SCREEN_HEIGHT))


def game():
    init()
    left = True
    reaching = 1
    idx = 0
    ascending = True
    maxCount = 0
    done = False
    vars = [left, reaching, idx, ascending, maxCount, done]
    while not vars[5] or Rana.moving:  # done
        for event in pygame.event.get():
            handle(event)
        if not Rana.moving:
            complete(vars)
        screen.fill(WHITE)
        update()
        draw()
        fillBorders()
        pygame.display.update()
        clock.tick(FRAMERATE)
    time.sleep(3)


game()
