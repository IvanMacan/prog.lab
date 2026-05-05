import turtle

t = turtle.Turtle()
t.speed(0)

def petal(color):
    t.color(color)
    t.begin_fill()
    for _ in range(2):
        t.circle(50, 60)
        t.left(120)
    t.end_fill()

def flower(x, y, petal_color, center_color):
    t.penup()
    t.goto(x, y)
    t.pendown()

    for _ in range(6):
        petal(petal_color)
        t.left(60)

    t.penup()
    t.goto(x, y - 15)
    t.pendown()
    t.color(center_color)
    t.begin_fill()
    t.circle(15)
    t.end_fill()


flower(-150, 0, "red", "yellow")
flower(0, 0, "blue", "orange")
flower(150, 0, "purple", "yellow")

t.penup()

for x in [-150, 0, 150]:
    t.goto(x, -15)
    t.setheading(-90)
    t.pendown()
    t.color("green")
    t.forward(150)
    t.penup()

turtle.done()
