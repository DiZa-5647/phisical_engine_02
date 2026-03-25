import turtle
drawing=turtle.Turtle(visible=False)
from math import *
turtle.tracer(0)
class AABB:
    def __init__(self, 
                 x=-200, 
                 y=0, 
                 width=100, 
                 height=100, 
                 dx=0.0, 
                 dy=0.0,
                 direction=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.dx = dx
        self.dy = dy
        
        self.direction = direction*0.0174527777777

    def left(self): return self.x - self.width/2
    def right(self): return self.x + self.width/2
    def bottom(self): return self.y - self.height/2
    def top(self): return self.y + self.height/2
    def center(self): return (self.x, self.y)

    def func(self,i,d):
        Si=sin(i)
        Ci=cos(i)

        x=self.width*(abs(Si)**2)*(1 if Si>=0 else -1)
        y=self.height*(abs(Ci)**2)*(1 if Ci>=0 else -1)

        x_new = self.x+((x*cos(d)) - (y*sin(d)))
        y_new = self.y+((x*sin(d)) + (y*cos(d)))

        return (x_new, y_new)
        # return (x,y)

    def draw(self):
            drawing.penup()
            drawing.goto(self.left(),self.top())
            drawing.pendown()
            drawing.goto(self.right(),self.top())
            drawing.goto(self.right(),self.bottom())
            drawing.goto(self.left(),self.bottom())
            drawing.goto(self.left(),self.top())
            drawing.penup()
            drawing.goto(self.center())
            drawing.write(str(self.dx)+"; "+str(self.dy))

    def draw02(self):
        dir=self.direction
        drawing.penup()
        drawing.goto(self.func(0,dir))
        drawing.pendown()
        for i in range(0,361):
            res=self.func(0.0174527777777*i,dir)
            drawing.goto(res)
        drawing.penup()
        drawing.goto(self.center())
        drawing.write(str(self.dx)+"; "+str(self.dy))

    def update(self):
        self.x += self.dx
        self.y += self.dy

    def goto(self, x, y):
        self.x = x
        self.y = y