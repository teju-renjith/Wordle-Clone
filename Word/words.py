import pandas as pd
import random
import os
import pygame
pygame.font.init()
from pygame.locals import *

words=pd.read_csv(os.path.join('Word',"5_letters.csv"))
row=random.randint(0,2499)
ITEM=words.iloc[row,0:]
item=""
for i in range(5):
    item=item+ITEM[i]

width=500
height=500+200
A=65
win=pygame.display.set_mode((width,height))
pygame.display.set_caption("WORDLE")
alpfont=pygame.font.SysFont('calibri',30)
boardfont=pygame.font.SysFont('consolas',80)  

line01=pygame.Rect(0,-5,width,10)
line02=pygame.Rect(-5,0,10,500)
line03=pygame.Rect(width-5,0,10,500)
line04=pygame.Rect(0,500-5,500,10)
line1=pygame.Rect(100-5,0,10,500)
line2=pygame.Rect(200-5,0,10,500)
line3=pygame.Rect(300-5,0,10,500)
line4=pygame.Rect(400-5,0,10,500)
line5=pygame.Rect(0,100-5,width,10)
line6=pygame.Rect(0,200-5,width,10)
line7=pygame.Rect(0,300-5,width,10)
line8=pygame.Rect(0,400-5,width,10)

enterbox=pygame.Rect(250+50,600,100,40)
clearbox=pygame.Rect(250-50-100,600,100,40)

lastbox=pygame.Rect(250-200,652,400,40)

letters=[]
startx=5
starty=510
gap=5

posx=0
posy=0
tempword=[]

gameover=0

