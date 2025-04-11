# this agent uses an LLM to decide what to do.
# it uses the OpenRouter API to select, prompt, and get the response from any number of LLMs

from kradle import (
    AgentManager,
    MinecraftAgent,
    JSON_RESPONSE_FORMAT,
)
from kradle.models import MinecraftEvent, InitParticipantResponse
from dotenv import load_dotenv
import os
import requests
import json

from prompts.config import (
    coding_prompt,
    coding_examples,
    creative_mode_prompt,
    skills_prompt,
    examples_prompt,
    persona_prompt,
    agent_prompt,
)

load_dotenv()

#the max number of times the LLM will retry to generate a valid response
MAX_RETRIES = 3

# let's define a model and persona for our agent
MODEL = "google/gemini-2.0-flash-001" # refer to https://openrouter.ai/models for all available models
PERSONA = "you are a cool resourceful agent. you really want to achieve the task that has been given to you."  # check out some other personas in prompts/config.py

# this is the username of the agent (eg. kradle.ai/<my-username>/agents/<my-agent-username>). if it does not exist, it will be created.
USERNAME = "python1"

# plus some additional settings:
DELAY_AFTER_ACTION = 100  # this adds a delay (in milliseconds) after an action is performed. increase this if the agent is too fast or if you want more time to see the agent's actions

# optional: your openrouter API key. If not provided, will obtain a key with a small amount of trial credit from the Kradle API
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# optional: defaults to openrouter, can be set to ollama
LLM_PROVIDER = os.getenv("LLM_PROVIDER") or "openrouter" 

