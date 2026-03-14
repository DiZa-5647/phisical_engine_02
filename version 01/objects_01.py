import turtle
drawing=turtle.Turtle(visible=False)
turtle.tracer(0)
class AABB:
    def __init__(self, 
                 x=-200, 
                 y=0, 
                 width=100, 
                 height=100, 
                 dx=0.0, 
                 dy=0.0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.dx = dx
        self.dy = dy

    def left(self): return self.x - self.width/2
    def right(self): return self.x + self.width/2
    def bottom(self): return self.y - self.height/2
    def top(self): return self.y + self.height/2
    def center(self): return (self.x, self.y)

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

    def update(self):
        self.x += self.dx
        self.y += self.dy

    def goto(self, x, y):
        self.x = x
        self.y = y