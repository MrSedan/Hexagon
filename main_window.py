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

def f(i):
    if i < 5:
        return i + 5
    else:
        return 13 - i

def start():
    clock = pg.time.Clock()
    playing = False
    SCREEN.fill((255,255,255))
    def displayhexagon():
        for i in range(9):
            x = i * 60 + 100
            for j in range(f(i)):
                y = 30 * j + abs(i - 4) * 15
                cell = Cell()
                SCREEN.blit(cell.pic, (x, HEIGHT / 2 - y))
                cell.x = x
                cell.y = HEIGHT / 2 - y
                cell.address = (i,j)
                listCells.append(cell)
                cell.on_click_listener()
    while 1:
        for i in pg.event.get():
            if i.type == pg.QUIT:
                return
            if i.type == MOUSEBUTTONDOWN:
                if not playing:
                    if WIDTH / 2 - 70 <= mouse[0] <= WIDTH / 2 + 70 and HEIGHT - 200 <= mouse[1] <= HEIGHT - 160:
                        return
                    if WIDTH / 2 - 90 <= mouse[0] <= WIDTH / 2 + 90 and HEIGHT - 400 <= mouse[1] <= HEIGHT - 320:
                        playing = True
                        SCREEN.fill((255, 255, 255))
                else:
                    if WIDTH - 190 <= mouse[0] <= WIDTH - 10 and 20 <= mouse[1] <= 100:
                        playing = False
                        SCREEN.fill((255, 255, 255))
                    for cell in listCells:
                        if cell.pic.get_rect().collidepoint(mouse[0],mouse[1]):
                            print("clicked on cell")
        mouse = pg.mouse.get_pos()
        if not playing:
            header = smallfont.render('Hexagon', True, (0, 0, 0))
            SCREEN.blit(header, (WIDTH / 2 - header.get_width() / 2, 200))
            if WIDTH / 2 - 70 <= mouse[0] <= WIDTH / 2 + 70 and HEIGHT - 200 <= mouse[1] <= HEIGHT - 160:
                pg.draw.rect(SCREEN, (0, 0, 255), [WIDTH / 2 - 70, WIDTH - 200, 140, 40])
            else:
                pg.draw.rect(SCREEN, (255, 255, 0), [WIDTH / 2 - 70, HEIGHT - 200, 140, 40])
            if WIDTH / 2 - 90 <= mouse[0] <= WIDTH / 2 + 90 and HEIGHT - 400 <= mouse[1] <= HEIGHT - 320:
                pg.draw.rect(SCREEN, (0, 0, 255), [WIDTH / 2 - 90, HEIGHT - 400, 180, 80])
            else:
                pg.draw.rect(SCREEN, (255, 255, 0), [WIDTH / 2 - 90, HEIGHT - 400, 180, 80])
            quit_text = smallfont.render('Quit', True, (0, 0, 0))
            SCREEN.blit(quit_text, (WIDTH / 2 - quit_text.get_width() / 2, HEIGHT - 200))
            play_text = smallfont.render('Play', True, (0, 0, 0))
            SCREEN.blit(play_text, (WIDTH / 2 - play_text.get_width() / 2, HEIGHT - 380))
        else:
            if WIDTH - 190 <= mouse[0] <= WIDTH - 10 and 20 <= mouse[1] <= 100:
                pg.draw.rect(SCREEN, (0, 0, 255), [WIDTH - 190, 20, 180, 80])
            else:
                pg.draw.rect(SCREEN, (255, 255, 0), [WIDTH - 190, 20, 180, 80])
            back_text = smallfont2.render('Main menu', True, (0, 0, 0))
            SCREEN.blit(back_text, (WIDTH - 210 + back_text.get_width() / 2, 45))
            # draw_regular_polygon(screen, (0, 0, 0), 6, 300, (width / 2, height / 2), 1)
            displayhexagon()
        clock.tick(FPS)
        pg.display.update()