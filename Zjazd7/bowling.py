import time
import gymnasium as gym
import numpy as np
import pickle

env = gym.make("Bowling-v1", render_mode="human")
state, _ = env.reset()


epsilon = 1.0
max_steps = 100
total_episodes = 10  # Liczba epizodów (zmniejsz na początek dla testów)

lr_rate = 0.01
gamma = 0.98

Q = np.zeros([env.observation_space.n, env.action_space.n])

def choose_action(state):
    action = 0
    if np.random.uniform(0, 1) < epsilon:
        action = env.action_space.sample()
    else:
        action = np.argmax(Q[state, :])
    return action

def learn(state, state2, reward, action):
    predict = Q[state, action]
    target = reward + gamma * np.max(Q[state2, :])
    Q[state, action] = Q[state, action] + lr_rate * (target - predict)

for episode in range(total_episodes):
    state = env.reset()
    t = 0

    while t < max_steps:
        env.render()

while t < max_steps:
    env.render()
    action = choose_action(state)
    state2, reward, done, info = env.step(action)
    learn(state, state2, reward, action)

    state = state2

    t+= 1

    if done:
        break

    time.sleep(0.1)

print(Q)

with open("bowling.txt", 'wb') as f:
    pickle.dump(Q, f)

