import  pygame as pg
from pygame.locals import *

from cell import Cell

pg.init()
WIDTH = 800
HEIGHT = 800
FPS = 60
smallfont = pg.font.Font("./fonts/Montserrat-Regular.ttf", 35)
smallfont2 = pg.font.Font("./fonts/Montserrat-Regular.ttf", 20)

SCREEN = pg.display.set_mode((WIDTH, HEIGHT), vsync=1)
something_clicked = False
listCells = []
listCellsAddresses = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (3, 0), (3, 1), (3, 2), (3, 4), (3, 5), (3, 6), (3, 7), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 6), (4, 7), (4, 8), (5, 0), (5, 1), (5, 2), (5, 4), (5, 5), (5, 6), (5, 7), (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (8, 0), (8, 1), (8, 2), (8, 3), (8, 4)]
listRedCells = {(3,0),(4,0),(5,0)}
listGreenCells = {(1,0),(2,0),(3,1),(4,1),(4,2),(5,1),(6,0),(7,0),(5,2),(6,1),(3,2),(2,1)}
# listGreenCells = [(0,0),(4,8),(8,0)]
# listRedCells = [(0,4),(4,0),(8,4)]
listNearestCells = set()
listFarCells = set()
clickedCell = ()
redMoveCount = 0
greenMoveCount = 0
redMove = True
win = False

def initialize():
    global something_clicked, listCells, listCellsAddresses, listGreenCells, listRedCells, listNearestCells,listFarCells, clickedCell, redMove, win, redMoveCount, greenMoveCount
    something_clicked = False
    listCells = []
    listCellsAddresses = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
                          (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (3, 0), (3, 1), (3, 2), (3, 4),
                          (3, 5), (3, 6), (3, 7), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 6), (4, 7), (4, 8),
                          (5, 0), (5, 1), (5, 2), (5, 4), (5, 5), (5, 6), (5, 7), (6, 0), (6, 1), (6, 2), (6, 3),
                          (6, 4), (6, 5), (6, 6), (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (8, 0), (8, 1),
                          (8, 2), (8, 3), (8, 4)]
    # listGreenCells = [(0, 0), (4, 8), (8, 0)]
    # listRedCells = [(0, 4), (4, 0), (8, 4)]
    listRedCells = {(3, 0), (4, 0), (5, 0)}
    listGreenCells = {(1,0),(2,0),(3,1),(4,1),(4,2),(5,1),(6,0),(7,0),(5,2),(6,1),(3,2),(2,1)}
    listNearestCells = set()
    listFarCells = set()
    clickedCell = ()
    redMove = True
    win = False
    redMoveCount = 0
    greenMoveCount = 0

def f(i):
    if i < 5:
        return i + 5
    else:
        return 13 - i


def checkRedCell(i,j):
    if (i,j) in listCellsAddresses and not (i,j) in listGreenCells|listRedCells:
        listNearestCells.add((i,j))

def showNearCells(cell: Cell):
    global listNearestCells
    i,j = cell.address[:]
    checkRedCell(i+1,j)
    checkRedCell(i,j+1)
    checkRedCell(i, j - 1)

    if i>=4:
        checkRedCell(i+1,j-1)
    elif i<4:
        checkRedCell(i + 1, j+1)

    if i<=4:
        checkRedCell(i -1 , j - 1)
    else:
        checkRedCell(i-1, j+1)

    checkRedCell(i - 1, j)

def checkFarCells(i,j):
    if (i,j) in listCellsAddresses and (i,j) not in listRedCells|listGreenCells|listNearestCells:
        listFarCells.add((i,j))

