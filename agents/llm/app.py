from kradle import AgentManager
from llm_agent import LLMAgent

# Create and serve our agent
# This creates a web server and an SSH tunnel (so our agent has a stable public URL)
app, connection_info = AgentManager.serve(LLMAgent, create_public_url=True)

# now go to app.kradle.ai and run this agent against a challenge!
