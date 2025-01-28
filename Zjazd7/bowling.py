import gym
import numpy as np
import time

env = gym.make("Bowling-v4", render_mode="human")

epsilon = 0.9
max_steps = 500
total_episodes = 100

lr_rate = 0.90
gamma = 0.80

Q = {}


def get_q_value(state, action):
    """
    Pobiera wartość Q dla danego stanu i akcji. Jeśli para (stan, akcja) nie istnieje,
    zwraca 0.0 jako wartość domyślną.

    Args:
        state (np.ndarray): Obecny stan gry, przedstawiony jako wektor lub tablica.
        action (int): Indeks akcji, dla której chcemy uzyskać wartość Q.

    Returns:
        float: Wartość Q dla danej pary (stan, akcja), domyślnie 0.0, jeśli nie istnieje w tabeli Q.

    Opis:
        Funkcja ta sprawdza tabelę Q, czy zawiera wartość dla podanej pary (stan, akcja).
        Jeśli para nie istnieje w tabeli, domyślnie zwraca 0.0, co oznacza, że agent jeszcze nie ocenił tej pary.
    """
    return Q.get((tuple(state.flatten()), action), 0.0)


def set_q_value(state, action, value):
    """
    Ustawia wartość Q dla danego stanu i akcji w tabeli Q.

    Args:
        state (np.ndarray): Obecny stan gry, przedstawiony jako wektor lub tablica.
        action (int): Indeks akcji, dla której chcemy ustawić wartość Q.
        value (float): Wartość Q, którą chcemy przypisać do danej pary (stan, akcja).

    Opis:
        Funkcja ta aktualizuje tabelę Q, przypisując określoną wartość Q dla pary (stan, akcja).
        Jeśli ta para (stan, akcja) jeszcze nie istnieje w tabeli Q, zostanie dodana.
    """
    Q[(tuple(state.flatten()), action)] = value


def choose_action(state):
    """
    Wybiera akcję na podstawie strategii epsilon-greedy. Epsilon-greedy to metoda,
    w której agent z pewnym prawdopodobieństwem (epsilon) wybiera akcję losowo (eksploracja),
    a z pozostałym prawdopodobieństwem wybiera akcję, która maksymalizuje wartość Q (eksploatacja).

    Args:
        state (np.ndarray): Obecny stan gry, przedstawiony jako wektor lub tablica.

    Returns:
        int: Indeks wybranej akcji na podstawie strategii epsilon-greedy.

    Opis:
        Ta funkcja zapewnia balans pomiędzy eksploracją (próbowanie nowych akcji) a eksploatacją
        (wybieranie najlepszych znanych akcji). Im mniejsze epsilon, tym więcej agent będzie eksploatował
        wcześniej nauczone akcje.
    """
    if np.random.uniform(0, 1) < epsilon:
        return env.action_space.sample()  # Eksploracja
    else:
        q_values = [get_q_value(state, action) for action in range(env.action_space.n)]
        return np.argmax(q_values)  # Eksploatacja


def learn(state, state2, reward, action):
    """
    Aktualizuje tabelę Q na podstawie algorytmu Q-learning. Funkcja oblicza wartość Q na podstawie
    bieżącej wartości Q, nagrody oraz maksymalnej wartości Q w przyszłym stanie.

    Args:
        state (np.ndarray): Obecny stan gry przed wykonaniem akcji.
        state2 (np.ndarray): Nowy stan gry po wykonaniu akcji.
        reward (float): Nagroda za wykonaną akcję.
        action (int): Indeks akcji, którą wykonał agent.

    Opis:
        Zgodnie z równaniem Q-learning, wartość Q dla pary (stan, akcja) jest aktualizowana na podstawie
        nagrody oraz maksymalnej wartości Q w następnym stanie. Działa to w następujący sposób:
        Q(s, a) ← Q(s, a) + α * (r + γ * max_a Q(s', a) - Q(s, a)),
        gdzie α to współczynnik uczenia, γ to współczynnik dyskontowania, r to nagroda,
        a max_a Q(s', a) to maksymalna wartość Q w stanie s'.
    """
    predict = get_q_value(state, action)
    max_q_next = max(get_q_value(state2, a) for a in range(env.action_space.n))
    target = reward + gamma * max_q_next
    set_q_value(state, action, predict + lr_rate * (target - predict))


for episode in range(total_episodes):
    state, _ = env.reset()
    total_reward = 0
    t = 0

    while t < max_steps:
        env.render()

        action = choose_action(state)
        next_state, reward, done, truncated, info = env.step(action)

        learn(state, next_state, reward, action)
        state = next_state

        total_reward += reward

        t += 1

        if done or truncated:
            break

        time.sleep(0.1)

    print(f"Epizod {episode + 1} zakończony. Całkowita nagroda: {total_reward}\n")

    epsilon = max(0.1, epsilon * 0.99)

print("Q-table po treningu:")
print(Q)

with open("bowling_results.txt", 'w') as f:
    f.write("Q-table po treningu:\n")
    f.write(str(Q))

env.close()
