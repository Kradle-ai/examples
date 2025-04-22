# LLM Based Agent

A Minecraft agent that uses GPT-4 through OpenRouter API to make decisions and interact with the game environment.

## Setup

1. Create a `.env` file with your Kradle API key and OpenRouter API key:
```
KRADLE_API_KEY=your_key_here
OPENROUTER_API_KEY=your_key_here
```

2. Install dependencies:
```bash
python -mvenv venv
. venv/bin/activate
pip install -r requirements.txt
```

3. Run the app that will start the agent:
```bash
python app.py
```

The agent will start on port 1500 with a tunnel setup to access it from the internet. You can customize the agent's namespace by modifying the `username` constant in `agent.py`.

## Configuration

- `PERSONA`: Define the agent's personality
- `MODEL`: Select the LLM model (default: google/gemini-2.0-flash-001)
- `DELAY_AFTER_ACTION`: Adjust action delay in milliseconds

You are encouraged to check out the prompts/config.py file to see the different prompts that are used to generate the agent's behavior.

## Smoke testing

To smoke test the agent, run the following command:
```bash
python test_smoke.py
```

It will use a sample init and observation to test the agent's connectivity and basic response with code.  

## Evaluation

The SDK has an `Experiment` class that can be used to evaluate agents' performance over several runs on a given challenge. 

To run an experiment, run the following command:
```bash
python eval.py
```

(you will need to change the challenge agent usernames in that file to the ones you want to use)