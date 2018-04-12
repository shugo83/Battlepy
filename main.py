import numpy as np
from random import randint
import time
import sys
import copy
from numpy import unravel_index


# Setup of globals

#board = np.zeros([10, 10], int)
#myboard = np.zeros([10, 10], int)
#compguess = np.zeros([10, 10], int)
#shots = np.zeros([10, 10], int)
#simlength = 1
#n = 10
#xa = np.array([[(i + j) % 2 for i in range(n)] for j in range(n)])
#
## random positions of boats
#boatlengths = [5, 4, 3, 3, 2]


# gocount = [None]*simlength    what is this


def setup():
    '''Generates all the game objects'''
    board = np.zeros([10, 10], int)
    myboard = np.zeros([10, 10], int)
    compguess = np.zeros([10, 10], int)
    shots = np.zeros([10, 10], int)
    newboats = np.zeros([10, 10], int)  # attempted generation locatations
    n = 10  # Board size
    xa = np.array([[(i + j) % 2 for i in range(n)] for j in range(n)])
    boatlengths = [5, 4, 3, 3, 2]
    return board, myboard, compguess, shots, xa, boatlengths, newboats


def comp_setup():
    goodguesslist = []  # list of hits
    badguesslist = []  # list of misses
    canguesslist = []  # list of not yet tried
    sunklist = []
    paritypdf = np.zeros([10, 10], int)
    pdfboard = np.zeros([10, 10], int)
    pdboard = np.zeros([10, 10], int)
    xg = []
    yg = []
#    precheck = 0
    return goodguesslist, badguesslist, canguesslist, sunklist, paritypdf, pdfboard, pdboard, xg, yg


def ask_if_sim():
    '''Determines if a player vs pc or pc vs pc game'''
    status_var = True
    while status_var:
        sim = input('Simulation? enter 0/1: ')
        try:
            sim = int(sim)
            if sim == 0 or sim == 1:
                status_var = False
        except (TypeError, ValueError):
            print('Enter 0 or 1')
    return sim


def ask_o():
    '''Determines orientation of ship'''
    status_var = True
    while status_var:
        o = input('enter orientation, 0 for vertical, 1 for horizontal: ')
        try:
            o = int(o)
        except (TypeError, ValueError):
            print('Enter 0 or 1')
        if o == 0 or o == 1:
            status_var = False
    return o


def ask_iter_count():
    '''Determines how many iterations to run'''
    status_var = True
    while status_var:
        simlength = input('how many iterations to run?: ')
        try:
            simlength = int(simlength)
            status_var = False
        except (TypeError, ValueError):
            print('Enter an integer')
    return simlength


def place_comp_ship(size, x, y, o):
    '''Place a computer ship on the board'''
    global board
    if o == 0:
        if size == 5:
                board[x, y] = 1
                board[x + 1, y] = 1
                board[x + 2, y] = 1
                board[x - 1, y] = 1
                board[x - 2, y] = 1
        elif size == 4:
                board[x, y] = 1
                board[x + 1, y] = 1
                board[x + 2, y] = 1
                board[x - 1, y] = 1
        elif size == 3:
                board[x, y] = 1
                board[x + 1, y] = 1
                board[x - 1, y] = 1
        elif size == 2:
                board[x, y] = 1
                board[x + 1, y] = 1
    if o == 1:
        if size == 5:
                board[x, y + 1] = 1
                board[x, y + 2] = 1
                board[x, y - 1] = 1
                board[x, y - 2] = 1
                board[x, y] = 1
        elif size == 4:
                board[x, y + 1] = 1
                board[x, y + 2] = 1
                board[x, y - 1] = 1
                board[x, y] = 1
        elif size == 3:
                board[x, y] = 1
                board[x, y + 1] = 1
                board[x, y - 1] = 1
        elif size == 2:
                board[x, y] = 1
                board[x, y + 1] = 1
    return board


def place_my_ship(size, x, y, o):
    global myboard
    if o == 0:
        if size == 5:
                myboard[x, y] = 1
                myboard[x + 1, y] = 1
                myboard[x + 2, y] = 1
                myboard[x - 1, y] = 1
                myboard[x - 2, y] = 1
        elif size == 4:
                myboard[x, y] = 1
                myboard[x + 1, y] = 1
                myboard[x + 2, y] = 1
                myboard[x - 1, y] = 1
        elif size == 3:
                myboard[x, y] = 1
                myboard[x + 1, y] = 1
                myboard[x - 1, y] = 1
        elif size == 2:
                myboard[x, y] = 1
                myboard[x + 1, y] = 1
    if o == 1:
        if size == 5:
                myboard[x, y + 1] = 1
                myboard[x, y + 2] = 1
                myboard[x, y - 1] = 1
                myboard[x, y - 2] = 1
                myboard[x, y] = 1
        elif size == 4:
                myboard[x, y + 1] = 1
                myboard[x, y + 2] = 1
                myboard[x, y - 1] = 1
                myboard[x, y] = 1
        elif size == 3:
                myboard[x, y] = 1
                myboard[x, y + 1] = 1
                myboard[x, y - 1] = 1
        elif size == 2:
                myboard[x, y] = 1
                myboard[x, y + 1] = 1
    return myboard

