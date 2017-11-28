############################################
## INITIALIZING PLAYERS AND PYGAME SCREEN ##
############################################

import random,time
names = ['']*40
from drv import randomrunner
names[30] = "Random Runner"
from drv import offlikeashot
names[31] = "Off Like A Shot"
from drv import steadyfreddy
names[32] = "Steady Freddy"
from PeterV import Equilizer
names[0] = "Equilizer"
from PeterV import Skyrocket
names[1] = "Skyrocket"

def controller(num,mypos,myfunds,distances):
    if num == 30:
        return randomrunner(mypos,myfunds,distances)
    elif num == 31:
        return offlikeashot(mypos,myfunds,distances)
    elif num == 32:
        return steadyfreddy(mypos,myfunds,distances)
    elif num == 0:
        return Equilizer(mypos,myfunds,distances)
    elif num == 1:
        return Skyrocket(mypos,myfunds,distances)

players = [0]*5
players[0] = int(input("Enter the AI number for the first team: "))
players[1] = int(input("Enter the AI number for the second team: "))
players[2] = int(input("Enter the AI number for the third team: "))
players[3] = int(input("Enter the AI number for the fourth team: "))
players[4] = int(input("Enter the AI number for the fifth team: "))

place = 1
rankings = [0]*15
positions = [0]*15
funds = [1000000]*5
teamscores = [0]*5

import pygame
pygame.init()
screen = pygame.display.set_mode((1000,650))
background = pygame.Surface((1000,650))
smallfont = pygame.font.SysFont('arial', 20)
medfont = pygame.font.SysFont('copperplate', 40)
largefont = pygame.font.SysFont('georgia', 60)


## DRAW BACKGROUND

colors = [(50,200,200),(250,125,0),(50,50,200),(50,200,50),(200,50,200)]

for j in range(0,151):
    for k in range(j%2,20,2):
        pygame.draw.rect(background,(200,200,200),(j*4,k*4,4,4),0)
title = pygame.image.load("thedash.png").convert_alpha()
background.blit(title,(176,5))
for j in range(0,5):
    pygame.draw.rect(background,(120,120,120),(42+120*j,77,40,540),3)
pygame.draw.rect(background,(255,215,0),(2,2,600,660),5)
pygame.draw.rect(background,(255,215,0),(2,77,600,30),5)
pygame.draw.rect(background,(255,215,0),(122,77,120,600),5)
pygame.draw.rect(background,(255,215,0),(362,77,120,600),5)
pygame.draw.rect(background,(255,215,0),(2,588,600,30),5)
for j in range(0,5):
    text = medfont.render(names[players[j]],1,colors[j],(0,0,0))
    background.blit(text,(630,25+120*j))

def display():
    screen.blit(background, (0,0))
    for j in range(0,5):
        text = smallfont.render('$'+str(max(funds[j],0)),1,(255,255,255),(0,0,0))
        width = text.get_width()
        screen.blit(text,(120*j+62-int(width/2),623))
    for j in range(0,5):
        for k in range(0,3):
            pygame.draw.circle(screen,colors[j],(23+39*k+120*j,603-int(511*positions[3*j+k]/100)),8,0)
            pygame.draw.circle(screen,(255,255,255),(23+39*k+120*j,603-int(511*positions[3*j+k]/100)),9,1)
            if rankings[3*j+k]>0:
                text = smallfont.render(str(rankings[3*j+k]),1,(255,255,255),(0,0,0))
                width = text.get_width()
                screen.blit(text,(120*j+39*k+22-int(width/2),112))
    for j in range(0,5):
        text = largefont.render(str(teamscores[j]),1,(200,200,200),(0,0,0))
        width = text.get_width()
        screen.blit(text,(850-width,55+120*j))
    pygame.display.flip()


##############################
## CONTROLLER RUNS THE RACE ##
##############################

display()
pygame.time.wait(500)

## GATHER BIDS, CLEAN UP VALUES
mainloop = True

