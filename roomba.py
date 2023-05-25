from random import randint
from time import sleep
import os
import curses
import argparse

#parse a few command line arguments
parser = argparse.ArgumentParser(description="Run simulations of a standard Teleporting Roomba probelm", formatter_class=argparse.MetavarTypeHelpFormatter)
parser.add_argument('--draw', '-d', dest = 'draw', action = "store_true", help = "display roomba movement during simulation")
parser.add_argument('--speed', '-s', dest = 'drawSpeed', type = float, default = 75, help = "drawing refresh rate in ms (default 75ms)")
parser.add_argument('--log', '-l', dest = 'log', action = "store_true", help = "save the simulation runs to trials.txt")
parser.add_argument('--runs', '-r', dest = 'runs', type = int, default = 1, help = "number of simulation runs")
parser.add_argument('--dimensions', '-dim', dest = 'dimensions', nargs = 2, type = int, default = [5,6], help = 'floor dimensions (y x)')
args = parser.parse_args()

#Set draw to True to print the grid while iterating; drawSpeed is the sleep time in seconds between frames
draw = args.draw
drawSpeed = args.drawSpeed

#Set runs to the number of runs you want to do, typically one for display, more if you want to log data
runs = args.runs

#set log to True to save run data to trials.txt
log = args.log

rows, columns = tuple(args.dimensions)
dirty = [[i,j] for i in range(rows) for j in range(columns)]
position = [0,0]
direction = [1,0]
seconds = 0

# Initialize curses if we're drawing
if draw:
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    stdscr.keypad(True)


def teleport():
    position = dirty[randint(0,len(dirty)-1)]
    direction = [[0,1],[0,-1],[1,0],[-1,0]][randint(0,3)]
    return(position, direction)
def drawFloor(dirtGrid,roomba,direction):
    global stdscr
    floor = [["·" for i in range(columns)] for j in range(rows)]
    dir = tuple(direction)
    avatar = {(0,1): ">", (0,-1): "<", (1,0): "V", (-1,0): "Λ"}
    for spot in dirtGrid:
        floor[spot[0]][spot[1]] = "#"
    floor[roomba[0]][roomba[1]] = f"{avatar[dir]}"
    for i in range(len(floor)):
        for j in range(len(floor[0])):
            stdscr.addch(i,j,floor[i][j])
    #print("\n".join(["".join(floor[i]) for i in range(len(floor))]),"\n")

def clean(position, direction):
    time = 0
    global stdscr
    while position[0] > -1 and position[0] < rows and position[1] > -1 and position[1] < columns:
        time += 1
        if len(dirty) == 0:
            break
        if position in dirty:
            dirty.remove(position)
        if(draw):
            drawFloor(dirty,position,direction)
            stdscr.refresh()
            sleep(drawSpeed/1000)
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
        #if draw: print(a)
        #if (i+1) % (runs/10) == 0 and runs > 1000: print(f'Runs completed: {i+1} of {runs}')

    #Logs results in trials.txt as comma separated list of run lengths
    if log:
        with open(f'{os.getcwd()}/trials.txt',"a+") as output:
            output.write(",".join([str(i) for i in results]))
    if returnRes: return results

#Reads from trials.txt to get the average run length
def average():
    with open(f"{os.getcwd()}/trials.txt","r") as runs:
        runs = runs.readlines()
        runs = [[int(i) for i in run.split(",")] for run in runs]
        a = []
        for run in runs: a.extend(run)
        print(f'Runs: {len(a):_}, Average: {sum(a)/len(a):.6f}')

def main(scr):
    # run(1, log = False)
    # average()
    global stdscr
    stdscr = scr
    a=run(runs, log=log)
    message = f'Runs: {len(a):_}, Average: {sum(a)/len(a):.6f}'
    if draw:
        stdscr.addstr(rows,0,message + "\n\nPress any key to exit")
        stdscr.getch()
    else:
        print(message)

if __name__ == '__main__':
    try:
        curses.wrapper(main)
    finally:
        curses.echo()
        curses.nocbreak()
        curses.endwin()