def random_place():
    '''Funtion to randomly place the ships ensureing that they do not collide
    or go off the board'''
    global boatlengths
    global board
    global newboats
    global sim
    for i in range(len(boatlengths)):
        placing = True
        while placing:
            x, y = randint(0, 9), randint(0, 9)  # location to try
            newboats[x, y] = 1
            o = randint(0, 1)  # create orientation

            if o == 0:
                if boatlengths[i] == 5:
                    if (x + 2 <= 9 and
                        x - 2 >= 0 and
                        board[x, y] == 0 and
                        board[x + 1, y] == 0 and
                        board[x + 2, y] == 0 and
                        board[x - 1, y] == 0 and
                        board[x - 2, y] == 0):

                        board = place_comp_ship((boatlengths[i]), x, y, o)
                        placing = False
                if int(boatlengths[i]) == 4:
                    if (x + 2 <= 9 and
                        x - 1 >= 0 and
                        board[x, y] == 0 and
                        board[x + 1, y] == 0 and
                        board[x + 2, y] == 0 and
                        board[x - 1, y] == 0):

                        board = place_comp_ship((boatlengths[i]), x, y, o)
                        placing = False
                elif int(boatlengths[i]) == 3:
                    if (x + 1 <= 9 and
                        x - 1 >= 0 and
                        board[x, y] == 0 and
                        board[x + 1, y] == 0 and
                        board[x - 1, y] == 0):

                        board = place_comp_ship((boatlengths[i]), x, y, o)
                        placing = False
                elif int(boatlengths[i]) == 2:
                    if (x + 1 <= 9 and
                        x >= 0 and
                        board[x, y] == 0 and
                        board[x + 1, y] == 0):

                        board = place_comp_ship((boatlengths[i]), x, y, o)
                        placing = False
            if o == 1:
                if int(boatlengths[i]) == 5:
                    if (y + 2 <= 9 and
                        y - 2 >= 0 and
                        board[x, y] == 0 and
                        board[x, y + 1] == 0 and
                        board[x, y + 2] == 0 and
                        board[x, y - 1] == 0 and
                        board[x, y - 2] == 0):

                        board = place_comp_ship((boatlengths[i]), x, y, o)
                        placing = False
                if int(boatlengths[i]) == 4:
                    if (y + 2 <= 9 and
                        y - 1 >= 0 and
                        board[x, y] == 0 and
                        board[x, y + 1] == 0 and
                        board[x, y + 2] == 0 and
                        board[x, y - 1] == 0):

                        board = place_comp_ship((boatlengths[i]), x, y, o)
                        placing = False
                elif int(boatlengths[i]) == 3:
                    if (y + 1 <= 9 and
                        y - 1 >= 0 and
                        board[x, y] == 0 and
                        board[x, y + 1] == 0 and
                        board[x, y - 1] == 0):

                        board = place_comp_ship((boatlengths[i]), x, y, o)
                        placing = False
                elif int(boatlengths[i]) == 2:
                    if (y + 1 <= 9 and
                        y >= 0 and
                        board[x, y] == 0 and
                        board[x, y + 1] == 0):

                        board = place_comp_ship((boatlengths[i]), x, y, o)
                        placing = False
            if sim == 0:
                if placing:
                    print('Fail')
                else:
                    print('Placed')
    print('All computer ships placed')
    return board, newboats


def ask_pos():
    valid = True
    while valid:
        g = input('enter position: ')

        if g == 'end':
            sys.exit()
        g = g.split(',')
        if len(g) == 2:
            gx = g[0]
            gy = g[1]
            try:
                float(gx), float(gy)
                gx = int(gx)
                gy = int(gy)
                if gx >= 0 and gx <= 9 and gy >= 0 and gy <= 9:
                    valid = False
                else:
                    print('coordinates must be 0-9')
            except (ValueError, TypeError):
                print('coordinates must be integers')
        else:
            print('enter coordinates in the format y,x')
    #        continue
    return gx, gy


