import pygame as pg
from math import *

class AABB:
    def __init__(self, 
                 x = 0,
                 y = 0,
                 width = 1,
                 height = 1,
                 mass=1,
                 dx = 0.0,
                 dy = 0.0,
                 direction = 0,
                 color = (255,255,255)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.mass=mass
        self.dx = dx
        self.dy = dy
        self.color = color
        self.direction=0.0174527777777*direction

        self.center_dot_radius = 3

        self.is_static = False

        self.air_friction = 0.5

    def left(self): return self.x - self.width
    def right(self): return self.x + self.width
    def top(self): return self.y - self.height
    def bottom(self): return self.y + self.height
    def center(self): return (self.x, self.y)

    def func(self,i,d):
        Si=sin(i)
        Ci=cos(i)

        x=self.width*(abs(Si)**2)*(1 if Si>=0 else -1)
        y=self.height*(abs(Ci)**2)*(1 if Ci>=0 else -1)

        x_new = self.x+((x*cos(d)) - (y*sin(d)))
        y_new = self.y+((x*sin(d)) + (y*cos(d)))

        return (x_new, y_new)

    def update(self, g, dt):
        if not self.is_static:
            if self.dx > 0:
                self.dx = max(0, self.dx - self.air_friction * dt)
            elif self.dx < 0:
                self.dx = min(0, self.dx + self.air_friction * dt)

            self.x += self.dx * dt
            self.dy+=g
            self.y += self.dy * dt

    def draw2(self, surface):
        pg.draw.lines(surface, self.color, True, [(self.left(), self.top()),
                                             (self.right(), self.top()),
                                             (self.right(), self.bottom()),
                                             (self.left(), self.bottom())], width=2)
        pg.draw.circle(surface, 
                       (255,0,0), 
                       (self.center()[0]+self.center_dot_radius/2, self.center()[1]+self.center_dot_radius/2), 
                       self.center_dot_radius)
        
    def draw(self, surface):
        for i in range(0,361):
            res=self.func(i,self.direction)
            pg.draw.line(surface, self.color, (res[0],res[1]),(res[0],res[1]), width=3)
        
class Circle:
    def __init__(self,
                 x = 0,
                 y = 0,
                 radius = 1,
                 mass = 1,
                 dx = 0.0,
                 dy = 0.0,
                 color=(255,255,255)):
        self.x = x
        self.y = y
        self.radius = radius
        self.mass = mass
        self.dx = dx
        self.dy = dy
        self.color = color

        self.center_dot_radius = 3

        self.is_static = False

        self.air_friction = 0.5

    def left(self): return self.x - self.radius
    def right(self): return self.x + self.radius
    def top(self): return self.y - self.radius
    def bottom(self): return self.y + self.radius
    def center(self): return (self.x, self.y)

    def update(self, g, dt):
        if not self.is_static:
            if self.dx > 0:
                self.dx = max(0, self.dx - self.air_friction * dt)
            elif self.dx < 0:
                self.dx = min(0, self.dx + self.air_friction * dt)

            self.x += self.dx * dt
            self.dy+=g
            self.y += self.dy * dt

    def draw(self, surface):
        pg.draw.circle(surface, self.color, self.center(), self.radius, width=2)
        pg.draw.circle(surface, 
                    (255,0,0), 
                    (self.center()[0]+self.center_dot_radius/2, self.center()[1]+self.center_dot_radius/2), 
                    self.center_dot_radius)
        
class Triange:
    def __init__(self, 
                 x = 0,
                 y = 0,
                 width = 1,
                 height = 1,
                 mass=1,
                 dx = 0.0,
                 dy = 0.0,
                 color = (255,255,255)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.mass=mass
        self.dx = dx
        self.dy = dy
        self.color = color

        self.center_dot_radius = 3

        self.is_static = False

        self.air_friction = 0.5

    def left(self): return self.x - self.width
    def right(self): return self.x + self.width
    def top(self): return self.y - self.height
    def bottom(self): return self.y + self.height
    def center(self): return (self.x, self.y)

    def update(self, g, dt):
        if not self.is_static:
            if self.dx > 0:
                self.dx = max(0, self.dx - self.air_friction * dt)
            elif self.dx < 0:
                self.dx = min(0, self.dx + self.air_friction * dt)

            self.x += self.dx * dt
            self.dy+=g
            self.y += self.dy * dt

    def draw(self, surface):
        pg.draw.lines(surface, self.color, True, [(self.left(),self.bottom()),
                                                  (self.x,self.top()),
                                                  (self.right(),self.bottom())], width=2)