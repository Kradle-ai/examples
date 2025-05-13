import os
import signal
import sys
from typing import Any
import logging

import jurigged  # type: ignore
from watchfiles import run_process
from watchfiles.main import FileChange

# from app import app

from base_llm_agent import BaseLLMAgent
from kradle import AgentManager
logging.getLogger('watchfiles').setLevel(logging.ERROR) # Disable watchfiles warnings to declutter
 
_default_logger = jurigged.live.default_logger


def _dev():
    # Set up signal handlers to exit cleanly
    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)

    print("🔥 Hot reloading enabled - changes to code will be applied automatically")
    _ = jurigged.watch(["*.py", "*/*.py"], logger=_custom_logger)

    app, connection_info = AgentManager.serve(BaseLLMAgent, create_public_url=True)
    print(f"Started agent, now reachable at URL: {connection_info}", flush=True)

def _signal_handler(sig, frame):
    # Exit cleanly
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)


def _custom_logger(event: Any) -> None:
    """A jurigged logger that omits watch operations."""
    if isinstance(event, jurigged.live.WatchOperation):
        # Ignore watch operations--too much clutter
        pass
    else:
        _default_logger(event)


def _log_restart(_changes: set[FileChange]) -> None:
    print("🔥 Restarting server...")


def watch_and_reload() -> None:
    """Run the application with hot reloading enabled."""
    # Start the development server with hot reloading
    run_process(
        ".",
        target=_dev,
        callback=_log_restart,
        debounce=500,  # Debounce time in milliseconds
    )


if __name__ == "__main__":
    watch_and_reload()
