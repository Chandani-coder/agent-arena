import random

class VerificationEnvironment:
    def __init__(self, evidence_accuracy=0.8):
        self.evidence_accuracy=evidence_accuracy
        self.truth= None

    def reset(self):
        self.truth = random.choice([0,1])
        evidence_a = self._generate_evidence()
        evidence_b = self._generate_evidence()

        return evidence_a, evidence_b

    def _generate_evidence(self):
        if random.random() < self.evidence_accuracy:
            return self.truth

        return 1-self.truth

    def step(self,action_a,action_b,agreement_bonus=0):
        correct_a = action_a == self.truth
        correct_b = action_b == self.truth
        reward_a = 1 if correct_a else -1
        reward_b = 1 if correct_b else -1

        if action_a==action_b:
            reward_a+=agreement_bonus
            reward_b+=agreement_bonus
        return reward_a, reward_b


