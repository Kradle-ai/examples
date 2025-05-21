from string import Template
from typing import Any, Optional, cast

from dotenv import load_dotenv
from kradle import Agent, Context, Kradle, OnEventResponse
from kradle.models import ChallengeInfo, MinecraftEvent, Observation
from typing_extensions import TypeAlias

from llm_clients import (
    LLMClient,
    LLMError,
    LLMResponse,
    OpenRouterClient,
    message_with_details,
    parse_action_from_response,
)
from prompts import config

"""
An example of a Minecraft-playing agent based on communication with an LLM.

This script can be run directly. To run it, you must supply a Kradle API key,
either via the KRADLE_API_KEY environment variable or by setting the API key
in a .env file in this directory. See .env-example for other values you can set.

If you run this script, it will register an agent with the given AGENT_NAME
with Kradle using a tunnel to create a temporary public URL so that the Kradle
web UI or Kradle Studio can connect to it.

After running the script, go to the Kradle web UI or Kradle Studio to start
challenges to test your agent.
"""

# AGENT_NAME is the name of the agent in Kradle. Agent names are unique within
# your Kradle user account. Think of this as naming a particular strategy; you
# might iterate on that strategy but the name will stick.
#
# During and after your agent is running it will have a unique URL:
# https://kradle.ai/<my-username>/agent/<my-agent-name>.
AGENT_NAME = "python1"

# The OpenRouter model ID for the large language model to use. Refer to
# https://openrouter.ai/models for available models. Use the "copy model ID"
# button to quickly get this value for the model you want to use.
#
# If you choose to use a different LLM API provider, use the appropriate model
# name or ID for that provider.
MODEL = "google/gemini-2.0-flash-001"

# This example builds up a prompt for your LLM containing broad instructions,
# reference documentation for the available skills, some code examples, etc.
# Along with this it includes a "personality prompt" that can help guide the
# agent's overall behavior. You can use this to get the agent to be more
# aggressive or to bias more toward building, exploration, or whatever else you
# might want it to focus on.
#
# Note: this is just a feature of this example and is not required for your
# agents if you don't want it.
PERSONALITY_PROMPT = "you are a cool resourceful agent. you really want to achieve the task that has been given to you."

# This adds a delay (in milliseconds) after an action is performed. Increase
# this if the agent is too fast or if you want more time to see the agent's
# actions
DELAY_AFTER_ACTION = 100

# Number of times the LLM will retry to generate a valid response
MAX_RETRIES = 3


def setup(kradle: Kradle) -> Agent:
    agent = kradle.agent(
        name=AGENT_NAME,
        # The name that will show up in the Kradle web UI.
        display_name=f"{AGENT_NAME} (llm)",
        # A short description of the agent.
        description="This is an LLM-based agent that can be used to perform tasks in Minecraft.",
        # Any additional configuration you want to supply to the agent. This is
        # optional, but for the sake of this example, we'll plumb through the
        # values above:
        config={
            "model": MODEL,
            "delay_after_action": DELAY_AFTER_ACTION,
            "max_retries": MAX_RETRIES,
            "personality_prompt": PERSONALITY_PROMPT,
        },
    )

    # You register handlers for certain events using decorators like this. The
    # Kradle SDK will call any function decorated with @agent.init when a
    # challenge run starts. You can use this to do any setup you need.
    #
    # Each participant will get their own `Context` object. You can use this to
    # store any state specific to that participant. No two participants will
    # share the same context, even if they're running in the same Python
    # process.
    @agent.init
    def init(challenge: ChallengeInfo, context: Context):
        # Use the OpenRouter client to make API calls to the LLM. There are
        # other clients available, see llm_clients.py for more.
        context["client"] = OpenRouterClient(context["model"], kradle.api)

        # Keep track of the conversation history with the LLM.
        context["history"] = []

    # Aside from init, the system will then generate `Observation` objects for
    # your agent to process. You register interest in certain events by using
    # `@agent.event` decorator.
    #
    # For any given participant, the same `Context` object will be passed
    # repeatedly to your event handler.
    @agent.event(
        MinecraftEvent.INITIAL_STATE,
        MinecraftEvent.CHAT,
        MinecraftEvent.MESSAGE,
        MinecraftEvent.COMMAND_EXECUTED,
        MinecraftEvent.IDLE,
    )
    def event(observation: Observation, context: Context) -> OnEventResponse:
        # Context values are untyped. If you're using type annotations, you can
        # declare locals like this to impose a type on these values.
        client: LLMClient = context["client"]

        # LLMs can fail to generate valid responses to a prompt, so attempt to
        # get a reasonable response up to MAX_RETRIES times. Note that by
        # pushing an error into the history, the next attempt will incorporate
        # the error message in the prompt.
        for attempt in range(MAX_RETRIES):
            llm_prompt = format_llm_prompt(observation, context)
            show_heading(llm_prompt, attempt)

            try:
                response = client.get_chat_completion(llm_prompt)
                action = parse_action_from_response(response)
                record_result(llm_prompt, response, None, context)
                return {
                    **action,
                    "delay": context["delay_after_action"],
                }
            except Exception as e:
                print(f"Error: {message_with_details(e)}")
                record_result(llm_prompt, response, e, context)
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
    """
    Combines the challenge, the current observation, history, and other information
    into a list of prompt messages to be sent to an LLM. Messages are of the
    form

    ```
    {
        "role": "system" | "developer" | "user" | "assistant" | "tool",
        "content": str
    }
    ```

    as described in the OpenRouter API documentation.

    See https://openrouter.ai/docs/api-reference/chat-completion."""

    challenge = context.challenge_info
    persona = context["personality_prompt"]
    history = context["history"]
    result = [
        *format_system_prompt(challenge, observation),
        {"role": "system", "content": substitute(config.persona_prompt, persona=persona)},
        *format_history_prompt(history),
        {"role": "user", "content": format_observation(observation)},
    ]

    return result


