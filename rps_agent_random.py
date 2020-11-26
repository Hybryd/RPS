def rps_agent_random(observation, configuration):
    from random import seed
    from random import randint
    import time
    seed(time.time()+4*time.time())
    return  randint(0,2)