def user_place():
    '''Allows player to place their ships on the board'''
    global boatlengths
    global myboard
    global sim
    for i in range(len(boatlengths)):
            k = i + 1
            print_my_board()
            status_pos = True
            while status_pos:
                x, y = ask_pos()
                o = ask_o()

                if o == 0:
                    if boatlengths[i] == 5:
                        if (x + 2 <= 9 and
                            x - 2 >= 0 and
                            myboard[x, y] == 0 and
                            myboard[x + 1, y] == 0 and
                            myboard[x + 2, y] == 0 and
                            myboard[x - 1, y] == 0 and
                            myboard[x - 2, y] == 0):

                            myboard = place_my_ship((boatlengths[i]), x, y, o)
                            status_pos = False
                    if int(boatlengths[i]) == 4:
                        if (x + 2 <= 9 and
                            x - 1 >= 0 and
                            myboard[x, y] == 0 and
                            myboard[x + 1, y] == 0 and
                            myboard[x + 2, y] == 0 and
                            myboard[x - 1, y] == 0):

                            myboard = place_my_ship((boatlengths[i]), x, y, o)
                            status_pos = False
                    elif int(boatlengths[i]) == 3:
                        if (x + 1 <= 9 and
                            x - 1 >= 0 and
                            myboard[x, y] == 0 and
                            myboard[x + 1, y] == 0 and
                            myboard[x - 1, y] == 0):

                            myboard = place_my_ship((boatlengths[i]), x, y, o)
                            status_pos = False
                    elif int(boatlengths[i]) == 2:
                        if (x + 1 <= 9 and
                            x >= 0 and
                            myboard[x, y] == 0 and
                            myboard[x + 1, y] == 0):

                            myboard = place_my_ship((boatlengths[i]), x, y, o)
                            status_pos = False
                if o == 1:
                    if int(boatlengths[i]) == 5:
                        if (y + 2 <= 9 and
                            y - 2 >= 0 and
                            myboard[x, y] == 0 and
                            myboard[x, y + 1] == 0 and
                            myboard[x, y + 2] == 0 and
                            myboard[x, y - 1] == 0 and
                            myboard[x, y - 2] == 0):

                            myboard = place_my_ship((boatlengths[i]), x, y, o)
                            status_pos = False
                    if int(boatlengths[i]) == 4:
                        if (y + 2 <= 9 and
                            y - 1 >= 0 and
                            myboard[x, y] == 0 and
                            myboard[x, y + 1] == 0 and
                            myboard[x, y + 2] == 0 and
                            myboard[x, y - 1] == 0):

                            myboard = place_my_ship((boatlengths[i]), x, y, o)
                            status_pos = False
                    elif int(boatlengths[i]) == 3:
                        if (y + 1 <= 9 and
                            y - 1 >= 0 and
                            myboard[x, y] == 0 and
                            myboard[x, y + 1] == 0 and
                            myboard[x, y - 1] == 0):

                            myboard = place_my_ship((boatlengths[i]), x, y, o)
                            status_pos = False
                    elif int(boatlengths[i]) == 2:
                        if (y + 1 <= 9 and
                            y >= 0 and
                            myboard[x, y] == 0 and
                            myboard[x, y + 1] == 0):

                            myboard = place_my_ship((boatlengths[i]), x, y, o)
                            status_pos = False
                if status_pos:
                    print('Collision detected, try again')
    print_my_board()
    return myboard


def print_my_board():
    '''Prints out the players board'''
    print('Here are your ships...')
    print('     0 1 2 3 4 5 6 7 8 9')
    print('    ---------------------')
    for k in range(10):
        print(k, '|', myboard[k])


def print_shots_board():
    '''Prints out locations of shots fired'''
    print('Here are your shots...')
    print('     0 1 2 3 4 5 6 7 8 9')
    print('    ---------------------')
    for k in range(10):
        print(k, '|', shots[k])


def shot_check(x, y):
    '''Checks to see if location is a hit or miss'''
    global board
    global shots

    if board[x, y] == 1:
        print('Hit!')
        shots[x, y] = 2
        board[x, y] = 0
    else:
        print('Miss!')
        shots[x, y] = 1
    return board, shots


def create_lists():
    '''Create lists used for guessing'''
    global compguess
    global goodguesslist
    global badguesslist
    global canguesslist
    global sunklist

    for x in range(10):
        for y in range(10):
            if compguess[x, y] == 2:
                goodguesslist.append([x, y])
            elif compguess[x, y] == 1:
                badguesslist.append([x, y])
            elif compguess[x, y] == 0:
                canguesslist.append([x, y])
            elif compguess[x, y] == 3:
                sunklist.append([x, y])
#    return goodguesslist, badguesslist, canguesslist, sunklist



    for t in range(0, 9):
        for r in range(0, 9):
            if t + 2 <= 9:
                if compguess[t, r] == 2 and compguess[t + 1, r] == 2:
                    trial = [t + 2, r]
                    if trial in canguesslist:
                        xg, yg= t + 2, r
                        guessing=False
#                                    print('line method1')
                        setco=1
                        continue
            if t-2>=0:
                if compguess[t,r]==2 and compguess[t-1,r]==2:
                    trial=[t-2,r]
                    if trial in canguesslist:
                        xg,yg=t-2,r
                        guessing=False
#                                    print('line method2')
                        setco=1
                        continue
            if r+2<=9:
                if compguess[t,r]==2 and compguess[t,r+1]==2:
                    trial=[t,r+2]
                    if trial in canguesslist:
                        xg,yg=t,r+2
                        guessing = False
#                                    print('line method3')
                        setco = 1
                        continue
            if r - 2 <= 9:
                if compguess[t, r] == 2 and compguess[t, r - 1] == 2:
                    trial = [t, r - 2]
                    if trial in canguesslist:
                        xg, yg = t, r - 2
                        guessing = False
#                                    print('line method4')
                        setco = 1
                        continue


