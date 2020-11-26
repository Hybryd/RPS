from random import seed
from random import randint
import time
import math

seed(299792458*time.time())

IDString = "rps"
agentHistory = ""
agentScore=0
opponentHistory = ""
opponentScore=0
mixedHistory =""
strategy = "minasi"

#
# r = 0
# p = 1
# s = 2
# r < p

def get_score(a, b):
    res = 0
    if (a==0): # R
        if (b==1): # P
            res = -1
        elif (b==2):
            res = 1
    elif (a==1): # P
        if (b==0): # R
            res = 1
        elif (b==2):
            res = -1
    elif (a==2): # S
        if (b==0): # R
            res = -1
        elif (b==1):
            res = 1
    return res

def updateScores():
    global mixedHistory
    global agentScore
    global opponentScore

    score = get_score(IDString.find(mixedHistory[-2].lower()),IDString.find(mixedHistory[-1].lower()))
    #print("SCORE = "+str(score))
    agentScore += score
    opponentScore -= score

def updateAgentHistory(agentAction):
    global agentHistory
    global mixedHistory
    agentHistory += IDString[agentAction].upper()
    mixedHistory += IDString[agentAction].upper()

def updateOpponentHistory(opponentAction):
    global opponentHistory
    global mixedHistory
    opponentHistory += IDString[opponentAction]
    mixedHistory += IDString[opponentAction]

def updateMixedHistory(agentAction,opponentAction):
    mixedHistory += IDString[agentAction].upper()+IDString[opponentAction]

def toInt(code):
    res = 0
    if code.lower() == "p" :
        res = 1
    elif code.lower() == "s" :
        res = 2
    return res

def beat(action):
    return (action+1)%3

def randomAction():
    return randint(0,2)

#
#   Minasi algorithm
#
def minasi():
    global mixedHistory
    res = randomAction()
    n = len(mixedHistory)
    i=n-1
    maximalSequence = mixedHistory[i] # last element : last opponent's action
    maximalSequenceFound = False

    while not maximalSequenceFound :

        if mixedHistory.count(maximalSequence, 0, len(mixedHistory)-len(maximalSequence)) >= 2 :
            i-=1
            maximalSequence = mixedHistory[i]+maximalSequence
            maximalSequenceFound = i<=1
        else :
            maximalSequenceFound = True
    maximalSequence = maximalSequence[1:]

    if len(maximalSequence) > 0 :
        # Get index list of all occurences of maximalSequence
        indexList = [i for i in range(len(mixedHistory)-len(maximalSequence)) if mixedHistory.startswith(maximalSequence, i)]

        # We concatenate all opponent's response into a string
        opponentActions = ""
        for i in indexList:
            opponentActions += mixedHistory[i+len(maximalSequence)+1]

        # We choose select the most recurrent opponent's response
        occurences = [opponentActions.count("r"),opponentActions.count("p"),opponentActions.count("s")]
        m=max(occurences)
        if(m!=0):
            maxActions = [i for i, j in enumerate(occurences) if j == m]
            res = beat(int(maxActions[0]))
    return res

#
#   Minasi algorithm applied on the agent himself
#   We suppose the opponent follows Minasi algorithm, so we can defeat him
#
def minasi_kill():
    global mixedHistory

    #rint("mixedHistory = "+str(mixedHistory))

    res = randomAction()
    n = len(mixedHistory)
    i=n-2
    maximalSequence = mixedHistory[i] # agent's last action (capital letters in mixedHistory)
    maximalSequenceFound = False

    while not maximalSequenceFound :
        #print("i = "+str(i))
        #print("maximalSequence = "+str(maximalSequence))
        #print("mixedHistory.count(maximalSequence, 0, len(mixedHistory)-len(maximalSequence)-1) = "+str(mixedHistory.count(maximalSequence, 0, len(mixedHistory)-len(maximalSequence)-1)))

        if mixedHistory.count(maximalSequence, 0, len(mixedHistory)-len(maximalSequence)-1) >= 2 :
            i-=1
            maximalSequence = mixedHistory[i]+maximalSequence
            maximalSequenceFound = i<=1
        else :
            maximalSequenceFound = True
    maximalSequence = maximalSequence[1:]
    #print(" FOUND maximalSequence = "+str(maximalSequence))

    if len(maximalSequence) > 0 :
        # Get index list of all occurences of maximalSequence
        indexList = [i for i in range(len(mixedHistory)-len(maximalSequence)-1) if mixedHistory.startswith(maximalSequence, i)]

        # We concatenate all agent's response into a string
        agentActions = ""
        for i in indexList:
            agentActions += mixedHistory[i+len(maximalSequence)+1]
        #print("agentActions = "+str(agentActions))

        # We choose select the most recurrent opponent's response
        occurences = [agentActions.count("R"),agentActions.count("P"),agentActions.count("S")]
        #print("occurences = "+str(occurences))

        m=max(occurences)
        #print("m = "+str(m))

        if(m!=0):
            maxActions = [i for i, j in enumerate(occurences) if j == m]
            #print("maxActions = "+str(maxActions))
            res = beat(beat(int(maxActions[0]))) # Beat minasi result applied on the agent himself
            #print("ACTION = "+str(IDString[res]))
    return res



def run(observation, configuration):
    global agentHistory
    global opponentHistory
    global strategy
    global agentScore
    global opponentScore

    action = randomAction()


    if observation.step > 0 :
        updateOpponentHistory(observation.lastOpponentAction)

        '''
        if(get_score(IDString.find(mixedHistory[-2].lower()),IDString.find(mixedHistory[-1].lower()))==1):
            print("--------> AGENT WIN")
        elif (get_score(IDString.find(mixedHistory[-2].lower()),IDString.find(mixedHistory[-1].lower()))==-1):
            print("--------> AGENT LOSE")
        else:
            print("--------> TIE")
        '''
        updateScores()

        if(observation.step>=500): # Misani killer
            if(agentScore-opponentScore > configuration.tieRewardThreshold + 10) :
                action = randomAction() # If we are in advance : we choose the random strategy
            else:
                action = minasi_kill()
        else:
            action = minasi()

    updateAgentHistory(action)

    return action
