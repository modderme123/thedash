############################################
## INITIALIZING PLAYERS AND PYGAME SCREEN ##
############################################

import random
import pygame
from controller import *

pygame.init()
screen = pygame.display.set_mode((1000, 650))
background = pygame.Surface((1000, 650))
smallfont = pygame.font.SysFont('arial', 20)
medfont = pygame.font.SysFont('copperplate', 40)
largefont = pygame.font.SysFont('georgia', 60)

# DRAW BACKGROUND

colors = [(50, 200, 200), (250, 125, 0), (50, 50, 200), (50, 200, 50), (200, 50, 200)]

for j in range(151):
    for k in range(j % 2, 20, 2):
        pygame.draw.rect(background, (200, 200, 200), (j * 4, k * 4, 4, 4), 0)
title = pygame.image.load("assets/thedash.png").convert_alpha()
background.blit(title, (176, 5))
for j in range(5):
    pygame.draw.rect(background, (120, 120, 120), (42 + 120 * j, 77, 40, 540), 3)
pygame.draw.rect(background, (255, 215, 0), (2, 2, 600, 660), 5)
pygame.draw.rect(background, (255, 215, 0), (2, 77, 600, 30), 5)
pygame.draw.rect(background, (255, 215, 0), (122, 77, 120, 600), 5)
pygame.draw.rect(background, (255, 215, 0), (362, 77, 120, 600), 5)
pygame.draw.rect(background, (255, 215, 0), (2, 588, 600, 30), 5)
for j in range(5):
    text = medfont.render(names[players[j]], 1, colors[j], (0, 0, 0))
    background.blit(text, (630, 25 + 120 * j))


def display():
    screen.blit(background, (0, 0))
    for j in range(5):
        text = smallfont.render('$' + str(max(funds[j], 0)), 1, (255, 255, 255), (0, 0, 0))
        width = text.get_width()
        screen.blit(text, (120 * j + 62 - int(width / 2), 623))
    for j in range(5):
        for k in range(3):
            pygame.draw.circle(screen, colors[j], (23 + 39 * k + 120 * j, 603 - int(511 * positions[3 * j + k] / 100)), 8, 0)
            pygame.draw.circle(screen, (255, 255, 255), (23 + 39 * k + 120 * j, 603 - int(511 * positions[3 * j + k] / 100)), 9, 1)
            if rankings[3 * j + k] > 0:
                text = smallfont.render(str(rankings[3 * j + k]), 1, (255, 255, 255), (0, 0, 0))
                width = text.get_width()
                screen.blit(text, (120 * j + 39 * k + 22 - int(width / 2), 112))
    for j in range(5):
        text = largefont.render(str(teamscores[j]), 1, (200, 200, 200), (0, 0, 0))
        width = text.get_width()
        screen.blit(text, (850 - width, 55 + 120 * j))
    pygame.display.flip()
    pygame.event.pump()


##############################
## CONTROLLER RUNS THE RACE ##
##############################

display()

# GATHER BIDS, CLEAN UP VALUES

mainloop = True
while (funds[0] >= 0 or funds[1] >= 0 or funds[2] >= 0 or funds[3] >= 0 or funds[4] >= 0) and mainloop:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                break

    distances = [random.randint(10, 19), random.randint(20, 29), random.randint(30, 39)]

    bids = gatherBids(distances)

    (shortwinbid, shortindex), (mediumwinbid, mediumindex), (longwinbid, longindex) = winningBids(bids)

    # ADVANCE RUNNERS, DEBIT ACCOUNTS, ASSIGN RANKS AS RUNNERS FINISH
    increments = [0] * 15

    if longwinbid >= 0:
        index = int(longindex / 3)
        funds[index] -= longwinbid
        increments[longindex] = min(distances[2], 100 - positions[longindex])
    if mediumwinbid >= 0:
        index = int(mediumindex / 3)
        funds[index] -= mediumwinbid
        increments[mediumindex] = min(distances[1], 100 - positions[mediumindex])
    if shortwinbid >= 0:
        index = int(shortindex / 3)
        funds[index] -= shortwinbid
        increments[shortindex] = min(distances[0], 100 - positions[shortindex])

    for j in range(15):
        increments[j] = increments[j] / 100
    for _ in range(100):
        for j in range(15):
            positions[j] += increments[j]
        display()
    for j in range(15):
        positions[j] = int(positions[j] + 0.5)

    if longwinbid >= 0:
        index = int(longindex / 3)
        if positions[longindex] == 100 and rankings[longindex] == 0:
            rankings[longindex] = place
            place += 1
            if rankings[index * 3] > 0 and rankings[index * 3 + 1] > 0 and rankings[index * 3 + 2] > 0:
                funds[index] = -1
    if mediumwinbid >= 0:
        index = int(mediumindex / 3)
        if positions[mediumindex] == 100 and rankings[mediumindex] == 0:
            rankings[mediumindex] = place
            place += 1
            if rankings[index * 3] > 0 and rankings[index * 3 + 1] > 0 and rankings[index * 3 + 2] > 0:
                funds[index] = -1
    if shortwinbid >= 0:
        index = int(shortindex / 3)
        if positions[shortindex] == 100 and rankings[shortindex] == 0:
            rankings[shortindex] = place
            place += 1
            if rankings[index * 3] > 0 and rankings[index * 3 + 1] > 0 and rankings[index * 3 + 2] > 0:
                funds[index] = -1

    updateScores()

    display()
    pygame.time.wait(200)

pygame.quit()
printScores()
