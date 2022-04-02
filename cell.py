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
                if self.address in main_window.listNearestCells:
                    if main_window.clickedCell in main_window.listRedCells and main_window.redMove:
                        main_window.listRedCells.append(self.address)
                        main_window.redMove = False
                    elif not main_window.redMove:
                        main_window.listGreenCells.append(self.address)
                        main_window.redMove = True
                    main_window.listNearestCells = set()
                    main_window.listFarCells = set()
                    main_window.SCREEN.fill((255, 255, 255))
                    main_window.displayhexagon()
                    return

                if self.address in main_window.listFarCells:
                    if main_window.clickedCell in main_window.listRedCells and main_window.redMove:
                        main_window.listRedCells.append(self.address)
                        main_window.listRedCells.remove(main_window.clickedCell)
                        main_window.redMove = False
                    elif not main_window.redMove:
                        main_window.listGreenCells.append(self.address)
                        main_window.listGreenCells.remove(main_window.clickedCell)
                        main_window.redMove = True
                    main_window.listNearestCells = set()
                    main_window.listFarCells = set()
                    main_window.SCREEN.fill((255, 255, 255))
                    main_window.displayhexagon()
                    return
                main_window.listNearestCells = set()
                main_window.listFarCells = set()
                if self.address in main_window.listRedCells and main_window.redMove or\
                        self.address in main_window.listGreenCells and not main_window.redMove:
                    print("Clicked on cell with chip")
                    main_window.showNearCells(self)
                    main_window.showFarCells(self)
                    main_window.clickedCell = self.address
                print("Clicked on cell", self.address)
                main_window.SCREEN.fill((255,255,255))
                main_window.displayhexagon()
            if pg.mouse.get_pressed(3)[0] == 0:
                main_window.something_clicked = False