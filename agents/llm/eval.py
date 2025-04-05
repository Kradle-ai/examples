# this file is used to start an experiment on the kradle platform
# it is used to evaluate the performance of agents over several runs

from kradle import Experiment
from dotenv import load_dotenv
from kradle import AgentManager
from agent import LLMBasedAgent
from threading import Thread
from dataclasses import asdict
import time
import json

load_dotenv()

# Start the agent in a separate thread
def start_agent():
    print("Starting agent service...")
    print("Model: ", LLMBasedAgent.model)
    print("Persona: ", LLMBasedAgent.persona)
    app, connection_info = AgentManager.serve(LLMBasedAgent, create_public_url=True)

Thread(target=start_agent).start()
time.sleep(5) # TODO: implement better way to wait for agent to start
print("Starting experiment...")

# Create an experiment to evaluate agent performance
experiment = Experiment(
    challenge_slug="team-kradle:zombie-survival",
    #challenge_slug="team-kradle:capture-the-flag-tutorial-v2",
    
    # Define participating agents
    participants=[
        {"agent": LLMBasedAgent.username}
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
file_json["variables"]["model"] = LLMBasedAgent.model
file_json["variables"]["persona"] = LLMBasedAgent.persona
file_json = file_json | asdict(experiment_results)
with open(file_name, 'w') as f:
    f.write(json.dumps(file_json, indent=4, default=str))

print("Experiment results saved to", file_name)