def game():
#    global sim
    global board
    global myboard
    global shots
    global compguess
    global goodguesslist
    global badguesslist
    global canguesslist
    global sunklist
    global xg
    global yg
    global paritypdf
    global pdfboard
    global pdboard
    global gocount


    if sim == 0:
        print('')
        print('Welcome, enter coodinates for shots in the format y,x')
        print('hits are shown by 2, and misses by 1')
    else:
        myboard = board

    gamestate = True
    while gamestate:
        gx, gy = ask_pos()
        board, shots = shot_check(gx, gy)

        remaining = int(np.sum(board))
        print('Enemy ships remaining =', remaining)
        create_lists()
        guessing = True
        setco = 0
        count = -1

        while guessing:
            # if point is on board, check to see if there are 2 consecutive
            # hits and set next point equal to coordinates if so

            # TODO add point to list of predicted hits, and then choose most
            # likely with pdf
            for t in range(0, 9):
                for r in range(0, 9):
                    if t + 2 <= 9:
                        if compguess[t, r] == 2 and compguess[t + 1, r] == 2:
                            trial = [t + 2, r]
                            if trial in canguesslist:
                                xg, yg = t + 2, r
                                guessing = False
                                setco = 1
                                continue
                    if t - 2 >= 0:
                        if compguess[t, r] == 2 and compguess[t - 1, r] == 2:
                            trial = [t - 2, r]
                            if trial in canguesslist:
                                xg, yg = t - 2, r
                                guessing = False
                                setco = 1
                                continue
                    if r + 2 <= 9:
                        if compguess[t, r] == 2 and compguess[t, r + 1] == 2:
                            trial = [t, r + 2]
                            if trial in canguesslist:
                                xg, yg = t, r + 2
                                guessing = False
                                setco = 1
                                continue
                    if r - 2 <= 9:
                        if compguess[t, r] == 2 and compguess[t, r - 1] == 2:
                            trial = [t, r - 2]
                            if trial in canguesslist:
                                xg, yg = t, r - 2
                                guessing = False
                                setco = 1
                                continue
            if setco == 0:
                # i dont know what this does
                    count=count+1
                    ###this fails sometimes without try below
                    try:
                        xi,yi=goodguesslist[count][0],goodguesslist[count][1]
                    except IndexError:
                        zz=randint(0,(len(canguesslist)-1))
                        xi,yi=canguesslist[zz][0],canguesslist[zz][1]
                        break
                    trial=[xi+1,yi]
                    if trial in canguesslist:
                        if sim==0:
                            print('thinking...')
                        xg,yg=xi+1,yi
                        guessing=False
                        setco=1
                        perimg.append([xg,yg])
                        precheck=1
                        continue
                    ###exists on can guess list guessing =false
                    trial=[xi-1,yi]
                    if trial in canguesslist:
                        if sim==0:
                            print('thinking...')
                        xg,yg=xi-1,yi
                        guessing=False
                        setco=1
                        perimg.append([xg,yg])
                        precheck=1
                        continue
                    trial=[xi,yi+1]
                    if trial in canguesslist:
                        if sim==0:
                            print('thinking...')
                        xg,yg=xi,yi+1
                        guessing=False
                        setco=1
                        perimg.append([xg,yg])
                        precheck=1

                        continue
                    trial=[xi,yi-1]
                    if trial in canguesslist:
                        if sim==0:
                            print('thinking...')
                        xg,yg=xi,yi-1
                        guessing=False
                        setco=1
                        perimg.append([xg,yg])

                        continue
                #check to see if locations around xi,yi are on the good guess list, if they are then guessing=false and carry on - want to get rid of this. need to stop guessing to the sides of a known 2 or more h in a row as that is where most of goes are wasted.
        #if there are no hits or open ships do parity map


            if setco == 0:

#                paritypdf = np.zeros([10, 10], int)
#                pdfboard = np.zeros([10, 10], int)
#                pdboard = np.zeros([10, 10], int)

                # for each boat go throuhg all possible locations and append to pdf
                # if it fits
                for le in range(len(boatlengths)):
                    for i in range(0, 10):
                        for j in range(0, 10):
                            for k in range(boatlengths[le]):
                                if j + boatlengths[le] <= 10:
                                    pdboard[i, j + k] += 1
                            check = 0
                            for n in range(0, 10):
                                for m in range(0, 10):
                                    if pdboard[n, m] == 1:
                                        if compguess[n, m] != 0:
                                            check = 1
                            if check == 0:
                                pdfboard += pdboard
                            pdboard = np.zeros([10, 10], int)
                for le in range(len(boatlengths)):
                    for i in range(0, 10):
                        for j in range(0, 10):
                            for k in range(boatlengths[le]):
                                if i+boatlengths[le] <= 10:
                                    pdboard[i + k, j] += 1
                            check = 0
                            for n in range(0, 10):
                                for m in range(0, 10):
                                    if pdboard[n, m] == 1:
                                        if compguess[n, m] != 0:
                                            check = 1
                            if check == 0:
                                pdfboard += pdboard
                            pdboard = np.zeros([10, 10], int)
    #            for i in range(0, 10):
    #                for j in range(0, 10):
    #                    if xa[i, j] == 1:
    #                        paritypdf[i, j] = pdfboard[i, j]
                # vectorised form should be faster
                paritypdf = xa * pdfboard

                cos = unravel_index(paritypdf.argmax(), paritypdf.shape)
                xg = int(cos[0])
                yg = int(cos[1])
                guessing = False


        if sim == 0:
            print('Computer guess...', xg, ',', yg)

