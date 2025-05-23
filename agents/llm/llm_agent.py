import os
import requests

from base_llm_agent import BaseLLMAgent
from dotenv import load_dotenv
from kradle import (AgentManager, JSON_RESPONSE_FORMAT)

load_dotenv()

# Default configuration settings
DEFAULT_USERNAME = os.getenv("USERNAME") or "python-llm-agent" # this must be different for each agent class
DEFAULT_MODEL = os.getenv("MODEL") or "google/gemini-2.0-flash-001"  # refer to https://openrouter.ai/models for all available models
DEFAULT_PERSONALITY_PROMPT = "you are a cool resourceful agent. you really want to achieve the task that has been given to you."
DEFAULT_LLM_PROVIDER = os.getenv("LLM_PROVIDER") or "openrouter"

# Factory method to create LLMAgent classes with custom configuration
def create_llm_agent_class(agent_config=None):
    # Set default values for all configuration parameters
    agent_config = agent_config or {}
    agent_config["username"] = agent_config.get('username', DEFAULT_USERNAME)
    agent_config["model"] = agent_config.get('model', DEFAULT_MODEL)
    agent_config["personality_prompt"] = agent_config.get('personality_prompt', DEFAULT_PERSONALITY_PROMPT)
    agent_config["llm_provider"] = agent_config.get('llm_provider', DEFAULT_LLM_PROVIDER)

    # Extends the BaseLLMAgent class to add support for Ollama
    class CustomLLMAgent(BaseLLMAgent):
        # Use the config values as class attributes
        config = agent_config
        username = config.get('username')
        display_name = config.get('display_name', username + " (llm)")
        description = config.get('description', "LLM-based agent using model " + config.get('model'))

        def init_participant(self, challenge_info):
            # Call the parent class's init_participant method
            response = super().init_participant(challenge_info)

            self.memory.model = self.config.get('model')
            self.memory.personality_prompt = self.config.get('personality_prompt')

            # Set additional configuration
            self.memory.llm_provider = self.config.get('llm_provider')
            self.memory.delay_after_action = self.config.get('delay_after_action', self.memory.delay_after_action)
            self.memory.history_num_conversation_turns = self.config.get('history_num_conversation_turns', None)

            return response

        # Override the _make_llm_request method to add Ollama support
        def _make_llm_request(self, json_payload):
            # Skip if we're already waiting for an LLM response
            if self.memory.wait_for_llm:
                print("Already waiting for LLM response, skipping new request")
                return {"code": "", "message":  f"Ignoring event, I'm already busy thinking", "delay": self.memory.delay_after_action}

            self.memory.wait_for_llm = str(os.getenv("WAIT_FOR_LLM_RESPONSE_BEFORE_MAKING_ANOTHER_REQUEST")).lower() == "true"
            response = ""

            try:
                if self.memory.llm_provider == "ollama":
                    json_payload["format"] = JSON_RESPONSE_FORMAT["json_schema"]["schema"]
                    json_payload["stream"] = False
                    json_payload["keep_alive"] = -1  # prevent model from timing out of cache
                    response = requests.post(
                        os.getenv("OLLAMA_API_URL"),
                        json=json_payload,
                        timeout=30,
                    ).json()
                else:
                    # Use the parent class implementation for OpenRouter
                    response = super()._make_llm_request(json_payload)
            finally:
                self.memory.wait_for_llm = False

            return response

        # Override the _extract_content_from_response method to handle Ollama responses
        def _extract_content_from_response(self, response):
            if self.memory.llm_provider == "ollama":
                if "message" in response:
                    return response["message"]["content"]
                print(f"Cannot parse response from Ollama: {response}")
                return ""
            else:
                # Use the parent class implementation for OpenRouter
                return super()._extract_content_from_response(response)

        def _build_history_prompt(self):
            if self.memory.history_num_conversation_turns is not None:
                return self.memory.llm_transcript[-self.memory.history_num_conversation_turns:]
            else:
                return super()._build_history_prompt()

        def __print_prompt(self, prompt):
            print("---PROMPT---")
            for p in prompt:
                print("--------------------------------")
                print("---" + p["role"] + "---")
                print(p["content"])
            print("---END PROMPT---")

    return CustomLLMAgent

# Create the default LLMAgent class for backward compatibility
if __name__ == "__main__":
    LLMAgent = create_llm_agent_class()
    # Create a web server and an SSH tunnel
    app, connection_info = AgentManager.serve(LLMAgent, create_public_url=True)
    print(f"Started agent, now reachable at URL: {connection_info}", flush=True)