for i in range(26):
    x=startx + (i%13)*37 + gap
    y=starty+(i//13)*37 + gap
    alp=A+i
    letters.append([x,y,chr(alp)])

def draw_win():

    win.fill((14,155,158))
    pygame.draw.rect(win,(0,115,115),line01)
    pygame.draw.rect(win,(0,115,115),line02)
    pygame.draw.rect(win,(0,115,115),line03)
    pygame.draw.rect(win,(0,115,115),line04)
    pygame.draw.rect(win,(0,115,115),line1)
    pygame.draw.rect(win,(0,115,115),line2)
    pygame.draw.rect(win,(0,115,115),line3)
    pygame.draw.rect(win,(0,115,115),line4)
    pygame.draw.rect(win,(0,115,115),line5)
    pygame.draw.rect(win,(0,115,115),line6)
    pygame.draw.rect(win,(0,115,115),line7)
    pygame.draw.rect(win,(0,115,115),line8)
    
    pygame.draw.rect(win,(0,75,75),enterbox)
    pygame.draw.rect(win,(0,75,75),clearbox)
    enter=alpfont.render("ENTER",1,(255,255,255))
    clear=alpfont.render("CLEAR",1,(255,255,255))
    win.blit(enter,(250+50+(100-enter.get_width())/2,600+8))
    win.blit(clear,(250-50-100+(100-clear.get_width())/2,600+8))

    pygame.draw.rect(win,(0,75,75),lastbox)

    for letter in letters:
        x,y,alphabet=letter
        box=pygame.Rect(x,y,35,35)
        pygame.draw.rect(win,(0,75,75),box)
        opalpha=alpfont.render(alphabet, 1, (255,255,255))
        win.blit(opalpha,(x+37/2-opalpha.get_width()/2,y+37/2-opalpha.get_height()/2))

    pygame.display.update()

def check_clear():
    global tempword,posx,posy
    X=posx-1
    Y=posy
    print(item)
    if len(tempword)!=0:
        box=pygame.Rect(X*100+5,Y*100+5,90,90)
        pygame.draw.rect(win,(14,155,158),box)
        pygame.display.update()
        tempword.pop()
        posx-=1

def check_enter():
    global posy,tempword
    global gameover
    count=0
    hashtable={}
    green_index=[]

    for i in range(5):
        if tempword[i].lower() == item[i]:
            q=item[i]
            green_index.append(i)
            count+=1
            if q in hashtable:
                hashtable[q]+=1
            else:
                hashtable[q]=1
            green=pygame.Rect(100*i+5,5+posy*100,90,90)
            pygame.draw.rect(win,(0,255,0),green)
            abc=boardfont.render(tempword[i],1,(255,255,255))
            win.blit(abc,(5+i*100+(90-abc.get_width())/2,5+posy*100+(90-abc.get_width())/2 - 10))

    if count==5:
        text=alpfont.render("YAY!",1,(255,255,255))  
        win.blit(text,(50+(400-text.get_width())/2,652+(40-text.get_height())/2))
        pygame.display.update()
        gameover=1
        return
            
    for i in range(5):

            if tempword[i].lower() in item:
                if i in green_index:
                    continue

                q=tempword[i].lower()
                if q in hashtable:
                    hashtable[q]+=1
                    if hashtable[q]>item.count(q):
                        pass
                    else:
                        yellow=pygame.Rect(100*i+5,5+posy*100,90,90)
                        pygame.draw.rect(win,(255,255,0),yellow)
                        abc=boardfont.render(tempword[i],1,(255,255,255))
                        win.blit(abc,(5+i*100+(90-abc.get_width())/2,5+posy*100+(90-abc.get_width())/2 - 10))
                else:
                    hashtable[q]=1
                    yellow=pygame.Rect(100*i+5,5+posy*100,90,90)
                    pygame.draw.rect(win,(255,255,0),yellow)
                    abc=boardfont.render(tempword[i],1,(255,255,255))
                    win.blit(abc,(5+i*100+(90-abc.get_width())/2,5+posy*100+(90-abc.get_width())/2 - 10))

    posy=posy+1
    posx=0
    tempword=[]

    if posy == 5 and count!=5:
        bla="Answer: "+item
        text=alpfont.render(bla,1,(255,255,255))  
        win.blit(text,(50+(400-text.get_width())/2,652+(40-text.get_height())/2))
        gameover=1
    
    pygame.display.update()


def click():
    global posx,posy,tempword
    x,y=pygame.mouse.get_pos()

    if (x > 300) and (x < 400):
        if (y > 600) and (y < 640) :
            if len(tempword)<5:
                text=alpfont.render("INCOMPLETE",1,(255,255,255))  
                win.blit(text,(50+(400-text.get_width())/2,652+(40-text.get_height())/2))
                pygame.display.update()
            else:
                check_enter()
                tempword=[]
                posx=0
    elif (x > 100) and (x < 200):
        if (y > 600) and (y < 640) :
            check_clear() 
    
    if x>10 and x<490 and y>515 and y<587:
        r = -1
        c = -1 

        for i in range(26):  
            if (x > startx + (i%13)*37 + gap) and (x < startx + (i%13)*37 + gap + 35):
                if (y > starty+(i//13)*37 + gap) and (y < starty+(i//13)*37 + gap + 35) :
                    c=i//13
                    r=i%13
        
        if posx==5:
            text=alpfont.render("FULL",1,(255,255,255))  
            win.blit(text,(50+(400-text.get_width())/2,652+(40-text.get_height())/2))
            pygame.display.update()
        else:
            Q=letters[r + 13*c][2]
            tempword.append(Q)

            abc=boardfont.render(Q,1,(255,255,255))
            win.blit(abc,(5+posx*100+(90-abc.get_width())/2,5+posy*100+(90-abc.get_width())/2 - 10))
            pygame.display.update()

            posx=posx+1

    else:
        pass

def restart():
    global item,posx,posy,tempword,gameover
    row=random.randint(0,2499)
    ITEM=words.iloc[row,0:]
    item=""
    for i in range(5):
        item=item+ITEM[i]
    posx=0
    posy=0
    tempword=[]
    draw_win()
    gameover=0
    main()
    

def main():

    clock=pygame.time.Clock()
    clock.tick(60)
    run=True
    draw_win()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == MOUSEBUTTONDOWN:
                pygame.draw.rect(win,(0,75,75),lastbox)
                click()
            if gameover==1:
                pygame.time.delay(1300)
                restart()

    pygame.quit()

    
if __name__=="__main__":
    main()
