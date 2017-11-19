import random

from src.drv import *
from src.petermilo import *

names = [''] * 40
# DRV
names[0] = "Random Runner"
names[1] = "Off Like A Shot"
names[2] = "Steady Freddy"
# PETERMILO
names[3] = "Equilizer"
names[4] = "Skyrocket"
names[5] = "RandomEquilizer"


def controller(num, mypos, myfunds, distances):
    if num == 0:
        return randomrunner(mypos, myfunds, distances)
    elif num == 1:
        return offlikeashot(mypos, myfunds, distances)
    elif num == 2:
        return steadyfreddy(mypos, myfunds, distances)
    elif num == 3:
        return Equilizer(mypos, myfunds, distances)
    elif num == 4:
        return Skyrocket(mypos, myfunds, distances)
    elif num == 5:
        return RandomEquilizer(mypos, myfunds, distances)


players = random.sample(range(6), 5)

place = 1
rankings = [0] * 15
positions = [0] * 15
funds = [1000000] * 5
teamscores = [0] * 5


def gatherBids(distances):
    bids = []
    for j in range(5):
        if funds[j] >= 0:
            mypos, myfunds = positions[:], funds[:]
            myfunds[0], myfunds[j] = myfunds[j], myfunds[0]
            mypos[0:3], mypos[3 * j:3 * j + 3] = mypos[3 * j:3 * j + 3], mypos[0:3]
            mybids = controller(players[j], mypos, myfunds, distances)
            total = 0
            for k in range(3):
                value = max(int(mybids[k][1]), 0)
                total += value
                if total <= funds[j]:
                    mybids[k][1] = value
                else:
                    total -= value
                    mybids[k][1] = 0
                if rankings[3 * j + k] > 0:
                    mybids[k][1] = -1
                if mybids[k][0] not in ['short', 'medium', 'long']:
                    mybids[k][0] = 'short'
            bids += mybids
        else:
            bids += 3 * [['short', -1]]
    return bids


def winningBids(bids):
    shortwinbid, mediumwinbid, longwinbid = -1, -1, -1
    shortindex, mediumindex, longindex = -1, -1, -1
    for j in range(15):
        if bids[j][0] == 'short':
            if bids[j][1] > shortwinbid:
                shortwinbid = bids[j][1]
                shortindex = j
        elif bids[j][0] == 'medium':
            if bids[j][1] > mediumwinbid:
                mediumwinbid = bids[j][1]
                mediumindex = j
        else:
            if bids[j][1] > longwinbid:
                longwinbid = bids[j][1]
                longindex = j

    return (shortwinbid, shortindex), (mediumwinbid, mediumindex), (longwinbid, longindex)


def updateScores():
    for j in range(5):
        score = 0
        for k in range(3):
            if rankings[3 * j + k] > 0:
                score += 100 - (rankings[3 * j + k] * (rankings[3 * j + k] - 1)) / 2
        teamscores[j] = int(score)


def printScores():
    print("Final scores for each of the five teams:")
    for j in range(5):
        print(names[j] + ": " + str(teamscores[j]))
