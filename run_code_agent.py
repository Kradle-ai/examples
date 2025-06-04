from typing import Any
import time

from dotenv import load_dotenv
from kradle import Agent, Context, Kradle, OnEventResponse
from kradle.models import ChallengeInfo, MinecraftEvent, Observation


"""
An example of a Minecraft-playing agent that sends code to the be executed.

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

CHALLENGE_SLUG = "team-kradle:open-ended"

# This example shows how the main communication loop works
# when the agent gets a message from the user, it responds with hello world

global_context: dict[str, Any] = {
    "challenge_started": False,
    "is_ready": False,
    "run_context": None
}

def setup(kradle: Kradle) -> Agent:
    agent = kradle.agent(
        name=AGENT_NAME,
        # The name that will show up in the Kradle web UI.
        display_name=f"{AGENT_NAME} (Run code)",
        # A short description of the agent.
        description="This is an agent that runs your code in Minecraft.",
        # Any additional configuration you want to supply to the agent. This is
        # optional, but for the sake of this example, we'll plumb through the
        # message we respond with
        config={
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
        # storing the context in a global variable so we can access it later
        print("challenge started")
        global global_context
        global_context["run_context"] = context
        global_context["challenge_started"] = True

    # Aside from init, the system will then generate `Observation` objects for
    # your agent to process. You register interest in certain events by using
    # `@agent.event` decorator.
    #
    # For any given participant, the same `Context` object will be passed
    # repeatedly to your event handler.

    @agent.event(
        MinecraftEvent.INITIAL_STATE, #listen to chat messages
    )
    def on_initial_state(observation: Observation, context: Context) -> OnEventResponse:
        print("received initial state message")
        global global_context
        global_context["is_ready"] = True
        return {
            "code": "",
            "message": "",
            "delay": 0,
        }

    @agent.event(
        MinecraftEvent.COMMAND_EXECUTED, #listen to execution results
    )
    def on_command_executed(observation: Observation, context: Context) -> OnEventResponse:
        # we just respond with the message from the config
        print("received command result")
        print(observation.output)
        global global_context
        global_context["is_ready"] = True
        return {
            "code": "",
            "message": "",
            "delay": 0,
        }

    return agent

if __name__ == "__main__":
    load_dotenv()

    kradle = Kradle(create_public_url=True, debug=True)
    agent = setup(kradle)
    app, connection_info = agent.serve()

    # now start a run
    print("starting run...")
    run = kradle._api_client.runs.create(
        challenge_slug = CHALLENGE_SLUG,
        participants = [
            {
                "agent": AGENT_NAME
            }
        ] 
    )

    while True:
        time.sleep(1)
        if not global_context["challenge_started"]:
            print("waiting for challenge to start...")
            
        if global_context["is_ready"] and global_context["run_context"]:
            print("sending code")
            run_context = global_context["run_context"]
            global_context["is_ready"] = False

            # Ask user for the code to execute
            user_code = input("Enter the code you want to execute in Minecraft: ")

            response = kradle._api_client.runs.send_action(
                run_id = run_context.run_id,
                participant_id = run_context.participant_id,
                action = {
                    "message": "coding",
                    "code": user_code
                }
            )
            print(response)
