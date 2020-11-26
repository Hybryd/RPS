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

    #agentHistory.append(agentAction)
    agentHistory += IDString[agentAction].upper()
    mixedHistory += IDString[agentAction].upper()

def updateOpponentHistory(opponentAction):
    global opponentHistory
    global mixedHistory
    #opponentHistory.append(opponentAction)
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

'''
def detectOpponentsStrategy():
    global agentHistory
    global opponentHistory
    global strategy
'''

#
#   Browse opponentHistory and list all patterns of minimal length minLength and occuring at least minOccurence times
#

def listPatterns(minLength, minOccurence):
    global agentHistory
    global opponentHistory

    res={}
    for sublen in range(minLength,int(len(opponentHistory)/minOccurence)):
        for i in range(0,len(opponentHistory)-sublen):
            sub = opponentHistory[i:i+sublen]
            cnt = opponentHistory.count(sub)
            if cnt >= minOccurence and sub not in res:
                 res[sub] = cnt
    return res

#
#   Browse opponentHistory and list all patterns of length fixedLength and occuring at least minOccurence times
#
def listPatternsFixedLength(fixedLength, minOccurence):
    global agentHistory
    global opponentHistory


    res={}

    for i in range(0,len(opponentHistory)-fixedLength):
        sub = opponentHistory[i:i+fixedLength]
        cnt = opponentHistory.count(sub)
        if cnt >= minOccurence and sub not in res:
             res[sub] = cnt
    return res

#
#   Minasi algorithm
#
# Even index in mixedHistory : agent
# Odd index in mixedHistory : opponent
#
def minasi():
    global mixedHistory

    #print(mixedHistory)

    res = randomAction()

    n = len(mixedHistory)
    i=n-1

    #print("n = "+str(n))
    #print("i = "+str(i))

    maximalSequence = mixedHistory[i] # last element : last opponent's action
    maximalSequenceFound = False



    while not maximalSequenceFound :
        #print("  TOUR")
        #print("i = "+str(i))
        if mixedHistory.count(maximalSequence, 0, len(mixedHistory)-len(maximalSequence)) >= 2 :
            #print("COUNT = "+str(mixedHistory.count(maximalSequence, 0, len(mixedHistory)-len(maximalSequence))))
            i-=1
            maximalSequence = mixedHistory[i]+maximalSequence
            #print("maximalSequence = "+str(maximalSequence))

            maximalSequenceFound = i<=1
        else :
            maximalSequenceFound = True


    maximalSequence = maximalSequence[1:]

    if len(maximalSequence) > 0 :
        #print("maximalSequence = "+str(maximalSequence))#print("Sorti = "+str(maximalSequence))
        #print("COUNT = "+str(mixedHistory.count(maximalSequence, 0, len(mixedHistory)-len(maximalSequence))))

        #parity=len(maximalSequence)%2
        # Get index list of all occurences of maximalSequence
        indexList = [i for i in range(len(mixedHistory)-len(maximalSequence)) if mixedHistory.startswith(maximalSequence, i)]

        # We concatenate all opponent's response in a string
        opponentActions = ""
        for i in indexList:
            #print("   i = "+str(i))

            opponentActions += mixedHistory[i+len(maximalSequence)+1]

        #print("opponentActions = "+str(opponentActions))
        # We choose select the most recurrent opponent's response
        occurences = [opponentActions.count("r"),opponentActions.count("p"),opponentActions.count("s")]
        #print("occurences = "+str(occurences))
        m=max(occurences)

        if(m!=0):
            maxActions = [i for i, j in enumerate(occurences) if j == m]
            res = beat(int(maxActions[0]))

    return res



#print(minasi())


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

        if strategy == "random" :
            action = randomAction()

        if strategy == "kill_repeater" :
            action = beat(toInt(agentHistory[-1]))

        if strategy == "kill_rotation" :

            # Determine tthe type of rotations : 0-1-2 (increasing) or 2-1-0 (decreasing)
            # At least 2 steps needed
            if(observation.step >= 2 ):
                if ( (toInt(opponentHistory[-1])-toInt(opponentHistory[-2]))%3 == 1 ) : #increasing rotation
                    action = beat(toInt(opponentHistory[-1])+1)
                else :
                    action = toInt(opponentHistory[-1])
            else :
                action = randomAction()

        if strategy == "minasi" :
            if(observation.step>=2):
                action = minasi()
            else:
                action = randomAction()

        #if True:#(len(opponentHistory)>2):
            #print(listPatternsFixedLength(3,2))
        #updateMixedHistory(action, observation.lastOpponentAction)

    updateAgentHistory(action)



    return action
