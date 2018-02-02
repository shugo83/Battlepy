# -*- coding: utf-8 -*-
import numpy as np
from random import randint
import time
import sys
#create board
board=np.zeros([10,10],int)
myboard=np.zeros([10,10],int)
compguess=np.zeros([10,10],int)
shots=np.zeros([10,10],int)

#random positions of boats
boatlengths=[5,5,3,3,1]
#boatlengths=[1]
newboats=np.zeros([10,10],int)
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
                    status=False
            elif int(boatlengths[i])==3:
                if x+1<=9 and x-1>=0 and board[x,y]==0 and board[x+1,y]==0 and board[x-1,y]==0:
                    board[x,y]=1
                    board[x+1,y]=1
                    board[x-1,y]=1
                    status=False
            elif int(boatlengths[i])==1 and board[x,y]==0:
                board[x,y]=1
                status=False
        if o==1:
            if int(boatlengths[i])==5:
                if y+2<=9 and y-2>=0 and board[x,y]==0 and board[x,y+1]==0 and board[x,y+2]==0 and board[x,y-1]==0 and board[x,y-2]==0:
                    board[x,y+1]=1
                    board[x,y+2]=1
                    board[x,y-1]=1
                    board[x,y-2]=1
                    board[x,y]=1
                    status=False
            elif int(boatlengths[i])==3:
                if y+1<=9 and y-1>=0 and board[x,y]==0 and board[x,y+1]==0 and board[x,y-1]==0:
                    board[x,y]=1
                    board[x,y+1]=1
                    board[x,y-1]=1
                    status=False
            elif int(boatlengths[i])==1 and board[x,y]==0:
                board[x,y]=1
                status=False
        if status==False:
            print('Placed')
        else:
            print('Fail')
print('Complete')
#user input of ships
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
                    status=False
                else:
                    print('collision, try again')
                    status=True
            elif int(boatlengths[i])==3:
                if x+1<=9 and x-1>=0 and myboard[x,y]==0 and myboard[x+1,y]==0 and myboard[x-1,y]==0:
                    myboard[x,y]=1
                    myboard[x+1,y]=1
                    myboard[x-1,y]=1
                    status=False
                else:
                    print('collision, try again')
            elif int(boatlengths[i])==1 and myboard[x,y]==0:
                myboard[x,y]=1
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
                    status=False
                else:
                    print('collision, try again')
            elif int(boatlengths[i])==3:
                if y+1<=9 and y-1>=0 and myboard[x,y]==0 and myboard[x,y+1]==0 and myboard[x,y-1]==0:
                    myboard[x,y]=1
                    myboard[x,y+1]=1
                    myboard[x,y-1]=1
                    status=False
                else:
                    print('collision, try again')
            elif int(boatlengths[i])==1 and myboard[x,y]==0:
                myboard[x,y]=1
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
print('Welcome, enter coodinates for shots in the format y,x')
print('hits are shown by 2, and misses by 1')
time.sleep(2)
print('enter your first guess')
gamestate=True
while gamestate:
    co=True
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
    goodguesslist=[]
    badguesslist=[]
    canguesslist=[]
    for x in range(10):
        for y in range(10):
            if compguess[x,y]==2:
                goodguesslist.append([x,y])
            elif compguess[x,y]==1:
                badguesslist.append([x,y])
            elif compguess[x,y]==0:
                canguesslist.append([x,y])
    if len(goodguesslist)==0:
        initial=True
        while initial:
            xg,yg=randint(0,9),randint(0,9)
            tes=[xg+1,yg]
            if tes not in badguesslist:
                tes=[xg-1,yg]
                if tes not in badguesslist:
                    tes=[xg,yg+1]
                    if tes not in badguesslist:
                        tes=[xg,yg-1]
                        if tes not in badguesslist:
                            initial=False
    else:
        guessing=True
        count=-1
        while guessing:
            count=count+1 ###this fails sometimes without try below
            try:
                xi,yi=goodguesslist[count][0],goodguesslist[count][1]
            except IndexError:
                zz=randint(0,(len(canguesslist)-1))
                xi,yi=canguesslist[zz][0],canguesslist[zz][1]
            newg=xi+1
            trial=[newg,yi]
            if trial in canguesslist:
                print('thinking...')
                xg,yg=newg,yi
                guessing=False
                continue
            ###exists on can guess list guessing =false
            newg=xi-1
            trial=[newg,yi]
            if trial in canguesslist:
                print('thinking...')
                xg,yg=newg,yi
                guessing=False
                continue
            newg=yi+1
            trial=[xi,newg]
            if trial in canguesslist:
                print('thinking...')
                xg,yg=xi,newg
                guessing=False
                continue
            newg=yi-1
            trial=[xi,newg]
            if trial in canguesslist:
                print('thinking...')
                xg,yg=xi,newg
                guessing=False
                continue
            #check to see if locations around xi,yi are on the good guess list, if they are then guessing=false and carry on.
    print('Computer guess...', xg,',',yg)
    if myboard[xg,yg]==1:
        print('Your ship was hit')
        myboard[xg,yg]=0
        compguess[xg,yg]=2
    else:
        print('Your ships are safe')
        compguess[xg,yg]=1
    myremaining=int(np.sum(myboard))
    print('You have ',myremaining, ' ships remaining')
    if myremaining==0 or remaining==0:
        if myremaining==0:
            print('You lose')
        elif remaining==0:
            print('You win')
        gamestate=False