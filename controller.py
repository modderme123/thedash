import random

from src.drv import *
from src.petermilo import *

names = [''] * 5
funcs = [None] * 5
# DRV
names[0], funcs[0] = "Random Runner", randomrunner
names[1], funcs[1] = "Off Like A Shot", offlikeashot
names[2], funcs[2] = "Steady Freddy", steadyfreddy
# PETERMILO
names[3], funcs[3] = "Equilizer", equilizer
names[4], funcs[4] = "Skyrocket", skyrocket


vals = []
for i in range(28, 34):
    for j in range(28, 34):
        for k in range(28, 34):
            vals.append([i, j, k])
#can be used for more in-deapth testing
#for i in range(20, 35):
#    vals.append([i, i, i])


class Controller:
    def __init__(self):
        self.players = random.sample(range(len(vals)), 5)
        self.place = 1
        self.rankings = [0] * 15
        self.positions = [0] * 15
        self.funds = [1000000] * 5
        self.teamscores = [0] * 5

    def set_distances(self):
        self.distances = [random.randint(x, x + 9) for x in [10, 20, 30]]

    def gather_bids(self):
        self.bids = []
        for j in range(5):
            if self.funds[j] >= 0:
                mypos, myfunds = self.positions[:], self.funds[:]
                myfunds[0], myfunds[j] = myfunds[j], myfunds[0]
                mypos[0:3], mypos[3 * j:3 * j + 3] = mypos[3 * j:3 * j + 3], mypos[0:3]
                mybids = equilizer(mypos, myfunds, self.distances, vals[self.players[j]])
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
                self.bids += [['short', -1]] * 3

    def winning_bids(self):
        self.winbids = [-1] * 3
        self.winindex = [-1] * 3
        dist_dict = {'short': 0, 'medium': 1, 'long': 2}
        for j in range(15):
            bidtype = dist_dict[self.bids[j][0]]
            if self.bids[j][1] > self.winbids[bidtype]:
                self.winbids[bidtype] = self.bids[j][1]
                self.winindex[bidtype] = j

    def instant_advance(self):
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

    def update_scores(self):
        for j in range(5):
            score = 0
            for k in range(3):
                if self.rankings[3 * j + k] > 0:
                    score += 100 - (self.rankings[3 * j + k] * (self.rankings[3 * j + k] - 1)) / 2
            self.teamscores[j] = int(score)

    def print_scores(self):
        print("Scores for each of the five teams this round:")
        player_names = ["Equilizer " + str(vals[j]) for j in self.players]
        for score, name in sorted(zip(self.teamscores, player_names), reverse=True):
            print(name + ": " + str(score))
