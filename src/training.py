from src.agent import Agent
from src.environment import VerificationEnvironment

env= VerificationEnvironment()
agent_a= Agent()
agent_b= Agent()

rewards_a=[]
rewards_b=[]
episodes=[]

for episode in range(1000):
    observation_a,observation_b=env.reset()

    action_a=agent_a.choose_action(observation_a)
    action_b=agent_b.choose_action(observation_b)

    reward_a,reward_b=env.step(action_a,action_b,agreement_bonus=0)
    rewards_a.append(reward_a)
    rewards_b.append(reward_b)
    
    episode_data= { 
        "episode":episode,
        "truth": env.truth,
        "observation_a" : observation_a,
        "observation_b": observation_b,
        "action_a": action_a,
        "action_b": action_b,
        "reward_a": reward_a,
        "reward_b": reward_b,
        "agreement": action_a == action_b,
        "correct_a": action_a == env.truth,
        "correct_b": action_b == env.truth
    }

    episodes.append(episode_data)
    agent_a.learn(observation_a,action_a,reward_a)
    agent_b.learn(observation_b,action_b,reward_b)

    if (episode+1)%100==0:
        avg_a= sum(rewards_a[-100:])/100
        avg_b= sum(rewards_b[-100:])/100

        print(
            f"Episodes {episode-98}-{episode+1}:"
            f"A reward:{avg_a:.2f} |"
            f"B reward: {avg_b:.2f}"
        )
total = len(episodes)

accuracy_a= sum(e["correct_a"] for e in episodes)/total
accuracy_b= sum(e["correct_b"] for e in episodes) / total

agreement_rate= sum(
    e["agreement"] for e in episodes
)/total

wrong_agreements= sum( e["agreement"]and not e["correct_a"]
for e in episodes)

wrong_agreement_rate= wrong_agreements/total

print("\n ===BASELINE===")
print(f"Agent A accuracy: {accuracy_a: .2%}")
print(f"Agent B accuracy: {accuracy_b: .2%}")
print(f"Agreement rate: {agreement_rate: .2%}")
print(f"Wrong agreement rate:{ wrong_agreement_rate:.2%}")