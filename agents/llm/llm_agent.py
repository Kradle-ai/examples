import os
import requests

from base_llm_agent import BaseLLMAgent
from dotenv import load_dotenv
from kradle import (
    AgentManager,
    JSON_RESPONSE_FORMAT
)

load_dotenv()

# Configuration settings
MODEL = "llama3.2"  # refer to https://openrouter.ai/models for all available models
PERSONA = "you are a cool resourceful agent. you really want to achieve the task that has been given to you."
USERNAME = "python1"
DELAY_AFTER_ACTION = 100  # milliseconds delay after an action
LLM_PROVIDER = os.getenv("LLM_PROVIDER") or "openrouter"
WAIT_FOR_LLM_RESPONSE_BEFORE_MAKING_ANOTHER_REQUEST = os.getenv("WAIT_FOR_LLM_RESPONSE_BEFORE_MAKING_ANOTHER_REQUEST") or False

class LLMAgent(BaseLLMAgent):
    persona = PERSONA
    model = MODEL
    username = USERNAME
    display_name = username + " (llm)"
    description = "This is an LLM-based agent that can be used to perform tasks in Minecraft."

    def init_participant(self, challenge_info):
        # Call the parent class's init_participant method
        response = super().init_participant(challenge_info)

        self.memory.model = MODEL
        self.memory.persona = PERSONA
        
        # Set additional configuration
        self.memory.delay_after_action = DELAY_AFTER_ACTION
        self.memory.llm_provider = LLM_PROVIDER
        self.memory.wait_for_llm = False
            
        # Log additional configuration
        print(f"Delay after action: {self.memory.delay_after_action}")
        self.log({"delay_after_action": self.memory.delay_after_action})
        
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

    def __print_prompt(self, prompt):
        print("---PROMPT---")
        for p in prompt:
            print("--------------------------------")
            print("---" + p["role"] + "---")
            print(p["content"])
        print("---END PROMPT---")

if __name__ == "__main__":
    from kradle import AgentManager
    
    # Create a web server and an SSH tunnel
    app, connection_info = AgentManager.serve(LLMAgent, create_public_url=True)
    print(f"Started agent, now reachable at URL: {connection_info}", flush=True) 