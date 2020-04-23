import turtle, random
import time
player = turtle.Turtle()
player.penup()
player.shape('turtle')

screen = turtle.Screen()
screen.title("Multiplying Game")
screen.tracer(0)
screen.bgcolor('teal')

allTurtles = [player]
bubbles = {}
def setupTurtleBubble(t, number):
    t.speed(0)
    t.ht()
    t.penup()
    intersecting = True
    while intersecting:
        t.goto(random.randint(-350,350), random.randint(-250,250))
        intersecting = False
        for turtle in allTurtles:
            if turtle.distance(t) < 75:
                intersecting = True

    stamp(t, number, "white")
    allTurtles.append(t)
    bubbles[t] = number

def stamp(t, number, color):
    t.clear()
    t.dot(50, color)
    back = 5
    if number > 99:
        back = 19
    elif number > 9:
        back = 12
    t.backward(back)
    t.right(90)
    t.forward(15)
    t.write(number, font=('arial', 18, 'normal'))
    t.backward(15)
    t.left(90)
    t.forward(back)

solutions = []
while len(solutions) < 10:
    num1 = random.randint(2,12)
    num2 = random.randint(2,12)
    sol = num1 * num2
    if sol not in solutions and sol > 12:
        t_num1 = turtle.Turtle()
        setupTurtleBubble(t_num1, num1)
        t_num2 = turtle.Turtle()
        setupTurtleBubble(t_num2, num2)
        t_sol = turtle.Turtle()
        setupTurtleBubble(t_sol, sol)
        solutions.append(sol)

turningRight = False
turningLeft = False
movingForward = False

def right():
    global turningRight
    turningRight = True
def right_release():
    global turningRight
    turningRight = False

def left():
    global turningLeft
    turningLeft = True
def left_release():
    global turningLeft
    turningLeft = False

def forward():
    global movingForward
    movingForward = True
def forward_release():
    global movingForward
    movingForward = False

screen.onkeypress(right, "Right")
screen.onkeypress(left, "Left")
screen.onkeypress(forward, "Up")
screen.onkeyrelease(right_release, "Right")
screen.onkeyrelease(left_release, "Left")
screen.onkeyrelease(forward_release, "Up")

screen.listen()

dummy = turtle.Turtle()
dummy.penup()
dummy.ht()

activated = {}



def isGroup():
    numbers = []
    for turtle in activated:
        numbers.append(activated[turtle])
    print(sum(i <= 12 for i in numbers))
    if sum(i <= 12 for i in numbers) == 2 and (numbers[0] == numbers[1] * numbers[2] or numbers[1] == numbers[0] * numbers[2] or numbers[2] == numbers[1] * numbers[0]):
        return True
    else:
        return False

def clearActivated():
    global activated
    for turtle in activated:
        turtle.clear()
        turtle.goto(1000,1000)
    activated = {}

def resetActivated():
    global activated
    for turtle in activated:
        stamp(turtle, activated[turtle], "red")
        screen.update()
        time.sleep(0.3)
    time.sleep(1)
    for turtle in activated:
        stamp(turtle, activated[turtle], "white")
        screen.update()
    activated = {}
    player.goto(0,0)


while True:
    screen.update()
    dummy.forward(1)
    if movingForward:
        player.forward(0.08 + (0.02 if turningLeft or turningRight else 0))
    if turningRight:
        player.right(0.08)
    if turningLeft:
        player.left(0.08)

    for turtle in bubbles:
        if player.distance(turtle) < 25 and turtle not in activated:
            stamp(turtle, bubbles[turtle], "green")
            activated[turtle] = bubbles[turtle]
            if len(activated) == 3 and isGroup():
                clearActivated()
            elif len(activated) == 3:
                resetActivated()
