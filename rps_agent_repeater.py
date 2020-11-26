def run(observation, configuration):
    if observation.step > 0:
        return observation.lastOpponentAction
    else :
        return 2
