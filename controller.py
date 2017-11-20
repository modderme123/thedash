import random

from src.drv import *
from src.petermilo import *

names = [''] * 6
funcs = [None] * 6
# DRV
names[0], funcs[0] = "Random Runner", randomrunner
names[1], funcs[1] = "Off Like A Shot", offlikeashot
names[2], funcs[2] = "Steady Freddy", steadyfreddy
# PETERMILO
names[3], funcs[3] = "Equilizer", Equilizer
names[4], funcs[4] = "Skyrocket", Skyrocket
names[5], funcs[5] = "RandomEquilizer", RandomEquilizer


class Controller:
    def __init__(self):
        self.players = random.sample(range(len(names)), 5)
        self.place = 1
        self.rankings = [0] * 15
        self.positions = [0] * 15
        self.funds = [1000000] * 5
        self.teamscores = [0] * 5

    def setDistances(self):
        self.distances = [random.randint(x, x + 9) for x in [10, 20, 30]]

    def gatherBids(self):
        self.bids = []
        for j in range(5):
            if self.funds[j] >= 0:
                mypos, myfunds = self.positions[:], self.funds[:]
                myfunds[0], myfunds[j] = myfunds[j], myfunds[0]
                mypos[0:3], mypos[3 * j:3 * j + 3] = mypos[3 * j:3 * j + 3], mypos[0:3]
                mybids = funcs[self.players[j]](mypos, myfunds, self.distances)
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
        self.winbids = [-1] * 3
        self.winindex = [-1] * 3
        distDict = {'short': 0, 'medium': 1, 'long': 2}
        for j in range(15):
            bidtype = distDict[self.bids[j][0]]
            if self.bids[j][1] > self.winbids[bidtype]:
                self.winbids[bidtype] = self.bids[j][1]
                self.winindex[bidtype] = j

    def instantAdvance(self):
        for i in reversed(range(3)):
            if self.winbids[i] >= 0:
                index = int(self.winindex[i] / 3)
                self.funds[index] -= self.winbids[i]
                self.positions[self.winindex[i]] = min(self.positions[self.winindex[i]] + self.distances[i], 100)
                if self.positions[self.winindex[i]] == 100 and self.rankings[self.winindex[i]] == 0:
                    self.rankings[self.winindex[i]] = self.place
                    self.place += 1
                    if all(x > 0 for x in self.rankings[index * 3:index * 3 + 3]):
                        self.funds[index] = -1

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
