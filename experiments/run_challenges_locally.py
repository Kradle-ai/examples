#!/usr/bin/env python3
"""
Example script for Kradle Studio experiment integration.

This script demonstrates how to run experiments through Kradle Studio.
"""

import time
import sys
import os
from dotenv import load_dotenv
from kradle import Experiment, AgentManager
from kradle.logger import KradleLogger

# Load .env file if it exists
load_dotenv()

# Set up logging
logger = KradleLogger()
logger.log_info("Starting Studio experiment example")

# Configuration (edit these values)
CHALLENGE_SLUG = "team-kradle:zombie-survival"  # Update with an existing challenge
AGENT_USERNAME = "james-new-agent"  # Update with your agent username
NUM_RUNS = 1  # Start with 1 for testing

# Check for API key
API_KEY = os.environ.get("KRADLE_API_KEY")
if not API_KEY:
    print("WARNING: No KRADLE_API_KEY found in environment or .env file")
    print("Create a .env file with your API key or set it as an environment variable")
    print("Example: KRADLE_API_KEY=your_api_key_here")
    sys.exit(1)

# Set API key programmatically
AgentManager.set_api_key(API_KEY)
logger.log_info(f"Using API key: {API_KEY[:4]}...{API_KEY[-4:]}")


def run_experiment(use_studio=True):
    """Run an experiment with the specified configuration."""
    logger.log_info(f"Creating experiment with use_studio={use_studio}")

    # Create the experiment
    experiment = Experiment(
        challenge_slug=CHALLENGE_SLUG,
        participants=[{"agent": AGENT_USERNAME}],
        use_studio=use_studio,  # Set to False to use cloud API instead
        fetch_run_logs=True,  # Set to False for faster execution if needed
    )

    # Start timing
    start_time = time.time()
    logger.log_info(f"Starting experiment execution with {NUM_RUNS} runs")

    try:
        # Run the experiment
        results = experiment.evaluate(num_runs=NUM_RUNS)

        # Calculate duration
        duration = time.time() - start_time
        logger.log_info(f"Experiment completed in {duration:.2f} seconds")

        # Display results
        print("\n===== EXPERIMENT RESULTS =====")
        results.display_results()

        # Display run details
        print("\n===== RUN DETAILS =====")
        results.display_runs(show_logs=False)

        return True
    except Exception as e:
        logger.log_error(f"Experiment failed: {str(e)}")
        print(f"\nERROR: {str(e)}")
        
        # Print the error cause if available for more detail
        if hasattr(e, '__cause__') and e.__cause__ is not None:
            print(f"Caused by: {e.__cause__}")
            
        return False


def main():
    """Run example based on command line arguments."""
    # Parse command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--cloud":
        use_studio = False
        print("Running with cloud API (use_studio=False)")
    else:
        use_studio = True
        print("Running with Studio API (use_studio=True)")

    print(f"Challenge: {CHALLENGE_SLUG}")
    print(f"Agent: {AGENT_USERNAME}")
    print(f"Runs: {NUM_RUNS}")
    print("\nStarting experiment...\n")

    success = run_experiment(use_studio)

    if success:
        print("\nExperiment completed successfully!")
        return 0
    else:
        print("\nExperiment failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
