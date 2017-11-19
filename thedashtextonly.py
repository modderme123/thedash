############################################
## INITIALIZING PLAYERS AND PYGAME SCREEN ##
############################################
from controller import *

##############################
## CONTROLLER RUNS THE RACE ##
##############################

# GATHER BIDS, CLEAN UP VALUES

print("Positions at each stage in the race, followed by available funds:")
while funds[0] >= 0 or funds[1] >= 0 or funds[2] >= 0 or funds[3] >= 0 or funds[4] >= 0:
    distances = [random.randint(10, 19), random.randint(20, 29), random.randint(30, 39)]

    bids = gatherBids(distances)

    # DETERMINE WINNING BIDS FOR EACH DISTANCE

    (shortwinbid, shortindex), (mediumwinbid, mediumindex), (longwinbid, longindex) = winningBids(bids)

    # ADVANCE RUNNERS, DEBIT ACCOUNTS, ASSIGN RANKS AS RUNNERS FINISH

    if longwinbid >= 0:
        index = int(longindex / 3)
        funds[index] -= longwinbid
        positions[longindex] = min(positions[longindex] + distances[2], 100)
        if positions[longindex] == 100 and rankings[longindex] == 0:
            rankings[longindex] = place
            place += 1
            if rankings[index * 3] > 0 and rankings[index * 3 + 1] > 0 and rankings[index * 3 + 2] > 0:
                funds[index] = -1
    if mediumwinbid >= 0:
        index = int(mediumindex / 3)
        funds[index] -= mediumwinbid
        positions[mediumindex] = min(positions[mediumindex] + distances[1], 100)
        if positions[mediumindex] == 100 and rankings[mediumindex] == 0:
            rankings[mediumindex] = place
            place += 1
            if rankings[index * 3] > 0 and rankings[index * 3 + 1] > 0 and rankings[index * 3 + 2] > 0:
                funds[index] = -1
    if shortwinbid >= 0:
        index = int(shortindex / 3)
        funds[index] -= shortwinbid
        positions[shortindex] = min(positions[shortindex] + distances[0], 100)
        if positions[shortindex] == 100 and rankings[shortindex] == 0:
            rankings[shortindex] = place
            place += 1
            if rankings[index * 3] > 0 and rankings[index * 3 + 1] > 0 and rankings[index * 3 + 2] > 0:
                funds[index] = -1

    updateScores()

    print(positions, funds)

print()
printScores()
