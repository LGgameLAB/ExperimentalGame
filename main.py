import pygame
from pygame import Vector2 as Vec
import math, random, sys

pygame.init()

win = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()
FPS = 60
GRAVITY = Vec(0, 15.8)
def dt():
    global clock
    return clock.get_time()*0.001

def randomGrav():
    global GRAVITY
    r = random.randint(0,4)
    if r == 1:
        GRAVITY = Vec(0, -15.8)
    elif r == 2:
        GRAVITY = Vec(0, 15.8)
    elif r == 3:
        GRAVITY = Vec(15.8, 0)
    elif r == 4:
        GRAVITY = Vec(-15.8, 0)
    else:
        GRAVITY = Vec(0, 0)
    
    print(GRAVITY)


class Player:
    def __init__(self, level):
        self.rect = pygame.Rect(50,50,25,25)
        self.vel = Vec(0,0)
        self.speed = 30
        self.jumpSpeed = 6000
        self.drag = 0.85
        self.image = pygame.Surface(self.rect.size)
        self.image.fill((0, 20, 140))
        self.level = level
    
    def update(self):
        self.move()

    def move(self):
        global GRAVITY
        gNorm = GRAVITY.normalize()

        keys = pygame.key.get_pressed()
        if GRAVITY:
            if keys[pygame.K_w] and self.canJump():
                self.vel.y -= self.jumpSpeed*dt()
        else:
            if keys[pygame.K_w]:
                self.vel.y -= self.speed*dt()
            if keys[pygame.K_s]:
                self.vel.y += self.speed*dt()
        if keys[pygame.K_a]:
            self.vel.x -= self.speed*dt()
        if keys[pygame.K_d]:
            self.vel.x += self.speed*dt()
        
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
                self.vel.x *= self.drag
            else:
                self.vel *= self.drag
        else:
            self.vel.xy = 0,0
    
    def checkCollide(self):
        for c in self.level.colliders:
            if self.rect.colliderect(c):
                return c
        return False
    
    def isJumpDir(x, y):
        if 
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
        self.render()
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
    
    def update(self):
        pass

    def render(self):
        s = len(self.data[0])*self.tileW
        self.image = pygame.Surface((s, s), pygame.SRCALPHA)
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
    # if random.randint(0, 234) == 160:
    #     randomGrav()
    pygame.display.flip()
