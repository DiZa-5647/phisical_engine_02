import pygame as pg

class AABB:
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
        pg.draw.lines(surface, self.color, True, [(self.left(), self.top()),
                                             (self.right(), self.top()),
                                             (self.right(), self.bottom()),
                                             (self.left(), self.bottom())], width=2)
        pg.draw.circle(surface, 
                       (255,0,0), 
                       (self.center()[0]+self.center_dot_radius/2, self.center()[1]+self.center_dot_radius/2), 
                       self.center_dot_radius)
        
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