import pygame
from pygame import sprite
from settings import *

class Camera():

    def __init__(self, player, width=WIDTH, height=HEIGHT):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.player = player
        self.limit = True

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def applyRect(self, rect):
        return rect.move(self.camera.topleft)
        
    def update(self):
        self.target = self.player
        x = -self.target.rect.centerx + int(WIDTH / 2)
        y = -self.target.rect.centery + int(HEIGHT / 2)
        if self.limit:
            x = max(-(self.width - WIDTH), min(0, x))
            y = max(-(self.height - HEIGHT), min(0, y))

        self.camera.topleft = x, y