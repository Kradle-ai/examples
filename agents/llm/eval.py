# this file is used to start an experiment on the kradle platform
# it is used to evaluate the performance of agents over several runs

from kradle import Experiment
from dotenv import load_dotenv
from kradle import AgentManager
from llm_agent import create_llm_agent_class
from base_llm_agent import BaseLLMAgent
from threading import Thread
from dataclasses import asdict
import time
import json

load_dotenv()

# Create an LLM agent with custom settings
AGENT_CLASS = create_llm_agent_class({ "model":"qwen2.5-coder:7b"})

# Start the agent in a separate thread
def start_agent(agent_class):
    print("Starting agent service...")
    print("Model: ", agent_class.config.get('model'))
    print("Persona: ", agent_class.config.get('persona'))
    app, connection_info = AgentManager.serve(agent_class, create_public_url=True)

Thread(target=start_agent, args=(AGENT_CLASS,)).start()
time.sleep(5) # TODO: implement better way to wait for agent to start
print("Starting experiment...")

# Create an experiment to evaluate agent performance
experiment = Experiment(
    challenge_slug="team-kradle:zombie-survival",
    #challenge_slug="team-kradle:capture-the-flag-tutorial-v2",
    
    # Define participating agents
    participants=[
        {"agent": AGENT_CLASS.config.get('username')}
        #{"agent": "python1", "role": "builder"},  
        #{"agent": "survivor1", "role": "defender"},
        #{"agent": "survivor1", "role": "builder"},
    ]
)

# Run the experiment 3 times and collect results
experiment_results = experiment.evaluate(num_runs=3)

# Display summary statistics of the experiment results
experiment_results.display_results()

# Display detailed information about each run (without showing logs)
experiment_results.display_runs(show_logs=False)

from datetime import datetime
file_name = f"experiment_results_{datetime.now().strftime('%Y%m%d_%H%M')}.json"

# Save json with logs to a file
file_json = dict()
file_json["variables"] = dict()
file_json["variables"]["model"] = AGENT_CLASS.config.get('model')
file_json["variables"]["persona"] = AGENT_CLASS.config.get('persona')
file_json = file_json | asdict(experiment_results)
with open(file_name, 'w') as f:
    f.write(json.dumps(file_json, indent=4, default=str))

print("Experiment results saved to", file_name)
