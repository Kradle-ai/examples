from dotenv import load_dotenv
from kradle import Agent, Context, Kradle, OnEventResponse
from kradle.models import ChallengeInfo, MinecraftEvent, Observation


"""
This script is used to test code in a challenge.
It will run the code in the challenge and return the result.
You can also log in the Minecraft client and send code to the agent via general chat.
"""

# AGENT_NAME is the name of the agent in Kradle. Agent names are unique within
# your Kradle user account. Think of this as naming a particular strategy; you
# might iterate on that strategy but the name will stick.
#
# During and after your agent is running it will have a unique URL:
# https://kradle.ai/<my-username>/agent/<my-agent-name>.

#the name of the agent in kradle
AGENT_NAME = "test-code-agent"

#the challenge you want to test code in
CHALLENGE_SLUG = "team-kradle:capture-the-flag-tutorial"

#your Minecraft username
USER_MINECRAFT_NAME = "kelmouja"

#the initial code to run (leave empty if you don't want to run any code)
INITIAL_CODE = "await skills.goToNearestBlock(bot, 'red_banner')"



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
            "message": "hello world!",
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
        MinecraftEvent.INITIAL_STATE,
    )
    def on_initial_state(observation: Observation, context: Context) -> OnEventResponse:
        print("received initial state")
        print(observation)
        return {
            "code": INITIAL_CODE,
            "message": "executing initial code: "+INITIAL_CODE,
            "delay": 0,
        }

    @agent.event(
        MinecraftEvent.CHAT,  # general chat messages
    )
    def on_chat(observation: Observation, context: Context) -> OnEventResponse:
        # we just respond with the message from the config
        print("received chat")
        print(observation)
        chat_message = observation.chat_messages
        for message in chat_message:
            print(message.sender)
            print(message.chat_msg)
            if message.sender == USER_MINECRAFT_NAME:
                msg = message.chat_msg
                if msg.startswith(" to general chat: "):
                    code = msg.split(" to general chat: ")[1]
                    print(code)
                    return {
                        "code": code,
                        "message": "executing code: "+code,
                        "delay": 0,
                    }


        return {
            "code": "",
            "message": context["message"],
            "delay": 0,
        }


    @agent.event(
        MinecraftEvent.COMMAND_EXECUTED,  # listen to execution results
    )
    def on_command_executed(observation: Observation, context: Context) -> OnEventResponse:
        print("received command executed")
        print(observation)
        return {
            "code": "",
            "message": "",
            "delay": 0,
        }

    @agent.event(
        MinecraftEvent.IDLE,
    )
    def on_idle(observation: Observation, context: Context) -> OnEventResponse:
        print("received idle")
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

    print("waiting for challenge to start...")
