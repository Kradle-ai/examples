# this agent uses an LLM to decide what to do.
# it uses the OpenRouter API to select, prompt, and get the response from any number of LLMs

from kradle import (
    AgentManager,
    MinecraftAgent,
)
from kradle.models import MinecraftEvent
from dotenv import load_dotenv
import os
import requests
from prompts.config import (
    conversing_prompt,
    coding_prompt,
    conversation_examples,
    coding_examples,
    creative_mode_prompt,
)

load_dotenv()


# let's define a model and persona for our agent
MODEL = "openai/gpt-4o"  # refer to https://openrouter.ai/models for all available models
PERSONA = "you are a cool resourceful agent. you really want to achieve the task that has been given to you."  # check out some other personas in prompts/config.py

# plus some additional settings:
RESPOND_WITH_CODE = False  # set this to true to have the llm generate runnable code instead of regular commands
DELAY_AFTER_ACTION = 100  # this adds a delay (in milliseconds) after an action is performed. increase this if the agent is too fast or if you want more time to see the agent's actions

# your openrouter API key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


# this is your agent class. It extends the MinecraftAgent class in the Kradle SDK
# you pass this whole class into the AgentManager.serve() below
# this lets Kradle manage the lifecycle of this agent.
# Kradle can create multiple instances of your agent (eg. adding two of the same agent to a challenge)
# each instance of this class is called a 'participant'
class LLMBasedAgent(MinecraftAgent):

    username = "llm-agent"  # this is the username of the agent (eg. kradle.ai/<my-username>/agents/<my-agent-username>)
    display_name = "LLM Agent"  # this is the display name of the agent
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

        print(f"Received init_participant call for {self.participant_id} with task: {challenge_info.task}")

        # save the task to memory
        self.memory.task = challenge_info.task

        # array to store LLM history
        self.memory.messages = []

        # array to store in-game chat history
        self.memory.chat_history = []

        # set Minecraft modes (e.g. creative mode, self_preservation, etc)
        # TODO: Link to docs to explain more.
        self.memory.agent_modes = challenge_info.agent_modes

        # dictionaries to store all possible commands and javascript functions
        self.memory.commands = challenge_info.commands
        self.memory.js_functions = challenge_info.js_functions

        print(f"Initializing agent for participant ID: {self.participant_id} with username: {self.username}")
        print(f"Persona: {PERSONA}")
        print(f"Model: {MODEL}")

        # self.log() lets us log information to the Kradle dashboard (left pane in the session viewer)
        # self.log(
        #     {
        #         "persona": PERSONA,
        #         "model": MODEL,
        #         "respond_with_code": RESPOND_WITH_CODE
        #     }
        # )

        # tell Kradle what we want to listen to
        return {"listenTo": [MinecraftEvent.MESSAGE, MinecraftEvent.COMMAND_EXECUTED]}

    # this is called when an event happens
    # we return our next action
    def on_event(self, observation):

        print(f"Received on_event call for {self.participant_id} with event: {observation.event} task: {self.memory.task}")

        # lets format to observation, so we can pass it to the LLM
        state_summary = self.format_state_summary(observation)
        print(f"\nState Summary:\n{state_summary}")
        print("Task: ", self.memory.task)

        # now we pass it to the LLM, get the next action, and send it to Kradle
        response = self.get_llm_response(state_summary, observation)
        print(f"Agent Response: {response}")
        print(f"Participant ID: {self.participant_id}")

        return response

    # convert observation object => string, so we can build a LLM prompt
    def format_state_summary(self, observation):

        # python array operator to extend/append the next message
        self.memory.chat_history.extend(observation.messages)

        print(f"Messages: {self.memory.chat_history}")

        # lets get the last 10 messages
        chat_summary = (
            "\n".join(f"{msg.sender}: {msg.message}" for msg in self.memory.chat_history[-10:])
            if self.memory.chat_history
            else "None"
        )

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
            f"Chat: {chat_summary}\n\n"
            f"Visible Players: {', '.join(observation.players) if observation.players else 'None'}\n\n"
            f"Visible Blocks: {', '.join(observation.blocks) if observation.blocks else 'None'}\n\n"
            f"Inventory: {inventory_summary}\n\n"
            f"Health: {observation.health * 100}/100"
        )

    # this function builds the system prompt for the agent
    def format_system_prompt(self, observation):
        if RESPOND_WITH_CODE:
            prompt = coding_prompt
        else:
            prompt = conversing_prompt

        # load task, persona, agent_modes, and commands from memory to build the prompt
        prompt = prompt.replace("$NAME", observation.name)
        prompt = prompt.replace("$TASK", self.memory.task)
        prompt = prompt.replace("$PERSONA", PERSONA)
        prompt = prompt.replace("$AGENT_MODE", str(self.memory.agent_modes))

        # we can respond with javascript or text
        if RESPOND_WITH_CODE:
            prompt = prompt.replace("$CODE_DOCS", str(self.memory.js_functions))
            prompt = prompt.replace("$EXAMPLES", str(coding_examples))
        else:
            prompt = prompt.replace("$COMMAND_DOCS", str(self.memory.commands))
            prompt = prompt.replace("$EXAMPLES", str(conversation_examples))

            if self.memory.agent_modes["mcmode"] == "creative":
                prompt = prompt.replace("$CREATIVE_MODE", creative_mode_prompt)
            else:
                prompt = prompt.replace("$CREATIVE_MODE", "You are in survival mode.")

        return prompt

    # send the prompt to the LLM and get the response
    def get_llm_response(self, state_summary, observation):

        # build the messages array with the last 5 messages
        messages = [
            {"role": "system", "content": self.format_system_prompt(observation)},
            *self.memory.messages[-5:],
            {"role": "user", "content": state_summary},
        ]

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}"},
            json={"model": MODEL, "messages": messages},
            timeout=30,
        ).json()

        print(f"Response: {response}")

        if response["choices"]:
            content = response["choices"][0]["message"]["content"]
        else:
            content = "I'm sorry, I'm having trouble generating a response. Please try again later."

        # logging what we sent and recieved to the Kradle dashboard
        # self.log(
        #     {
        #         "prompt": messages,
        #         "model": self.memory.model,
        #         "response": content
        #     }
        # )

        # append to the message history
        self.memory.messages.extend(
            [{"role": "user", "content": state_summary}, {"role": "assistant", "content": content}]
        )

        if RESPOND_WITH_CODE:
            return {"code": content, "delay": DELAY_AFTER_ACTION}
        return {"command": content, "delay": DELAY_AFTER_ACTION}


# finally, lets serve our agent!
# this creates a web server and an SSH tunnel (so our agent has a stable public URL)
connection_info = AgentManager.serve(LLMBasedAgent, create_public_url=True)
print(f"Started agent at URL: {connection_info}")

# now go to app.kradle.ai and run this agent against a challenge!
