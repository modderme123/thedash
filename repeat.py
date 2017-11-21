from controller import names, Controller

scoresums = [0] * len(names)
for _ in range(2000):
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

ordered = sorted(zip(scoresums, names), reverse=True)
for score, name in ordered:
    print(name + ": " + str(score))
