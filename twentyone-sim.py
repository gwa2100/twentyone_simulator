from random import shuffle
from random import randint
import multiprocessing
import matplotlib.pyplot as plt
import numpy

colors = ['♥','♦','♠','♣']
playerWins = 0
dealerWins = 0
push = 0
playerBlackJack = 0
playerAI = True
HIT = 1
STAND = 2
DOUBLE = 3
SPLIT = 4
FMODE = True
PMODE = False
DEBUG = False

def DblOrHit(candouble):
    if candouble:
        return DOUBLE
    else:
        return HIT

def DblOrStand(candouble):
    if candouble:
        return DOUBLE
    else:
        return STAND

def ToSplit(candblaftersplit):
    if candblaftersplit:
        return SPLIT
    else:
        return HIT


def AIPlayerRoutine(playerhand, dealershowcard, candouble, cansplit, candblaftersplit):
    'AI PLAYER ROUTINE'
    'return 1 for hit 2 for stand 3 for double 4 for split'
    
    x = playerhand.evaluate()
    soft = playerhand.soft_aces_flag
    d = dealershowcard.value
    if x < 9:
        return HIT
    elif x == 9:
        if d in [3,4,5,6]:
            return DblOrHit(candouble)
        else:
            return HIT
    elif x == 10:
        if d in range(2,9):
            return DblOrHit(candouble)
        else:
            return HIT
    elif x == 11:
        return DblOrHit(candouble)
    elif x == 12:
        if d in [2,3,7,8,9,10,1]:
            return HIT
        else:
            return STAND
    elif x == 13:
        if soft:
            if d in [2,3,4,7,8,9,10,1]:
                return HIT
            else:
                return DOUBLE
        else:
            if d in [2,3,4,5,6]:
                return STAND
            else:
                return HIT
    elif x == 14:
        if soft:
            if d in [2,3,4,7,8,9,10,1]:
                return HIT
            else:
                return DblOrHit(candouble)
        else:
            if d in [2,3,4,5,6]:
                return STAND
            else:
                return HIT
    elif x == 15:
        if soft:
            if d in [4,5,6]:
                return DblOrHit(candouble)
            else:
                return HIT
        else:
            if d in [2,3,4,5,6]:
                return STAND
            else:
                return HIT
    elif x == 16:
        if soft:
            if d in [4,5,6]:
                return DblOrHit(candouble)
            else:
                return HIT
        else:
            if d in [2,3,4,5,6]:
                return STAND
            else:
                return HIT
    elif x == 17:
        if soft:
            if d in [3,4,5,6]:
                return DblOrHit(candouble)
            else:
                return HIT
        else:
            return STAND

    elif x == 18:
        if soft:
            if d in [2,3,4,5,6]:
                return DblOrStand(candouble)
            elif d in [7,8]:
                return STAND
            else:
                return HIT
        else:
            return STAND

    elif x == 19:
        if soft:
            if d == 6:
                return DblOrStand(candouble)
            else:
                return STAND
        else:
            return STAND

    elif x >= 20:
        return STAND


class Card:
    def __init__(self,p_color, p_value):
        self.value = p_value
        self.color = p_color
    def printCard(self):
        valToPrint = ""
        if self.value == 1:
            valToPrint = "A"
        elif self.value == 11:
            valToPrint = "J"
        elif self.value == 12:
            valToPrint = "Q"
        elif self.value == 13:
            valToPrint = "K"
        else:
            valToPrint = str(self.value)
        print (valToPrint + self.color)

class Deck:
    def __init__(self):
        'Initialize Standard Deck'
        self.cards = []
        self.cards = [Card(color, value) for value in range(1,14) for color in colors]
        

class Hand:
    def __init__(self):
        self.handScore = 0
        self.soft_aces_flag = False
        self.cards = []

    def evaluate(self):
        aces_at_eleven = 0
        self.handScore = 0
        for c in self.cards:
            if c.value == 11 or c.value == 12 or c.value == 13:
                self.handScore += 10
            elif c.value == 1:
                if self.handScore < 11:
                    self.handScore += 11
                    aces_at_eleven += 1
                else:
                    self.handScore += 1
            else:
                self.handScore += c.value
        if self.handScore > 21 and aces_at_eleven != 0:
            aces_at_eleven -= 1
            self.handScore -= 10
        if aces_at_eleven > 0:
            self.soft_aces_flag = True
        return self.handScore
    
    def hit(self, p_card):
        self.cards.append(p_card)

    def getCards(self):
        return self.cards

    'Need to figure out how splitting, doubling, and blackjack will be handled.'

class Shoe:
    def __init__(self,p_decks, p_shuffle_precision):
        self.cards = []
        self.yellow_card_position = randint(28,int((52 * p_decks) / 3))
        self.decks = p_decks
        self.shuffle_precision = p_shuffle_precision
        for x in range (1,p_decks):
            tmpDeck = Deck()
            for c in tmpDeck.cards:
                self.cards.append(c)
        shuffle(self.cards)
    
    def drawCard(self):
        if DEBUG: print (">>>" + str(len(self.cards)) + " / " + str(self.yellow_card_position))
        return self.cards.pop()


