import pygame as pg
import main_window

class Cell():
    def __init__(self):
        self.pic = pg.image.load('im1.png')
        self.rect = self.pic.get_rect()
        self.x = 0
        self.y = 0
        self.address = (0,0)
    def on_click_listener(self):
        pos = pg.mouse.get_pos()
        self.rect.topleft = (self.x, self.y)
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed(3)[0] == 1 and not main_window.something_clicked:
                main_window.something_clicked = True
                print("Clicked on cell", self.address)
            if pg.mouse.get_pressed(3)[0] == 0:
                main_window.something_clicked = False