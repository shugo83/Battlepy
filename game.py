# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 08:50:28 2018

@author: shugo
"""

# -*- coding: utf-8 -*-
import numpy as np
from random import randint
import time
import sys
import copy
from numpy import unravel_index
#create board
board=np.zeros([10,10],int)
myboard=np.zeros([10,10],int)
compguess=np.zeros([10,10],int)
shots=np.zeros([10,10],int)
simlength=1
n = 10
xa=np.array([[(i+j)%2 for i in range(n)] for j in range(n)])

#random positions of boats
boatlengths=[5,4,3,3,2]
gocount=[None]*simlength
q=True
#sim=0
while q:
    sim=input('sim? 0 for no, 1 for yes: ')
    sim=int(sim)
    if sim==0 or sim==1:
        q=False
if sim==1:
    simlength=input('how many iterations to run?: ')
    simlength=int(sim)
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