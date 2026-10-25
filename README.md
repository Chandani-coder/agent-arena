# Agent Arena

### Multi-Agent Reward Experiment

Agent Arena is an interactive experiment for studying how **reward design changes the behaviour of multiple learning agents**.

The experiment focuses on a simple question:

> **What happens when agents are increasingly rewarded for agreeing with each other?**

The system runs two agents in a verification environment and sweeps across different agreement-bonus values. It measures whether increased coordination improves useful agreement—or simply encourages agents to agree, including when they are wrong.

---

## Why This Matters

In multi-agent systems, agreement can look like successful coordination.

But **agreement is not the same as correctness**.

If agents receive additional reward for agreeing, they may learn that reaching consensus is more valuable than independently verifying the evidence. This creates a potential failure mode:

**Higher agreement → lower verification pressure → more incorrect agreement**

Agent Arena provides a small, controlled environment for observing this trade-off.

---

## Experiment

For each agreement-bonus value, the system runs multiple independent trials.

### Reward sweep

The current experiment evaluates:

```text
0
0.5
1
2
3
5
```

For every bonus, the agents interact with the environment for a configurable number of episodes.

The experiment can be configured through the Streamlit sidebar:

- **Episodes** — number of interaction episodes per trial
- **Trials per bonus** — independent repetitions for each reward setting

---

## Metrics

The experiment tracks several complementary measurements.

### Individual accuracy

The fraction of episodes in which each agent selects the correct answer.

```text
Agent Accuracy
```

### Agreement rate

How often both agents select the same answer.

```text
Agreement Rate
```

### Correct agreement rate

How often the agents agree **and their shared answer is correct**.

```text
Correct Agreement Rate
```

### Wrong agreement rate

How often the agents agree **and their shared answer is incorrect**.

```text
Wrong Agreement Rate
```

This distinction is the key measurement of the experiment.

A system that increases agreement while also increasing wrong agreement may be becoming **more coordinated without becoming more reliable**.

---

## Results

The observed reward sweep shows a clear behavioural transition.

At low agreement bonuses, the agents maintain relatively high individual accuracy and moderate agreement.

As the agreement bonus increases:

- agreement rises substantially
- individual accuracy falls
- incorrect agreement increases
- the system reaches a much more consensus-heavy behaviour

In the current run, the agreement rate increases from roughly **0.64 at bonus 0** to roughly **0.87 at bonus 3–5**, while individual accuracy falls from roughly **0.76–0.77** to roughly **0.53**.

This suggests that the additional agreement reward can dominate the agents' behaviour: they become better at reaching consensus, but the consensus becomes substantially less reliable.

These results are from the current experimental configuration and should be treated as an observation of this environment, not as a general claim about all multi-agent systems.

---

## Architecture

```text
                ┌─────────────────────┐
                │    Streamlit UI     │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │   Reward Sweep       │
                │  0 → 5 bonus        │
                └──────────┬──────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
       ┌─────────────┐           ┌─────────────┐
       │   Agent A   │           │   Agent B   │
       └──────┬──────┘           └──────┬──────┘
              │                         │
              └──────────┬──────────────┘
                         ▼
              ┌─────────────────────┐
              │ Verification        │
              │ Environment         │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │ Metrics & Statistics│
              └─────────────────────┘
```

The experiment separates:

- agent decision-making
- environment dynamics
- reward calculation
- learning
- experiment aggregation
- visualization

---

## Project Structure

```text
agent-arena/
│
├── app.py
├── src/
│   ├── agent.py
│   └── environment.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Running Locally

Clone the repository and enter the project:

```bash
git clone <your-repository-url>
cd agent-arena
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

Activate it on Linux/macOS:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

The application will open in your browser.

---

## Using the Experiment

1. Choose the number of episodes.
2. Choose the number of trials per reward setting.
3. Click **Run Experiment**.
4. Inspect the accuracy and agreement plots.
5. Compare correct versus incorrect agreement.
6. Use the detailed results table to examine the underlying statistics.

---

## What This Experiment Demonstrates

The important result is not simply that agreement increases.

The more interesting observation is the **separation between coordination and correctness**.

A reward can successfully optimize the behaviour it explicitly rewards while simultaneously degrading another property that we actually care about.

In this environment:

```text
Agreement ↑
       │
       ├── Correct agreement
       │
       └── Wrong agreement ↑
           
Accuracy ↓
```

This is a small experimental demonstration of a broader problem in multi-agent learning:

> **Optimizing for coordination does not necessarily produce reliable coordination.**

---

## Limitations

This is a controlled experimental environment, not a benchmark for real-world multi-agent systems.

Important limitations include:

- only two agents are evaluated
- the environment is intentionally simplified
- the reward sweep uses a small set of bonus values
- results depend on the agent and environment implementation
- the current experiment measures behavioural outcomes rather than establishing a general causal law

The experiment is therefore best viewed as a **minimal testbed for reward-induced coordination behaviour**.

---

## Future Work

Potential extensions include:

- larger numbers of agents
- asymmetric reward structures
- noisy or incomplete evidence
- independent versus shared histories
- adversarial agents
- different learning algorithms
- longer training horizons
- confidence-aware agreement
- evidence-based verification
- statistical significance testing
- detecting persistent incorrect consensus
- comparing agreement reward against explicit verification rewards

---

## Tech Stack

- Python
- Streamlit
- Statistics
- Custom multi-agent environment

---

## Author

**Chandani**

Built as an experimental project exploring **multi-agent learning, reward design, coordination, and reliability**.
