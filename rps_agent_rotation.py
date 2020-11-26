rotationType = "increasing"

def rps_agent_random(observation, configuration):
    global rotationType
    action = 0

    if rotationType == "increasing":
        action = observation.step%3
    else :
        action = (2-observation.step)%3
    return action
