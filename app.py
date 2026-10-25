import streamlit as st

from src.agent import Agent
from src.environment import VerificationEnvironment

st.set_page_config(
    page_title="Agent Arena",
    layout= "wide"
)

# TITLE 
st.title(" Agent Arena ")
#SUBHEADER
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

agreement_bonus= st.sidebar.slider(
"Agreement Bonus",
min_value=0.0,
max_value=5.0, 
value=0.0,
step=0.5
)

def run_experiment(agreement_bonus, episodes):
    env= VerificationEnvironment()

    agent_a= Agent()
    agent_b= Agent()

    correct_a=0
    correct_b=0
    agreements=0
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

            if action_a != env.truth:
                wrong_agreements+=1

    accuracy_a= correct_a / episodes
    accuracy_b= correct_b/ episodes 
    agreement_rate= agreements / episodes

    if agreements > 0:
        wrong_given_agreement=(wrong_agreements/agreements)
    else:
        wrong_given_agreement=0
    return { 
        "accuracy_a": accuracy_a,
        "accuracy_b":accuracy_b,
        "agreement_rate": agreement_rate,
        "wrong_given_agreement": wrong_given_agreement
    }

#RUN EXPERIMENT

if st.button("▶ Run Experiment"):
    baseline = run_experiment(
        agreement_bonus=0,
        episodes= episodes
    )
    pressure= run_experiment(
        agreement_bonus= agreement_bonus,
        episodes= episodes
    )
    st.session_state["baseline"] = baseline
    st.session_state["pressure"]= pressure
    
#RESULTS

if "baseline" in st.session_state:

    baseline= st.session_state["baseline"]
    pressure= st.session_state["pressure"]

    st.divider()
    st.header("Experiments Results")

    chart_data={
        "Metric": [
            "Agent A Accuracy",
            "Agent B Accuracy",
            "Agreement Rate",
            "Wrong | Agreement"
        ],
        "Baseline":[
            baseline["accuracy_a"],
            baseline["accuracy_b"],
            baseline["agreement_rate"],
            baseline["wrong_given_agreement"]
        ],
        "Agreement Pressure":[
            pressure["accuracy_a"],
            pressure["accuracy_b"],
            pressure["agreement_rate"],
            pressure["wrong_given_agreement"]
        ]
    }

    st.bar_chart(
        chart_data,
        x= "Metric",
        y=["Baseline", "Agreement Pressure"]
    )

    st.info(
        "When agreement is rewarded, agents may learn to coordinate"
        "more strongly-even when that coordination leads to incorrect decisions."
    )

    st.write(
        "Does rewarding agreement improve cooperation "
        "or encourage agents to agree when they are wrong?"
    )

    col1, col2 = st.columns(2)
    
    #BASELINE
    with col1:
        st.subheader(" 🔵Baseline")

        st.caption("Agreement bonus= 0")
        
        st.metric(
            "Agent A Accuracy",
            f"{baseline["accuracy_a"]:.1%}"
        )

        st.metric(
            "Agent B Accuracy",
            f"{baseline["accuracy_b"]:.1%}"
        )

        st.metric(
            "Agreement Rate",
            f"{baseline["agreement_rate"]:.1%}"
        )

        st.metric("Wrong Agreement",
        f"{baseline["wrong_given_agreement"]:.1%}"
        )

    # AGREEMENT PRESSURE
    with col2:
        st.subheader("🔴 Agreement Pressure")

        st.caption(
            f"Agreement bonus={agreement_bonus}"
        )

        st.metric(
            "Agent A Accuracy",
            f"{pressure["accuracy_a"]:.1%}"
        )
        
        st.metric(
            "Agent B Accuracy",
            f"{pressure["accuracy_b"]:.1%}"
        )

        st.metric(
            "Agreement Rate",
            f"{pressure["agreement_rate"]:.1%}"
        )

        st.metric(
            "Wrong Agreement",
            f"{pressure["wrong_given_agreement"]:.1%}"
        )
        

