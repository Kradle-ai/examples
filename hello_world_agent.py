from string import Template
from typing import Any, Optional, cast

from dotenv import load_dotenv
from kradle import Agent, Context, Kradle, OnEventResponse
from kradle.models import ChallengeInfo, MinecraftEvent, Observation
from typing_extensions import TypeAlias


"""
An example of a Minecraft-playing agent that says hello world.

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


# This example shows how the main communication loop works
# when the agent gets a message from the user, it responds with hello world


def setup(kradle: Kradle) -> Agent:
    agent = kradle.agent(
        name=AGENT_NAME,
        # The name that will show up in the Kradle web UI.
        display_name=f"{AGENT_NAME} (hello world)",
        # A short description of the agent.
        description="This is an agent that says hello world.",
        # Any additional configuration you want to supply to the agent. This is
        # optional, but for the sake of this example, we'll plumb through the
        # message we respond with
        config={
            "message": "hello world!"
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
        # since this is a hello world agent, we don't need to do anything here
        pass

    # Aside from init, the system will then generate `Observation` objects for
    # your agent to process. You register interest in certain events by using
    # `@agent.event` decorator.
    #
    # For any given participant, the same `Context` object will be passed
    # repeatedly to your event handler.
    @agent.event(
        MinecraftEvent.CHAT, #general chat messages
    )
    def event(observation: Observation, context: Context) -> OnEventResponse:
        # we just respond with the message from the config
        return {
            "code": "",
            "message": context["message"],
            "delay": 0,
        }

    @agent.event(
        MinecraftEvent.MESSAGE, #direct messages from other players
    )
    def event(observation: Observation, context: Context) -> OnEventResponse:
        # we just respond with the message from the config, as a direct message to the sender
        chat_message = observation.chat_messages[0]
        return {
            "code": f"skills.whisper(bot, '{chat_message.sender}', '{context["message"]}')",
            "message": "",
            "delay": 0,
        }

    return agent

if __name__ == "__main__":
    load_dotenv()

    kradle = Kradle(create_public_url=True, debug=True)
    agent = setup(kradle)
    app, connection_info = agent.serve()