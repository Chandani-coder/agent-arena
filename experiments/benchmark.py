import random
import json
from src.agent import Agent
from src.environment import VerificationEnvironment

EPISODES= 1000
TRIALS= 20

def calculate_metrics(episodes):
    total= len(episodes)

    accuracy_a= sum(e["correct_a"] for e in episodes)/total

    accuracy_b= sum( e["correct_b"] for e in episodes)/total

    agreement_count = sum( e["agreement"] for e in episodes)

    agreement_rate= agreement_count/total

    wrong_agreements= sum( e["agreement"] and not e["correct_a"] for e in episodes)

    wrong_agreement_rate= wrong_agreements/total

    if agreement_count>0:
        wrong_given_agreement= ( wrong_agreements/ agreement_count)

    else:
        wrong_given_agreement= 0

    return{ "accuracy_a": accuracy_a,
    "accuracy_b":accuracy_b,
    "agreement_rate": agreement_rate,
    "wrong_agreement_rate": wrong_agreement_rate,
    "wrong_given_agreement": wrong_given_agreement}

def run_experiment(condition, seed):
    random.seed(seed)

    env= VerificationEnvironment()

    agent_a= Agent()
    agent_b= Agent()

    episodes= []

    for episode in range(EPISODES):
        observation_a, observation_b = env.reset()

        #CONDITION 1: BASELINE
        if condition=="baseline":

            action_a= agent_a.choose_action(observation_a)
            action_b= agent_b.choose_action(observation_b)

            reward_a, reward_b = env.step(
                action_a, action_b, agreement_bonus=0
            )

            #CONDITION 2 : COMMUNICATION

        elif condition == "communication":

            initial_action_a = agent_a.choose_action(observation_a)
            initial_action_b = agent_b.choose_action(observation_b)

            # Simple communication
            # each agent sees the other's decision

            action_a = initial_action_b
            action_b= initial_action_a

            reward_a, reward_b = env.step(
                action_a, action_b, agreement_bonus=0
            )

        #CONDITION 3: AGREEMENT PRESSURE

        elif condition == "agreement_pressure":

            action_a= agent_a.choose_action(observation_a)
            action_b= agent_b.choose_action(observation_b)

            reward_a, reward_b = env.step(
                action_a, action_b, agreement_bonus=2
            )

        else:
            raise ValueError(
                f"Unknown condition: {condition}"
            )

        episodes.append({
            "correct_a":action_a==env.truth,
            "correct_b": action_b ==env.truth,
            "agreement": action_a ==action_b
        })

        agent_a.learn(
            observation_a,action_a,reward_a
        )

        agent_b.learn(
            observation_b, action_b, reward_b
        )

    return calculate_metrics(episodes)

def average_results(results):
    return{
        metric: sum( result[metric] for result in results)/len(results)
        for metric in results[0]
    }

conditions=[
        "baseline","communication","agreement_pressure"
]
all_results={}

for condition in conditions:
    trial_results = []
    for trial in range(TRIALS):
        result = run_experiment(
            condition, seed=trial
        )
        trial_results.append(result)

    all_results[condition] = average_results(
        trial_results
    )

print("\n" + "=" * 60)
print("           AGENT ARENA ")
print("           REPEATED EXPERIMENT")
print("=" * 60)

for condition, result in all_results.items():

    print(f"\n--- {condition.upper()}---")

    print(f"Agent A accuracy:   "
    f"{result["accuracy_a"]:.2%}")

    print(
        f"Agent B accuracy:   "
        f"{result["accuracy_b"]:.2%}"
    )

    print("Agreement rate:    "
    f"{result["agreement_rate"]:.2%}")

    print(f"Wrong agreement rate:  "
    f"{result["wrong_agreement_rate"]:.2%}")

    print(f" Wrong | agreement:   "
    f"{result["wrong_given_agreement"]:.2%}")

with open("results/benchmark_results.json", "w") as f:
    json.dump(all_results, f, indent=4)
print("\nResults saved to results/benchmark_results.json")

print("\n" + "=" * 60)
