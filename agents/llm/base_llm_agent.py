# This base class uses the OpenRouter API to select, prompt, and get the response from the LLM of choice
from kradle import (AgentManager, MinecraftAgent, JSON_RESPONSE_FORMAT)
from kradle.models import MinecraftEvent, InitParticipantResponse
from classproperty import classproperty
from dotenv import load_dotenv
import requests
import json
import os

# Use a module import to load the prompts rather than creating unqualified names
# here to allow hot reloading of the prompts.
from prompts import config

load_dotenv()

# Let's define a model and persona for our agent
MODEL = "google/gemini-2.0-flash-001" # refer to https://openrouter.ai/models for all available models
PERSONA = "you are a cool resourceful agent. you really want to achieve the task that has been given to you." # check out some other personas in prompts/config.py

# Username of the agent in kradle (eg. kradle.ai/<my-username>/agents/<my-agent-username>). Will be created if it doesn't exist.
USERNAME = "python1"

# Plus some additional settings:
DELAY_AFTER_ACTION = 100  # This adds a delay (in milliseconds) after an action is performed. Increase this if the agent is too fast or if you want more time to see the agent's actions
MAX_RETRIES = 3 # Number of times the LLM will retry to generate a valid response

# This is your agent class. It extends the MinecraftAgent class in the Kradle SDK
# You pass this whole class into the AgentManager.serve() below
# This lets Kradle manage the lifecycle of this agent
# Kradle can create multiple instances of your agent (eg. adding two of the same agent to a challenge)
# Each instance of this class is called a 'participant'
class BaseLLMAgent(MinecraftAgent):
    # These class properties describe the agent's configuration to the Kradle
    # agent manager. They're implemented as functions here to allow hot
    # reloading of the values above.

    @classproperty
    def persona(cls):
        return PERSONA

    @classproperty
    def model(cls):
        return MODEL

    @classproperty
    def username(cls):
        return USERNAME

    @classproperty
    def display_name(cls):
        return cls.username + " (llm)"  # display name of the agent

    @classproperty
    def description(cls):
        return "This is an LLM-based agent that can be used to perform tasks in Minecraft."

    # This method is called when the session starts
    # Return a list of in-game events you wish to listen to
    # These will trigger the on_event() function when they occur
    def init_participant(self, challenge_info):
        print(f"Received init_participant call for {self.participant_id} with run_id: {challenge_info.run_id}")

        # Initialize memory with challenge information
        # self.memory is a utility instantiated for you by the Kradle SDK to store and retrieve information
        # It persists across the lifecycle of this participant
        self.memory.task = challenge_info.task
        self.memory.llm_transcript = []  # store LLM interaction history
        self.memory.game_chat_history = []  # store in-game chat history
        self.memory.agent_modes = challenge_info.agent_modes  # Minecraft modes (creative, self_preservation, etc)
        self.memory.js_functions = challenge_info.js_functions  # available JavaScript functions
        self.memory.delay_after_action = DELAY_AFTER_ACTION

        # Look for OpenRouter API key in environment variables, falling back to Kradle API if not found
        self.memory.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        if self.memory.openrouter_api_key is None or len(self.memory.openrouter_api_key) < 20:
            human = self._internal_api_client.humans.get()
            self.memory.openrouter_api_key = human["openRouterKey"]

        # Log initialization info to console
        print(f"Initializing agent for participant ID: {self.participant_id} with username: {self.username}")
        print(f"Task: {self.memory.task}")

        # Tell Kradle what events we want to listen to
        return InitParticipantResponse({"listenTo": [MinecraftEvent.CHAT, MinecraftEvent.COMMAND_EXECUTED, MinecraftEvent.MESSAGE, MinecraftEvent.IDLE]})

    # Called when an event happens, we process the observation and return an action
    # See https://app.kradle.ai/docs/how-kradle-works for details on observations and actions
    def on_event(self, observation):
        # Extend/append to the in-game chat history
        self.memory.game_chat_history.extend(observation.chat_messages)

        # Format the observation for the LLM
        observation_summary = self._format_observation(observation)

        print(f"\033[91m########################################################")
        print(f"\nObservation Summary:\n{observation_summary}")
        print(f"\033[91m########################################################\033[0m")

        # Generate and return the agent's response
        response = self.__generate_llm_agent_action(observation_summary, observation)
        print(f"Participant '{self.participant_id}' Agent Response: {response}")

        return response

    # Convert observation object to a string for the LLM prompt
    def _format_observation(self, observation):
        print(f"Minecraft Chat History: {self.memory.game_chat_history}")

        # Let's get everything in our inventory
        inventory_summary = (
            ", ".join([f"{count} {name}" for name, count in observation.inventory.items()])
            if observation.inventory
            else "None"
        )

        # Return string with everything the LLM needs to know about the state of the game
        formatted_output = (
            f"Event received: {observation.event if observation.event else 'None'}\n\n"
            f"Command Output:\n{observation.output if observation.output else 'Output: None'}\n\n"
            f"Position: {observation.position}\n\n"
        )

        if observation.chat_messages:
            formatted_output += f"Latest Chat: {observation.chat_messages}\n\n"

        formatted_output += (
            f"Visible Players: {', '.join(observation.players) if observation.players else 'None'}\n\n"
            f"Visible Blocks: {', '.join(observation.blocks) if observation.blocks else 'None'}\n\n"
            f"Visible Entities: {', '.join(observation.entities) if observation.entities else 'None'}\n\n"
            f"Inventory: {inventory_summary}\n\n"
            f"Health: {observation.health * 100}/100"
        )

        return formatted_output

    # Builds the system prompt for the agent
    def _build_system_prompt(self, observation):
        system_prompt = []

        # Build coding prompt from template, including task, agent_modes, and creative_mode
        prompt = config.coding_prompt
        prompt = prompt.replace("$NAME", observation.name)
        prompt = prompt.replace("$TASK", self.memory.task)
        prompt = prompt.replace("$AGENT_MODE", str(self.memory.agent_modes))

        if self.memory.agent_modes["mcmode"] == "creative":
            prompt = prompt.replace("$CREATIVE_MODE", config.creative_mode_prompt)
        else:
            prompt = prompt.replace("$CREATIVE_MODE", "You are in survival mode.")

        system_prompt.append({"role": "system", "content": prompt})

        # Skills prompt with code documentation to give the agent context about the available commands
        prompt = config.skills_prompt
        prompt = prompt.replace("$CODE_DOCS", str(self.memory.js_functions))
        system_prompt.append({"role": "system", "content": prompt})

        # Minecraft modes (creative, self_preservation, etc) available in the challenge
        prompt = config.agent_prompt
        prompt = prompt.replace("$AGENT_MODE", str(self.memory.agent_modes))
        system_prompt.append({"role": "system", "content": prompt})

        # Examples prompt
        prompt = config.examples_prompt
        prompt = prompt.replace("$EXAMPLES", str(config.coding_examples))
        system_prompt.append({"role": "system", "content": prompt})

        # Persona prompt
        prompt = config.persona_prompt
        prompt = prompt.replace("$PERSONA", type(self).persona)
        system_prompt.append({"role": "system", "content": prompt})

        return system_prompt

    # Build prompt from conversation transcript so agent has historical context on past interactions
    def _build_history_prompt(self):
        return self.memory.llm_transcript[-5:] # last 5 messages from the conversation history

    # Generate a complete agent response by querying the LLM and processing the result
    def __generate_llm_agent_action(self, observation_summary, observation, max_retries=MAX_RETRIES):
        if max_retries < MAX_RETRIES:
            print(f"\033[91m########################################################")
            print(f"\033[91mRetrying LLM response for the {MAX_RETRIES - max_retries} time\033[0m")
            print(f"\033[91m########################################################\033[0m")

        # Build the complete prompt with system instructions, historical context, and user input
        llm_prompt = [
            *self._build_system_prompt(observation),
            *self._build_history_prompt(),
            {"role": "user", "content": observation_summary},
        ]
        print(f"LLM Prompt: {llm_prompt}")

        json_payload = {
            "model": type(self).model,
            "messages": llm_prompt,
            "require_parameters": True,
        }

        # Make LLM request
        response = self._make_llm_request(json_payload)

        # Process the response
        content, action, success, error_message = self._process_llm_response(response)

        # Log interaction to Kradle dashboard
        self.log({"prompt": self._truncate_prompt(llm_prompt), "model": type(self).model, "response": content})

        # Update conversation history for future LLM context
        self.memory.llm_transcript.extend([
            {"role": "user", "content": observation_summary},
            {"role": "assistant", "content": content}
        ])

        # Return action if successful
        if success:
            return {
                "code": action["code"],
                "message": action["message"],
                "delay": self.memory.delay_after_action
            }
        else:
            if max_retries <= 0:
                return {"code": "", "message": "I'm sorry, I'm having trouble generating a response. Please try again later.", "delay": self.memory.delay_after_action}

            # We didn't succeed, so add the error message to the transcript and retry
            self.memory.llm_transcript.append({
                "role": "system",
                "content": f"your last response was not valid because: {error_message}"
            })

            return self.__generate_llm_agent_action(observation_summary, observation, max_retries - 1)

    # Make a request to the LLM API, defaults to OpenRouter (override for other LLM providers)
    def _make_llm_request(self, json_payload):
        json_payload["response_format"] = JSON_RESPONSE_FORMAT
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {self.memory.openrouter_api_key}"},
            json=json_payload,
            timeout=30,
        ).json()
        return response

    # Extract content from the LLM response, defaults to OpenRouter structured output
    def _extract_content_from_response(self, response):
        if "choices" in response and response["choices"]:
            return response["choices"][0]["message"]["content"]

        print(f"Cannot parse response from LLM: {response}")
        return ""

    # Process the LLM response to extract the action
    def _process_llm_response(self, response):
        success = False
        content = ""
        action = {"code": "", "message": ""}
        error_message = ""

        try:
            content = self._extract_content_from_response(response)
            if not content:
                print(f"Error: Empty content from LLM response. Full response: {response}")
                error_message = "Unable to extract content from LLM response"
                return content, action, success, error_message

            # Find the JSON part in the content
            start = content.find("{")
            end = content.rfind("}") + 1
            content_to_parse = content[start:end]
            if content_to_parse == "":
                print(f"Error: Could not parse JSON in response. Received: {content}")
                error_message = "Unable to parse JSON from LLM response"
                return content, action, success, error_message

            # Parse the content string as JSON and extract the code and message
            try:
                json_content = json.loads(content_to_parse)
                action = {
                    "code": json_content.get("code", ""),
                    "message": json_content.get("message", "")
                }
                success = True # Success! Let's return the action
                return content, action, success, error_message

            except Exception as e:
                print(f"Unable to parse JSON from LLM response for content: {content_to_parse} with error: {e}")
                error_message = "Unable to parse JSON from LLM response"
                return content, action, success, error_message

        except Exception as e:
            print(f"Unexpected error processing LLM response: {e}")
            error_message = f"Error processing LLM response: {str(e)}"
            return content, action, success, error_message

    # Utility function to truncate the prompt to 2000 characters for more readable logs
    def _truncate_prompt(self, prompt):
        truncated_prompt = []
        for p in prompt:
            truncated_p = p.copy()  # Create a shallow copy of the dict
            if len(truncated_p["content"]) > 2000:
                truncated_p["content"] = truncated_p["content"][:2000] + "..."
            truncated_prompt.append(truncated_p)
        return truncated_prompt

# Finally, lets serve our agent!
if __name__ == "__main__":
    # Create a web server and SSH tunnel for a stable public URL
    app, connection_info = AgentManager.serve(BaseLLMAgent, create_public_url=True)
    print(f"Started agent, now reachable at URL: {connection_info}", flush=True)

# Now go to app.kradle.ai and run this agent against a challenge!
