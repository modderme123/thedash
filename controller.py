import random

from src.drv import *
from src.petermilo import *

names = [''] * 6
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


class Controller:
    def __init__(self):
        self.players = random.sample(range(len(names)), 5)
        self.place = 1
        self.rankings = [0] * 15
        self.positions = [0] * 15
        self.funds = [1000000] * 5
        self.teamscores = [0] * 5

    def setDistances(self):
        self.distances = [random.randint(10, 19), random.randint(20, 29), random.randint(30, 39)]

    def gatherBids(self):
        self.bids = []
        for j in range(5):
            if self.funds[j] >= 0:
                mypos, myfunds = self.positions[:], self.funds[:]
                myfunds[0], myfunds[j] = myfunds[j], myfunds[0]
                mypos[0:3], mypos[3 * j:3 * j + 3] = mypos[3 * j:3 * j + 3], mypos[0:3]
                mybids = controller(self.players[j], mypos, myfunds, self.distances)
                total = 0
                for k in range(3):
                    value = max(int(mybids[k][1]), 0)
                    total += value
                    if total <= self.funds[j]:
                        mybids[k][1] = value
                    else:
                        total -= value
                        mybids[k][1] = 0
                    if self.rankings[3 * j + k] > 0:
                        mybids[k][1] = -1
                    if mybids[k][0] not in ['short', 'medium', 'long']:
                        mybids[k][0] = 'short'
                self.bids += mybids
            else:
                self.bids += 3 * [['short', -1]]

    def winningBids(self):
        self.shortwinbid, self.mediumwinbid, self.longwinbid = -1, -1, -1
        self.shortindex, self.mediumindex, self.longindex = -1, -1, -1
        for j in range(15):
            if self.bids[j][0] == 'short':
                if self.bids[j][1] > self.shortwinbid:
                    self.shortwinbid = self.bids[j][1]
                    self.shortindex = j
            elif self.bids[j][0] == 'medium':
                if self.bids[j][1] > self.mediumwinbid:
                    self.mediumwinbid = self.bids[j][1]
                    self.mediumindex = j
            else:
                if self.bids[j][1] > self.longwinbid:
                    self.longwinbid = self.bids[j][1]
                    self.longindex = j

    def payMove(self, runner, bid, size):
        if bid >= 0:
            index = int(runner / 3)
            self.funds[index] -= bid
            self.positions[runner] = min(self.positions[runner] + self.distances[size], 100)
            if self.positions[runner] == 100 and self.rankings[runner] == 0:
                self.rankings[runner] = self.place
                self.place += 1
                if self.rankings[index * 3] > 0 and self.rankings[index * 3 + 1] > 0 and self.rankings[index * 3 + 2] > 0:
                    self.funds[index] = -1

    def instantAdvance(self):
        self.payMove(self.longindex, self.longwinbid, 2)
        self.payMove(self.mediumindex, self.mediumwinbid, 1)
        self.payMove(self.shortindex, self.shortwinbid, 0)

    def updateScores(self):
        for j in range(5):
            score = 0
            for k in range(3):
                if self.rankings[3 * j + k] > 0:
                    score += 100 - (self.rankings[3 * j + k] * (self.rankings[3 * j + k] - 1)) / 2
            self.teamscores[j] = int(score)

    def printScores(self):
        print("Scores for each of the five teams this round:")
        ordered = sorted(zip(self.teamscores, [names[j] for j in self.players]), reverse=True)
        for score, name in ordered:
            print(name + ": " + str(score))
