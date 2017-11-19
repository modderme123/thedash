from controller import *

game = Controller()
print("Positions at each stage in the race, followed by available funds:")
while game.funds[0] >= 0 or game.funds[1] >= 0 or game.funds[2] >= 0 or game.funds[3] >= 0 or game.funds[4] >= 0:
    game.setDistances()
    game.gatherBids()
    game.winningBids()
    game.instantAdvance()
    game.updateScores()
    print(game.positions, game.funds)

print()
game.printScores()
