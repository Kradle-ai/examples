from kradle import AgentManager
from llm_agent import create_llm_agent_class

qwen25class = create_llm_agent_class({ "username": "qwen25", "model": "qwen/qwen-2.5-coder-32b-instruct" })
#geminiclass = create_llm_agent_class({ "username": "gemini", "model": "google/gemini-2.0-flash-001" })
#gpt4oclass = create_llm_agent_class({ "username": "gpt4o", "model": "openai/gpt-4o-mini" })

# Create and serve our agent
# This creates a web server and an SSH tunnel (so our agent has a stable public URL)
app, connection_info = AgentManager.serve(qwen25class, create_public_url=True)
#app, connection_info = AgentManager.serve(geminiclass, create_public_url=True)
#app, connection_info = AgentManager.serve(gpt4oclass, create_public_url=True)

# now go to app.kradle.ai and run this agent against a challenge!