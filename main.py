import numpy as np
from random import randint
import time
import sys
from numpy import unravel_index
import logging

format_string = '%(levelname)8s:\t%(message)s'
logging.basicConfig(format=format_string, level=logging.INFO)


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
    xg = 5
    yg = 5
#    precheck = 0
    return (goodguesslist, badguesslist, canguesslist, sunklist, paritypdf,
            pdfboard, pdboard, xg, yg)


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
    if sim ==0:
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
    goodguesslist = []
    badguesslist = []
    canguesslist = []

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
                        guessing = False
#                                    print('line method1')
                        setco = 1
                        continue
            if t - 2 >= 0:
                if compguess[t, r] == 2 and compguess[t - 1, r] == 2:
                    trial = [t - 2, r]
                    if trial in canguesslist:
                        xg, yg = t - 2, r
                        guessing = False
#                                    print('line method2')
                        setco = 1
                        continue
            if r + 2 <= 9:
                if compguess[t, r] == 2 and compguess[t, r + 1] == 2:
                    trial = [t, r + 2]
                    if trial in canguesslist:
                        xg, yg = t, r + 2
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
    '''The main game logic'''
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
    global goes

    goc = 0  # go counter

    if sim == 0:
        print('')
        print('Welcome, enter coodinates for shots in the format y,x')
        print('hits are shown by 2, and misses by 1')
    else:
        myboard = board

    gamestate = True
    while gamestate:
        if sim == 0:
            gx, gy = ask_pos()
            board, shots = shot_check(gx, gy)

        remaining = int(np.sum(board))
        if sim == 0:
            print('Enemy ships remaining =', remaining)
#        else:  # DEBUG ONLY
#            print('Enemy ships remaining =', remaining)
        create_lists()
        guessing = True
        setco = 0
        count = -1

        while guessing:
            goc = goc + 1  # TODO syntax
            # if point is on board, check to see if there are 2 adjacent
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
                # if point is on good guess list of hits, check to see if
                # adjacent points can be guessed
                while setco == 0 and count < len(goodguesslist):
                    count = count + 1
#                    print(count)
                    # this fails sometimes without try below
                    try:
                        xi, yi = (goodguesslist[count][0],
                                 goodguesslist[count][1])
                    except IndexError:
                        zz = randint(0, (len(canguesslist) - 1))
                        xi, yi = canguesslist[zz][0], canguesslist[zz][1]
                    trial = [xi + 1, yi]
                    if trial in canguesslist:
                        if sim == 0:
                            print('thinking...')
                        xg, yg = xi + 1, yi
                        guessing = False
                        setco = 1
#                        perimg.append([xg,yg])
                        precheck = 1

                    trial = [xi - 1, yi]
                    if trial in canguesslist:
                        if sim == 0:
                            print('thinking...')
                        xg, yg = xi - 1, yi
                        guessing = False
                        setco = 1
#                        perimg.append([xg,yg])
                        precheck = 1

                    trial = [xi, yi + 1]
                    if trial in canguesslist:
                        if sim == 0:
                            print('thinking...')
                        xg, yg = xi, yi + 1
                        guessing = False
                        setco = 1
#                        perimg.append([xg,yg])
                        precheck = 1

                    trial = [xi, yi - 1]
                    if trial in canguesslist:
                        if sim == 0:
                            print('thinking...')
                        xg, yg = xi, yi - 1
                        guessing = False
                        setco = 1
#                        perimg.append([xg,yg])


                #check to see if locations around xi,yi are on the good guess list, if they are then guessing=false and carry on - want to get rid of this. need to stop guessing to the sides of a known 2 or more h in a row as that is where most of goes are wasted.
        #if there are no hits or open ships do parity map


            if setco == 0:
#                print('parity method')
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
        myremaining = int(np.sum(myboard))
        if sim == 0:
            print('You have ', myremaining, ' ships remaining')
            print_shots_board()
        if sim == 1:
            remaining = myremaining

        if myremaining == 0 or remaining == 0:
            if sim == 0:
                if myremaining == 0:
                    print('You lose')
                elif remaining == 0:
                    print('You win')
                gamestate = False
            else:
                gamestate = False
    return goc


board, myboard, compguess, shots, xa, boatlengths, newboats = setup()
(goodguesslist, badguesslist, canguesslist, sunklist, paritypdf,
 pdfboard, pdboard, xg, yg) = comp_setup()
sim = ask_if_sim()
gocount = []

if sim == 1:
    simlength = ask_iter_count()
    gocount = []
    gocount = [None]*simlength
#    div = int(simlength / 25)
    tstart = time.time()
    for i in range(simlength):
        board, myboard, compguess, shots, xa, boatlengths, newboats = setup()
        (goodguesslist, badguesslist, canguesslist, sunklist, paritypdf,
         pdfboard, pdboard, xg, yg) = comp_setup()

        board, newboats = random_place()
        goes = game()
        gocount[i] = goes

        sys.stdout.write('\r')
        sys.stdout.write(
                '|%-25s| %d%%' % ('█'* int(25*i/simlength), 100*i/simlength))
        sys.stdout.flush()

    tend = time.time()
    sys.stdout.write('\r')
    average = sum(gocount) / float(simlength)
    time_per_game = (tend - tstart) / simlength
    print('Average of ' +
          str(round(average, 2)) +
          ' @ ' +
          str(round(time_per_game, 5)) +
          's per game')


else:
    myboard = user_place()
    simlength = 1
    gocount = [None]*simlength
    board, newboats = random_place()
    game()