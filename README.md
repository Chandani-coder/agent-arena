
**Agent Arena**
Multi-Agent Reward Experiment

Agent Arena is a small experimental environment for studying how rewarding agreement between agents can affect correctness and coordination.

"When two agents receive an additional reward for aggreing, do they become better coordinated -- or do they start aggreing even when they are wrong?"

The experiment varies an agreement bonus and measures its effect on agent accuracy, agreement frequency, and incorrect agreements.

**Research Question**
Multi-agent systems can be rewarded for cooperating or reaching consensus.
However, rewarding agreement may create an unintended incentive.

**Agents may learn that agreeing is valuable even when the agreed-upon answer is incorrect.**

Agent Arena investigates this trade-off experimentally.

We sweep across different agreement bonuses and observe whether increasing the reward for coordination preserves task correctness.

**Experiment Setup**

Two agents interact with a shared verification environment:

     VERIFICATION ENVIRONMENT 
            ||
        OBSERVATION
        |         | 
    AGENT A     AGENT B
          (actions)
             ||
        Reward Function 
              +
           Agreemennt
             Bonus

For every episode:

1. The environment generates a verification task.
2. Both agents receive their observations.
3. Each agent independently chooses an action.
4. The environment calculates their rewards.
5. An additional agreement bonus can be applied when 
   both agents choose the same action.
6. Each agent learns from its reward.
7. The resulting actions are compared against the environment's ground truth.

**Variables**
-> Independent Variable 
++ Agreement Bonus ++
The experiment currently evaluates:-
   0
   0.5
   1
   2
   3
   5
The bonus represents an additional reward associated with the agents reaching the same decision.

-> Dependent Variables
++ Agent Accuracy ++
The fraction of episodes in which an agent's action matches the environment's ground truth.

  accuracy = correct decisions / total episodes

Accuracy is measured independently for Agent A and Agent B.

++ Agreement Rate ++
The fraction of episodes in which both agents select the same action.

  agreement rate = agreements / total episodes

++ Correct Agreement Rate ++
The fraction of all episodes where the agents both agree and their shared decision is correct.

  correct agreement rate = correct agreements / total episodes

++ Wrong Agreement Rate ++
The fraction of all episodes where the agents agree on an incorrect answer.
   wrong agreement rate= wrong agreements / total episodes

++ Wrong | Agreement ++
The fraction of agreements that are incorrect.

wrong | agreement = wrong agreements / total agreements

This is particularly important because a high agreement rate alone does not imply reliable coordination.

**Experimental Design**
Each agreement bonus is evaluated across multiple independent trials.

The Streamlit interface allows the number of episodes and trials to be configured.

Default settings:

   Episodes: 1000
   Trials per bonus: 10

For each trial, the agents are initialzed and trained for the specified number of episodes.

The experiment then aggregate results across trials using:
   (i) Mean          (ii) Standard deviation

This helps distinguish the overall trend from variation between individual runs.

**Observed Pattern**
The experiment shows a sharp transition around an agreement bonus of approximately 2.

At lower bonuses:

   Agreement ~ 64%
   Accuracy ~ 76-77%
   Wrong agreements ~ 8-11%

At higher bonuses:

   Agreement ~ 85-87%
   Accuracy ~ 53-55%
   Wrong agreements ~ 43-46%

The impoertant observation is that agreement increases while correctness decreases.

This suggests that, in this environment, sufficiently strong agreement incentives can produce a form of coordination failure: the agents become more likely to reach the same decision, but that shared decision is increasingly likely to be wrong.

**Why This Matters**
A multi-agent system can appear highly coordinated while actually becoming less reliable.

If evaluation focuses only on:
    "Do the agents agree?"

then increasing the agreement reward may look successful.

But if we additionally ask:
   "Are they correct?"
   "How often are their agreements wrong?"
a different picture emerges.

Agent Arena therefore treats agreement and correctness as separate dimensions.

The experimen demonstrates why optimizing a proxy such as consensus can be dangerous when the proxy is not perfectly aligned with the underlying objective.

**Dashboard**
The Streamlit dashboard provides:

++ Accuracy vs Agreement Bonus++
Compares Agent A and Agent B accuracy as the agreement reward changes.

++ Agreement Behaviour ++
Shows: 
   -> Agreement Rate
   -> Correct Agreement Rate
   -> Wrong Agreement Rate

as a function of the agreement bonus.

**Detailed Results**

The dashboard also exposes the aggregated experimental results, including mean and standard deviation across trials.

**Reproducing the Experiment**
The main experiment is controlled from the Streamlit sidebar.

You can change:
-> Number of episodes
-> Number of trials
and rerun the reward sweep.

The reward sweep evaluates the predefined agreement bonuses:
     bonuses= [0,0.5,1,2,3,5]

**Limitations**
This is a controlled experimental environment rather than a realistic deployment-scale multi-agent system.

The results should therefore be interpreted as evidence about the behaviour of the implemented environment and agents, not as proof that agreement bonuses will always produce the same behaviour in other systems.

Important factors for future experiments include:

-> Different agent learning strategies
-> Different environment difficulty
-> Different reward structures
-> More trials
-> More random seeds
-> Alternative agreement incentives
-> Different observation structures
-> Longer training horizons
-> Statistical significance testing


**Core Takeaway**
  Agreement is not the same thing as correctness.

A reward function that strongly incentives consensus can improve coordination metrics while simultaneously degrading the reliability of the system.

Agent Arena is designed to make that trade-off visible.
