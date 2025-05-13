import os
import signal
import sys
from typing import Any
import logging

import jurigged  # type: ignore
from watchfiles import run_process
from watchfiles.main import FileChange

from app import app

_default_logger = jurigged.live.default_logger


def _dev():
    # Set up signal handlers to exit cleanly
    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)

    print("🔥 Hot reloading enabled - changes to code will be applied automatically")
    _ = jurigged.watch(["*.py", "*/*.py"], logger=_custom_logger)

    app(debug=True)


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

    # Disable watchfiles warnings to declutter
    logging.getLogger("watchfiles").setLevel(logging.ERROR)

    # Run the application, watching only the top-level files for changes.
    # Changes to the `app` function or the agent_config dictionary aren't
    # picked up by jurigged, so we need to restart the server to see those.
    run_process("app.py", "dev.py", target=_dev, callback=_log_restart)


if __name__ == "__main__":
    watch_and_reload()