def format_system_prompt(challenge: ChallengeInfo, observation: Observation) -> Messages:
    """
    Formats system prompt messages for the LLM.
    """

    # Tell the LLM which Minecraft mode it's playing in.
    if challenge.agent_modes["mcmode"] == "creative":
        creative_mode = config.creative_mode_prompt
    else:
        creative_mode = "You are in survival mode."

    result = [
        # The coding prompt gives the LLM high-level instructions about the
        # problem it needs to solve.
        substitute(
            config.coding_prompt,
            NAME=observation.name,
            TASK=challenge.task,
            AGENT_MODE=challenge.agent_modes,
            CREATIVE_MODE=creative_mode,
        ),
        # The skills prompt gives the LLM code documentation about the available
        # commands.
        substitute(config.skills_prompt, CODE_DOCS=challenge.js_functions),
        # Minecraft modes (creative, self_preservation, etc) available in
        # the challenge
        substitute(config.agent_prompt, AGENT_MODE=challenge.agent_modes),
        # The examples prompt gives the LLM examples of code it could generate.
        substitute(config.examples_prompt, EXAMPLES=config.coding_examples),
    ]

    return [{"role": "system", "content": message} for message in result]


def format_history_prompt(history: list[Message]) -> Messages:
    """
    Returns the last 5 messages in the conversation history to feed into the
    next LLM prompt.
    """
    return history[-5:]


def format_observation(observation: Observation) -> str:
    """Converts observation object to a string for the LLM prompt."""

    def _format_value(value: Any) -> Any:
        return value if value else "None"

    def _format_list(items: list[str]) -> str:
        return ", ".join(items) if items else "None"

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


def substitute(prompt: str, **kwargs) -> str:
    """
    Uses Python template strings to substitute variables into pre-built,
    parameterized prompts.
    """
    template = Template(prompt)
    return template.safe_substitute(**kwargs)


def show_heading(llm_prompt: Messages, attempt: int) -> None:
    """
    Prints a big blocky heading to the console to indicate the start of an LLM call.
    """
    if attempt == 0:
        print(f"\033[91m########################################################")
        print(f"\nObservation Summary:\n{llm_prompt[-1]['content']}")
        print(f"\033[91m########################################################\033[0m")
    else:
        print(f"\033[91m########################################################")
        print(f"\033[91mRetrying LLM response for the {attempt + 1} time\033[0m")
        print(f"\033[91m########################################################\033[0m")

    print(f"LLM Prompt: {llm_prompt}")


def record_result(
    llm_prompt: Messages,
    response: Optional[LLMResponse],
    error: Optional[Exception],
    context: Context,
) -> None:
    """
    Records the result of an LLM call both in the conversation history and
    remotely via the Kradle API.
    """
    history: list[Message] = context["history"]

    request = llm_prompt[-1]["content"]
    history.append({"role": "user", "content": request})

    content: Optional[str]
    if response and response.content:
        content = response.content
    elif isinstance(error, LLMError) and error.content:
        content = error.content
    else:
        content = None

    if content:
        history.append({"role": "assistant", "content": content})

    if error:
        history.append({"role": "system", "content": f"your last response was not valid because: {str(error)}"})

    log_result(llm_prompt, content, context)


def log_result(llm_prompt: Messages, response: Optional[str], context: Context) -> None:
    """
    Logs the result of an LLM call to the Kradle API for display in the UI.
    """
    message = {
        "prompt": truncate_prompt(llm_prompt),
        "model": context["model"],
        "response": response,
    }

    # TODO(wilhuff): The type on this API is seemingly wrong
    # ... but the old code worked. Investigate.
    context.log(cast(str, message))


def truncate_prompt(prompt: Messages, length: int = 2000) -> Messages:
    """
    Truncates prompt messages to a maximum length, useful for creating more
    readable logs.
    """
    truncated_prompt = []
    for p in prompt:
        truncated_p = p.copy()  # Create a shallow copy of the dict
        if len(truncated_p["content"]) > length:
            truncated_p["content"] = truncated_p["content"][:length] + "..."
        truncated_prompt.append(truncated_p)
    return truncated_prompt


if __name__ == "__main__":
    load_dotenv()

    kradle = Kradle(create_public_url=True, debug=True)
    agent = setup(kradle)
    app, connection_info = agent.serve()
    print(f"Started agent, now reachable at URL: {connection_info}", flush=True)