#        gocount[trialcount] += 1
        if myboard[xg, yg] == 1:
            if sim == 0:
                print('Your ship was hit')
            myboard[xg, yg] = 0
            compguess[xg, yg] = 2
        else:
            if sim == 0:
                print('Your ships are safe')
            compguess[xg, yg] = 1
#        print('     0 1 2 3 4 5 6 7 8 9')
#        print('    ---------------------')
#        for i in range(10):
#            print(i,'|', compguess[i])
        myremaining = int(np.sum(myboard))
        if sim == 0:
            print('You have ', myremaining, ' ships remaining')
        if sim == 1:
            remaining = myremaining
        if myremaining == 0 or remaining == 0:
            if sim == 0:
                if myremaining == 0:
                    print('You lose')
                elif remaining == 0:
                    print('You win')
                gamestate = False


board, myboard, compguess, shots, xa, boatlengths, newboats = setup()
goodguesslist, badguesslist, canguesslist, sunklist, paritypdf, pdfboard, pdboard, xg, yg = comp_setup()
sim = ask_if_sim()
if sim == 1:
    simlength = ask_iter_count()
else:
    myboard = user_place()
    simlength = 1
gocount = [None]*simlength
board, newboats = random_place()
game()
sys.exit()






















































for trialcount in range(0,simlength):
    print(trialcount)
    gocount[trialcount]=0
    board=np.zeros([10,10],int)
    myboard=np.zeros([10,10],int)
    compguess=np.zeros([10,10],int)
    shots=np.zeros([10,10],int)
    #boatlengths=[1]
    newboats=np.zeros([10,10],int)
    name5=np.zeros([10,10],int)
    name4=np.zeros([10,10],int)
    name3=np.zeros([10,10],int)
    name2=np.zeros([10,10],int)
    stat5=1
    stat4=1
    stat3=1
    stat2=1
    reduced=0
    perimg=[]
    precheck=0
    adjlist=0



    if sim==0:
        print('At any point during the game, type \'end\' to quit')
        print('0 indicates an empty location, 1 indicates a ship')
        time.sleep(2)
        print('Computer placing ships')
    for i in range(len(boatlengths)):
        status=True
        while status:
            x,y=randint(0,9),randint(0,9)
    #        coordinates to try
    #        print(x,y)
            newboats[x,y]=1
    #     create orientation
            o=randint(0,1)
    #        test if location is free and if so place object
            if o==0:
                if int(boatlengths[i])==5:
                    if x+2<=9 and x-2>=0 and board[x,y]==0 and board[x+1,y]==0 and board[x+2,y]==0 and board[x-1,y]==0 and board[x-2,y]==0:
                        board[x,y]=1
                        board[x+1,y]=1
                        board[x+2,y]=1
                        board[x-1,y]=1
                        board[x-2,y]=1
                        name5[x,y]=1
                        name5[x+1,y]=1
                        name5[x+2,y]=1
                        name5[x-1,y]=1
                        name5[x-2,y]=1
                        status=False
                if int(boatlengths[i])==4:
                    if x+2<=9 and x-1>=0 and board[x,y]==0 and board[x+1,y]==0 and board[x+2,y]==0 and board[x-1,y]==0:
                        board[x,y]=1
                        board[x+1,y]=1
                        board[x+2,y]=1
                        board[x-1,y]=1
                        name4[x,y]=1
                        name4[x+1,y]=1
                        name4[x+2,y]=1
                        name4[x-1,y]=1
                        status=False
                elif int(boatlengths[i])==3:
                    if x+1<=9 and x-1>=0 and board[x,y]==0 and board[x+1,y]==0 and board[x-1,y]==0:
                        board[x,y]=1
                        board[x+1,y]=1
                        board[x-1,y]=1
                        name3[x,y]=1
                        name3[x+1,y]=1
                        name3[x-1,y]=1
                        status=False
                elif int(boatlengths[i])==2:
                    if x+1<=9 and x>=0 and board[x,y]==0 and board[x+1,y]==0:
                        board[x,y]=1
                        board[x+1,y]=1
                        name2[x,y]=1
                        name2[x+1,y]=1
                        status=False
            if o==1:
                if int(boatlengths[i])==5:
                    if y+2<=9 and y-2>=0 and board[x,y]==0 and board[x,y+1]==0 and board[x,y+2]==0 and board[x,y-1]==0 and board[x,y-2]==0:
                        board[x,y+1]=1
                        board[x,y+2]=1
                        board[x,y-1]=1
                        board[x,y-2]=1
                        board[x,y]=1
                        name5[x,y+1]=1
                        name5[x,y+2]=1
                        name5[x,y-1]=1
                        name5[x,y-2]=1
                        name5[x,y]=1
                        status=False
                if int(boatlengths[i])==4:
                    if y+2<=9 and y-1>=0 and board[x,y]==0 and board[x,y+1]==0 and board[x,y+2]==0 and board[x,y-1]==0:
                        board[x,y+1]=1
                        board[x,y+2]=1
                        board[x,y-1]=1
                        board[x,y]=1
                        name4[x,y+1]=1
                        name4[x,y+2]=1
                        name4[x,y-1]=1
                        name4[x,y]=1
                        status=False
                elif int(boatlengths[i])==3:
                    if y+1<=9 and y-1>=0 and board[x,y]==0 and board[x,y+1]==0 and board[x,y-1]==0:
                        board[x,y]=1
                        board[x,y+1]=1
                        board[x,y-1]=1
                        name3[x,y]=1
                        name3[x,y+1]=1
                        name3[x,y-1]=1
                        status=False
                elif int(boatlengths[i])==2:
                    if y+1<=9 and y>=0 and board[x,y]==0 and board[x,y+1]==0:
                        board[x,y]=1
                        board[x,y+1]=1
                        name2[x,y]=1
                        name2[x,y+1]=1
                        status=False
            if sim==0:
                if status==False:
                    print('Placed')
                else:
                    print('Fail')
    name5a=copy.copy(name5)
    name99=copy.copy(name5)
    name4a=copy.copy(name4)
    name3a=copy.copy(name3)
    name2a=copy.copy(name2)
    if sim==0:
        print('Complete')
    #user input of ships
    if sim==0:
        for i in range(len(boatlengths)):
            k=i+1
            print('Boat number',k , 'with length = ', boatlengths[i])
            print('     0 1 2 3 4 5 6 7 8 9')
            print('    ---------------------')
            for j in range(10):
                print(j,'|', myboard[j])
            status=True
            while status:
                g=input('enter your position: ')
                if g=='end':
                    sys.exit()
                g=g.split(',')
                if len(g)==2:
                     gx=g[0]
                     gy=g[1]
                     try:
                         float(gx),float(gy)
                         gx=int(gx)
                         gy=int(gy)
                         if gx>=0 and gx<=9 and gy>=0 and gy<=9:
                             print(' ')
                         else:
                             print('coordinates must be 0-9')
                     except (ValueError, TypeError):
                         print('coordinates must be integers')
                         continue
                else:
                    print('enter coordinates in the format y,x')
                    continue
                x,y=gx,gy
        #        coordinates to try
        #        print(x,y)
        #     create orientation
                o=input('enter orientation, 0 for vertical, 1 for horizontal: ')
                if g=='end':
                    sys.exit()
                try:
                    float(o)
                    o=int(o)
                    if o==0 or o==1:
                        print(' ')
                    else:
                            print('orientation must be 0-1')
                except (ValueError, TypeError):
                    print('orientation must be an integer')
                if o==0:
                    if int(boatlengths[i])==5:
                        if x+2<=9 and x-2>=0 and myboard[x,y]==0 and myboard[x+1,y]==0 and myboard[x+2,y]==0 and myboard[x-1,y]==0 and myboard[x-2,y]==0:
                            myboard[x,y]=1
                            myboard[x+1,y]=1
                            myboard[x+2,y]=1
                            myboard[x-1,y]=1
                            myboard[x-2,y]=1
                            name5[x,y]=1
                            name5[x+1,y]=1
                            name5[x+2,y]=1
                            name5[x-1,y]=1
                            name5[x-2,y]=1
                            status=False
                        else:
                            print('collision, try again')
                            status=True
                    elif int(boatlengths[i])==4:
                        if x+2<=9 and x-1>=0 and myboard[x,y]==0 and myboard[x+1,y]==0 and myboard[x+2,y]==0 and myboard[x-1,y]==0:
                            myboard[x,y]=1
                            myboard[x+1,y]=1
                            myboard[x+2,y]=1
                            myboard[x-1,y]=1
                            name4[x,y]=1
                            name4[x+1,y]=1
                            name4[x+2,y]=1
                            name4[x-1,y]=1
                            status=False
                        else:
                            print('collision, try again')
                    elif int(boatlengths[i])==3:
                        if x+1<=9 and x-1>=0 and myboard[x,y]==0 and myboard[x+1,y]==0 and myboard[x-1,y]==0:
                            myboard[x,y]=1
                            myboard[x+1,y]=1
                            myboard[x-1,y]=1
                            name3[x,y]=1
                            name3[x+1,y]=1
                            name3[x-1,y]=1
                            status=False
                        else:
                            print('collision, try again')
                    elif int(boatlengths[i])==2:
                        if x+1<=9 and x>=0 and myboard[x,y]==0 and myboard[x+1,y]==0:
                            myboard[x,y]=1
                            myboard[x+1,y]=1
                            name2[x,y]=1
                            name2[x+1,y]=1
                            status=False
                        else:
                            print('collision, try again')
                if o==1:
                    if int(boatlengths[i])==5:
                        if y+2<=9 and y-2>=0 and myboard[x,y]==0 and myboard[x,y+1]==0 and myboard[x,y+2]==0 and myboard[x,y-1]==0 and myboard[x,y-2]==0:
                            myboard[x,y+1]=1
                            myboard[x,y+2]=1
                            myboard[x,y-1]=1
                            myboard[x,y-2]=1
                            myboard[x,y]=1
                            name5[x,y+1]=1
                            name5[x,y+2]=1
                            name5[x,y-1]=1
                            name5[x,y-2]=1
                            name5[x,y]=1
                            status=False
                        else:
                            print('collision, try again')
                    elif int(boatlengths[i])==4:
                        if y+2<=9 and y-1>=0 and myboard[x,y]==0 and myboard[x,y+1]==0 and myboard[x,y+2]==0 and myboard[x,y-1]==0:
                            myboard[x,y+1]=1
                            myboard[x,y+2]=1
                            myboard[x,y-1]=1
                            myboard[x,y]=1
                            name4[x,y+1]=1
                            name4[x,y+2]=1
                            name4[x,y-1]=1
                            name4[x,y]=1
                            status=False
                        else:
                            print('collision, try again')
                    elif int(boatlengths[i])==3:
                        if y+1<=9 and y-1>=0 and myboard[x,y]==0 and myboard[x,y+1]==0 and myboard[x,y-1]==0:
                            myboard[x,y]=1
                            myboard[x,y+1]=1
                            myboard[x,y-1]=1
                            name3[x,y]=1
                            name3[x,y+1]=1
                            name3[x,y-1]=1
                            status=False
                        else:
                            print('collision, try again')
                    elif int(boatlengths[i])==2:
                        if y+1<=9 and y>=0 and myboard[x,y]==0 and myboard[x,y+1]==0:
                            myboard[x,y]=1
                            myboard[x,y+1]=1
                            name2[x,y]=1
                            name2[x,y+1]=1
                            status=False
                        else:
                            print('collision, try again')
                if status==False:
                    print('Placed')
        print('Here are your ships...')
        print('     0 1 2 3 4 5 6 7 8 9')
        print('    ---------------------')
        for k in range(10):
                print(k,'|', myboard[k])
    #ask user for guess
    if sim==0:
        print('Welcome, enter coodinates for shots in the format y,x')
        print('hits are shown by 2, and misses by 1')
        time.sleep(2)
        print('enter your first guess')
    if sim==1:
        myboard=board

    gamestate=True
    while gamestate:
        co=True
        if sim==0:
            while co:
                g=input('enter your guess: ')
                if g=='end':
                    sys.exit()
                g=g.split(',')
                if len(g)==2:
                     gx=g[0]
                     gy=g[1]
                     try:
                         float(gx),float(gy)
                         gx=int(gx)
                         gy=int(gy)
                         if gx>=0 and gx<=9 and gy>=0 and gy<=9:
                             co=False
                         else:
                             print('coordinates must be 0-9')
                     except (ValueError, TypeError):
                             print('coordinates must be integers')
                     else:
                         print('enter coordinates in the format y,x')

            if board[gx,gy]==1:
                print('Hit!')
                shots[gx,gy]=2
                board[gx,gy]=0
            else:
                print('Miss!')
                shots[gx,gy]=1
            print('     0 1 2 3 4 5 6 7 8 9')
            print('    ---------------------')
            for i in range(10):
                print(i,'|', shots[i])
            remaining=int(np.sum(board))
            print('Enemy ships remaining =', remaining)
    #    computer guess logic
        goodguesslist=[] # list of hits
        badguesslist=[]  # list of misses
        canguesslist=[]  #list of not yet tried
        sunklist=[]
        precheck=0
