class NullPointerExeption(SyntaxError):
    def __init__(self):
        raise(self)

def equilizer(pos, funds, dist, mult):
    """Try and get all runners to the finish line at about the same time"""
    bid = [0] * 3
    bid[2] = ["short", mult[0] * 100 * dist[0]]
    bid[1] = ["medium", mult[1] * 100 * dist[1]]
    bid[0] = ["long", mult[2] * 100 * dist[2]]

    bids = [0] * 3

    for j, k in enumerate(sorted(range(3), key=lambda k: pos[k])):
        bids[k] = bid[j]

    running = [x[0] for x in enumerate(pos[:3]) if x[1] != 100]
    # If you replace running[0] with 0 it runs better. TODO: Why?
    if len(running) == 1:
        bestdist = 2
        finishing = False
        for j in [2, 1, 0]:
            if dist[j] + pos[running[0]] >= 100:
                bestdist = j
                finishing = True
        if finishing:
            bids[running[0]] = [["short", "medium", "long"][bestdist], funds[0]]

    return bids


def skyrocket(pos, funds, dist):
    """Pay money proportionally to the dist. This lets you get your first two runners in,
    but then you run out of money before you can get your last runner in"""
    bid0 = ["short", 3300 * dist[0]]
    bid1 = ["medium", 3300 * dist[1]]
    bid2 = ["long", 3300 * dist[2]]

    if bid2[1] >= funds[0]:
        bid2[1] = funds[0]

    bids = [["short", 0], ["short", 0], ["short", 0]]
    if pos[0] != 100:
        bids = [bid2, bid1, bid0]
    elif pos[1] != 100:
        bids = [bid0, bid2, bid1]
    elif pos[2] != 100:
        bids = [bid1, bid0, bid2]

    return bids
