from controller import *

game = Controller()
print("Positions at each stage in the race, followed by available funds:")
while any(x >= 0 for x in game.funds):
    game.setDistances()
    game.gatherBids()
    game.winningBids()
    game.instantAdvance()
    game.updateScores()
    print(game.positions, game.funds)

print()
game.printScores()
