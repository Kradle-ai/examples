# this agent uses hardcoded actions:
# it responds to any private message with a Hello World! chat message

from kradle import KradleAPI, AgentManager, MinecraftAgent, MinecraftEvent
from kradle.models import Observation
from dotenv import load_dotenv
import os

# Load the api key from the .env file
load_dotenv()

# Read the JavaScript code from file
with open(os.path.join(os.path.dirname(__file__), 'build_walls.js'), 'r') as f:
    BUILD_WALLS_CODE = f.read()

class ZombieSurvivalAgent(MinecraftAgent):

    username = "zombie-survival-test-agent"  # this is the username of the agent
    display_name = "Zombie Survival Test Agent"  # this is the display name of the agent
    description = "This is an agent that survives zombies."

    # the is the first call that the agent gets when the session starts
    # agent_config contains all the instructions for the agent, starting with the task
    # the agent returns a list of events that it is interested in, which will later trigger the on_event function
    def init_participant(self, challenge_info):
        print(f"Initializing with task {challenge_info.task}")

        # Easily log a message to the Kradle session
        # for easy debugging
        #  self.log("Hello World bot initializing!")

        # Specify events to receive:
        # - MESSAGE: When chat messages received
        return {"listenTo": []}

    # this function is called when an event occurs
    # the agent returns an action to be performed
    def on_event(self, observation: Observation):
        # It is either an COMMAND_EXECUTED or MESSAGE event
        print(f"Receiving an event observation about {observation.event}")

        if observation.event == MinecraftEvent.INITIAL_STATE:
            return {
                "code": BUILD_WALLS_CODE,
                "message": "building walls!",
                "delay": 100
            }

        # Respond with an ignore message
        # should not happen, since we are not listening to any events
        return {
            "code": "",
            "message": "ignoring events...",
            "delay": 100
        }


# This creates a web server and opens a tunnel so it's accessible.
# It will automatically update the URL for this agent on Kradle to
# connect to this server
app,connection_info = AgentManager.serve(ZombieSurvivalAgent, create_public_url=True, debug=True)
print(f"Started agent at URL: {connection_info}")

# now go to app.kradle.ai and run this agent against a challenge
