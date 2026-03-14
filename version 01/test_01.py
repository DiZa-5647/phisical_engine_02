import turtle
from objects_01 import *
import time

def intersection(a,b):
    if a.right() < b.left() or b.right() < a.left():
        return False
    if a.top() < b.bottom() or b.top() < a.bottom():
        return False
    
    return True

def pushout(a,b):
    overlay_x = min(a.right(),b.right()) - max(a.left(), b.left())

    overlay_y = min(a.top(),b.top()) - max(a.bottom(), b.bottom())

    if overlay_x < overlay_y:
        if a.x < b.x:
            a.x -= overlay_x
        else:
            a.x += overlay_x
    else:
        if a.y < b.y:
            a.y -= overlay_y
        else:
            a.y += overlay_y

sq1=AABB(y=20,dx=0.05, dy=0.01)
sq2=AABB(x=0, y=0, width=150, height=150, dx=-0.04)
objects=[sq1,sq2]
def update_scene():
    drawing.clear()
    for a in objects:
        for b in objects:
            if a != b:
                if intersection(a,b):
                    pushout(a,b)
        a.update()

    for obj in objects:
        obj.draw()
    

while True:
    update_scene()
    turtle.update()
    # time.sleep(.01)
turtle.done()