while (funds[0]>=0 or funds[1]>=0 or funds[2]>=0 or funds[3]>=0 or funds[4]>=0) and mainloop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False
                
    bids = []
    distances = [random.randint(10,19),random.randint(20,29),random.randint(30,39)]
    for j in range(0,5):
        if funds[j] >= 0:
            mypos,myfunds = positions[:],funds[:]
            myfunds[0],myfunds[j] = myfunds[j],myfunds[0]
            mypos[0:3],mypos[3*j:3*j+3] = mypos[3*j:3*j+3],mypos[0:3]
            mybids = controller(players[j],mypos,myfunds,distances)
            total = 0
            for k in range(0,3):
                value = max(int(mybids[k][1]),0)
                total += value
                if total <= funds[j]:
                    mybids[k][1] = value
                else:
                    total -= value
                    mybids[k][1] = 0
                if rankings[3*j+k]>0:
                    mybids[k][1] = -1                
                if mybids[k][0] not in ['short','medium','long']:
                    mybids[k][0] = 'short'
            bids += mybids
        else:
            bids += 3*[['short',-1]]


## DETERMINE WINNING BIDS FOR EACH DISTANCE
    
    shortwinbid,mediumwinbid,longwinbid = -1,-1,-1
    for j in range(0,15):
        if bids[j][0] == 'short':
            if bids[j][1] > shortwinbid:
                shortwinbid = bids[j][1]
                shortindex = j
        elif bids[j][0] == 'medium':
            if bids[j][1] > mediumwinbid:
                mediumwinbid = bids[j][1]
                mediumindex = j
        else:
            if bids[j][1] > longwinbid:
                longwinbid = bids[j][1]
                longindex = j


## ADVANCE RUNNERS, DEBIT ACCOUNTS, ASSIGN RANKS AS RUNNERS FINISH

    increments = [0]*15

    if longwinbid >= 0:
        index = int(longindex/3)
        funds[index] -= longwinbid
        increments[longindex] = min(distances[2],100-positions[longindex])
    if mediumwinbid >= 0:
        index = int(mediumindex/3)
        funds[index] -= mediumwinbid
        increments[mediumindex] = min(distances[1],100-positions[mediumindex])
    if shortwinbid >= 0:
        index = int(shortindex/3)
        funds[index] -= shortwinbid
        increments[shortindex] = min(distances[0],100-positions[shortindex])

    for j in range(0,15):
        increments[j] = increments[j]/100
    for k in range(0,100):
        pygame.event.get()
        for j in range(0,15):
            positions[j] += increments[j]
        display()
    for j in range(0,15):
        positions[j] = int(positions[j]+0.5)

    if longwinbid >= 0:
        index = int(longindex/3)
        if positions[longindex]==100 and rankings[longindex]==0:
            rankings[longindex] = place
            place += 1
            if rankings[index*3]>0 and rankings[index*3+1]>0 and rankings[index*3+2]>0:
                funds[index] = -1
    if mediumwinbid >= 0:
        index = int(mediumindex/3)
        if positions[mediumindex]==100 and rankings[mediumindex]==0:
            rankings[mediumindex] = place
            place += 1
            if rankings[index*3]>0 and rankings[index*3+1]>0 and rankings[index*3+2]>0:
                funds[index] = -1
    if shortwinbid >= 0:
        index = int(shortindex/3)
        if positions[shortindex]==100 and rankings[shortindex]==0:
            rankings[shortindex] = place
            place += 1
            if rankings[index*3]>0 and rankings[index*3+1]>0 and rankings[index*3+2]>0:
                funds[index] = -1

    for j in range(0,5):
        score = 0
        for k in range(0,3):
            if rankings[3*j+k] > 0:
                score += 100-(rankings[3*j+k]*(rankings[3*j+k]-1))/2
        teamscores[j] = int(score)

    display()
    pygame.time.wait(200)


################################################
## USER WILL PRESS ESC TO CLOSE PYGAME WINDOW ##
################################################


pygame.display.flip()
while mainloop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False
pygame.quit()
