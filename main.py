############################################
## INITIALIZING PLAYERS AND PYGAME SCREEN ##
############################################

import pygame
from controller import vals, Controller

game = Controller()

pygame.init()
screen = pygame.display.set_mode((1000, 650))
background = pygame.Surface((1000, 650))
smallfont = pygame.font.SysFont('arial', 20)
medfont = pygame.font.SysFont('copperplate', 30)
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
    text = medfont.render("Equilizer " + str(vals[game.players[j]]), 1, colors[j], (0, 0, 0))
    background.blit(text, (630, 25 + 120 * j))


def display():
    pygame.event.pump()
    screen.blit(background, (0, 0))
    for j in range(5):
        text = smallfont.render('$' + str(max(game.funds[j], 0)), 1, (255, 255, 255), (0, 0, 0))
        width = text.get_width()
        screen.blit(text, (120 * j + 62 - int(width / 2), 623))
    for j in range(5):
        for k in range(3):
            pygame.draw.circle(screen, colors[j], (23 + 39 * k + 120 * j, 603 - int(511 * game.positions[3 * j + k] / 100)), 8, 0)
            pygame.draw.circle(screen, (255, 255, 255), (23 + 39 * k + 120 * j, 603 - int(511 * game.positions[3 * j + k] / 100)), 9, 1)
            if game.rankings[3 * j + k] > 0:
                text = smallfont.render(str(game.rankings[3 * j + k]), 1, (255, 255, 255), (0, 0, 0))
                width = text.get_width()
                screen.blit(text, (120 * j + 39 * k + 22 - int(width / 2), 112))
    for j in range(5):
        text = largefont.render(str(game.teamscores[j]), 1, (200, 200, 200), (0, 0, 0))
        width = text.get_width()
        screen.blit(text, (850 - width, 55 + 120 * j))
    pygame.display.flip()


##############################
## CONTROLLER RUNS THE RACE ##
##############################

display()

# GATHER BIDS, CLEAN UP VALUES

mainloop = True
while any(x >= 0 for x in game.funds) and mainloop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                break

    game.set_distances()
    game.gather_bids()
    game.winning_bids()

    # ADVANCE RUNNERS, DEBIT ACCOUNTS, ASSIGN RANKS AS RUNNERS FINISH
    increments = [0] * 15

    for j in reversed(range(3)):
        if game.winbids[j] >= 0:
            index = int(game.winindex[j] / 3)
            game.funds[index] -= game.winbids[j]
            increments[game.winindex[j]] = min(game.distances[j], 100 - game.positions[game.winindex[j]]) / 100

    for _ in range(100):
        for j in range(15):
            game.positions[j] += increments[j]
        display()
    for j in range(15):
        game.positions[j] = int(game.positions[j] + 0.5)

    for j in reversed(range(3)):
        if game.winbids[j] >= 0:
            index = int(game.winindex[j] / 3)
            if game.positions[game.winindex[j]] == 100 and game.rankings[game.winindex[j]] == 0:
                game.rankings[game.winindex[j]] = game.place
                game.place += 1
                if all(x > 0 for x in game.rankings[index * 3:index * 3 + 3]):
                    game.funds[index] = -1

    game.update_scores()

    display()
    pygame.time.wait(200)

pygame.quit()
game.print_scores()
