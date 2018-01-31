# -*- coding: utf-8 -*-
import numpy as np
from random import randint
import time
#create board
board=np.zeros([10,10],int)
myboard=np.zeros([10,10],int)
shots=np.zeros([10,10],int)
#random positions of boats
boatlengths=[5,3,3,1,1]
newboats=np.zeros([10,10],int)
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
#        print(o)
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
    print('     0 1 2 3 4 5 6 7 8 9')
    print('    ---------------------')
    for j in range(10):
        print(j,'|', myboard[j])
    status=True
    while status:
        g=input('enter your position: ')
        g=g.split(',')
        if len(g)==2:
             gx=g[0]
             gy=g[1]
             try:
                 float(gx),float(gy)
                 gx=int(gx)
                 gy=int(gy)
                 if gx>=0 and gx<=9 and gy>=0 and gy<=9:
                     status=False
                 else:
                     print('coordinates must be 0-9')
                     continue
             except (ValueError, TypeError):
                 status=True
                 print('coordinates must be integers')
                 continue
        else:
            print('enter coordinates in the format y,x')
            continue
        x,y=gx,gy
#        coordinates to try
#        print(x,y)
#     create orientation
        stat=True
        while stat:
            o=input('enter orientation, 0 for vertical, 1 for horizontal: ')
            try:
                 float(o)
                 o=int(o)
                 if o==0 or o==1:
                     stat=False
                 else:
                     print('coordinates must be 0-9')
            except (ValueError, TypeError):
                 stat=True
                 print('coordinates must be integers')
            if o==0:
                if int(boatlengths[i])==5:
                    if x+2<=9 and x-2>=0 and myboard[x,y]==0 and myboard[x+1,y]==0 and myboard[x+2,y]==0 and myboard[x-1,y]==0 and myboard[x-2,y]==0:
                        myboard[x,y]=1
                        myboard[x+1,y]=1
                        myboard[x+2,y]=1
                        myboard[x-1,y]=1
                        myboard[x-2,y]=1
                        stat=False
                    else:
                        print('collision, try again')
                        continue
                elif int(boatlengths[i])==3:
                    if x+1<=9 and x-1>=0 and myboard[x,y]==0 and myboard[x+1,y]==0 and myboard[x-1,y]==0:
                        myboard[x,y]=1
                        myboard[x+1,y]=1
                        myboard[x-1,y]=1
                        stat=False
                    else:
                        print('collision, try again')
                        continue
                elif int(boatlengths[i])==1 and myboard[x,y]==0:
                    myboard[x,y]=1
                    stat=False
                else:
                    print('collision, try again')
                    continue
            if o==1:
                if int(boatlengths[i])==5:
                    if y+2<=9 and y-2>=0 and myboard[x,y]==0 and myboard[x,y+1]==0 and myboard[x,y+2]==0 and myboard[x,y-1]==0 and myboard[x,y-2]==0:
                        myboard[x,y+1]=1
                        myboard[x,y+2]=1
                        myboard[x,y-1]=1
                        myboard[x,y-2]=1
                        myboard[x,y]=1
                        stat=False
                    else:
                        print('collision, try again')
                        continue
                elif int(boatlengths[i])==3:
                    if y+1<=9 and y-1>=0 and myboard[x,y]==0 and myboard[x,y+1]==0 and myboard[x,y-1]==0:
                        myboard[x,y]=1
                        myboard[x,y+1]=1
                        myboard[x,y-1]=1
                        stat=False
                    else:
                        print('collision, try again')
                        continue
                elif int(boatlengths[i])==1 and myboard[x,y]==0:
                    myboard[x,y]=1
                    stat=False
                else:
                    print('collision, try again')
                    continue
            if stat==False:
                print('Placed')
            else:
                print('Fail')
print('Here are your ships...')
print('     0 1 2 3 4 5 6 7 8 9')
print('    ---------------------')
for k in range(10):
        print(k,'|', myboard[k])
#ask user for guess
print('Welcome, enter coodinates for shots in the format y,x')
time.sleep(2)
print('enter your first guess')
gamestate=True
while gamestate:
    co=True
    while co:
        g=input('enter your guess: ')
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
                 co=True
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
    if np.sum(board)==0:
        print('GAME OVER')
        gamestate=False

    else:
        remaining=int(np.sum(board))
        print('Ships remaining =', remaining)








    print('done')
    gamestate=False

#    if board[x,y]==0:
#        board[x,y]=1


#check for hit and report