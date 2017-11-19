from controller import *

scoresums = [0] * len(names)
for _ in range(100):
    game = Controller()

    while game.funds[0] >= 0 or game.funds[1] >= 0 or game.funds[2] >= 0 or game.funds[3] >= 0 or game.funds[4] >= 0:
        distances = [random.randint(10, 19), random.randint(20, 29), random.randint(30, 39)]

        game.gatherBids(distances)

        game.winningBids()

        game.instantAdvance(distances)

        game.updateScores()

    for j in range(5):
        scoresums[game.players[j]] += game.teamscores[j]

print("Sum of scores for all teams:")

ordered = sorted(zip(scoresums, names), reverse=True)
for score, name in ordered:
    print(name + ": " + str(score))
