import pygame
import numpy as np
import time
from datetime import datetime

pygame.init()
pygame.display.set_caption("Sudoku")

FONT=pygame.font.SysFont("comicsans",34)
BLACK=(0,0,0)
RED=(255,0,0)
WHITE=(255,255,255)
SILVER=(128,128,128)
BLUE=(0,0,255)

FONT2=pygame.font.SysFont("comicsans",80)

WIDTH=600
HEIGHT=600+66
WIN=pygame.display.set_mode((WIDTH,HEIGHT))
BOARD=[[7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]]

s=BOARD[:]

class Grid:
    def __init__(self,board,s,startTime,width=WIDTH,height=HEIGHT):
        self.width=width 
        self.height=height 
        self.board=board
        self.solution=dict()
        self.s=s
        self.startTime=startTime
    
    def solveBoard(self):
        for coord,val in self.s.items():
            i,j=coord 
            self.board[i][j]=val
    
    def validPos(self,row,col,val):
        for num in self.board[row]:
            if num==val:
                return False 
        for i in range(len(self.board)):
            if self.board[i][col]==val:
                return False 
        startRow=row//3*3
        startCol=col//3*3
        for i in range(startRow,startRow+3):
            for j in range(startCol,startCol+3):
                if self.board[i][j]==val:
                    return False 
        return True 
    
    def findEmpty(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j]==0:
                    return (i,j)
        return None
    
    def drawButton(self):
        pygame.draw.rect(WIN,BLUE,(470,600,100,60),4)
        t=FONT.render('SOLVE',1,(0,0,0))
        WIN.blit(t,(445+t.get_width()/2,620))
    
    def drawGrid(self):
        sepX=int(WIDTH/9) #66
        sepY=66 #int(HEIGHT/9)
        vLineCount=0
        xLineCount=0
        for i in range(0,HEIGHT+sepX,sepX):
            if  not vLineCount%3 and vLineCount!=9:
                pygame.draw.line(WIN,(0,0,0),(i,0),(i,HEIGHT-70),5)
                vLineCount+=1
                continue 
            else:
                pygame.draw.line(WIN,(0,0,0),(i,0),(i,HEIGHT-70))
                vLineCount+=1

        for j in range(0,HEIGHT+sepY,sepY):
            if not xLineCount%3 and xLineCount>0 and xLineCount<9:
                pygame.draw.line(WIN,(0,0,0),(0,j),(WIDTH,j),5)
                xLineCount+=1
                continue
            pygame.draw.line(WIN,(0,0,0),(0,j),(WIDTH,j))
            xLineCount+=1

    def fillGrid(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j]!=0 and type(self.board[i][j])==int:
                    s=str(self.board[i][j])
                    text=FONT.render(s,1,BLACK)
                    Pos=[i*66+33-text.get_width()/2,j*66+33-text.get_height()/2]
                    WIN.blit(text,(Pos[1],Pos[0]))
                
                elif type(self.board[i][j])==str:
                    s=self.board[i][j]
                    text=FONT.render(s,1,SILVER)
                    WIN.blit(text,(j*66+5,i*66+5))
    
    def addVal(self,mx,my):
        i,j,xPos,yPos=self.getIndices(mx,my)
        run=True
        while run:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                if event.type==pygame.MOUSEBUTTONDOWN:
                    mx,my=pygame.mouse.get_pos()
                    self.removeRect(xPos,yPos)
                    i,j,xPos,yPos=self.getIndices(mx,my)
                pygame.draw.rect(WIN,RED,(xPos,yPos,66,66),4)
                self.drawGrid()
                self.fillGrid()
                self.drawButton()
                pygame.display.update()
                if event.type==pygame.KEYDOWN and not self.valPresent(mx,my):
                    if event.key==pygame.K_1:
                        BOARD[j][i]=str(1)
                    if event.key==pygame.K_2:
                        BOARD[j][i]=str(2)
                    if event.key==pygame.K_3:
                        BOARD[j][i]=str(3)
                    if event.key==pygame.K_4:
                        BOARD[j][i]=str(4)
                    if event.key==pygame.K_5:
                        BOARD[j][i]=str(5)
                    if event.key==pygame.K_6:
                        BOARD[j][i]=str(6)
                    if event.key==pygame.K_7:
                        BOARD[j][i]=str(7)
                    if event.key==pygame.K_8:
                        BOARD[j][i]=str(8)
                    if event.key==pygame.K_9:
                        BOARD[j][i]=str(9)
                    if event.key==pygame.K_RETURN  and type(BOARD[j][i])==str:
                        if int(BOARD[j][i])==self.s[(j,i)]:
                            self.board[j][i]=int(self.board[j][i])
                        else:
                            self.drawX(xPos,yPos)
                            self.board[j][i]=0
                        
                    run=False
                
    def removeRect(self,x,y):
        pygame.draw.rect(WIN,WHITE,(x,y,90,90))
    
    def getIndices(self,mx,my):
        xPos=0
        yPos=0
        i=0
        j=0
        while xPos<mx:
            xPos+=66
            i+=1
        while yPos<my:
            yPos+=66
            j+=1
        xPos-=66
        i-=1
        yPos-=66
        j-=1
        return i,j,xPos,yPos
    
    def valPresent(self,mx,my):
        xPos=yPos=0
        i=j=0
        while xPos<mx:
            xPos+=66
            i+=1
        while yPos<my:
            yPos+=66 
            j+=1
        i-=1
        j-=1
        print(i,j,xPos,yPos)
        print(type(self.board[j][i]))
        if BOARD[j][i]!=0:
            if type(self.board[j][i])==str:
                return False
            if type(self.board[j][i])==int:
                return True
        return False

    def drawX(self,xPos,yPos):
        s=FONT2.render('X',1,RED)
        WIN.blit(s,(xPos,yPos))
        pygame.display.update()
        time.sleep(1)

def main():
    run=True
    grid=Grid(BOARD,s,datetime.now().time())
    while run:
        WIN.fill((255,255,255))
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False 
            if event.type==pygame.MOUSEBUTTONDOWN:
                mx,my=pygame.mouse.get_pos()
                if mx>=470 and mx<=570 and my>=600 and my<=690:
                    grid.solveBoard()
                else:
                    if not grid.valPresent(mx,my):
                        grid.addVal(mx,my)
        grid.drawGrid()
        grid.fillGrid()
        grid.drawButton()
        pygame.display.update()
            
    pygame.quit()

def solveBoard(board):
    vals={}
    sol={}
    for i in range(len(board)):
        for j in range(len(board[0])):
            vals[(i,j)]=board[i][j]
    _solve(board)
    for i in range(len(board)):
        for j in range(len(board[0])):
            sol[(i,j)]=board[i][j]
    for key in vals:
        i,j=key
        board[i][j]=vals[(i,j)]
    return sol

def _solve(board):
    empty=findEmpty(board)
    if not empty:
        return True
    row,col=empty
    for i in range(1,10):
        if validNumber(row,col,board,i):
            board[row][col]=i
            if _solve(board):
                return True 
            board[row][col]=0
    return False 

def findEmpty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j]==0:
                return (i,j)
    return False 

def validNumber(row,col,board,val):
    for num in board[row]:
        if num==val:
            return False
    for i in range(len(board)):
        if board[i][col]==val:
            return False
    startRow=(row//3)*3
    startCol=(col//3)*3 
    for i in range(startRow,startRow+3):
        for j in range(startCol,startCol+3):
            if board[i][j]==val:
                return False 
    return True



if __name__=='__main__':
    s=solveBoard(BOARD)
    main()
