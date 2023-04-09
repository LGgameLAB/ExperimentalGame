import pygame
from pygame import Vector2 as Vec
import math, random, sys

pygame.init()

win = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()
FPS = 60
GRAVITY = Vec(0, 0)
GRAVSPEED = 15.8
GRAVDIRS = [Vec(x) for x in [ (0,-1), (0,1), (-1,0), (1,0) ]]
print('''
PLEASE READ:

Use arrow keys to change Gravity (along with spacebar to nuetralize)
AND use WASD to move the character
''')
def dt():
    global clock
    return clock.get_time()*0.001

class Player:
    def __init__(self, level):
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
        self.level = level
    
    def update(self):
        self.move()

    def move(self):
        global GRAVITY
        keys = pygame.key.get_pressed()
        if GRAVITY:
            gNorm = GRAVITY.normalize()
            dir = self.getDir[(gNorm.x, gNorm.y)]
            if keys[pygame.K_w] and self.canJump():
                self.vel += dir[0]*self.jumpSpeed*dt()
        else:
            dir = self.up
            if keys[pygame.K_w]:
                self.vel += dir[0]*self.speed*dt()
            if keys[pygame.K_s]:
                self.vel += dir[1]*self.speed*dt()
        if keys[pygame.K_a]:
            self.vel += dir[2]*self.speed*dt()
        if keys[pygame.K_d]:
            self.vel += dir[3]*self.speed*dt()
        
        self.vel += GRAVITY*dt()
        lim = 20 if GRAVITY else 6
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

            if GRAVITY:
                if GRAVITY.y:
                    self.vel.x *= self.drag
                else:
                    self.vel.y *= self.drag
            else:
                self.vel *= self.drag
        else:
            self.vel.xy = 0,0
    
    def checkCollide(self):
        for c in self.level.colliders:
            if self.rect.colliderect(c):
                return c
        return False
    
    # def isJumpDir(x, y):
    #     if 
    def canJump(self):
        global GRAVITY
        self.rect.topleft += GRAVITY.normalize()#/max(abs(min(GRAVITY.x, GRAVITY.y)), abs(max(GRAVITY.x, GR.y)))
        result = self.checkCollide()
        self.rect.topleft -= GRAVITY.normalize()
        return bool(result)

class Level:
    def __init__(self, data):
        self.data = data
        self.tileW = 25
        self.color = (150, 0, 0)
        self.colliders = []
        self.arrowPic = pygame.image.load("arrow.png")
        self.render()
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
    
    def update(self):
        global GRAVITY, GRAVSPEED
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            GRAVITY = GRAVDIRS[0]*GRAVSPEED
            self.render()
        if keys[pygame.K_DOWN]:
            GRAVITY = GRAVDIRS[1]*GRAVSPEED
            self.render()
        if keys[pygame.K_LEFT]:
            GRAVITY = GRAVDIRS[2]*GRAVSPEED
            self.render()
        if keys[pygame.K_RIGHT]:
            GRAVITY = GRAVDIRS[3]*GRAVSPEED
            self.render()
        if keys[pygame.K_SPACE]:
            GRAVITY = Vec(0, 0)
            self.render()

    def render(self):
        s = len(self.data[0])*self.tileW
        self.image = pygame.Surface((s, s), pygame.SRCALPHA)
        if GRAVITY:
            img = pygame.transform.rotate(self.arrowPic, GRAVITY.angle_to((0, 0)))
            self.image.blit(img, img.get_rect(center=(s/2, s/2)) )
        for col in range(len(self.data)):
            for row in range(len(self.data[col])):
                if int(self.data[col][row]):
                    rect = pygame.Rect(row*self.tileW, col*self.tileW, self.tileW, self.tileW)
                    self.colliders.append(rect)
                    pygame.draw.rect(self.image, self.color, rect, 3)
        return self.image


with open("data.txt", "r") as f:
    data = f.read().split('\n')
    lvl1 = Level(data)

p = Player(lvl1)
sprites = [lvl1, p]
run = True
while run:
    for v in pygame.event.get():
        if v.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    clock.tick(FPS)
    win.fill((0,0,0))
    for obj in sprites:
        obj.update()
    for obj in sprites:
        win.blit(obj.image, obj.rect)
    pygame.display.flip()
