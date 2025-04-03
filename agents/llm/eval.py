# this file is used to start an experiment on the kradle platform
# it is used to evaluate the performance of agents over several runs

from kradle import Experiment
from dotenv import load_dotenv
load_dotenv()

# Create an experiment to evaluate agent performance
experiment = Experiment(
    #challenge_slug="team-kradle:zombie-survival-v2",
    challenge_slug="team-kradle:capture-the-flag-tutorial-v2",
    
    # Define participating agents
    participants=[
        {"agent": "python1"}
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