#        if stat5==0:

        setco=0
        for x in range(10): # generating lists - keep
            for y in range(10):
                if compguess[x,y]==2:
                    goodguesslist.append([x,y])
                elif compguess[x,y]==1:
                    badguesslist.append([x,y])
                elif compguess[x,y]==0:
                    canguesslist.append([x,y])
                elif compguess[x,y]==3:
                    sunklist.append([x,y])

        if setco==0:
            guessing=True
            count=-1
            while guessing:
#                ####################################if2 or more values in a line =2 try next one .
                for t in range(0,9):
                    for r in range(0,9):
                        if t+2<=9:
                            if compguess[t,r]==2 and compguess[t+1,r]==2:
                                trial=[t+2,r]
                                if trial in canguesslist:
                                    xg,yg=t+2,r
                                    guessing=False
#                                    print('line method1')
                                    setco=1
                                    continue
                        if t-2>=0:
                            if compguess[t,r]==2 and compguess[t-1,r]==2:
                                trial=[t-2,r]
                                if trial in canguesslist:
                                    xg,yg=t-2,r
                                    guessing=False
#                                    print('line method2')
                                    setco=1
                                    continue
                        if r+2<=9:
                            if compguess[t,r]==2 and compguess[t,r+1]==2:
                                trial=[t,r+2]
                                if trial in canguesslist:
                                    xg,yg=t,r+2
                                    guessing=False
