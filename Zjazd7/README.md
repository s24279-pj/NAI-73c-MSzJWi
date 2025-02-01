# Q-learning for Bowling-v4 Environment

## Project Description

This project implements a **Q-learning** agent to play the **Bowling-v4** game using OpenAI Gym. The agent learns optimal actions through reinforcement learning, balancing exploration and exploitation.

### Features:

- Uses **Q-learning** to train the agent.
- Implements **epsilon-greedy** action selection.
- Stores and updates **Q-values** dynamically.
- Saves the trained **Q-table** for future use.
- Provides real-time game rendering.

## Project Structure

### Files and Scripts

- `bowling_q_learning.py`: Main script that trains the Q-learning agent in the **Bowling-v4** environment.
- `bowling_results.txt`: Stores the **Q-table** after training.
- `README.md`: Documentation for the project (this file).

## Algorithm Details

### Hyperparameters:

- **Epsilon (ε)**: 0.83 (decays over time to encourage exploitation)
- **Max Steps per Episode**: 600
- **Total Episodes**: 100
- **Learning Rate (α)**: 0.90
- **Discount Factor (γ)**: 0.80

### Functions:

- `get_q_value(state, action)`: Retrieves the **Q-value** for a given state-action pair.
- `set_q_value(state, action, value)`: Updates the **Q-value** in the Q-table.
- `choose_action(state)`: Implements **epsilon-greedy** action selection.
- `learn(state, state2, reward, action)`: Updates the Q-table using the Q-learning formula.

## Usage

### Requirements

Install the required dependencies before running the script:

```bash
pip install gym numpy
```

If the script does not work, you may need to install the Atari dependencies for Gym:

```bash
pip install gym[atari]
```

### Running the Script

To start training the Q-learning agent, run:

```bash
python bowling_q_learning.py
```

### Output

- The agent plays **100 episodes** of Bowling-v4.
- Displays the **total reward** after each episode.
- Saves the **Q-table** to `bowling_results.txt` after training.

  ![Screenshot](https://github.com/s24279-pj/NAI-73c-MSzJWi/blob/main/Zjazd7/images/Zrzut%20ekranu%202025-01-28%20o%2013.58.21.png)

## Evaluation

The agent's performance is measured by:

- **Total reward per episode**: A higher reward indicates better performance.
- **Q-table**: The final Q-table provides learned action values.

## Demo
[![Video](https://github.com/s24279-pj/NAI-73c-MSzJWi/edit/main/Zjazd7/images/movie.mov)]

## Authors

- Marta Szpilka
- Jakub Więcek
