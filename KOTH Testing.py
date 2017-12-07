import random

def Testrun(ai1,ai2,ai3,ai4,ai5):
    while any(x >= 0 for x in game.funds):
        players = random.sample(range(len(vals)), 5)
        place = 1
        rankings = [0] * 15
        positions = [0] * 15
        funds = [1000000] * 5
        teamscores = [0] * 5

        # set distances
        distances = [random.randint(x, x + 9) for x in [10, 20, 30]]

        # gather bids
        bids = []
        for j in range(5):
            if funds[j] >= 0:
                mypos, myfunds = positions[:], funds[:]
                myfunds[0], myfunds[j] = myfunds[j], myfunds[0]
                mypos[0:3], mypos[3 * j:3 * j + 3] = mypos[3 * j:3 * j + 3], mypos[0:3]
                mybids = equilizer(mypos, myfunds, distances, vals[players[j]])
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
                bids += [['short', -1]] * 3

        # winning bids
        winbids = [-1] * 3
        winindex = [-1] * 3
        dist_dict = {'short': 0, 'medium': 1, 'long': 2}
        for j in range(15):
            bidtype = dist_dict[bids[j][0]]
            if bids[j][1] > winbids[bidtype]:
                winbids[bidtype] = bids[j][1]
                winindex[bidtype] = j

        # instant advance
        for i in reversed(range(3)):
            if winbids[i] >= 0:
                index = int(winindex[i] / 3)
                funds[index] -= winbids[i]
                positions[winindex[i]] = min(positions[winindex[i]] + distances[i], 100)
                if positions[winindex[i]] == 100 and rankings[winindex[i]] == 0:
                    rankings[winindex[i]] = place
                    place += 1
                    if all(x > 0 for x in rankings[index * 3:index * 3 + 3]):
                        funds[index] = -1

    # update scores
        for j in range(5):
            score = 0
            for k in range(3):
                if rankings[3 * j + k] > 0:
                    score += 100 - (rankings[3 * j + k] * (rankings[3 * j + k] - 1)) / 2
            teamscores[j] = int(score)
    return [teamscores[j] for j in range(5)]

def maxpos(array):
    temp = []
    for item in array:
        temp.append(item)
    temp.sort()
    return array.index(temp[len(temp)-1])


vals = []
points = []

for i in range(28, 34):
    for j in range(28, 34):
        for k in range(28, 34):
            vals.append([i, j, k])
            points.append(0)
            


King = 0

for j in range(int(input("Amount of testing: "))):
    competitors = [King]+random.sample(vals,4)
    results = Testrun(vals[competitors[0]],vals[competitors[1]],vals[competitors[2]],vals[competitors[3]],vals[competitors[4]])
    if maxpos(results) == 0:
        points[King] += 1
    else:
        King = competitors[maxpos(results)]


ordered = sorted(zip(points, range(len(vals))), reverse=True)
for score, j in ordered:
    print("Equilizer " + str(vals[j]) + ": " + str(score))