import random

def randomrunner(_pos, funds, dist):
    """randomly bids between a tenth and a third of available funds on each distance"""
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
    return [["short", bid0], ["medium", bid1], ["long", bid2]]


def offlikeashot(_pos, funds, dist):
    """always bids a certain fraction of available funds on each distance"""
    dollars = funds[0]
    if dist[0] < 100:
        bid0 = int(dollars / 5)
    if dist[1] < 100:
        bid1 = int(dollars / 8)
    if dist[2] < 100:
        bid2 = int(dollars / 10)
    return [["long", bid0], ["medium", bid1], ["short", bid2]]


def steadyfreddy(_pos, _funds, dist):
    """always bid proportionally to the distance"""
    bid0 = 2500 * dist[0]
    bid1 = 2500 * dist[1]
    bid2 = 2500 * dist[2]
    bids = [["short", bid0], ["medium", bid1], ["long", bid2]]
    random.shuffle(bids)
    return bids
