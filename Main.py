# Anthony Maringo Alm4cu
import random
import Players
import csv

# Make tuple of the board of the properties
board = []
boardFile = open("board.txt", 'r')
for line in boardFile:
    board.append(line.strip())
board = tuple(board)
boardFile.close()

# Make a list of how many times each spot was landed on
timesLandedOn = []
for space in board:
    timesLandedOn.append(0)

# Make list of Chance Cards
chance = []
chanceTop = 0
chanceFile = open("chance.txt", 'r')
for line in chanceFile:
    chance.append(line.strip())
chanceFile.close()

# Make list of Community Chest cards
communityChest = []
ccTop = 0
communityChestFile = open("communityChest.txt", 'r')
for line in communityChestFile:
    communityChest.append(line.strip())
communityChestFile.close()

# Function to shuffle a deck when empty
random.shuffle(communityChest)
ccTop = 0

# players
p1 = Players.Player()
p2 = Players.Player()
p3 = Players.Player()
p4 = Players.Player()


players = [p1, p2,p3]


def rollDice():
    global die1, die2
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)


def drawCommuityChest(player):
    global ccTop
    if ccTop >= len(communityChest):
        ccTop = 0
    curCard = communityChest[ccTop]
    ccTop += 1
    if curCard == "Advance to Go":
        player.curPos = board.index("Go")
        timesLandedOn[player.curPos] += 1
    elif curCard == "Go to Jail":
        player.curPos = board.index("Jail")
        player.inJail = True
        timesLandedOn[player.curPos] += 1
    else:
        return


def drawChance(player):
    global chanceTop
    if chanceTop >= len(chance):
        chanceTop = 0
    curCard = chance[chanceTop]
    chanceTop += 1

    if curCard == "Advance to Go":
        player.curPos = board.index("Go")
        timesLandedOn[player.curPos] += 1
    elif curCard == "Advance to Illinois Ave.":
        player.curPos = board.index("Illinois Avenue")
        timesLandedOn[player.curPos] += 1
    elif curCard == "Advance to St. Charles Place.":
        player.curPos = board.index("St. Charles Place")
        timesLandedOn[player.curPos] += 1

    elif curCard == "Advance token to nearest Utility.":
        if board.index("Electric Company") < player.curPos < board.index("Water Works"):
            player.curPos = board.index("Water Works")
        else:
            player.curPos = board.index("Electric Company")
        timesLandedOn[player.curPos] += 1

    elif curCard == "Advance token to the nearest Railroad":
        if board.index("Short Line") < player.curPos < board.index("Reading Railroad"):
            player.curPos = board.index("Reading Railroad")
        if board.index("Reading Railroad") < player.curPos < board.index("Pennsylvania Railroad"):
            player.curPos = board.index("Pennsylvania Railroad")
        if board.index("Pennsylvania Railroad") < player.curPos < board.index("B&O Railroad"):
            player.curPos = board.index("B&O Railroad")
        if board.index("B&O Railroad") < player.curPos < board.index("Short Line"):
            player.curPos = board.index("Short Line")
        timesLandedOn[player.curPos] += 1

    elif curCard == "Go Back Three {3} Spaces.":
        player.curPos -= 3
        timesLandedOn[player.curPos] += 1

    elif curCard == "Go to Jail":
        player.curPos = board.index("Jail")
        timesLandedOn[player.curPos] += 1

    elif curCard == "Take a trip to Reading Railroad.":
        player.curPos = board.index("Reading Railroad")
        timesLandedOn[player.curPos] += 1

    elif curCard == "Advance token to Boardwalk":
        player.curPos = board.index("Boardwalk")
        timesLandedOn[player.curPos] += 1
    else:
        return


def executeTurn(player):
    if player.inJail:
        if player.rollsInJail == 3:
            player.inJail = False
            return

        elif die1 == die2:
            player.inJail = False
            return
        else:
            player.rollsInJail += 1

    player.curPos += die1 + die2

    if player.curPos >= len(board):  # make them go around the board
        player.curPos = player.curPos - len(board)

    # increment the number of times that space was landed on
    timesLandedOn[player.curPos] += 1
    if board[player.curPos] == "Community Chest":
        drawCommuityChest(player)
    elif board[player.curPos] == "Chance":
        drawChance(player)
    elif board[player.curPos] == "Go To Jail":
        player.curPos = board.index("Jail")
        player.inJail = True


turnsPerPlayer = 30

while turnsPerPlayer > 0:

    for player in players:  # have each player rollDice the dice
        rollDice()

        executeTurn(player)

        # Go again if you get doubles
        if die1 == die2:
            rollDice()
            executeTurn(player)

        if die1 == die2:
            rollDice()
            executeTurn(player)
        # Go to jail if you get 3 doubles
        if die1 == die2:
            player.inJail = True

    turnsPerPlayer -= 1

print(board)
print(timesLandedOn)
print(sum(timesLandedOn))

# with open('data.csv', 'w') as fd:
#     writer = csv.writer(fd)
#     writer.writerow(board)

with open('data.csv', 'a') as fd:
    writer = csv.writer(fd)
    writer.writerow(timesLandedOn)

# to collect lots of data at once, use bash commands
# for run in {1..10}; do python3 Main.py;done