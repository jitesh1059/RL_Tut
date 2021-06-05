import gym
import numpy as np

env = gym.make("MountainCar-v0")

LEARNING_RATE = 0.1
DISCOUNT = 0.95
EPISODES = 25000

DISCRETE_OS_SIZE = [20] * len(env.observation_space.high)
discrete_os_win_size = (env.observation_space.high - 
                        env.observation_space.low) / DISCRETE_OS_SIZE

q_table = np.random.uniform(low=-2, high=0, size=(DISCRETE_OS_SIZE + [env.action_space.n]))

def get_discrete_state(state):
    discrete_state = (state - env.observation_space.low) / discrete_os_win_size
    return tuple(discrete_state.astype(np.int64))


for episode in range(EPISODES):

    discrete_state = get_discrete_state(env.reset())

    #print(discrete_state)

    done = False

    while not done:
        action = np.argmax(q_table[discrete_state])
        new_state, reward, done, _ = env.step(action)

        new_discrete_state = get_discrete_state(new_state)
        if not done:
            max_future_q = np.max(q_table[new_discrete_state])
            current_q = q_table[discrete_state + (action, )]
            new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
            q_table[discrete_state + (action, )] = new_q

        elif new_state[0] >= env.goal_position:
            print(f"We made it on episode {episode}")
            env.render()
            q_table[discrete_state + (action, )] = 0
        
        discrete_state = new_discrete_state

env.close()