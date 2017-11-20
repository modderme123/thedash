from controller import *

scoresums = [0] * len(names)
for _ in range(1000):
    game = Controller()
    while any(x >= 0 for x in game.funds):
        game.setDistances()
        game.gatherBids()
        game.winningBids()
        game.instantAdvance()
        game.updateScores()

    for j in range(5):
        scoresums[game.players[j]] += game.teamscores[j]

print("Sum of scores for all teams tested 1000 times:")

ordered = sorted(zip(scoresums, names), reverse=True)
for score, name in ordered:
    print(name + ": " + str(score))
