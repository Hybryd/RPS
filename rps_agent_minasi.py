from random import seed
from random import randint
import time

seed(299792458*time.time())

IDString = "rps"
agentHistory = ""
opponentHistory = ""
mixedHistory =""
strategy = "minasi"

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



def run(observation, configuration):
    global agentHistory
    global opponentHistory
    global strategy

    action = 0

    # First step
    if observation.step == 0 :
        action = 2

    # Later
    else :
        updateOpponentHistory(observation.lastOpponentAction)

        if(observation.step>=2):
            action = minasi()
        else:
            action = randomAction()

    updateAgentHistory(action)

    return action
