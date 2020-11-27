from random import seed
from random import randint
import time
from anytree import Node, RenderTree

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




def run(observation, configuration):
    global agentHistory
    global opponentHistory
    global strategy

    action = 0

    # First step
    if observation.step == 0 :
        action = random()

    # Later
    else :
        updateOpponentHistory(observation.lastOpponentAction)

        if(observation.step>=2):
            action = 1#####
        else:
            action = randomAction()

    updateAgentHistory(action)

    return action
