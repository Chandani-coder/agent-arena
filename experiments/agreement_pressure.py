from src.agent import Agent
from src.environment import VerificationEnvironment

env= VerificationEnvironment()

agent_a = Agent()
agent_b = Agent()

episodes=[]

for episode in range(1000):
    observation_a, observation_b= env.reset()

    # Agents make independent decisions
    action_a= agent_a.choose_action(observation_a)
    action_b = agent_a.choose_action(observation_b)

    #Environment appliess agreement pressure

    reward_a, reward_b = env.step(
        action_a, action_b, agreement_bonus=2
    )

    episodes.append({
        "episode": episode,
        "truth": env.truth,
        "observation_a": observation_a,
        "observation_b": observation_b,
        "action_a": action_a,
        "action_b":action_b,
        "reward_a": reward_a,
        "reward_b": reward_b,
        "agreement":action_a==action_b,
        "correct_a":action_a==env.truth,
        "correct_b": action_b == env.truth
    })

    #This is where the reward changes the agents

    agent_a.learn(
        observation_a, action_a, reward_a
    )

    agent_b.learn(
        observation_b, action_b, reward_b
    )

    total= len(episodes)

    accuracy_a= sum(e["correct_a"] for e in episodes)/total

    accuracy_b= sum( e["correct_b"] for e in episodes)/total

    agreement_rate= sum( e["agreement"] for e in episodes)/ total

    wrong_agreements= sum(e["agreement"] and not e["correct_a"] for e in episodes)

    wrong_agreement_rate= wrong_agreements/total

    agreement_count=sum(e["agreement"] for e in episodes)

    wrong_agreement_given_agreement=(
        wrong_agreements/ agreement_count if agreement_count>0 else 0
    )

    print("\n===AGREEMENT PRESSURE ===")
    print(f"Agent A accuracy :{ accuracy_a:.2%}")
    print(f"Agent B accuracy :{ accuracy_b:.2%}")
    print(f"Agreement rate:{ agreement_rate:.2%}")
    print(f"Wrong Agreement rate :{wrong_agreement_rate:.2%}")
    print(f"Wrong agreement| agreement"
    f"{wrong_agreement_given_agreement:.2%}")