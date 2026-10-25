import streamlit as st
import statistics
from src.agent import Agent
from src.environment import VerificationEnvironment

st.set_page_config(
    page_title="Agent Arena",
    layout= "wide"
)

st.title(" Agent Arena ")

st.subheader(" Multi Agent Reward Experiment")

st.write("Explore how changing the reward structure affects "
"agent accuracy and agreement.")


#EXPERIMENT SETTINGS

st.sidebar.header("Experiment settings")

episodes= st.sidebar.slider(
    "Episodes",
    min_value=100,
    max_value= 2000,
    value= 1000,
    step=100,
)

trials =  st.sidebar.slider(
    "Trials per bonus ",
    min_value=2,
    max_value=20,
    value = 10,
    step= 1
)

def run_experiment(agreement_bonus, episodes, seed= None):
    if seed is not None:
        import random
        random.seed(seed)

    env= VerificationEnvironment()

    agent_a= Agent()
    agent_b= Agent()

    correct_a=0
    correct_b=0
    agreements=0
    correct_agreements=0
    wrong_agreements=0

    for _ in range(episodes):
        observation_a, observation_b = env.reset()

        action_a = agent_a.choose_action(observation_a)
        action_b = agent_b.choose_action(observation_b)

        reward_a, reward_b= env.step(
            action_a, action_b, agreement_bonus=agreement_bonus
        )

        agent_a.learn(
            observation_a,
            action_a,
            reward_a
        )
        
        agent_b.learn(
            observation_b, 
            action_b, 
            reward_b
        )

        if action_a == env.truth:
            correct_a +=1

        if action_b == env.truth:
            correct_b +=1

        if action_a==action_b:
            agreements+=1

            if action_a == env.truth:
                correct_agreements+=1
            else:
                wrong_agreements+=1

    accuracy_a= correct_a / episodes
    accuracy_b= correct_b/ episodes 
    agreement_rate= agreements / episodes

    correct_agreement_rate = correct_agreements / episodes
    wrong_agreement_rate = wrong_agreements / episodes

    if agreements > 0:
        wrong_given_agreement=(wrong_agreements/agreements)
        correct_given_agreement= correct_agreements / agreements
    else:
        wrong_given_agreement=0
        correct_given_agreement=0

    return { 
        "accuracy_a": accuracy_a,
        "accuracy_b":accuracy_b,
        "agreement_rate": agreement_rate,
        "wrong_given_agreement": wrong_given_agreement,
        "correct_given_agreement": correct_given_agreement,
        "correct_agreement_rate":correct_agreement_rate,
        "wrong_agreement_rate": wrong_agreement_rate,
    }

def run_reward_sweep(episodes, trials):
    bonuses=[0,0.5,1,2,3,5]
    results= []

    for bonus in bonuses:

        trial_results=[]
    
        for trial in range(trials):
            result = run_experiment(
                agreement_bonus=bonus,
                episodes=episodes,
                seed= trial
            )
            trial_results.append(result)

        results.append({
            "Agreement Bonus": bonus,
            "Agent A Accuracy Mean": sum(
                r["accuracy_a"] for r in trial_results
                )/trials,

            "Agent A Accuracy Std": statistics.stdev(
                r["accuracy_a"] for r in trial_results
            ),

            "Agent B Accuracy Mean": sum(
                r["accuracy_b"] for r in trial_results
            )/trials,

            "Agent B Accuracy Std": statistics.stdev(
                r["accuracy_b"] for r in trial_results
            ),

            "Agreement Rate Mean": sum(
                r["agreement_rate"] for r in trial_results
            )/trials,

            "Agreement Rate Std": statistics.stdev(
                r["agreement_rate"] for r in trial_results
            ),

            "Wrong | Agreement Mean": sum(
                r["wrong_given_agreement"]
                for r in trial_results
            )/trials,

            "Wrong | Agreement Std": statistics.stdev(
                r["wrong_given_agreement"] for r in trial_results
            ),

            "Correct | Agreement Mean": sum(
                r["correct_given_agreement"]
                for r in trial_results
            )/trials,

            "Correct | Agreement Std": statistics.stdev(
                r["correct_given_agreement"] for r in trial_results
            ),

            "Correct Agreement Rate Mean": sum(
                r["correct_agreement_rate"] for r in trial_results
            )/trials,

            "Wrong Agreement Rate Mean": sum(
                r["wrong_agreement_rate"] for r in trial_results
            )/trials,

            "Correct Agreement Rate Std":statistics.stdev(
                r["correct_agreement_rate"] for r in trial_results
            ),

            "Wrong Agreement Rate Std": statistics.stdev(
                r["wrong_agreement_rate"] for r in trial_results
            ),

        })

    return results


#RUN EXPERIMENT
if st.button("▶ Run Experiment"):
    with st.spinner("Running Agent Arena Experiment..."):
        sweep_results= run_reward_sweep(episodes, trials)

    st.session_state["sweep_results"] = sweep_results

    
#RESULTS
if "sweep_results" in st.session_state:

    results= st.session_state["sweep_results"]

    st.divider()
    st.header("Reward Sweep Results")

    st.write(
        "How does increasing the agreement reward affect "
        "accuracy, agreement, and incorrect agreement?"
    )

    chart_data={
        "Agreement Bonus": [
            r["Agreement Bonus"] for r in results
        ],
        "Agent A Accuracy":[
            r["Agent A Accuracy Mean"] for r in results
        ],
        "Agent B Accuracy":[
            r["Agent B Accuracy Mean"] for r in results
        ],
        "Agreement Rate":[
            r["Agreement Rate Mean"] for r in results
        ],
        "Wrong | Agreement":[
            r["Wrong | Agreement Mean"] for r in results
        ],
        "Correct | Agreement":[
            r["Correct | Agreement Mean"] for r in results
        ],
        "Correct Agreement Rate":[
            r["Correct Agreement Rate Mean"] for r in results
        ],
        "Wrong Agreement Rate":[
            r["Wrong Agreement Rate Mean"] for r in results
        ],  
    }

    # Accuracy chart
    st.subheader("Accuracy vs Agreement Bonus")

    st.line_chart(
        chart_data,
        x="Agreement Bonus",
        y=[
            "Agent A Accuracy",
            "Agent B Accuracy",
        ]
    )

    # Agreement behaviour chart

    st.subheader("Agreement Behaviour")

    st.line_chart(
        chart_data,
        x= "Agreement Bonus",
        y=[
            "Agreement Rate",
            "Correct Agreement Rate",
            "Wrong Agreement Rate"
        ]
    )
    # Raw results table

    st.subheader("Detailed Results")

    st.dataframe(
        results,
        width="stretch"
    )

    st.info(
        "Increasing the agreement reward can push agents toward"
        "higher agreement. The important question is whether this"
        "coordination preserves correctness or increases incorrect"
        "agreements."
    )