def showFarCells(cell: Cell):
    global listFarCells
    i, j = cell.address[:]
    if i<4:
        if i==3:
            checkFarCells(i + 2, j-1)
            checkFarCells(i + 2, j)
            checkFarCells(i + 2, j + 1)
        else:
            checkFarCells(i+2,j)
            checkFarCells(i + 2, j+1)
            checkFarCells(i + 2, j+2)
    else:
        checkFarCells(i + 2, j-2)
        checkFarCells(i + 2, j-1)
        checkFarCells(i + 2, j)

    if i>4:
        if i==5:
            checkFarCells(i - 2, j-1)
            checkFarCells(i - 2, j)

            checkFarCells(i - 2, j+1)
        else:
            checkFarCells(i-2,j)
            checkFarCells(i - 2, j+1)
            checkFarCells(i - 2, j+2)
    else:
        checkFarCells(i - 2, j-2)
        checkFarCells(i - 2, j - 1)
        checkFarCells(i - 2, j)

    checkFarCells(i, j+2)
    checkFarCells(i, j-2)

    if i>=4:
        checkFarCells(i + 1, j+1)
        checkFarCells(i + 1, j-2)
    else:
        checkFarCells(i + 1, j + 2)
        checkFarCells(i + 1, j - 1)

    if i<=4:
        checkFarCells(i - 1, j + 1)
        checkFarCells(i - 1, j - 2)
    else:
        checkFarCells(i - 1, j + 2)
        checkFarCells(i - 1, j - 1)

def checkNearCellsForAnotherChips(cell: Cell):
    i, j = cell.address[:]
    if redMove:
        if (i+1,j) in listGreenCells:
            listGreenCells.remove((i+1,j))
            listRedCells.append((i+1,j))
        if (i,j+1) in listGreenCells:
            listGreenCells.remove((i, j+1))
            listRedCells.append((i, j+1))
        if (i,j-1) in listGreenCells:
            listGreenCells.remove((i, j-1))
            listRedCells.append((i, j-1))
        if i >= 4:
            if (i + 1, j - 1) in listGreenCells:
                listGreenCells.remove((i + 1, j-1))
                listRedCells.append((i + 1, j-1))
        elif i < 4:
            if (i + 1, j + 1) in listGreenCells:
                listGreenCells.remove((i + 1, j+1))
                listRedCells.append((i + 1, j+1))
        if i <= 4:
            if (i - 1, j - 1) in listGreenCells:
                listGreenCells.remove((i -1, j-1))
                listRedCells.append((i -1, j-1))
        else:
            if (i - 1, j + 1) in listGreenCells:
                listGreenCells.remove((i -1, j+1))
                listRedCells.append((i - 1, j+1))

        if (i - 1, j) in listGreenCells:
            listGreenCells.remove((i -1, j))
            listRedCells.append((i - 1, j))
    else:
        if (i+1,j) in listRedCells:
            listRedCells.remove((i+1,j))
            listGreenCells.append((i+1,j))
        if (i,j+1) in listRedCells:
            listRedCells.remove((i, j+1))
            listGreenCells.append((i, j+1))
        if (i,j-1) in listRedCells:
            listRedCells.remove((i, j-1))
            listGreenCells.append((i, j-1))
        if i >= 4:
            if (i + 1, j - 1) in listRedCells:
                listRedCells.remove((i + 1, j-1))
                listGreenCells.append((i + 1, j-1))
        elif i < 4:
            if (i + 1, j + 1) in listRedCells:
                listRedCells.remove((i + 1, j+1))
                listGreenCells.append((i + 1, j+1))
        if i <= 4:
            if (i - 1, j - 1) in listRedCells:
                listRedCells.remove((i -1, j-1))
                listGreenCells.append((i -1, j-1))
        else:
            if (i - 1, j + 1) in listRedCells:
                listRedCells.remove((i -1, j+1))
                listGreenCells.append((i - 1, j+1))

        if (i - 1, j) in listRedCells:
            listRedCells.remove((i -1, j))
            listGreenCells.append((i - 1, j))

