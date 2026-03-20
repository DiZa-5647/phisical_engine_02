import pygame as pg
import math
import sys
import os
from objects_02 import *
from formuls import *

pg.init()

WIDTH, HEIGHT = 800, 600

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Physical Engine v02")

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

def load_texture(path):
    try:
        if os.path.exists(path):
            return pg.image.load(path).convert_alpha()
        else:
            print(f"Warning: Texture not found at {path}")
            placeholder = pg.Surface((32, 32))
            placeholder.fill((255, 0, 255))
            return placeholder
    except pg.error as e:
        print(f"Error loading texture {path}: {e}")
        placeholder = pg.Surface((32, 32))
        placeholder.fill((255, 0, 255))
        return placeholder

floor = AABB(x=0,
             y=HEIGHT - 60,
             width=WIDTH,
             height=60,
             mass=0,
             dx=0,
             dy=0,
             color=GREEN)
floor.is_static = True

objs = [floor]

script_dir = os.path.dirname(os.path.abspath(__file__))
textures_dir = os.path.join(script_dir, "textures")

category_1_nonactive = load_texture(os.path.join(textures_dir, "category_1_nonactive.png"))
category_2_nonactive = load_texture(os.path.join(textures_dir, "category_2_nonactive.png"))
category_3_nonactive = load_texture(os.path.join(textures_dir, "category_3_nonactive.png"))
category_1_active = load_texture(os.path.join(textures_dir, "category_1_active.png"))
category_2_active = load_texture(os.path.join(textures_dir, "category_2_active.png"))
category_3_active = load_texture(os.path.join(textures_dir, "category_3_active.png"))

textures = {
    1: {"active": category_1_active, "nonactive": category_1_nonactive},
    2: {"active": category_2_active, "nonactive": category_2_nonactive},
    3: {"active": category_3_active, "nonactive": category_3_nonactive}
}

ui = [(category_1_nonactive, (0, 0)), (category_2_nonactive, (32, 0)), (category_3_nonactive, (64, 0))]

def update_scene(objects, dt):
    for obj in objects:
        obj.update(g, dt)
    
    for i in range(len(objects)):
        for j in range(i + 1, len(objects)):
            if intersection(objects[i], objects[j]):
                pushout(objects[i], objects[j])
    
    for obj in objects:
        obj.draw(screen)

chosen_category = 0
x0, y0, x1, y1 = None, None, None, None
drawing = False

running = True
while running:
    dt = clock.tick(FPS) / 1000.0
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_1:
                chosen_category = 1
                ui[0] = (textures[1]["active"], (0, 0))
                ui[1] = (textures[2]["nonactive"], (32, 0))
                ui[2] = (textures[3]["nonactive"], (64, 0))
            elif event.key == pg.K_2:
                chosen_category = 2
                ui[0] = (textures[1]["nonactive"], (0, 0))
                ui[1] = (textures[2]["active"], (32, 0))
                ui[2] = (textures[3]["nonactive"], (64, 0))
            elif event.key == pg.K_3:
                chosen_category = 3
                ui[0] = (textures[1]["nonactive"], (0, 0))
                ui[1] = (textures[2]["nonactive"], (32, 0))
                ui[2] = (textures[3]["active"], (64, 0))
        
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                x0, y0 = event.pos
                drawing = True
        
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                x1, y1 = event.pos
                
                if x0 is not None and y0 is not None:
                    radius = distance2D(x0, y0, x1, y1)
                    
                    if chosen_category == 1:
                        try:
                            new_obj = AABB(x=x0+abs(x0-x1)/2,
                                           y=y0+abs(y0-y1)/2,
                                           width=abs(x1 - x0)/2,
                                           height=abs(y1 - y0)/2,
                                           mass=max(1, radius / 100),
                                           dx=0.1,
                                           dy=0.1,
                                           color=WHITE)
                            objs.append(new_obj)
                        except Exception as e:
                            print(f"Error creating object: {e}")
                    
                    elif chosen_category == 2:
                        try:
                            new_obj = Circle(x=x0,
                                             y=y0,
                                             radius=radius,
                                             mass=max(1, radius / 100),
                                             dx=0.1,
                                             dy=0.1,
                                             color=WHITE)
                            objs.append(new_obj)
                            pass
                        except Exception as e:
                            print(f"Error creating circle: {e}")
                
                x0, y0, x1, y1 = None, None, None, None
                drawing = False
    
    screen.fill(BLACK)
    
    if drawing and x0 is not None and y0 is not None:
        mouse_x, mouse_y = pg.mouse.get_pos()
        
        if chosen_category == 1:
            rect = pg.Rect(min(x0, mouse_x), min(y0, mouse_y), 
                          abs(mouse_x - x0), abs(mouse_y - y0))
            pg.draw.rect(screen, WHITE, rect, 2)
        elif chosen_category == 2:
            radius = distance2D(x0, y0, mouse_x, mouse_y)
            pg.draw.circle(screen, WHITE, (x0, y0), int(radius), 2)
    
    update_scene(objs, dt)
    
    for image, pos in ui:
        screen.blit(image, pos)
    
    font = pg.font.Font(None, 24)
    text = font.render(f"Objects: {len(objs)}", True, WHITE)
    screen.blit(text, (10, HEIGHT - 30))
    
    pg.display.flip()

pg.quit()
sys.exit()