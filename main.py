import turtle, random
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import math
import numpy as np
import random

player = turtle.Turtle()
player.penup()
player.shape('turtle')

screen = turtle.Screen()
screen.title("Multiplying Game")
screen.tracer(0)
screen.bgcolor('teal')

allTurtles = [player]
bubbles = {}

NUM_SOLUTIONS = 2

''' data tracking containers '''
firstMove = True
startTime = 0

# track periods where user is inactive
inactivePeriods = []
lastInactive = -1


# not near turtles but switch right/left rapidly
unnecessaryChange = {}
unnecessaryChange["time"] = []
unnecessaryChange["frequency"] = []

# near turtles and switch right/left rapidly
dodgeChange = {}
dodgeChange["time"] = []
dodgeChange["frequency"] = []

lastLeft = 0
lastRight = 0


# incorrect answers because bad format. i.e. a 2,2,4 group
# math being right doesn't matter
incorrectAnswersDirections = 0
# incorrect answers because math wasn't right
# could also indicate bad planning
incorrectAnswersMath = 0


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
while len(solutions) < NUM_SOLUTIONS:
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


def roundDownNearest(x, factor):
    return int(math.floor(x / float(factor))) * factor

def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier


def checkSuddenDirectionChange(lastOppDirection):
    nearOtherTurtles = False
    for turtle in bubbles:
        if turtle.distance(player) <= 35:
            nearOtherTurtles = True
            break

    def addFreq(lst):
        timeBin = roundDownNearest(int(time.time() - startTime), 2)
        if timeBin not in lst["time"]:
            lst["time"].append(timeBin)
            lst["frequency"].append(1)
        else:
            lst["frequency"][lst["time"].index(timeBin)] += 1

    if nearOtherTurtles and time.time() - lastOppDirection < 1:
        addFreq(dodgeChange)
        return True
    elif time.time() - lastOppDirection < 1:
        addFreq(unnecessaryChange)
        return True
    return False

def checkInactivity():
    global lastInactive
    if lastInactive != -1 and time.time() - lastInactive > 2:
        timeBinStart = truncate(lastInactive - startTime, 1)
        timeBinEnd = truncate(time.time() - startTime, 1)

        inactivePeriods.append({"start": timeBinStart, "end": timeBinEnd})
        lastInactive = -1

def checkFirstMove():
    global firstMove, startTime
    if firstMove:
        firstMove = False
        startTime = time.time()

def right():
    global turningRight, lastLeft
    turningRight = True

    checkFirstMove()
    if checkSuddenDirectionChange(lastLeft):
        lastLeft = 0
    checkInactivity()

def right_release():
    global turningRight, lastInactive, lastRight
    turningRight = False
    lastInactive = time.time()
    lastRight = time.time()

def left():
    global turningLeft, lastRight
    turningLeft = True

    checkFirstMove()
    if checkSuddenDirectionChange(lastRight):
        lastRight = 0
    checkInactivity()

def left_release():
    global turningLeft, lastInactive, lastLeft
    turningLeft = False
    lastInactive = time.time()
    lastLeft - time.time()

def forward():
    global movingForward
    movingForward = True

    checkFirstMove()
    checkInactivity()

def forward_release():
    global movingForward, lastInactive
    movingForward = False
    lastInactive = time.time()

screen.onkeypress(right, "Right")
screen.onkeypress(left, "Left")
screen.onkeypress(forward, "Up")
screen.onkeyrelease(right_release, "Right")
screen.onkeyrelease(left_release, "Left")
screen.onkeyrelease(forward_release, "Up")

screen.listen()



activated = {}

