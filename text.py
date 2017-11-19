from controller import *

##############################
## CONTROLLER RUNS THE RACE ##
##############################

game = Controller()
print("Positions at each stage in the race, followed by available funds:")
while game.funds[0] >= 0 or game.funds[1] >= 0 or game.funds[2] >= 0 or game.funds[3] >= 0 or game.funds[4] >= 0:
    distances = [random.randint(10, 19), random.randint(20, 29), random.randint(30, 39)]

    game.gatherBids(distances)

    game.winningBids()

    game.instantAdvance(distances)

    game.updateScores()

    print(game.positions, game.funds)

print()
game.printScores()
