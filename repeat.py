from controller import names, Controller

vals = []
for i in range(28, 34):
    for j in range(28, 34):
        for k in range(28, 34):
            vals.append([i, j, k])
#can be used for more in-deapth testing
#for i in range(20, 35):
#    vals.append([i, i, i])


scoresums = [0] * len(vals)
for _ in range(1000000):
    game = Controller(vals)
    while any(x >= 0 for x in game.funds):
        game.set_distances()
        game.gather_bids()
        game.winning_bids()
        game.instant_advance()
        game.update_scores()

    for j in range(5):
        scoresums[game.players[j]] += game.teamscores[j]

print("Sum of scores for all teams tested 100000 times:")

ordered = sorted(zip(scoresums, range(len(vals))), reverse=True)
for score, j in ordered:
    print("Equilizer " + str(vals[j]) + ": " + str(score))
