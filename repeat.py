from controller import names, Controller, vals

scoresums = [0] * len(vals)
for _ in range(10000):
    game = Controller()
    while any(x >= 0 for x in game.funds):
        game.set_distances()
        game.gather_bids()
        game.winning_bids()
        game.instant_advance()
        game.update_scores()

    for j in range(5):
        scoresums[game.players[j]] += game.teamscores[j]

print("Sum of scores for all teams tested 1000 times:")

ordered = sorted(zip(scoresums, range(len(vals))), reverse=True)
for score, j in ordered:
    print("Equilizer " + str(vals[j]) + ": " + str(score))
