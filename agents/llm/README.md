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

3. Run the script that will start the agent:
```bash
python simple_llm_agent.py
```

The agent will start on port 1500 with a tunnel setup to access it from the internet. You can customize the agent's namespace by modifying the `AGENT_NAME` constant in `simple_llm_agent.py`.

## Configuration

- `PERSONALITY_PROMPT`: Define the agent's personality
- `MODEL`: Select the LLM model (default: google/gemini-2.0-flash-001)
- `DELAY_AFTER_ACTION`: Adjust action delay in milliseconds - useful if you want more time to see what the agent is doing

You are encouraged to check out the prompts/config.py file to see the different prompts that are used to generate the agent's behavior.

## hot loading

To run your agent is hot loading mode (lets you make changes during session), run the following command:
```bash
jurigged -v simple_llm_agent.py
```