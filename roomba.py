from random import randint
from time import sleep
import os

#Set draw to True to print the grid while iterating; drawSpeed is the sleep time in seconds between frames
draw = False
drawSpeed = .1

rows, columns = 5,6
dirty = [[i,j] for i in range(rows) for j in range(columns)]
position = [0,0]
direction = [1,0]
seconds = 0

def reset():
    dirty = [[i,j] for i in range(rows) for j in range(columns)]
    position = (0,0)
    direction = [1,0]
    seconds = 0
def teleport():
    position = dirty[randint(0,len(dirty)-1)]
    direction = [[0,1],[0,-1],[1,0],[-1,0]][randint(0,3)]
    return(position, direction)
def drawFloor(dirtGrid,roomba,direction):
    floor = [[" · " for i in range(columns)] for j in range(rows)]
    dir = tuple(direction)
    avatar = {(0,1): ">", (0,-1): "<", (1,0): "V", (-1,0): "Λ"}
    for spot in dirtGrid:
        floor[spot[0]][spot[1]] = " # "
    floor[roomba[0]][roomba[1]] = f" {avatar[dir]} "
    print("\n".join(["".join(floor[i]) for i in range(len(floor))]),"\n")

def clean(position, direction):
    time = 0
    while position[0] > -1 and position[0] < rows and position[1] > -1 and position[1] < columns:
        time += 1
        if len(dirty) == 0:
            break
        if position in dirty:
            dirty.remove(position)
        if(draw):
            drawFloor(dirty,position,direction)
            sleep(drawSpeed)
        position = [sum(x) for x in zip(position, direction)]
    return time

results = []

#Runs one cycle of cleaning a floor and returns the number of cleaning steps (seconds)
def cycle():
    seconds = 0
    global position
    global direction
    global dirty
    seconds += clean(position, direction)
    while len(dirty) > 0:
        position, direction = teleport()
        seconds += clean(position, direction)
        # if draw: print(seconds)
    dirty = [[i,j] for i in range(rows) for j in range(columns)]
    position = (0,0)
    direction = [1,0]
    return seconds

#Log {runs} number of simulations, optionally logging each run length to trials.txt and returning the list of run lengths
def run(runs, log = False, returnRes = True):
    for i in range(runs):
        a = cycle()
        results.append(a)
        if draw: print(a)
        if (i+1) % (runs/10) == 0: print(f'Runs completed: {i+1} of {runs}')

    #Logs results in trials.txt as comma separated list of run lengths
    if log:
        with open(f'{os.getcwd()}/trials.txt',"a+") as output:
            output.write(",".join([str(i) for i in results]))
            output.write("\n")
    if returnRes: return results

#Reads from trials.txt to get the average run length
def average():
    with open(f"{os.getcwd()}/trials.txt","r") as runs:
        runs = runs.readlines()
        runs = [[int(i) for i in run.split(",")] for run in runs]
        a = []
        for run in runs: a.extend(run)
        print(f'Runs: {len(a):_}, Average: {sum(a)/len(a):.6f}')

# run(1, log = False)
# average()
a=run(1000, log=True)
print(f'Runs: {len(a):_}, Average: {sum(a)/len(a):.6f}')