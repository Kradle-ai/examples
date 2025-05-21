from string import Template
from typing import Any, Optional, cast
from typing_extensions import TypeAlias
from kradle import Agent, Context, Kradle
from kradle.models import ChallengeInfo, MinecraftEvent, Observation

from llm_clients import LLMClient, LLMError, LLMResponse, OpenRouterClient, parse_action_from_response
from prompts import config


# Let's define a model and persona for our agent

# Username of the agent in kradle (e.g.
# kradle.ai/<my-username>/agents/<my-agent-username>). Will be created if it
# doesn't exist.
USERNAME = "python1"

# Refer to https://openrouter.ai/models for all available models.
MODEL = "google/gemini-2.0-flash-001"

# Check out some other personas in prompts/config.py.
PERSONA = "you are a cool resourceful agent. you really want to achieve the task that has been given to you."

# Plus some additional settings:

# This adds a delay (in milliseconds) after an action is performed. Increase
# this if the agent is too fast or if you want more time to see the agent's
# actions
DELAY_AFTER_ACTION = 100

# Number of times the LLM will retry to generate a valid response
MAX_RETRIES = 3


def setup(kradle: Kradle) -> Agent:
    agent = kradle.agent(
        username=USERNAME,
        display_name=f"{USERNAME} (llm)",
        description="This is an LLM-based agent that can be used to perform tasks in Minecraft.",
    )

    # This method is called when the session starts.
    @agent.init
    def init(challenge: ChallengeInfo, context: Context):
        context["client"] = OpenRouterClient(MODEL, kradle.api)
        context["history"] = []
        context["model"] = MODEL
        context["persona"] = PERSONA
        context["delay_after_action"] = DELAY_AFTER_ACTION

    @agent.event(
        MinecraftEvent.INITIAL_STATE,
        MinecraftEvent.CHAT,
        MinecraftEvent.MESSAGE,
        MinecraftEvent.COMMAND_EXECUTED,
        MinecraftEvent.IDLE,
    )
    def event(observation: Observation, context: Context):
        client: LLMClient = context["client"]
        history: list[Message] = context["history"]

        for attempt in range(MAX_RETRIES):
            llm_prompt = format_llm_prompt(observation, context)
            show_heading(llm_prompt, attempt)

            # TODO(wilhuff): This still needs simplification work.
            try:
                response = client.get_chat_completion(llm_prompt)
                action = parse_action_from_response(response)
                log_result(llm_prompt, response.content, context)
                return action
            except LLMError as e:
                print(f"Error: {e.message_with_details()}")
                history_push_error(history, str(e))
                log_result(llm_prompt, e.content, context)
                continue
            except Exception as e:
                print(f"Error: {e}")
                history_push_error(history, str(e))
                log_result(llm_prompt, response.content if response else None, context)
                continue

        # If we fall out of the loop, we've failed.
        return {
            "code": "",
            "message": "I'm sorry, I'm having trouble generating a response. Please try again later.",
            "delay": context["delay_after_action"],
        }

    return agent


Message: TypeAlias = dict[str, str]
Messages: TypeAlias = list[Message]


def format_llm_prompt(observation: Observation, context: Context) -> Messages:
    challenge = context.challenge_info
    persona = context["persona"]
    history = context["history"]
    result = [
        *format_system_prompt(challenge, observation),
        {"role": "system", "content": substitute(config.persona_prompt, persona=persona)},
        *format_history_prompt(history),
        {"role": "user", "content": format_observation(observation)},
    ]

    return result