# this is your agent class. It extends the MinecraftAgent class in the Kradle SDK
# you pass this whole class into the AgentManager.serve() below
# this lets Kradle manage the lifecycle of this agent.
# Kradle can create multiple instances of your agent (eg. adding two of the same agent to a challenge)
# each instance of this class is called a 'participant'
class LLMBasedAgent(MinecraftAgent):
    persona = PERSONA
    model = MODEL

    username = USERNAME  # this is the username of the agent (eg. kradle.ai/<my-username>/agents/<my-agent-username>)
    display_name = username + " (llm)"  # this is the display name of the agent
    description = "This is an LLM-based agent that can be used to perform tasks in Minecraft."

    # this method is called when the session starts
    # challenge_info has variables, like challenge_info.task
    # use the return statement of this method to send a list of in-game events you wish to listen to.
    # these will trigger the on_event() function when they occur
    def init_participant(self, challenge_info):

        # self.memory is a utility instantiated for you
        # that can be used to store and retrieve information
        # it persists across the lifecycle of this participant.
        # It is an instance of the StandardMemory class in the Kradle SDK

        print(f"Received init_participant call for {self.participant_id} with run_id: {challenge_info.run_id}")

        # save the task to memory
        self.memory.task = challenge_info.task

        # array to store LLM interaction history
        self.memory.llm_transcript = []

        # array to store in-game chat history
        self.memory.game_chat_history = []

        # set Minecraft modes (e.g. creative mode, self_preservation, etc)
        # TODO: Link to docs to explain more.
        self.memory.agent_modes = challenge_info.agent_modes

        # dictionaries to store all possible javascript functions
        self.memory.js_functions = challenge_info.js_functions

        # storing in memory if you're using a Redis Memory, and want to make your agent resilient to restarts
        self.memory.persona = LLMBasedAgent.persona
        self.memory.model = LLMBasedAgent.model
        self.memory.llm_provider = LLM_PROVIDER # optional: set LLM_PROVIDER to ollama if you want to use ollama instead of openrouter
        self.memory.delay_after_action = DELAY_AFTER_ACTION

        # try to find the openrouter api key in the environment variables
        if OPENROUTER_API_KEY is not None and len(OPENROUTER_API_KEY) > 20:
            self.memory.openrouter_api_key = OPENROUTER_API_KEY
        else:
            # get the openrouter api key from the kradle API
            human = self._internal_api_client.humans.get()
            self.memory.openrouter_api_key = human["openRouterKey"]

        print(f"Initializing agent for participant ID: {self.participant_id} with username: {self.username}")
        print(f"Persona: {self.memory.persona}")
        print(f"Model: {self.memory.model}")
        print(f"Task: {self.memory.task}")
        print(f"Delay after action: {self.memory.delay_after_action}")
        print(f"Agent modes: {self.memory.agent_modes}")

        # self.log() lets us log information to the Kradle dashboard (left pane in the session viewer)
        self.log(
            {
                "persona": self.memory.persona,
                "model": self.memory.model,
                "delay_after_action": self.memory.delay_after_action,
            }
        )

        return InitParticipantResponse({"listenTo": [MinecraftEvent.CHAT, MinecraftEvent.COMMAND_EXECUTED, MinecraftEvent.MESSAGE, MinecraftEvent.IDLE, MinecraftEvent.HEALTH]})

    # this is called when an event happens
    # we return our next action
    def on_event(self, observation):
        # Skip if we're already waiting for an LLM response
        if self.memory.wait_for_llm:
            print("Already waiting for LLM response, skipping new request")
            return {"code": "", "message":  f"Ignoring event {observation.event}, I'm busy thinking", "delay": self.memory.delay_after_action}

        # Process the observation and get LLM response
        try:
            if self.memory.llm_provider == "ollama":
                self.memory.wait_for_llm = True # When using ollama, we should wait for the LLM response before making another request
            
            # extend/append to the in-game chat history
            self.memory.game_chat_history.extend(observation.chat_messages)

            observation_summary = self.__format_observation(observation)
            
            print("================================================")
            print(f"\nObservation Summary:\n{observation_summary}")
            # print("Task: ", self.memory.task)

            print("================================================")
            response = self.__get_llm_response(observation_summary, observation)
            print(f"Agent Response: {response}")
            # print(f"Participant ID: {self.participant_id}")

            # if the response is empty, return an empty response
            if response["code"] == "":
                response["code"] = "await console.log('I am thinking about code...');"

            return response
        finally:
            self.memory.wait_for_llm = False

    # convert observation from object => string, so we can build a LLM prompt
    def __format_observation(self, observation):

        # python array operation to extend/append to the in-game chat history
        self.memory.game_chat_history.extend(observation.chat_messages)

        print(f"Minecraft Chat History: {self.memory.game_chat_history}")

        # lets get everythign in our inventory
        inventory_summary = (
            ", ".join([f"{count} {name}" for name, count in observation.inventory.items()])
            if observation.inventory
            else "None"
        )

        # return a string with everything the LLM needs to know
        return (
            f"Event received: {observation.event if observation.event else 'None'}\n\n"
            f"{observation.output if observation.output else 'Output: None'}\n\n"
            f"Position: {observation.position}\n\n"
            f"Latest Chat: {observation.chat_messages}\n\n" if observation.chat_messages else ""
            f"Visible Players: {', '.join(observation.players) if observation.players else 'None'}\n\n"
            f"Visible Blocks: {', '.join(observation.blocks) if observation.blocks else 'None'}\n\n"
            f"Visible Entities: {', '.join(observation.entities) if observation.entities else 'None'}\n\n"
            f"Inventory: {inventory_summary}\n\n"
            f"Health: {observation.health * 100}/100"
        )

    # this function builds the system prompt for the agent
    def __build_system_prompt(self, observation):

        system_prompt = []
        # build the system prompt for the agent
        prompt = coding_prompt
        
        # load task, persona, agent_modes, and commands from memory to build the prompt
        prompt = prompt.replace("$NAME", observation.name)
        prompt = prompt.replace("$TASK", self.memory.task)
        prompt = prompt.replace("$AGENT_MODE", str(self.memory.agent_modes))
        
        if self.memory.agent_modes["mcmode"] == "creative":
            prompt = prompt.replace("$CREATIVE_MODE", creative_mode_prompt)
        else:
            prompt = prompt.replace("$CREATIVE_MODE", "You are in survival mode.")

        system_prompt.append({"role": "system", "content": prompt})

        prompt = skills_prompt
        prompt = prompt.replace("$CODE_DOCS", str(self.memory.js_functions))
        system_prompt.append({"role": "system", "content": prompt})

        prompt = agent_prompt
        prompt = prompt.replace("$AGENT_MODE", str(self.memory.agent_modes))
        system_prompt.append({"role": "system", "content": prompt})

        prompt = examples_prompt
        prompt = prompt.replace("$EXAMPLES", str(coding_examples))
        system_prompt.append({"role": "system", "content": prompt})

        prompt = persona_prompt
        prompt = prompt.replace("$PERSONA", self.memory.persona)
        system_prompt.append({"role": "system", "content": prompt})

        return system_prompt

    # utility function to truncate the prompt to 2000 characters for more readable logs
    def __truncate_prompt(self, prompt):
        truncated_prompt = []
        for p in prompt:
            truncated_p = p.copy()  # Create a shallow copy of the dict
            if len(truncated_p["content"]) > 2000:
                truncated_p["content"] = truncated_p["content"][:2000] + "..."
            truncated_prompt.append(truncated_p)
        return truncated_prompt

    def __print_prompt(self, prompt):
        print("---PROMPT---")
        for p in prompt:
            print("--------------------------------")
            print("---" + p["role"] + "---")
            print(p["content"])
        print("---END PROMPT---")

    # send the prompt to the LLM and get the response
    def __get_llm_response(self, observation_summary, observation, max_retries=MAX_RETRIES):

        if max_retries < MAX_RETRIES:
            print(f"\033[91m########################################################")
            print(f"\033[91m########################################################")
            print(f"\033[91mRetrying LLM response for the {MAX_RETRIES - max_retries} time\033[0m")
            print(f"\033[91m########################################################")
            print(f"\033[91m########################################################")

        # prompt = system prompt + last 5 LLM interactions + last observation
        llm_prompt = [
            *self.__build_system_prompt(observation),
            *self.memory.llm_transcript[-5:],
            {"role": "user", "content": observation_summary},
        ]

        json_payload = {
            "model": self.memory.model,
            "messages": llm_prompt,
            "require_parameters": True,
        }

        truncated_prompt = self.__truncate_prompt(llm_prompt)
        # print(f"using model: {self.memory.model}")
        # self.__print_prompt(truncated_prompt)
        
        if self.memory.llm_provider == "ollama":
            json_payload["format"] = JSON_RESPONSE_FORMAT["json_schema"]["schema"]
            json_payload["stream"] = False
            json_payload["keep_alive"] = -1 # prevent model from timing out of cache
            response = requests.post(
                os.getenv("OLLAMA_API_URL"),
                json=json_payload,
                timeout=30,
            ).json()
        else:
            json_payload["response_format"] = JSON_RESPONSE_FORMAT
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.memory.openrouter_api_key}"},
                json=json_payload,
                timeout=30,
            ).json()

        content, action, success, error_message = self.__process_llm_response(response)

        # logging what we sent and recieved to the Kradle dashboard
        self.log({"prompt": truncated_prompt, "model": self.memory.model, "response": content})

        # append to the message history
        self.memory.llm_transcript.extend(
            [
                {"role": "user", "content": observation_summary},
                {"role": "assistant", "content": content }
            ]
        )

        if success:
            return {"code": action["code"], "message": action["message"], "delay": self.memory.delay_after_action}
        
        if max_retries <= 0:
            return {"code": "", "message": "I'm sorry, I'm having trouble generating a response. Please try again later.", "delay": self.memory.delay_after_action}

        self.memory.llm_transcript.append({"role": "system", "content": f"your last response was not valid because: {error_message}"})

        return self.__get_llm_response(observation_summary, observation, max_retries - 1)

    def __process_llm_response(self, response):
        success = False
        content = ""
        action = None
        error_message = ""
        try:
            if "choices" in response and response["choices"]:
                # Example response from OpenRouter
                # response = {
                #    "choices": [
                #        {
                #            "message": {
                #                "content": """```json 
                #                { 
                #                "code": "await skills.attackNearest(bot, 'pig', true); await skills.move(bot, 10, 10, 10);", 
                #                "message": "Hunting for pigs!" 
                #                } 
                #                ```"""
                #            }
                #         }
                #    ]
                #}
                content = response["choices"][0]["message"]["content"]
            elif "message" in response:
                # Example response from Ollama
                # response = {
                #    "message": {
                #        "role": "assistant",
                #        "content": "{
                #            \"code\": \"await skills.goToNearestBlock(bot, 'oak_fence', 5);\",
                #            \"message\": \"Finding a safe spot to build a shelter.\"
                #        }"
                #    }
                content = response["message"]["content"]
            else:
                print(f"Cannot parse response from LLM: {response}")

            #find the first { and the last  }
            start = content.find("{")
            end = content.rfind("}") + 1
            content_to_parse = content[start:end]

            if content_to_parse == "":
                print(f"Error: Could not parse JSON in response. Received: {content}")
                action = { "code": "", "message": "" }
                error_message = "Unable to parse JSON from LLM response"
                return content, action, success, error_message

            # Parse the content string as JSON
            try:
                json_content = json.loads(content_to_parse)
                action = { "code": json_content["code"] if "code" in json_content else "", "message": json_content["message"] if "message" in json_content else "" }
                success = True
            except Exception as e:
                print(f"Unable to parse JSON from LLM response for content: {content_to_parse} with error: {e}")
                error_message = "Unable to parse JSON from LLM response"
                return content, action, success, error_message

        except Exception as e:
            print(f"Error: {e}")
            error_message = str(e) if e else ""

        return content, action, success, error_message

# finally, lets serve our agent!

if __name__ == "__main__":    
    # this creates a web server and an SSH tunnel (so our agent has a stable public URL)
    app, connection_info = AgentManager.serve(LLMBasedAgent, create_public_url=True)
    print(f"Started agent, now reachable at URL: {connection_info}", flush=True)

# now go to app.kradle.ai and run this agent against a challenge!