import controller

GAME = controller.Controller()
print("Positions at each stage in the race, followed by available funds:")
while any(x >= 0 for x in GAME.funds):
    GAME.set_distances()
    GAME.gather_bids()
    GAME.winning_bids()
    GAME.instant_advance()
    GAME.update_scores()
    print(GAME.positions, GAME.funds)

print()
GAME.print_scores()
