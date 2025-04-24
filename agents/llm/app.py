from kradle import AgentManager
from llm_agent import create_llm_agent_class

import os

def app(debug=False):
    try:
        # gemini_class = create_llm_agent_class({ "username": "gemini", "model": "google/gemini-2.0-flash-001" })
        # gpt4o_class = create_llm_agent_class({ "username": "gpt4o", "model": "openai/gpt-4o-mini" })
        qwen25_class = create_llm_agent_class({ "username": "qwen25", "model": "qwen/qwen-2.5-coder-32b-instruct" })

        # Create and serve our agent
        # This creates a web server and an SSH tunnel (so our agent has a stable public URL)
        # AgentManager.serve(gemini_class, create_public_url=True)
        # AgentManager.serve(gpt4o_class, create_public_url=True)
        app, url = AgentManager.serve(qwen25_class, create_public_url=True, debug=debug)
    except KeyboardInterrupt:
        os._exit(0)

    # now go to app.kradle.ai and run this agent against a challenge!
    print(f"Started agent, now reachable at URL: {url}\n", flush=True)

if __name__ == "__main__":
    app()