#Мне самому страшно, что я написал, но оно работает...
def checkCellForMove(cell: Cell):
    i, j = cell.address[:]
    t = 0
    if i<4:
        if i==3:
            if (i+2,j-1) in listCellsAddresses and (i+2,j-1) not in listRedCells|listGreenCells: t+=1
            if (i+2,j)in listCellsAddresses and (i+2,j) not in listRedCells | listGreenCells: t += 1
            if (i+2,j+1) in listCellsAddresses and (i+2,j+1) not in listRedCells | listGreenCells: t += 1
            # t+=len({(i+2,j-1),(i+2,j),(i+2,j+1)} & (listRedCells|listGreenCells))
        else:
            if (i+2,j) in listCellsAddresses and (i+2,j) not in listRedCells | listGreenCells: t += 1
            if (i+2,j+1) in listCellsAddresses and (i+2,j+1) not in listRedCells | listGreenCells: t += 1
            if (i+2,j+2) in listCellsAddresses and (i+2,j+2) not in listRedCells | listGreenCells: t += 1
            # t+=len({(i+2,j),(i+2,j+1),(i+2,j+2)} & (listRedCells|listGreenCells))
    else:
        if (i+2,j-2) in listCellsAddresses and (i+2,j-2) not in listRedCells | listGreenCells: t += 1
        if (i+2,j-1) in listCellsAddresses and (i+2,j-1) not in listRedCells | listGreenCells: t += 1
        if (i+2,j) in listCellsAddresses and (i+2,j) not in listRedCells | listGreenCells: t += 1
        # t+= len({(i+2,j-2),(i+2,j-1),(i+2,j)} & (listRedCells|listGreenCells))
    if i>4:
        if i==5:
            if (i-2,j-1) in listCellsAddresses and (i-2,j-1) not in listRedCells | listGreenCells: t += 1
            if (i-2,j) in listCellsAddresses and (i-2,j) not in listRedCells | listGreenCells: t += 1
            if (i-2,j+1) in listCellsAddresses and (i-2,j+1) not in listRedCells | listGreenCells: t += 1
            # t+=len({(i-2,j-1),(i-2,j),(i-2,j+1)} & (listRedCells|listGreenCells))
        else:
            if (i-2,j) in listCellsAddresses and (i-2,j) not in listRedCells | listGreenCells: t += 1
            if (i-2,j+1) in listCellsAddresses and (i-2,j+1) not in listRedCells | listGreenCells: t += 1
            if (i-2,j+2) in listCellsAddresses and (i-2,j+2) not in listRedCells | listGreenCells: t += 1
            # t+=len({(i-2,j),(i-2,j+1),(i-2,j+2)} & (listRedCells|listGreenCells))
    else:
        if (i-2,j) in listCellsAddresses and (i-2,j) not in listRedCells | listGreenCells: t += 1
        if (i-2,j-1) in listCellsAddresses and (i-2,j-1) not in listRedCells | listGreenCells: t += 1
        if (i-2,j-2) in listCellsAddresses and (i-2,j-2) not in listRedCells | listGreenCells: t += 1
        # t+=len({(i-2,j),(i-2,j+1),(i-2,j+2)} & (listGreenCells|listRedCells))
    if (i,j+2) in listCellsAddresses and (i,j+2) not in listRedCells | listGreenCells: t += 1
    if (i,j-2) in listCellsAddresses and (i,j-2) not in listRedCells | listGreenCells: t += 1
    # t+= len({(i,j+2),(i,j-2)} & (listRedCells|listGreenCells))

    if i>=4:
        if (i+1,j+1) in listCellsAddresses and (i+1,j+1) not in listRedCells | listGreenCells: t += 1
        if (i+1,j-2) in listCellsAddresses and (i+1,j-2) not in listRedCells | listGreenCells: t += 1
        # t+= len({(i+1,j+1),(i+1,j-2)} & (listGreenCells|listRedCells))
    else:
        if (i+1,j+2) in listCellsAddresses and (i+1,j+2) not in listRedCells | listGreenCells: t += 1
        if (i+1,j-1) in listCellsAddresses and (i+1,j-1) not in listRedCells | listGreenCells: t += 1
        # t+=len({(i+1,j+2), (i+1,j-1)} & (listGreenCells|listRedCells))
    if i<=4:
        if (i-1,j+1) in listCellsAddresses and (i-1,j+1) not in listRedCells | listGreenCells: t += 1
        if (i-1,j-2) in listCellsAddresses and (i-1,j-2) not in listRedCells | listGreenCells: t += 1
        # t+= len({(i-1,j+1),(i-1,j-2)} & (listGreenCells|listRedCells))
    else:
        if (i-1,j+2) in listCellsAddresses and (i-1,j+2) not in listRedCells | listGreenCells: t += 1
        if (i-1,j-1) in listCellsAddresses and (i-1,j-1) not in listRedCells | listGreenCells: t += 1
        # t+=len({(i-1,j+2),(i-1,j-1)} & (listGreenCells|listRedCells))
    return t

