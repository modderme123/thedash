# randomly bids between a tenth and a third of available funds on each distance
def randomrunner(pos, funds, dist):
    import random
    dollars = funds[0]
    if dist[0] < 100:
        bid0 = random.randint(int(dollars / 10), int(dollars / 3))
    else:
        bid0 = 0
    if dist[1] < 100:
        bid1 = random.randint(int(dollars / 10), int(dollars / 3))
    else:
        bid1 = 0
    if dist[2] < 100:
        bid2 = random.randint(int(dollars / 10), int(dollars / 3))
    else:
        bid2 = 0
    return [['short', bid0], ['medium', bid1], ['long', bid2]]

# always bids a certain fraction of available funds on each distance


def offlikeashot(pos, funds, dist):
    dollars = funds[0]
    if dist[0] < 100:
        bid0 = int(dollars / 5)
    if dist[1] < 100:
        bid1 = int(dollars / 8)
    if dist[2] < 100:
        bid2 = int(dollars / 10)
    return [['long', bid0], ['medium', bid1], ['short', bid2]]

# always bid proportionally to the distance


def steadyfreddy(pos, funds, dist):
    import random
    bid0 = 1000 * dist[0]
    bid1 = 1000 * dist[1]
    bid2 = 1000 * dist[2]
    bids = [['short', bid0], ['medium', bid1], ['long', bid2]]
    random.shuffle(bids)
    return bids
