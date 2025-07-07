import logging
import queue
import textwrap
import time
from typing import Union, Callable
import threading

from dotenv import load_dotenv
from kradle import Agent, Context, Kradle, OnEventResponse
from kradle.models import ChallengeInfo, MinecraftEvent, Observation
import rich


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


def setup(kradle: Kradle, event_queue: queue.Queue[Union[ChallengeInfo, Observation]]) -> Agent:
    agent = kradle.agent(
        name=AGENT_NAME,
        # The name that will show up in the Kradle web UI.
        display_name=f"{AGENT_NAME} (Run code)",
        # A short description of the agent.
        description="This is an agent that runs your code in Minecraft.",
        # Any additional configuration you want to supply to the agent. This is
        # optional, but for the sake of this example, we'll plumb through the
        # message we respond with
        config={},
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
        event_queue.put(challenge)

    # Aside from init, the system will then generate `Observation` objects for
    # your agent to process. You register interest in certain events by using
    # `@agent.event` decorator.
    #
    # For any given participant, the same `Context` object will be passed
    # repeatedly to your event handler.

    @agent.event(
        MinecraftEvent.INITIAL_STATE,  # listen for startup.
    )
    def on_initial_state(observation: Observation, context: Context) -> OnEventResponse:
        print("received initial state")
        event_queue.put(observation)
        return {
            "code": "",
            "message": "",
            "delay": 0,
        }

    @agent.event(
        MinecraftEvent.COMMAND_EXECUTED,  # listen to execution results
    )
    def on_command_executed(observation: Observation, context: Context) -> OnEventResponse:
        print("received command executed")
        event_queue.put(observation)
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
        event_queue.put(observation)
        return {
            "code": "",
            "message": "",
            "delay": 0,
        }

    return agent


def main() -> None:
    load_dotenv()

    kradle = Kradle(create_public_url=True, debug=True)
    event_queue: queue.Queue[Union[ChallengeInfo, Observation]] = queue.Queue()
    agent = setup(kradle, event_queue)
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
    challenge = event_queue.get()
    assert isinstance(challenge, ChallengeInfo)
    print(textwrap.fill(f"Challenge started for task: {challenge.task}"))

    observation = event_queue.get()
    assert isinstance(observation, Observation)
    assert observation.event == MinecraftEvent.INITIAL_STATE.value
    print("received initial state")

    while True:
        # Wait just a moment to avoid commingling output with the flask server.
        time.sleep(0.1)

        # Ask user for the code to execute with deferred logging
        with deferred_logging:
            try:
                user_code = input("Enter the code you want to execute in Minecraft: ")
            except (EOFError, KeyboardInterrupt):
                print("Input cancelled, exiting.")
                return

        print("sending code")
        response = kradle._api_client.runs.send_action(
            run_id = challenge.run_id,
            participant_id = challenge.participant_id,
            action = {
                "message": "coding",
                "code": user_code
            }
        )
        print(response)

        print("waiting for execution result...")
        observation = event_queue.get()
        if isinstance(observation, Observation):
            if observation.event == MinecraftEvent.COMMAND_EXECUTED.value:
                print(observation.output)
            else:
                print(f"Something went wrong and the agent is now idle.")


class DeferredLogging:
    """Context manager that defers logging calls during critical sections like
    user input.

    Using this prevents log lines from interfering with user input.
    """

    def __init__(self) -> None:
        """
        Sets up alternate logging handlers that defer logging calls while
        self._is_deferring is set.
        """
        self._is_deferring = threading.Event()
        self._deferred_calls: queue.Queue[Callable[[], None]] = queue.Queue()

        outer_self = self

        class HandlerWrapper(logging.Handler):
            def __init__(self, original_handler: logging.Handler) -> None:
                self.original_handler = original_handler
                self.wrapped_emit = outer_self._make_deferred(original_handler.emit)

            def emit(self, record: logging.LogRecord) -> None:
                self.wrapped_emit(self.original_handler, record)

        def wrap(handler: logging.Handler) -> logging.Handler:
            return HandlerWrapper(handler)

        def wrap_handlers(logger: logging.Logger) -> None:
            logger.handlers = [wrap(h) for h in logger.handlers]

        wrap_handlers(logging.root)
        wrap_handlers(logging.getLogger("werkzeug"))

        # Also defer print() calls for complete coverage
        import builtins
        self._original_print = builtins.print
        builtins.print = self._make_deferred(builtins.print)

        # Also defer rich.console.Console.print calls
        self._original_console_print = rich.console.Console.print
        rich.console.Console.print = self._make_deferred_console_print()  # type: ignore

    def __enter__(self) -> None:
        """Start deferring logging calls."""
        self._is_deferring.set()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stops deferring and execute all queued logging calls."""
        self._is_deferring.clear()

        # Execute all queued logging calls.
        while True:
            try:
                call = self._deferred_calls.get_nowait()
                call()
            except queue.Empty:
                break

    def _make_deferred_console_print(self) -> Callable[..., None]:
        """Create a deferred version of Rich Console.print."""

        def unbound_print(self_console, *args, **kwargs):
            self._original_console_print(self_console, *args, **kwargs)

        return self._make_deferred(unbound_print)

    def _make_deferred(self, handler: Callable[..., None]) -> Callable[..., None]:
        def deferred_handler(*args, **kwargs):
            if self._is_deferring.is_set():
                self._deferred_calls.put(lambda: handler(*args, **kwargs))
            else:
                handler(*args, **kwargs)

        return deferred_handler


# Create a global instance
deferred_logging = DeferredLogging()


if __name__ == "__main__":
    main()