def isGroup():
    global incorrectAnswersDirections, incorrectAnswersMath
    numbers = []
    for turtle in activated:
        numbers.append(activated[turtle])

    if sum(i <= 12 for i in numbers) == 2 and (numbers[0] == numbers[1] * numbers[2] or numbers[1] == numbers[0] * numbers[2] or numbers[2] == numbers[1] * numbers[0]):
        return True
    elif sum(i <= 12 for i in numbers) != 2:
        incorrectAnswersDirections += 1
    else:
        incorrectAnswersMath += 1

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
        time.sleep(0.2)
    time.sleep(0.5)
    for turtle in activated:
        stamp(turtle, activated[turtle], "white")
        screen.update()
    activated = {}
    player.goto(0,0)

score = 0
dummy = turtle.Turtle()
dummy.penup()
dummy.ht()

while score < NUM_SOLUTIONS:
    screen.update()
    dummy.forward(1)
    if movingForward:
        player.forward(0.1 + (0.02 if turningLeft or turningRight else 0))
    if turningRight:
        player.right(0.1)
    if turningLeft:
        player.left(0.1)

    for turtle in bubbles:
        if player.distance(turtle) < 25 and turtle not in activated:
            stamp(turtle, bubbles[turtle], "green")
            activated[turtle] = bubbles[turtle]
            if len(activated) == 3 and isGroup():
                clearActivated()
                score += 1
            elif len(activated) == 3:
                resetActivated()

endTime = time.time()
timeTaken = endTime - startTime

player.goto(0,0)
player.write("You WON!", font=("arial", 24, "normal"))
player.ht()
screen.update()
time.sleep(3)


periodStatus = {'time': [], 'active': []}
start = 0
for period in inactivePeriods:
    periodStart = int(period["start"] * 10)
    periodEnd = int(period["end"] * 10)

    for i in range(start, periodStart):
        periodStatus["time"].append(i/10.0)
        periodStatus["active"].append(1)
    for i in range(periodStart, periodEnd):
        periodStatus["time"].append(i/10.0)
        periodStatus["active"].append(0)

    start = periodEnd

for i in range(start, int(truncate(timeTaken, 1) * 10)):
        periodStatus["time"].append(i/10.0)
        periodStatus["active"].append(1)

print("Period Status: ")
print(periodStatus)
df = pd.DataFrame(data = periodStatus)
sns.lineplot(x="time", y="active", data=df)
plt.savefig('Period_Status.png')
plt.clf()

for i in range(0, int(timeTaken), 2):
    if i not in unnecessaryChange["time"]:
        unnecessaryChange["time"].append(i)
        unnecessaryChange["frequency"].append(0)
print("UNNECESSARY CHANGES: ")
print(unnecessaryChange)
df = pd.DataFrame(data = unnecessaryChange)
sns.lineplot(x="time", y="frequency", data=df)
plt.savefig('Unnecessary.png')
plt.clf()

for i in range(0, int(timeTaken), 2):
    if i not in dodgeChange["time"]:
        dodgeChange["time"].append(i)
        dodgeChange["frequency"].append(0)
print("DODGE CHANGES: ")
print(dodgeChange)
df = pd.DataFrame(data = dodgeChange)
sns.lineplot(x="time", y="frequency", data=df)
plt.savefig('Dodge.png')
plt.clf()

print("INCORRECT DIRECTIONS")
print(incorrectAnswersDirections)

print("INCORRECT MATH")
print(incorrectAnswersMath)

labels = ["Openness", "Conscientious", "Neuroticism", "Agreeableness", "Extraversion"]
stats = [random.randint(0,100) for i in range(5)]
angles=np.linspace(0, 2*np.pi, len(labels), endpoint=False)
stats=np.concatenate((stats,[stats[0]]))
angles=np.concatenate((angles,[angles[0]]))

fig=plt.figure()
ax = fig.add_subplot(111, polar=True)
ax.plot(angles, stats, 'o-', linewidth=2)
ax.fill(angles, stats, alpha=0.25)
ax.set_thetagrids(angles * 180/np.pi, labels)
ax.set_title("Skill Chart")
ax.grid(True)

plt.savefig('radar.png')
plt.clf()

