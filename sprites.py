import pygame
from pygame import sprite
from pygame import Vector2 as Vec
from settings import *

class Camera(pygame.sprite.Sprite):

    def __init__(self, game, target):
        self.game = game
        super().__init__(game.sprites)
        self.camera = pygame.Rect(0, 0, self.game.level.rect.w, self.game.level.rect.h)
        self.width = self.camera.w
        self.height = self.camera.h
        self.target = target
        self.limit = True

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def applyRect(self, rect):
        return rect.move(self.camera.topleft)
        
    def update(self):
        x = -self.target.rect.centerx + int(WIDTH / 2)
        y = -self.target.rect.centery + int(HEIGHT / 2)
        if self.limit:
            x = max(-(self.width - WIDTH), min(0, x))
            y = max(-(self.height - HEIGHT), min(0, y))

        self.camera.topleft = x, y

class Collider(pygame.sprite.Sprite):
    def __init__(self, game, rect):
        self.game = game
        super().__init__(self.game.level.colliders)
        self.rect = pygame.Rect(rect)

class Block(pygame.sprite.Sprite):
    groups = []
    def __init__(self, game, rect):
        self.game = game
        super().__init__(game.sprites, self.groups)
        self.rect = pygame.Rect(rect)
        self.load()
    
    def load(self):
        pass

    @classmethod
    def getblock(self, key):
        newb = [cls for cls in Block.__subclasses__() if cls._identify == key]
        return newb[0] if newb else False

class Mover(Block):
    _identify = '2'
    imgCache = None
    def __init__(self, game, rect):
        self.groups = game.level.colliders
        super().__init__(game, rect)
    
    def load(self):
        self.image = self.render() if not self.imgCache else self.imgCache
        self.imgCache = self.image
        self.vel = Vec(0, 0)

    def render(self):
        size = self.game.level.tileW
        newS = pygame.Surface((size, size)).convert()
        pygame.draw.rect(newS,(0, 30, 120), (0, 0, size, size), 3)
        return newS

    def update(self):
        self.vel += self.game.gravity*self.game.dt()
        lim = 20 if self.game.gravity else 6
        if self.vel.length() > 0.1:
            self.vel.scale_to_length( max( -lim, min(lim, self.vel.length()) ) )

            self.rect.x += round(self.vel.x)
            collide = self.checkCollide()
            if collide:
                if self.vel.x > 0:
                    self.rect.right = collide.left
                else:
                    self.rect.left = collide.right
                self.vel.x = 0
            
            self.rect.y += round(self.vel.y)
            collide = self.checkCollide()
            if collide:
                if self.vel.y > 0:
                    self.rect.bottom = collide.top
                else:
                    self.rect.top = collide.bottom
                self.vel.y = 0
        else:
            self.vel.xy = 0,0
    
    def checkCollide(self):
        for c in self.game.level.colliders:
            if self.rect.colliderect(c.rect) and not c == self:
                return c.rect
        return False

class LeverLeft(Block):
    _identify = '3'
    def load(self):
        print("why")
        size = self.game.level.tileW
        self.image = pygame.Surface((size, size)).convert()
        pygame.draw.line(self.image, (0, 200, 40), (12.5, 25), (0, 0), 4)
        self.lastgrav = self.game.gravity.copy()
        self.newgrav = GRAVDIRS[2]*GRAVSPEED
        self.toggled = False
        self.lastToggled = 0

    def update(self):
        if now() - self.lastToggled > 300:
            if pygame.key.get_pressed()[pygame.K_e]:
                if Vec(self.rect.center).distance_to(self.game.player.rect.center) < 35:
                    self.toggle()
    
    def toggle(self):
        if self.toggled:
            pass
        else:
            self.image = pygame.Surface(self.image.get_size()).convert()
            pygame.draw.line(self.image, (0, 200, 40), (12.5, 25), (25, 0), 4)
            self.game.gravity = self.newgrav
        self.toggled = not self.toggled