# this file is used to start an experiment on the kradle platform
# it is used to evaluate the performance of agents over several runs

from kradle import Experiment
from kradle.models import RunRequest
from dotenv import load_dotenv
from kradle import AgentManager
from dataclasses import asdict
import json
import os
import random

load_dotenv()


challenge_slug = "team-kradle:zombie-survival"

agents = [
    "team-kradle:gemini20",
    "team-kradle:claude37-sonnet",
    "team-kradle:llama31",
    "team-kradle:claude-35-haiku",
    "team-kradle:gpt4o-mini",
    "team-kradle:o4-mini",
    "team-kradle:mistral31",
]

num_runs = 3
num_agents_per_run = 3

runs = []

for i in range(num_runs):
    # Randomly select agents for each run
    selected_agents = random.sample(agents, num_agents_per_run)
    print(f"Run {i+1}: Selected agents: {selected_agents}")
    
    runs.append(RunRequest(
        challenge_slug=challenge_slug,
        participants=[{"agent": agent} for agent in selected_agents]))

print("Starting experiment...")

# Create an experiment to evaluate agent performance
experiment = Experiment(
    use_studio=False
)

# Run the experiment 3 times and collect results
experiment_results = experiment.evaluate(runs, num_concurrent_runs=3)

# Display summary statistics of the experiment results
experiment_results.display_results()

# Display detailed information about each run (without showing logs)
experiment_results.display_runs(show_logs=False)

from datetime import datetime
# create the experiment_results directory if it doesn't exist
if not os.path.exists("experiment_results"):
    os.makedirs("experiment_results")

file_name = f"experiment_results/results_{datetime.now().strftime('%Y%m%d_%H%M')}.json"

# Save json with logs to a file
file_json = dict()
file_json = file_json | asdict(experiment_results)
with open(file_name, 'w') as f:
    f.write(json.dumps(file_json, indent=4, default=str))

print("Experiment results saved to", file_name)