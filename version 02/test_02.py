import pygame as pg
import math
import sys
from objects_02 import *

pg.init()

WIDTH, HEIGHT = 800, 600

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Phisical Engive v02")

clock = pg.time.Clock()
FPS = 60

g = 20

def intersection(a, b):
    if a.right() <= b.left() or b.right() <= a.left():
        return False
    
    if a.bottom() <= b.top() or b.bottom() <= a.top():
        return False
    
    return True

def pushout(a, b):
    friction = 0.75
    
    v1_x, v1_y = a.dx, a.dy
    v2_x, v2_y = b.dx, b.dy
    m1, m2 = a.mass, b.mass
    
    overlay_x = min(a.right(), b.right()) - max(a.left(), b.left())
    overlay_y = min(a.bottom(), b.bottom()) - max(a.top(), b.top())
    
    if overlay_x < overlay_y:
        dir = 1 if a.x < b.x else -1
        
        if not a.is_static and not b.is_static:
            a.x -= dir * (overlay_x / 2)
            b.x += dir * (overlay_x / 2)

            a.dx = friction * ((m1 - m2) * v1_x + 2 * m2 * v2_x) / (m1 + m2)
            b.dx = friction * ((m2 - m1) * v2_x + 2 * m1 * v1_x) / (m1 + m2)
        elif not a.is_static:
            a.x -= dir * overlay_x
            a.dx = -v1_x * friction
        elif not b.is_static:
            b.x += dir * overlay_x
            b.dx = -v2_x * friction
    else:
        dir = 1 if a.y < b.y else -1
        
        if not a.is_static and not b.is_static:
            a.y -= dir * (overlay_y / 2)
            b.y += dir * (overlay_y / 2)

            a.dy = friction * ((m1 - m2) * v1_y + 2 * m2 * v2_y) / (m1 + m2)
            b.dy = friction * ((m2 - m1) * v2_y + 2 * m1 * v1_y) / (m1 + m2)
        elif not a.is_static:
            a.y -= dir * overlay_y
            a.dy = -v1_y * friction
        elif not b.is_static:
            b.y += dir * overlay_y
            b.dy = -v2_y * friction
        

sq1=AABB(x=200, 
         y=300, 
         width=20, 
         height=20,
         mass=1,
         dx=160,
         dy=0.0, 
         color=(0,0,255))

sq2=AABB(x=400, 
         y=300, 
         width=40, 
         height=40,
         mass=2,
         dx=-80,
         dy=0.0,
         color=(0,255,0))

floor=AABB(x=0,
           y=600,
           width=1000,
           height=60)
floor.is_static = True

objs = [sq1, sq2, floor]

def update_scene(objects, dt):
    for obj in objects:
        obj.update(g, dt)
    
    for i in range(len(objects)):
        for j in range(i + 1, len(objects)):
            if intersection(objects[i], objects[j]):
                pushout(objects[i], objects[j])

    for obj in objects:
        obj.draw(screen)

running = True
while running:
    dt=clock.tick(FPS)/1000
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    screen.fill(BLACK)

    update_scene(objs, dt)

    pg.display.flip()
    clock.tick(FPS)

pg.quit()
sys.exit()