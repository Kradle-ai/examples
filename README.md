# LLM Based Agent

A Minecraft agent that uses an LLM through OpenRouter API to make decisions and interact with the game environment.

## Setup

1. Create a `.env` file with your Kradle API key and OpenRouter API key:
```
KRADLE_API_KEY=your_key_here
```

2. Install dependencies:
```bash
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

3. Run the script that will start a hello world agent (the simplest agent you could build):

```bash
python hello_world_agent.py
```

The agent will start on port 1500 with a tunnel setup to access it from the internet. You can customize the agent's namespace by modifying the `AGENT_NAME` constant in `hello_world_agent.py`.

4. Run the script that will start an LLM agent

```bash
python simple_llm_agent.py
```

Similarly to hello world agent, the agent will start on port 1500 with a tunnel setup to access it from the internet. You can customize the agent's namespace by modifying the `AGENT_NAME` constant in `simple_llm_agent.py`.

## Configuration

- `PERSONALITY_PROMPT`: Define the agent's personality
- `MODEL`: Select the LLM model (default: google/gemini-2.0-flash-001)
- `STEP_BY_STEP`: Set to `True` if you want to follow the agent flow step by step

You are encouraged to check out the helpers/prompts.py file to see the different prompts that are used to generate the agent's behavior.

## hot loading

To run your agent is hot loading mode (lets you make changes during session), run the following command:
```bash
jurigged -v simple_llm_agent.py
```