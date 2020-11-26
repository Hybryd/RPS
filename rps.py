from kaggle_environments import make, evaluate
import sys
from random import seed
from random import randint
from kaggle_environments import utils
import time
seed(time.time()+4*time.time())

env = make("rps", debug=True, configuration={"episodeSteps": 1000 })

#################################
# AGENT A TESTER
#################################

#################################


agent1 = utils.read_file("rps_agent_minasi_killer.py")
agent2 = utils.read_file("rps_agent_minasi.py")

steps = env.run([agent1, agent2])
#for i in steps :
#    print(str(i[0]["action"]) + str(" - ") + str(i[1]["action"]) + str(" : ")+str(i[0]["reward"]) + str(" - ") + str(i[1]["reward"]))

print(str(steps[-2][0]["reward"]) + str(" - ") + str(steps[-2][1]["reward"]))


# BUG : steps[-1] reset les scores

# Check if agents are correctly written
'''
env.run([agent1, agent2])

print("Success!" if env.state[0].status == env.state[1].status == "DONE" else "Failed...")
'''

'''
trials = 10
wins = 0
avg = 0
#print('Running {} matches; this may take a few seconds'.format(trials))


#print("My Agent vs Random Agent:", mean_reward(evaluate("connectx", [agent1, agent2], num_episodes=10)))

for trial in range(trials):
    current_score = evaluate("rps", [agent1, agent2], configuration={"episodeSteps": 10})
    print(current_score)
    if current_score[0][0] > 0:
        wins += 1
    avg += current_score[0][0] - current_score[0][1]
print('wins: {} / {}'.format(wins, trials),
    '\tavg score: {}'.format(avg / trials))
'''
