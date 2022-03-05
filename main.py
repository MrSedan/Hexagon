import pygame as pg
from pygame.locals import *
pg.init()
clock = pg.time.Clock()
FPS = 60
smallfont = pg.font.Font("./fonts/Montserrat-Regular.ttf", 35)


def main():
    screen = pg.display.set_mode((1920, 1080))
    screen.fill((255,255,255))
    width = screen.get_width()
    height = screen.get_height()
    header = smallfont.render('Hexagon',True, (0,0,0))
    screen.blit(header,(width/2-header.get_width()/2,200))

    while 1:
        for i in pg.event.get():
            if i.type == pg.QUIT:
                return
            if i.type == MOUSEBUTTONDOWN:
                if width/2-70 <= mouse[0] <= width/2+70 and height-200 <= mouse[1] <= height-160:
                    return
        mouse = pg.mouse.get_pos()
        if width / 2 - 70 <= mouse[0] <= width / 2 + 70 and height - 200 <= mouse[1] <= height - 160:
            pg.draw.rect(screen, (0, 0, 255), [width / 2 - 70, height - 200, 140, 40])
        else:
            pg.draw.rect(screen, (255, 255, 0), [width / 2 - 70, height - 200, 140, 40])
        quit_text = smallfont.render('Quit', True, (0, 0, 0))
        screen.blit(quit_text, (width / 2 - quit_text.get_width() / 2, height - 200))
        clock.tick(FPS)
        pg.display.update()


if __name__ == '__main__':
    main()
