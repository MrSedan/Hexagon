import pygame as pg
from math import cos, sin, pi
from pygame.locals import *

pg.init()
clock = pg.time.Clock()
FPS = 1488
smallfont = pg.font.Font("./fonts/Montserrat-Regular.ttf", 35)
smallfont2 = pg.font.Font("./fonts/Montserrat-Regular.ttf", 20)
hex = pg.image.load('im1.png')


def draw_regular_polygon(surface, color, vertex_count, radius, position, width=0):
    n, r = vertex_count, radius
    x, y = position
    pg.draw.polygon(surface, color, [
        (x + r * cos(2 * pi * i / n), y + r * sin(2 * pi * i / n))
        for i in range(n)
    ], width)


def f(i):
    if i < 5:
        return i + 5
    else:
        return 13 - i

def main():
    def displayhexagon():
        for i in range(9):
            x = i * 60+100
            for j in range(f(i)):
                y = 30 * j + abs(i - 4) * 15
                screen.blit(hex, (x, height/2-y))
    screen = pg.display.set_mode((800, 800))
    screen.fill((255, 255, 255))
    width = screen.get_width()
    height = screen.get_height()
    playing = False
    while 1:
        for i in pg.event.get():
            if i.type == pg.QUIT:
                return
            if i.type == MOUSEBUTTONDOWN:
                if not playing:
                    if width / 2 - 70 <= mouse[0] <= width / 2 + 70 and height - 200 <= mouse[1] <= height - 160:
                        return
                    if width / 2 - 90 <= mouse[0] <= width / 2 + 90 and height - 400 <= mouse[1] <= height - 320:
                        playing = True
                        screen.fill((255, 255, 255))
                else:
                    if width - 190 <= mouse[0] <= width - 10 and 20 <= mouse[1] <= 100:
                        playing = False
                        screen.fill((255, 255, 255))
        mouse = pg.mouse.get_pos()
        if not playing:
            header = smallfont.render('Hexagon', True, (0, 0, 0))
            screen.blit(header, (width / 2 - header.get_width() / 2, 200))
            if width / 2 - 70 <= mouse[0] <= width / 2 + 70 and height - 200 <= mouse[1] <= height - 160:
                pg.draw.rect(screen, (0, 0, 255), [width / 2 - 70, height - 200, 140, 40])
            else:
                pg.draw.rect(screen, (255, 255, 0), [width / 2 - 70, height - 200, 140, 40])
            if width / 2 - 90 <= mouse[0] <= width / 2 + 90 and height - 400 <= mouse[1] <= height - 320:
                pg.draw.rect(screen, (0, 0, 255), [width / 2 - 90, height - 400, 180, 80])
            else:
                pg.draw.rect(screen, (255, 255, 0), [width / 2 - 90, height - 400, 180, 80])
            quit_text = smallfont.render('Quit', True, (0, 0, 0))
            screen.blit(quit_text, (width / 2 - quit_text.get_width() / 2, height - 200))
            play_text = smallfont.render('Play', True, (0, 0, 0))
            screen.blit(play_text, (width / 2 - play_text.get_width() / 2, height - 380))
        else:
            if width - 190 <= mouse[0] <= width - 10 and 20 <= mouse[1] <= 100:
                pg.draw.rect(screen, (0, 0, 255), [width - 190, 20, 180, 80])
            else:
                pg.draw.rect(screen, (255, 255, 0), [width - 190, 20, 180, 80])
            back_text = smallfont2.render('Main menu', True, (0, 0, 0))
            screen.blit(back_text, (width - 210 + back_text.get_width() / 2, 45))
            # draw_regular_polygon(screen, (0, 0, 0), 6, 300, (width / 2, height / 2), 1)
            displayhexagon()
        clock.tick(FPS)
        pg.display.update()


if __name__ == '__main__':
    main()
