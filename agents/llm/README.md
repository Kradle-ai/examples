# LLM Based Agent

A Minecraft agent that uses GPT-4 through OpenRouter API to make decisions and interact with the game environment.

## Setup

1. Create a `.env` file with your Kradle API key and OpenRouter API key:
```
KRADLE_API_KEY=your_key_here
KRADLE_AGENT_USERNAME=your_agent_username_in_kradle
OPENROUTER_API_KEY=your_key_here
MODEL=google/gemini-2.0-flash-001 # or any other model supported by OpenRouter
#CUSTOM_LLM_CHAT_API_URL_OVERRIDE="http://192.168.1.200:11434/api/chat" enable and only override if you want to use a local LLM eg from ollama
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app that will start the agent:
```bash
python app.py
```

The agent will start on port 1500 with a tunnel setup to access it from the internet. You can customize the agent's namespace by modifying the `username` constant in `agent.py`.

## Configuration

- `PERSONA`: Define the agent's personality
- `DELAY_AFTER_ACTION`: Adjust action delay in milliseconds
- `WAIT_FOR_LLM_RESPONSE_BEFORE_MAKING_ANOTHER_REQUEST`: If true, the agent will wait for the LLM response before making another request. Useful to prevent the agent from making too many requests when hitting a local ollama endpoint

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