def RunGame():
    playerBlackJack = 0
    playerWins = 0
    dealerWins = 0
    push = 0
    currentRound = 0
    gamePlaying = True
    myshoe = "BLANKS"
    myshoe = Shoe(6,6)
    while gamePlaying == True:
        currentRound += 1
        if PMODE: print ("Current Round: " + str(currentRound))
        dealerhand = Hand()
        playershand = Hand()
        dealerhand.hit(myshoe.drawCard())
        playershand.hit(myshoe.drawCard())
        dealerhand.hit(myshoe.drawCard())
        playershand.hit(myshoe.drawCard())

        if (dealerhand.cards[0].value in [10,11,12,13] and dealerhand.cards[1].value == 1) or (dealerhand.cards[0].value == 1 and dealerhand.cards[1].value in [10,11,12,13]):
            if PMODE:
                print ("DEALER BLACKJACK")
                for c in dealerhand.cards:
                    c.printCard()
        else:
            if PMODE: print ("Beginning Play:")
            playersScore = 0
            playerplaying = True
            while playerplaying:
                if PMODE: print ("Dealer Showing: ")
                dealershowcard = dealerhand.cards[1]
                if PMODE: 
                    dealershowcard.printCard()
                    print ("")
                    print ("Your Hand: ")
                    for c in playershand.cards:
                        c.printCard()
                if playerAI == False:
                    hitorstay = input("1) Hit 2) Stay:")
                else:
                    'AI WILL PLAY'
                    AIAnswer = AIPlayerRoutine(playershand,dealershowcard,False,False, False)
                    'Remove once we can handle splits'
                    if AIAnswer == SPLIT:
                        hitorstay = 1
                    else:
                        hitorstay = AIAnswer
                    


                if hitorstay == 1:
                    drawnCard = myshoe.drawCard()
                    if PMODE:  
                        print("Drawn Card:")
                        drawnCard.printCard()
                    playershand.hit(drawnCard)
                else:
                    playerplaying = False
                if playershand.evaluate() > 21:
                    if PMODE:
                        print ("Player Busted!")
                    playerplaying = False
            
            if playershand.evaluate() < 22:
                'JUST CHECK TO SEE IF THE PLAYER HAD A BLACKJACK FOR STATS PURPOSES'
                if ((playershand.cards[0].value in [10,11,12,13] and playershand.cards[1].value == 1) or (playershand.cards[0].value == 1 and playershand.cards[1].value in [10,11,12,13])) and len(playershand.cards) == 2:
                    playerBlackJack += 1

                if PMODE:   print ("Dealers Play:")
                dealer_playing = True
                while dealer_playing == True:
                    currentscore = dealerhand.evaluate()
                    if PMODE:
                        print("DEALERS HAND:")
                        for c in dealerhand.getCards():
                            c.printCard()
                        print("Current Score:" + str(currentscore))
                    if currentscore < 17:
                        if PMODE: print ("Dealer Hitting: Under 16")
                        dealerhand.hit(myshoe.drawCard())
                    elif currentscore == 17 and dealerhand.soft_aces_flag == True:
                        if PMODE: print ("Dealer Hitting: Soft 17")
                        dealerhand.hit(myshoe.drawCard())
                    else:
                        if PMODE: print ("Dealer Staying")
                        dealer_playing = False
            
            if (dealerhand.evaluate() > 21 or dealerhand.evaluate() < playershand.evaluate()) and playershand.evaluate() < 22:
                if PMODE: print("Player wins!")
                playerWins += 1
            elif (dealerhand.evaluate() < 21 and playershand.evaluate() > 21) or (playershand.evaluate() < dealerhand.evaluate()):
                if PMODE: print("Dealer Wins!")
                dealerWins += 1
            elif (dealerhand.evaluate() == playershand.evaluate()):
                if PMODE: print("PUSH!")
                push += 1
            else:
                print("Unhandled Game Condition!")
        if len(myshoe.cards) < myshoe.yellow_card_position:
            gamePlaying = False
            if PMODE: print("Shoe has hit the yellow...ending")
    return (playerWins, dealerWins, push, playerBlackJack)


print("~~~~~~~~~~~GAME TEST~~~~~~~~~~~~~")
shoestorun = int(input("Shoes to run:"))
currentShoe = 0
results = []
for x in range(shoestorun):
    results.append(RunGame())
    currentShoe += 1
    if FMODE: 
        if currentShoe % 1000 == 0: print ("Current Shoe: " + str(currentShoe))
    else:
        print ("Current Shoe: " + str(currentShoe))

playerWinsList = []
dealerWinsList = []
pushList = []
playerBlackJackList = []
for r in results:
    playerWins += r[0]
    playerWinsList.append(r[0])
    dealerWins += r[1]
    dealerWinsList.append(r[1])
    push += r[0]
    pushList.append(r[2])
    playerBlackJack += r[3]
    playerBlackJackList.append(r[3])

print ("STATS:")
print ("Shoes Ran:")
print (str(currentShoe))
print ("Player Wins:")
print (str(playerWins))
print ("Dealer Wins:")
print (str(dealerWins))
print ("Pushes:")
print (str(push))
print ("Player BlackJacks:")
print (str(playerBlackJack))
print ("% win/loss")
print (str((playerWins/float(playerWins + dealerWins))*100))
print("Potential Gain or Loss:")
print ("Betting assumed at $3.00 and 1.5x blackjack")
wins = playerWins * 3.00
losses = dealerWins * 3.00
wins += playerBlackJack * (3.00 * 1.5)
net = wins - losses
print ( str(net))


z = numpy.polyfit(range(len(playerWinsList)),playerWinsList, 1)
p = numpy.poly1d(z)


plt.plot(playerWinsList)
plt.plot(p(range(len(playerWinsList))))
'plt.plot(dealerWinsList)'
'plt.plot(pushList)'
plt.show()