#                                    print('line method3')
                                    setco=1
                                    continue
                        if r-2<=9:
                            if compguess[t,r]==2 and compguess[t,r-1]==2:
                                trial=[t,r-2]
                                if trial in canguesslist:
                                    xg,yg=t,r-2
                                    guessing=False
#                                    print('line method4')
                                    setco=1
                                    continue
                ############################################################################
                if setco==0:
                    count=count+1
                    ###this fails sometimes without try below
                    try:
                        xi,yi=goodguesslist[count][0],goodguesslist[count][1]
                    except IndexError:
                        zz=randint(0,(len(canguesslist)-1))
                        xi,yi=canguesslist[zz][0],canguesslist[zz][1]
                        break
                    trial=[xi+1,yi]
                    if trial in canguesslist:
                        if sim==0:
                            print('thinking...')
                        xg,yg=xi+1,yi
                        guessing=False
                        setco=1
                        perimg.append([xg,yg])
                        precheck=1
                        continue
                    ###exists on can guess list guessing =false
                    trial=[xi-1,yi]
                    if trial in canguesslist:
                        if sim==0:
                            print('thinking...')
                        xg,yg=xi-1,yi
                        guessing=False
                        setco=1
                        perimg.append([xg,yg])
                        precheck=1
                        continue
                    trial=[xi,yi+1]
                    if trial in canguesslist:
                        if sim==0:
                            print('thinking...')
                        xg,yg=xi,yi+1
                        guessing=False
                        setco=1
                        perimg.append([xg,yg])
                        precheck=1

                        continue
                    trial=[xi,yi-1]
                    if trial in canguesslist:
                        if sim==0:
                            print('thinking...')
                        xg,yg=xi,yi-1
                        guessing=False
                        setco=1
                        perimg.append([xg,yg])

                        continue
                #check to see if locations around xi,yi are on the good guess list, if they are then guessing=false and carry on - want to get rid of this. need to stop guessing to the sides of a known 2 or more h in a row as that is where most of goes are wasted.
        #if there are no hits or open ships do parity map
        if setco==0:
