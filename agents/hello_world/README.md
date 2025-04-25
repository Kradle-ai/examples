# Hello World Agent

A minimal Minecraft agent that responds to private messages with "Hello World!" via the in-game Minecraft chat.

## Setup

1. Create a `.env` file with your Kradle API key:
```
KRADLE_API_KEY=your_key_here
```

2. Install dependencies:
```bash
python -mvenv venv
. venv/bin/activate
pip install -r requirements.txt
```

3. Run the agent:
```bash
python agent.py
```

The agent will start on port 1500 with a tunnel setup to access it from the internet. You can customize the agent's namespace by modifying the `username` constant in `agent.py`.