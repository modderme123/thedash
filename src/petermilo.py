def Equilizer(pos,funds,dist):
    bid0 = 3000*dist[0]
    bid1 = 3000*dist[1]
    bid2 = 3000*dist[2]
    bids = [0,0,0]
    donecount = [0,1,2]
    
    for j in range(3):
        if pos[j]>=pos[(j+1)%3] and pos[j]>=pos[(j+2)%3] and not(["short",bid0] in bids):
            bids[j] = ["short",bid0]
        elif pos[j]<=pos[(j+1)%3] and pos[j]<=pos[(j+2)%3] and not(["long",bid0] in bids):
            bids[j] = ["long",bid2]
        if pos[j] == 100:
            donecount.remove(j)
        
    
    for j in range(3):
        if bids[j] == 0:
            bids[j] = ["medium",bid1]

    if len(donecount) == 1:
        bestdist = 2
        finishing = False
        for j in range(2,-1,-1):
            if dist[j]+pos[donecount[0]] >= 100:
                bestdist = j
                finishing = True
        if finishing:
            bids[donecount[0]] = [["short","medium","long"][bestdist],funds[0]]
    return bids

def Skyrocket(pos,funds,dist):
    bid0 = 3300*dist[0]
    bid1 = 3300*dist[1]
    bid2 = 3300*dist[2]

    if bid2>=funds[0]:
        bid2 = funds[0]

    if pos[0] !=100:
        bids = [["long",bid2],["medium",bid1],["short",bid0]]
    elif pos[1] !=100:
        bids = [["short",bid0],["long",bid2],["medium",bid1]]
    elif pos[2] !=100:
        bids = [["medium",bid1],["short",bid0],["long",bid2]]
    else:
        bids = [["short",0],["short",0],["short",0]]
        
    return bids