#            print('parity guess')
            if stat2==0 and reduced==0:  ####in theory should help if 2 is not found last
#                n=10
#                xa=np.array([[(i+j)%2 for i in range(n)] for j in range(n)])
                reduced=1
#                print('reduced parity')
            paritypdf=np.zeros([10,10],int)
            pdfboard=np.zeros([10,10],int)
            pdboard=np.zeros([10,10],int)
            for le in range(len(boatlengths)):
                for i in range(0,10):
                    for j in range(0,10):
                        for k in range(boatlengths[le]):
                            if j+boatlengths[le]<=10:
                                pdboard[i,j+k]+=1
                        check=0
                        for n in range(0,10):
                            for m in range(0,10):
                                if pdboard[n,m]==1:
                                    if compguess[n,m]!=0:
                                        check=1
                        if check==0:
                            pdfboard+=pdboard
                        pdboard=np.zeros([10,10],int)
            for le in range(len(boatlengths)):
                for i in range(0,10):
                    for j in range(0,10):
                        for k in range(boatlengths[le]):
                            if i+boatlengths[le]<=10:
                                pdboard[i+k,j]+=1
                        check=0
                        for n in range(0,10):
                            for m in range(0,10):
                                if pdboard[n,m]==1:
                                    if compguess[n,m]!=0:
                                        check=1
                        if check==0:
                            pdfboard+=pdboard
                        pdboard=np.zeros([10,10],int)
            for i in range(0,10):
                for j in range(0,10):
                    if xa[i,j]==1:
                        paritypdf[i,j]=pdfboard[i,j]
            if setco==0:
                cos=unravel_index(paritypdf.argmax(),paritypdf.shape)
                xg=int(cos[0])
                yg=int(cos[1])
        #if there is a single hit, guess around that

        # end of guessing logic
        if sim==0:
            print('Computer guess...', xg,',',yg)
        gocount[trialcount]+=1
        if myboard[xg,yg]==1:
            if sim==0:
                print('Your ship was hit')
            myboard[xg,yg]=0
            compguess[xg,yg]=2
            name5[xg,yg]=0
            name4[xg,yg]=0
            name3[xg,yg]=0
            name2[xg,yg]=0
            if stat5==1:
                if int(np.sum(name5))==0:
                    stat5=0
#                    print('5sunk')
                    for kk in range(10):
                        for ll in range(10):
                            if name5a[kk,ll]==1:
                                compguess[kk,ll]=3
            if stat4==1:
                if int(np.sum(name4))==0:
                    stat4=0
#                    print('4sunk')
                    for i in range(10):
                        for j in range(10):
                            if name4a[i,j]==1:
                                compguess[i,j]=3
            if stat3==1:
                if int(np.sum(name3))==0: # or int(np.sum(name3))==3:
                    stat3=0
#                    print('3sunk')
                    for i in range(10):
                        for j in range(10):
                            if name3a[i,j]==1:
                                compguess[i,j]=3
            if stat2==1:
                if int(np.sum(name2))==0:
                    stat2=0
#                    print('2sunk')
                    for i in range(10):
                        for j in range(10):
                            if name2a[i,j]==1:
                                compguess[i,j]=3
        else:
            if sim==0:
                print('Your ships are safe')
            compguess[xg,yg]=1
#        print('     0 1 2 3 4 5 6 7 8 9')
#        print('    ---------------------')
#        for i in range(10):
#            print(i,'|', compguess[i])
        myremaining=int(np.sum(myboard))
        if sim==0:
            print('You have ',myremaining, ' ships remaining')
        if sim==1:
            remaining=myremaining
        if myremaining==0 or remaining==0:
            if sim==0:
                if myremaining==0:
                    print('You lose')
                elif remaining==0:
                    print('You win')
            gamestate=False
print(gocount)
np.savetxt('gamelengthsa.csv', gocount, delimiter=',', fmt='%s')