def displayhexagon():
    global listCells, greenMoveCount, redMoveCount
    listCells = []
    for i in range(9):
        x = i * 60 + 100
        for j in range(f(i)):
            y = 30 * j + abs(i - 4) * 15
            cell = Cell()
            cell.address = (i, j)
            green_f = pg.image.load("green_f.png")
            red_f = pg.image.load("red_f.png")
            nearestCell = pg.image.load("nearestCell.png")
            farCell = pg.image.load("farCell.png")
            if (i,j) in listGreenCells:
                SCREEN.blit(green_f,(x+10*i+20, HEIGHT / 2 - y-10*j+10))
                greenMoveCount+=checkCellForMove(cell)
            if (i, j) in listRedCells:
                SCREEN.blit(red_f, (x + 10 * i + 13, HEIGHT / 2 - y - 10 * j + 7))
                redMoveCount+=checkCellForMove(cell)
            if (i, j) in listNearestCells: SCREEN.blit(nearestCell, (x+10*i, HEIGHT / 2 - y-10*j))
            if (i, j) in listFarCells: SCREEN.blit(farCell, (x + 10 * i, HEIGHT / 2 - y - 10 * j))
            if (i,j) in listCellsAddresses: SCREEN.blit(cell.pic, (x + 10 * i, HEIGHT / 2 - y - 10 * j))
            cell.x = x+10*i
            cell.y = HEIGHT / 2 - y - 10*j
            listCells.append(cell)
            cell.on_click_listener()
            print(f'Red: {redMoveCount}')
            print(f'Green: {greenMoveCount}')