def format_system_prompt(challenge: ChallengeInfo, observation: Observation) -> Messages:
    if challenge.agent_modes["mcmode"] == "creative":
        creative_mode = config.creative_mode_prompt
    else:
        creative_mode = "You are in survival mode."

    result = [
        # Build coding prompt from template, including task, agent_modes,
        # and creative_mode
        substitute(
            config.coding_prompt,
            NAME=observation.name,
            TASK=challenge.task,
            AGENT_MODE=challenge.agent_modes,
            CREATIVE_MODE=creative_mode,
        ),
        # Skills prompt with code documentation to give the agent context
        # about the available commands
        substitute(config.skills_prompt, CODE_DOCS=challenge.js_functions),
        # Minecraft modes (creative, self_preservation, etc) available in
        # the challenge
        substitute(config.agent_prompt, AGENT_MODE=challenge.agent_modes),
        # Examples prompt
        substitute(config.examples_prompt, EXAMPLES=config.coding_examples),
    ]

    return [{"role": "system", "content": message} for message in result]


def format_history_prompt(history: list[Message]) -> Messages:
    return history[-5:]


def push_history(history: list[Message], llm_prompt: Messages, response: LLMResponse) -> None:
    request = llm_prompt[-1]["content"]
    history.append({"role": "user", "content": request})
    history.append({"role": "assistant", "content": response.content})


def history_push_error(history: list[Message], error: str) -> None:
    history.append({"role": "system", "content": f"your last response was not valid because: {error}"})


def format_observation(observation: Observation) -> str:
    """Converts observation object to a string for the LLM prompt."""

    # Let's get everything in our inventory
    inventory_summary = _format_list([f"{count} {name}" for name, count in observation.inventory.items()])

    # Return string with everything the LLM needs to know about the state of the game
    result = [
        f"Event received: {_format_value(observation.event)}",
        f"Command Output:\n{_format_value(observation.output)}",
        f"Position: {_format_value(observation.position)}",
    ]

    if observation.chat_messages:
        result.append(f"Latest Chat: {_format_value(observation.chat_messages)}")

    result.extend(
        [
            f"Visible Players: {_format_list(observation.players)}",
            f"Visible Blocks: {_format_list(observation.blocks)}",
            f"Visible Entities: {_format_list(observation.entities)}",
            f"Inventory: {inventory_summary}",
            f"Health: {observation.health * 100}/100",
        ]
    )

    return "\n\n".join(result)


def _format_value(value: Any) -> Any:
    return value if value else "None"


def _format_list(items: list[str]) -> str:
    return ", ".join(items) if items else "None"


def substitute(prompt: str, **kwargs) -> str:
    template = Template(prompt)
    return template.safe_substitute(**kwargs)


def show_heading(llm_prompt: Messages, attempt: int) -> None:
    if attempt == 0:
        print(f"\033[91m########################################################")
        print(f"\nObservation Summary:\n{llm_prompt[-1]['content']}")
        print(f"\033[91m########################################################\033[0m")
    else:
        print(f"\033[91m########################################################")
        print(f"\033[91mRetrying LLM response for the {attempt + 1} time\033[0m")
        print(f"\033[91m########################################################\033[0m")

    print(f"LLM Prompt: {llm_prompt}")


def log_result(llm_prompt: Messages, response: Optional[str], context: Context) -> None:
    message = {
        "prompt": truncate_prompt(llm_prompt),
        "model": context["model"],
        "response": response,
    }

    # TODO(wilhuff): The type on this API is seemingly wrong
    # ... but the old code worked. Investigate.
    context.log(cast(str, message))


# Utility function to truncate the prompt to 2000 characters for more readable logs
def truncate_prompt(prompt: Messages) -> Messages:
    truncated_prompt = []
    for p in prompt:
        truncated_p = p.copy()  # Create a shallow copy of the dict
        if len(truncated_p["content"]) > 2000:
            truncated_p["content"] = truncated_p["content"][:2000] + "..."
        truncated_prompt.append(truncated_p)
    return truncated_prompt


if __name__ == "__main__":
    kradle = Kradle(create_public_url=True, debug=True)
    agent = setup(kradle)
    app, connection_info = agent.serve()
    print(f"Started agent, now reachable at URL: {connection_info}", flush=True)
