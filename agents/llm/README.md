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
pip install -r requirements.txt
```

3. Run the agent:
```bash
python agent.py
```

The agent will start on port 1500 with a tunnel setup to access it from the internet. You can customize the agent's namespace by modifying the `username` constant in `agent.py`.

## Configuration

- `PERSONA`: Define the agent's personality
- `MODEL`: Select the LLM model (default: google/gemini-2.0-flash-001)
- `DELAY_AFTER_ACTION`: Adjust action delay in milliseconds