def start():
    global something_clicked
    clock = pg.time.Clock()
    playing = False
    SCREEN.fill((255,255,255))
    while 1:
        for i in pg.event.get():
            if i.type == pg.QUIT:
                return
            if i.type == MOUSEBUTTONDOWN:
                if not playing:
                    if WIDTH / 2 - 70 <= mouse[0] <= WIDTH / 2 + 70 and HEIGHT - 200 <= mouse[1] <= HEIGHT - 160:
                        something_clicked = True
                        return
                    if WIDTH / 2 - 90 <= mouse[0] <= WIDTH / 2 + 90 and HEIGHT - 360 <= mouse[1] <= HEIGHT - 280:
                        something_clicked = True
                        playing = True
                        SCREEN.fill((255, 255, 255))
                        initialize()
                        displayhexagon()
                else:
                    if WIDTH - 190 <= mouse[0] <= WIDTH - 10 and 20 <= mouse[1] <= 100:
                        something_clicked = True
                        playing = False
                        SCREEN.fill((255, 255, 255))
        mouse = pg.mouse.get_pos()
        if not playing:
            header = smallfont.render('Hexagon', True, (0, 0, 0))
            SCREEN.blit(header, (WIDTH / 2 - header.get_width() / 2, 200))
            if WIDTH / 2 - 70 <= mouse[0] <= WIDTH / 2 + 70 and HEIGHT - 200 <= mouse[1] <= HEIGHT - 160:
                pg.draw.rect(SCREEN, (0, 0, 255), [WIDTH / 2 - 70, WIDTH - 200, 140, 40])
            else:
                pg.draw.rect(SCREEN, (255, 255, 0), [WIDTH / 2 - 70, HEIGHT - 200, 140, 40])
            if WIDTH / 2 - 90 <= mouse[0] <= WIDTH / 2 + 90 and HEIGHT - 360 <= mouse[1] <= HEIGHT - 280:
                pg.draw.rect(SCREEN, (0, 0, 255), [WIDTH / 2 - 90, HEIGHT - 360, 180, 80])
            else:
                pg.draw.rect(SCREEN, (255, 255, 0), [WIDTH / 2 - 90, HEIGHT - 360, 180, 80])
            quit_text = smallfont.render('Quit', True, (0, 0, 0))
            SCREEN.blit(quit_text, (WIDTH / 2 - quit_text.get_width() / 2, HEIGHT - 200))
            play_text = smallfont.render('Play', True, (0, 0, 0))
            SCREEN.blit(play_text, (WIDTH / 2 - play_text.get_width() / 2, HEIGHT - 340))
        else:
            for i in listCells:
                i.on_click_listener()
            if len(listRedCells) > len(listGreenCells) and len(listRedCells)+len(listGreenCells)==58 or greenMoveCount==0 or len(listGreenCells)==0:
                winText = smallfont2.render('Red win!', True, (0, 0, 0))
                SCREEN.blit(winText, (WIDTH / 2 - winText.get_width() / 2, 50))
            elif len(listRedCells) == len(listGreenCells) and len(listRedCells)+len(listGreenCells)==58:
                winText = smallfont2.render('Draw!', True, (0, 0, 0))
                SCREEN.blit(winText, (WIDTH / 2 - winText.get_width() / 2, 50))
            elif len(listRedCells) < len(listGreenCells) and len(listRedCells)+len(listGreenCells)==58 or redMoveCount==0 or len(listRedCells)==0:
                winText = smallfont2.render('Green win!', True, (0, 0, 0))
                SCREEN.blit(winText, (WIDTH / 2 - winText.get_width() / 2, 25))
            else:
                winText = smallfont2.render('Playing', True, (0, 0, 0))
                SCREEN.blit(winText, (WIDTH / 2 - winText.get_width() / 2, 50))
                move = smallfont2.render(f'{"Red" if redMove else "Green"} turn', True, (255,0,0) if redMove else (0,255,0))
                SCREEN.blit(move, (WIDTH/2-move.get_width()/2, 30))

            if WIDTH - 190 <= mouse[0] <= WIDTH - 10 and 20 <= mouse[1] <= 100:
                pg.draw.rect(SCREEN, (0, 0, 255), [WIDTH - 190, 20, 180, 80])
            else:
                pg.draw.rect(SCREEN, (255, 255, 0), [WIDTH - 190, 20, 180, 80])
            green_count = smallfont2.render(f'Green: {len(listGreenCells)}', True, (0,0,0))
            SCREEN.blit(green_count, (WIDTH / 2 - winText.get_width() / 2-150, 15))
            red_count = smallfont2.render(f'Red: {len(listRedCells)}', True, (0, 0, 0))

            SCREEN.blit(red_count, (WIDTH / 2 - winText.get_width() / 2-150, 45))
            back_text = smallfont2.render('Main menu', True, (0, 0, 0))
            SCREEN.blit(back_text, (WIDTH - 210 + back_text.get_width() / 2, 45))
            # draw_regular_polygon(screen, (0, 0, 0), 6, 300, (width / 2, height / 2), 1)
            # displayhexagon()
        clock.tick(FPS)
        pg.display.update()