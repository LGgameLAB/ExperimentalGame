import pygame
from pygame import Vector2 as Vec
from pygame.sprite import Group
import math, random, sys
from settings import *
from sprites import Camera, Collider, Block

pygame.init()

win = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()
GRAVITY = Vec(0, 0)
print('''
PLEASE READ:

Use arrow keys to change Gravity (along with spacebar to nuetralize)
AND use WASD to move the character
''')
class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        super().__init__(game.sprites)
        self.rect = pygame.Rect(50,50,25,25)
        self.vel = Vec(0,0)
        # direction binds for W, S, A, D 
        self.up = [Vec(x) for x in [ (0,-1), (0,1), (-1,0), (1,0) ]]
        self.down = [Vec(x) for x in [ (0,1), (0,-1), (-1,0), (1,0) ]]
        self.right = [Vec(x) for x in [ (-1, 0), (1,0), (0,1), (0,-1) ]]
        self.left = [Vec(x) for x in [ (1, 0), (-1,0), (0,-1), (0,1) ]]
        self.getDir = {(0, 1):self.up, (0, -1): self.down, (1, 0): self.right, (-1, 0): self.left}
        self.speed = 30
        self.jumpSpeed = 600
        self.drag = 0.85
        self.image = pygame.Surface(self.rect.size)
        self.image.fill((0, 20, 140))
        self.level = game.level
    
    def update(self):
        self.move()

    def move(self):
        keys = pygame.key.get_pressed()
        if self.game.gravity:
            gNorm = self.game.gravity.normalize()
            dir = self.getDir[(gNorm.x, gNorm.y)]
            if keys[pygame.K_w] and self.canJump():
                self.vel += dir[0]*self.jumpSpeed*self.game.dt()
        else:
            dir = self.up
            if keys[pygame.K_w]:
                self.vel += dir[0]*self.speed*self.game.dt()
            if keys[pygame.K_s]:
                self.vel += dir[1]*self.speed*self.game.dt()
        if keys[pygame.K_a]:
            self.vel += dir[2]*self.speed*self.game.dt()
        if keys[pygame.K_d]:
            self.vel += dir[3]*self.speed*self.game.dt()
        
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

            if self.game.gravity:
                if self.game.gravity.y:
                    self.vel.x *= self.drag
                else:
                    self.vel.y *= self.drag
            else:
                self.vel *= self.drag
        else:
            self.vel.xy = 0,0
    
    def checkCollide(self):
        for c in self.level.colliders:
            if self.rect.colliderect(c.rect):
                return c.rect
        return False
    
    # def isJumpDir(x, y):
    #     if 
    def canJump(self):
        global GRAVITY
        self.rect.topleft += self.game.gravity.normalize()#/max(abs(min(GRAVITY.x, GRAVITY.y)), abs(max(GRAVITY.x, GR.y)))
        result = self.checkCollide()
        self.rect.topleft -= self.game.gravity.normalize()
        return bool(result)

class Level(pygame.sprite.Sprite):
    def __init__(self, game, file):
        self.game = game
        super().__init__(game.sprites)
        with open(file, "r") as f:
            data = f.read().split('\n')
            self.data = data
        self.tileW = 25
        self.color = (150, 0, 0)
        self.colliders = pygame.sprite.Group()
        self.arrowPic = pygame.image.load("arrow.png")
        
    def load(self):
        self.render()
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
    
    def update(self):        
        keys = pygame.key.get_pressed()
        # if keys[pygame.K_UP]:
        #     self.game.gravity = GRAVDIRS[0]*GRAVSPEED
        # if keys[pygame.K_DOWN]:
        #     self.game.gravity = GRAVDIRS[1]*GRAVSPEED
        # if keys[pygame.K_LEFT]:
        #     self.game.gravity = GRAVDIRS[2]*GRAVSPEED
        # if keys[pygame.K_RIGHT]:
        #     self.game.gravity = GRAVDIRS[3]*GRAVSPEED
        # if keys[pygame.K_SPACE]:
        #     self.game.gravity = Vec(0, 0)


    def render(self):
        w = len(self.data[0])*self.tileW
        h = len(self.data)*self.tileW
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        if self.game.gravity:
            img = pygame.transform.rotate(self.arrowPic, self.game.gravity.angle_to((0, 0)))
            self.image.blit(img, img.get_rect(center=(w/2, h/2)) )
        for col in range(len(self.data)):
            for row in range(len(self.data[col])):
                value = self.data[col][row]
                if int(value):
                    rect = pygame.Rect(row*self.tileW, col*self.tileW, self.tileW, self.tileW)
                    newblock = Block.getblock(str(value))
                    if newblock:
                        newblock(self.game, rect)
                    else:
                        Collider(self.game, rect)
                        pygame.draw.rect(self.image, self.color, rect, 3)
        return self.image

class Game:
    def __init__(self):
        self.gravity = Vec(0, 0)
        self.win = pygame.display.set_mode((500, 500))
        self.clock = pygame.time.Clock()
        self.sprites = Group()

        self.level = Level(self, "data3.txt")
        self.level.load()
        self.player = Player(self)
        self.camera = Camera(self, self.player)
        self.gravity = GRAVDIRS[1]*GRAVSPEED

    def dt(self):
        return self.clock.get_time()*0.001
    
    def run(self):
        while True:
            for v in pygame.event.get():
                if v.type == pygame.QUIT:
                    self.quit()
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                self.quit()
                break
            self.clock.tick(FPS)
            win.fill((0,0,0))
            self.sprites.update()
            for obj in self.sprites:
                try:
                    self.win.blit(obj.image, self.camera.apply(obj))
                except:
                    pass
            pygame.display.flip() 
            
    def quit(self):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    g = Game()
    g.run()
