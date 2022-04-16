import pygame as pg
from pygame.locals import *
import pygame_menu
import menu_theme

from cell import Cell

pg.init()
WIDTH = 1280
HEIGHT = 720
FPS = 60
smallfont = pg.font.Font("./fonts/Montserrat-Regular.ttf", 35)
smallfont2 = pg.font.Font("./fonts/Montserrat-Regular.ttf", 20)

SCREEN = pg.display.set_mode((WIDTH, HEIGHT), vsync=1)
pg.display.set_caption("Hexagon game")
icon = pg.image.load("red_f.png")
pg.display.set_icon(icon)
something_clicked = False
listCells = []
listCellsAddresses = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 0),
                      (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (3, 0), (3, 1), (3, 2), (3, 4), (3, 5), (3, 6),
                      (3, 7), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 6), (4, 7), (4, 8), (5, 0), (5, 1), (5, 2),
                      (5, 4), (5, 5), (5, 6), (5, 7), (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (7, 0),
                      (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (8, 0), (8, 1), (8, 2), (8, 3), (8, 4)]
listGreenCells = {(0, 0), (4, 8), (8, 0)}
listRedCells = {(0, 4), (4, 0), (8, 4)}
listNearestCells = set()
listFarCells = set()
clickedCell = ()
redMoveCount = 0
greenMoveCount = 0
redMove = True
win = False
SCREEN_COLOR = (0,0,0)


def initialize():
    global something_clicked, listCells, listCellsAddresses, listGreenCells, listRedCells, listNearestCells, listFarCells, clickedCell, redMove, win, redMoveCount, greenMoveCount
    something_clicked = False
    listCells = []
    listCellsAddresses = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
                          (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (3, 0), (3, 1), (3, 2), (3, 4),
                          (3, 5), (3, 6), (3, 7), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 6), (4, 7), (4, 8),
                          (5, 0), (5, 1), (5, 2), (5, 4), (5, 5), (5, 6), (5, 7), (6, 0), (6, 1), (6, 2), (6, 3),
                          (6, 4), (6, 5), (6, 6), (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (8, 0), (8, 1),
                          (8, 2), (8, 3), (8, 4)]
    listGreenCells = {(0, 0), (4, 8), (8, 0)}
    listRedCells = {(0, 4), (4, 0), (8, 4)}
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


def checkRedCell(i, j):
    if (i, j) in listCellsAddresses and not (i, j) in listGreenCells | listRedCells:
        listNearestCells.add((i, j))


def showNearCells(cell: Cell):
    global listNearestCells
    i, j = cell.address[:]
    checkRedCell(i + 1, j)
    checkRedCell(i, j + 1)
    checkRedCell(i, j - 1)

    if i >= 4:
        checkRedCell(i + 1, j - 1)
    elif i < 4:
        checkRedCell(i + 1, j + 1)

    if i <= 4:
        checkRedCell(i - 1, j - 1)
    else:
        checkRedCell(i - 1, j + 1)

    checkRedCell(i - 1, j)


def checkFarCells(i, j):
    if (i, j) in listCellsAddresses and (i, j) not in listRedCells | listGreenCells | listNearestCells:
        listFarCells.add((i, j))


def showFarCells(cell: Cell):
    global listFarCells
    i, j = cell.address[:]
    if i < 4:
        if i == 3:
            checkFarCells(i + 2, j - 1)
            checkFarCells(i + 2, j)
            checkFarCells(i + 2, j + 1)
        else:
            checkFarCells(i + 2, j)
            checkFarCells(i + 2, j + 1)
            checkFarCells(i + 2, j + 2)
    else:
        checkFarCells(i + 2, j - 2)
        checkFarCells(i + 2, j - 1)
        checkFarCells(i + 2, j)

    if i > 4:
        if i == 5:
            checkFarCells(i - 2, j - 1)
            checkFarCells(i - 2, j)

            checkFarCells(i - 2, j + 1)
        else:
            checkFarCells(i - 2, j)
            checkFarCells(i - 2, j + 1)
            checkFarCells(i - 2, j + 2)
    else:
        checkFarCells(i - 2, j - 2)
        checkFarCells(i - 2, j - 1)
        checkFarCells(i - 2, j)

    checkFarCells(i, j + 2)
    checkFarCells(i, j - 2)

    if i >= 4:
        checkFarCells(i + 1, j + 1)
        checkFarCells(i + 1, j - 2)
    else:
        checkFarCells(i + 1, j + 2)
        checkFarCells(i + 1, j - 1)

    if i <= 4:
        checkFarCells(i - 1, j + 1)
        checkFarCells(i - 1, j - 2)
    else:
        checkFarCells(i - 1, j + 2)
        checkFarCells(i - 1, j - 1)

def checkNearCellsForAnotherChips(cell: Cell):
    i, j = cell.address[:]
    if redMove:
        if (i + 1, j) in listGreenCells:
            listGreenCells.remove((i + 1, j))
            listRedCells.add((i + 1, j))
        if (i, j + 1) in listGreenCells:
            listGreenCells.remove((i, j + 1))
            listRedCells.add((i, j + 1))
        if (i, j - 1) in listGreenCells:
            listGreenCells.remove((i, j - 1))
            listRedCells.add((i, j - 1))
        if i >= 4:
            if (i + 1, j - 1) in listGreenCells:
                listGreenCells.remove((i + 1, j - 1))
                listRedCells.add((i + 1, j - 1))
        elif i < 4:
            if (i + 1, j + 1) in listGreenCells:
                listGreenCells.remove((i + 1, j + 1))
                listRedCells.add((i + 1, j + 1))
        if i <= 4:
            if (i - 1, j - 1) in listGreenCells:
                listGreenCells.remove((i - 1, j - 1))
                listRedCells.add((i - 1, j - 1))
        else:
            if (i - 1, j + 1) in listGreenCells:
                listGreenCells.remove((i - 1, j + 1))
                listRedCells.add((i - 1, j + 1))

        if (i - 1, j) in listGreenCells:
            listGreenCells.remove((i - 1, j))
            listRedCells.add((i - 1, j))
    else:
        if (i + 1, j) in listRedCells:
            listRedCells.remove((i + 1, j))
            listGreenCells.add((i + 1, j))
        if (i, j + 1) in listRedCells:
            listRedCells.remove((i, j + 1))
            listGreenCells.add((i, j + 1))
        if (i, j - 1) in listRedCells:
            listRedCells.remove((i, j - 1))
            listGreenCells.add((i, j - 1))
        if i >= 4:
            if (i + 1, j - 1) in listRedCells:
                listRedCells.remove((i + 1, j - 1))
                listGreenCells.add((i + 1, j - 1))
        elif i < 4:
            if (i + 1, j + 1) in listRedCells:
                listRedCells.remove((i + 1, j + 1))
                listGreenCells.add((i + 1, j + 1))
        if i <= 4:
            if (i - 1, j - 1) in listRedCells:
                listRedCells.remove((i - 1, j - 1))
                listGreenCells.add((i - 1, j - 1))
        else:
            if (i - 1, j + 1) in listRedCells:
                listRedCells.remove((i - 1, j + 1))
                listGreenCells.add((i - 1, j + 1))

        if (i - 1, j) in listRedCells:
            listRedCells.remove((i - 1, j))
            listGreenCells.add((i - 1, j))


def checkCellForMove(cell: Cell):
    i, j = cell.address[:]
    t = 0
    if i < 4:
        if i == 3:
            if (i + 2, j - 1) in listCellsAddresses and (i + 2, j - 1) not in listRedCells | listGreenCells: t += 1
            if (i + 2, j) in listCellsAddresses and (i + 2, j) not in listRedCells | listGreenCells: t += 1
            if (i + 2, j + 1) in listCellsAddresses and (i + 2, j + 1) not in listRedCells | listGreenCells: t += 1
        else:
            if (i + 2, j) in listCellsAddresses and (i + 2, j) not in listRedCells | listGreenCells: t += 1
            if (i + 2, j + 1) in listCellsAddresses and (i + 2, j + 1) not in listRedCells | listGreenCells: t += 1
            if (i + 2, j + 2) in listCellsAddresses and (i + 2, j + 2) not in listRedCells | listGreenCells: t += 1
    else:
        if (i + 2, j - 2) in listCellsAddresses and (i + 2, j - 2) not in listRedCells | listGreenCells: t += 1
        if (i + 2, j - 1) in listCellsAddresses and (i + 2, j - 1) not in listRedCells | listGreenCells: t += 1
        if (i + 2, j) in listCellsAddresses and (i + 2, j) not in listRedCells | listGreenCells: t += 1
    if i > 4:
        if i == 5:
            if (i - 2, j - 1) in listCellsAddresses and (i - 2, j - 1) not in listRedCells | listGreenCells: t += 1
            if (i - 2, j) in listCellsAddresses and (i - 2, j) not in listRedCells | listGreenCells: t += 1
            if (i - 2, j + 1) in listCellsAddresses and (i - 2, j + 1) not in listRedCells | listGreenCells: t += 1
        else:
            if (i - 2, j) in listCellsAddresses and (i - 2, j) not in listRedCells | listGreenCells: t += 1
            if (i - 2, j + 1) in listCellsAddresses and (i - 2, j + 1) not in listRedCells | listGreenCells: t += 1
            if (i - 2, j + 2) in listCellsAddresses and (i - 2, j + 2) not in listRedCells | listGreenCells: t += 1
    else:
        if (i - 2, j) in listCellsAddresses and (i - 2, j) not in listRedCells | listGreenCells: t += 1
        if (i - 2, j - 1) in listCellsAddresses and (i - 2, j - 1) not in listRedCells | listGreenCells: t += 1
        if (i - 2, j - 2) in listCellsAddresses and (i - 2, j - 2) not in listRedCells | listGreenCells: t += 1
    if (i, j + 2) in listCellsAddresses and (i, j + 2) not in listRedCells | listGreenCells: t += 1
    if (i, j - 2) in listCellsAddresses and (i, j - 2) not in listRedCells | listGreenCells: t += 1

    if i >= 4:
        if (i + 1, j + 1) in listCellsAddresses and (i + 1, j + 1) not in listRedCells | listGreenCells: t += 1
        if (i + 1, j - 2) in listCellsAddresses and (i + 1, j - 2) not in listRedCells | listGreenCells: t += 1
    else:
        if (i + 1, j + 2) in listCellsAddresses and (i + 1, j + 2) not in listRedCells | listGreenCells: t += 1
        if (i + 1, j - 1) in listCellsAddresses and (i + 1, j - 1) not in listRedCells | listGreenCells: t += 1
    if i <= 4:
        if (i - 1, j + 1) in listCellsAddresses and (i - 1, j + 1) not in listRedCells | listGreenCells: t += 1
        if (i - 1, j - 2) in listCellsAddresses and (i - 1, j - 2) not in listRedCells | listGreenCells: t += 1
    else:
        if (i - 1, j + 2) in listCellsAddresses and (i - 1, j + 2) not in listRedCells | listGreenCells: t += 1
        if (i - 1, j - 1) in listCellsAddresses and (i - 1, j - 1) not in listRedCells | listGreenCells: t += 1
    return t

def return_to_main_menu():
    pass

def displayhexagon():
    global listCells, greenMoveCount, redMoveCount
    redMoveCount = 0
    greenMoveCount = 0
    listCells = []
    for i in range(9):
        x = i * 60 + WIDTH/4
        for j in range(f(i)):
            y = 30 * j + abs(i - 4) * 15
            cell = Cell()
            cell.address = (i, j)
            green_f = pg.image.load("green_f.png")
            red_f = pg.image.load("red_f.png")
            nearestCell = pg.image.load("nearestCell.png")
            farCell = pg.image.load("farCell.png")
            if (i, j) in listGreenCells:
                SCREEN.blit(green_f, (x + 10 * i + 20, HEIGHT/1.5 - y - 10 * j + 10))
                greenMoveCount += checkCellForMove(cell)
            if (i, j) in listRedCells:
                SCREEN.blit(red_f, (x + 10 * i + 13, HEIGHT/1.5  - y - 10 * j + 7))
                redMoveCount += checkCellForMove(cell)
            if (i, j) in listNearestCells: SCREEN.blit(nearestCell, (x + 10 * i, HEIGHT/1.5  - y - 10 * j))
            if (i, j) in listFarCells: SCREEN.blit(farCell, (x + 10 * i, HEIGHT/1.5  - y - 10 * j))
            if (i, j) in listCellsAddresses: SCREEN.blit(cell.pic, (x + 10 * i, HEIGHT/1.5  - y - 10 * j))
            cell.x = x + 10 * i
            cell.y = HEIGHT/1.5  - y - 10 * j
            listCells.append(cell)
            cell.on_click_listener()

playing = False

def start_the_game(menu: pygame_menu.menu):
    global something_clicked, playing
    something_clicked = True
    playing = True
    menu.disable()
    SCREEN.fill(SCREEN_COLOR)
    initialize()
    displayhexagon()

def start():
    global something_clicked, playing
    clock = pg.time.Clock()
    SCREEN.fill(SCREEN_COLOR)
    menu = pygame_menu.Menu('Hexagon', WIDTH, HEIGHT, theme=menu_theme.menu_theme, column_min_width=100)
    menu.add.button('Play',start_the_game, menu)
    menu.add.button('Quit', pygame_menu.events.PYGAME_QUIT)
    menu.mainloop(SCREEN)
    while 1:
        for i in pg.event.get():
            if i.type == pg.QUIT:
                return
            if i.type == MOUSEBUTTONDOWN:
                if playing:
                    if WIDTH - 400 <= mouse[0] <= WIDTH - 220 and 20 <= mouse[1] <= 100:
                        something_clicked = True
                        playing = False
                        SCREEN.fill(SCREEN_COLOR)
                        menu.enable()
                        menu.mainloop(SCREEN)
        mouse = pg.mouse.get_pos()
        if playing:
            for i in listCells:
                i.on_click_listener()
            if len(listRedCells) > len(listGreenCells) and len(listRedCells) + len(
                    listGreenCells) == 58 or greenMoveCount == 0 or len(listGreenCells) == 0:
                winText = smallfont2.render('Red win!', True, (255, 255, 255))
                SCREEN.blit(winText, (WIDTH / 2 - winText.get_width() / 2, 50))
            elif len(listRedCells) == len(listGreenCells) and len(listRedCells) + len(listGreenCells) == 58:
                winText = smallfont2.render('Draw!', True, (255, 255, 255))
                SCREEN.blit(winText, (WIDTH / 2 - winText.get_width() / 2, 50))
            elif len(listRedCells) < len(listGreenCells) and len(listRedCells) + len(
                    listGreenCells) == 58 or redMoveCount == 0 or len(listRedCells) == 0:
                winText = smallfont2.render('Green win!', True, (255, 255, 255))
                SCREEN.blit(winText, (WIDTH / 2 - winText.get_width() / 2, 25))
            else:
                winText = smallfont2.render('Playing', True, (255, 255, 255))
                SCREEN.blit(winText, (WIDTH / 2 - winText.get_width() / 2, 50))
                move = smallfont2.render(f'{"Red" if redMove else "Green"} turn', True,
                                         (255, 0, 0) if redMove else (0, 255, 0))
                SCREEN.blit(move, (WIDTH / 2 - move.get_width() / 2, 30))
            if redMove:
                if WIDTH - 400 <= mouse[0] <= WIDTH - 220 and 20 <= mouse[1] <= 100:
                    pg.draw.rect(SCREEN, (255, 0, 0), [WIDTH - 400, 20, 180, 80], 0, 3)
                else:
                    pg.draw.rect(SCREEN, (255, 115, 115), [WIDTH - 400, 20, 180, 80], 0, 3)
            else:
                if WIDTH - 400 <= mouse[0] <= WIDTH - 220 and 20 <= mouse[1] <= 100:
                    pg.draw.rect(SCREEN, (48, 191, 65), [WIDTH - 400, 20, 180, 80], 0, 3)
                else:
                    pg.draw.rect(SCREEN, (40, 255, 87), [WIDTH - 400, 20, 180, 80], 0, 3)

            green_count = smallfont2.render(f'Green: {len(listGreenCells)}', True, (255, 255, 255))
            SCREEN.blit(green_count, (WIDTH / 2 - winText.get_width() / 2 - 150, 15))
            red_count = smallfont2.render(f'Red: {len(listRedCells)}', True, (255, 255, 255))

            SCREEN.blit(red_count, (WIDTH / 2 - winText.get_width() / 2 - 150, 45))
            back_text = smallfont2.render('Main menu', True, (255, 255, 255))
            SCREEN.blit(back_text, (WIDTH - 420  + back_text.get_width() / 2, 45))
        clock.tick(FPS)
        pg.display.update()
