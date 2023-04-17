import pygame
from pygame import Vector2 as Vec

WIDTH, HEIGHT = 500, 500
FPS = 60
GRAVSPEED = 15.8
GRAVDIRS = [Vec(x) for x in [ (0,-1), (0,1), (-1,0), (1,0) ]]

def now():
    return pygame.time.get_ticks()