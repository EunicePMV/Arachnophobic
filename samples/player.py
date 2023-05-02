import pygame as pg
import numpy as np

class Player():
    def __init__(self, speed):
        self.width = 64
        self.height = 64
        self.speed = speed
        self.direction = True
        self.moveX = 0
        self.moveY = 0
        self.spriteY = 0
        self.player = pg.Surface((self.width, self.height))
        self.spriteSheet = pg.image.load("samples/assets/imgs/chara-map-Sheet.png").convert()
        self.spriteSheet = pg.transform.scale2x(self.spriteSheet)
        self.spriteFlipped = pg.transform.flip(self.spriteSheet, True, False)
        # self.sprite = self.spriteSheet.subsurface((self.spriteX, self.spriteY, self.width, self.height))
        self.player.set_colorkey((0, 0, 0))
        self.rect = self.player.get_rect()

    def setPos(self, posX, posY):
        self.rect.x = posX
        self.rect.y = posY

    def fillColor(self, color):
        self.color = color
        self.player.fill(self.color)

    def blitPlayer(self, canvas: pg.Surface): 
        self.player.blit(self.spriteSheet if self.direction else self.spriteFlipped, (0, 0), (0, self.spriteY, self.width, self.height))
        canvas.blit(self.player, self.rect)
    
    def registerEvent(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_s:
                self.moveY = 1
            elif event.key == pg.K_w:
                self.moveY = -1
            if event.key == pg.K_d:
                self.direction = True
                self.moveX = 1
            elif event.key == pg.K_a:
                self.direction = False
                self.moveX = -1
        if event.type == pg.KEYUP:
            if event.key == pg.K_s or event.key == pg.K_w:
                self.moveY = 0
            if event.key == pg.K_a or event.key == pg.K_d:
                self.moveX = 0

    def move(self, camera):
        self.rect.y += self.speed * self.moveY
        camera.x += self.speed * self.moveX

    