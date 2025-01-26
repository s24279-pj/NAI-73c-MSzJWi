import gym
import numpy as np
import time

# Ustawienia środowiska
env = gym.make("Bowling-v4", render_mode="human")
state, _ = env.reset()

# Parametry dla algorytmu Q-learning
epsilon = 1.0
max_steps = 100
total_episodes = 10

lr_rate = 0.90
gamma = 0.98

# Liczba przedziałów dla dyskretyzacji
num_bins = 10

# Ustal przedziały dyskretyzacji na podstawie kształtu przestrzeni obserwacji
obs_bins = [
    np.linspace(low, high, num_bins)
    for low, high in zip(env.observation_space.low.flatten(), env.observation_space.high.flatten())
]

def discretize_state(state):
    state = state.flatten()  # Spłaszcz stan
    discrete_state = tuple(np.digitize(s, bins) - 1 for s, bins in zip(state, obs_bins))
    return discrete_state

Q = {}

def get_q_value(state, action):
    """Pobiera wartość Q dla danego stanu i akcji, inicjalizując ją zerem, jeśli nie istnieje."""
    return Q.get((state, action), 0.0)

def set_q_value(state, action, value):
    """Ustawia wartość Q dla danego stanu i akcji."""
    Q[(state, action)] = value

def choose_action(state):
    if np.random.uniform(0, 1) < epsilon:
        return env.action_space.sample()
    else:
        q_values = [get_q_value(state, action) for action in range(env.action_space.n)]
        return np.argmax(q_values)

def learn(state, state2, reward, action):
    predict = get_q_value(state, action)
    max_q_next = max(get_q_value(state2, a) for a in range(env.action_space.n))
    target = reward + gamma * max_q_next
    set_q_value(state, action, predict + lr_rate * (target - predict))

for episode in range(total_episodes):
    state, _ = env.reset()
    state = discretize_state(state)  # Dyskretyzacja stanu
    total_reward = 0  # Sumowanie nagród w trakcie jednego epizodu
    t = 0

    while t < max_steps:
        env.render()
        action = choose_action(state)
        next_state, reward, done, truncated, info = env.step(action)
        next_state = discretize_state(next_state)  # Dyskretyzacja następnego stanu
        # Wypisz informacje o nagrodzie i akcji
        print(f"Epizod {episode + 1}, Krok {t + 1}: Akcja: {action}, Nagroda: {reward}")
        print(info)  # Debugowanie zawartości info

        learn(state, next_state, reward, action)
        state = next_state

        total_reward += reward

        t += 1

        if done:
            break

        time.sleep(0.1)

    print(f"Epizod {episode+1} zakończony. Całkowita nagroda: {total_reward}\n")

print("Q-table po treningu:")
print(Q)

# Zapisz wyniki do pliku
with open("bowling_results.txt", 'w') as f:
    f.write("Q-table po treningu:\n")
    f.write(str(Q))
