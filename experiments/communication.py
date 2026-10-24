from src.agent import Agent
from src.environment import VerificationEnvironment

env= VerificationEnvironment()

agent_a= Agent()
agent_b= Agent()

episodes=[]

for episode in range(1000):
    observation_a, observation_b = env.reset()

    # Stage 1: independent decisions

    initial_action_a= agent_a.choose_action(observation_a)
    initial_action_b= agent_b.choose_action(observation_b)

    # Stage2 : agents see each other's decisions

    final_action_a= initial_action_a
    final_action_b= initial_action_b

    if initial_action_b!= initial_action_a:
        final_action_a= initial_action_b

    if initial_action_a != initial_action_b:
        final_action_b= initial_action_a

    #Stage 3: environment evaluates final decisions

    reward_a, reward_b = env.step(
        final_action_a,
        final_action_b,
        agreement_bonus=0
    )

    episodes.append({
        "episode": episode,
        "truth": env.truth,
        "observation_a": observation_a,
        "observation_b": observation_b,
        "initial_action_a":initial_action_a,
        "initial_action_b": initial_action_b,
        "final_action_a":final_action_a,
        "final_action_b": final_action_b,
        "reward_a": reward_a,
        "reward_b": reward_b,
        "agreement": final_action_a==final_action_b,
        "correct_a": final_action_a==env.truth,
        "correct_b": final_action_b==env.truth
    })

    agent_a.learn(
        observation_a,
        final_action_a,
        reward_a
    )

    agent_b.learn(
        observation_b,
        final_action_b,
        reward_b
    )

    total= len(episodes)

    accuracy_a= sum(
        e["correct_a"] for e in episodes
    )/total

    accuracy_b= sum(
        e["correct_b"] for e in episodes
    )/total

    agreement_rate= sum(
        e["agreement"] for e in episodes
    )/total

    wrong_agreements= sum(
        e["agreement"] and not e["correct_a"]
        for e in episodes
    )

    wrong_agreement_rate= wrong_agreements/total
    print("\n ===COMMUNICATION ===")
    print(f"Agent A accuracy:{accuracy_a: .2%}")
    print(f"Agent B accuracy: {accuracy_b: .2%}")
    print(f"Agreement rate:{agreement_rate: .2%}")
    print(f"Wrong agreement rate: {wrong_agreement_rate:.2%}")