# this file is used to start an experiment on the kradle platform
# it is used to evaluate the performance of agents over several runs

from kradle import Experiment
from kradle.models import RunRequest
from dotenv import load_dotenv
from kradle import AgentManager
from llm_agent import create_llm_agent_class
from dataclasses import asdict
import json

load_dotenv()

# Create an LLM agent with custom settings
gemini_class = create_llm_agent_class({ "username": "gemini", "model": "google/gemini-2.0-flash-001" })
gpt4o_class = create_llm_agent_class({ "username": "gpt4o", "model": "openai/gpt-4o-mini" })
qwen25_class = create_llm_agent_class({ "username": "qwen25", "model": "qwen/qwen-2.5-coder-32b-instruct" })

builder_persona = "You are a master builder. You create walls of cobblestone around you to take refuge inside. You are efficient, and don't build the floor or ceiling, but the walls must be at least 3 blocks high to protect you. When the zombies arrive, you stay inside quietly and don't perform any actions, so they won't find you. "
escapist_persona = "You are an evasive survival expert. You believe that building is too much work, running is for winners. You prepare by going to a safe position very far off in the distance. When the zombies start appearing, you go into the cowardice mode and move away quickly to avoid danger. "
fighter_persona = "You are a fighter. You don't concern yourself with building or running, you stay put and get into a defensive stance before the zombies arrive. To prepare, you equip your weapon and move around to get a better position. You can't wait to attack the zombies and tear them to pieces! "

personas = [
    {
        "persona": builder_persona,
        "shortname": "build"
    },
    {
        "persona": escapist_persona,
        "shortname": "escape"
    },
    {
        "persona": fighter_persona,
        "shortname": "fight"
    }
]

models = [{
    "shortname": "gem2f",
    "model_id": "google/gemini-2.0-flash-001"
}, {
    "shortname": "gpt4o",
    "model_id": "openai/gpt-4o-mini"
}, {
    "shortname": "qwn25c",
    "model_id": "qwen/qwen-2.5-coder-32b-instruct"
}]

agent_classes = []
for model in models:
    for persona in personas:
        agent_class = create_llm_agent_class({
            "username": f"{model['shortname']}-{persona['shortname']}",
            "model": model["model_id"],
            "persona": persona["persona"]
        })
        agent_classes.append(agent_class)

for agent_class in agent_classes:
    AgentManager.serve(agent_class, create_public_url=True)

runs = []
for agent_class in agent_classes:
    new_run = RunRequest(
        challenge_slug="team-kradle:zombie-survival",
        participants=[
            {"agent": agent_class.config.get('username')}
        ]
    )
    for i in range(3): # run the same agent class 3 times
        runs.append(new_run)

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
file_name = f"experiment_results_{datetime.now().strftime('%Y%m%d_%H%M')}.json"

# Save json with logs to a file
file_json = dict()
file_json = file_json | asdict(experiment_results)
with open(file_name, 'w') as f:
    f.write(json.dumps(file_json, indent=4, default=str))

print("Experiment results saved to", file_name)