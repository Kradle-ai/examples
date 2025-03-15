# this agent uses hardcoded actions:
# it responds to any private message with a Hello World! chat message

from kradle import KradleAPI, AgentManager, MinecraftAgent, MinecraftEvent
from kradle.models import Observation
from dotenv import load_dotenv

# Load the api key from the .env file
load_dotenv()


class HelloWorldAgent(MinecraftAgent):

    username = "hello-world-agent"  # this is the username of the agent
    display_name = "Hello World Agent"  # this is the display name of the agent
    description = "This is an agent that responds to any private message with a Hello World! chat message."

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
        return {"listenTo": [MinecraftEvent.MESSAGE]}

    # this function is called when an event occurs
    # the agent returns an action to be performed
    def on_event(self, observation: Observation):
        # It is either an COMMAND_EXECUTED or MESSAGE event
        print(f"Receiving an event observation about {observation.event}")

        # Log the chat message to Kradle for debugging
        #  self.log(f"Received a chat message: {observation.message}")

        # Respond with a hello world message
        return {
            "chat": "Hello World!",
        }


# This creates a web server and opens a tunnel so it's accessible.
# It will automatically update the URL for this agent on Kradle to
# connect to this server
connection_info = AgentManager.serve(HelloWorldAgent, create_public_url=True)
print(f"Started agent at URL: {connection_info}")

# now go to app.kradle.ai and run this agent against a challenge
