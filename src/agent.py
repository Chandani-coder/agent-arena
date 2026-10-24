import random

class Agent:
    def __init__(self, learning_rate=0.1, exploration_rate=0.1):
        self.learning_rate = learning_rate
        self.exploration_rate= exploration_rate

        self.q_table={
            0:{0: 0.0, 1:0.0},
            1:{0:0.0, 1:0.0}
        }

    def choose_action(self, observation):
        if random.random() < self.exploration_rate:
            return random.choice([0,1])
        
        return max(
            self.q_table[observation],
            key= self.q_table[observation].get
        )

    def learn(self, observation, action, reward):
        old_value=self.q_table[observation][action]

        new_value= old_value + self.learning_rate*(reward-old_value)

        self.q_table[observation][action]=new_value