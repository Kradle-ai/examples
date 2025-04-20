from watchfiles import run_process
from app import app
import signal, os, sys

import logging
logging.getLogger('watchfiles').setLevel(logging.ERROR) # Disable watchfiles warnings to declutter

def signal_handler(sig, frame):
    # Exit cleanly
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)

def dev():
    # Set up signal handlers to exit cleanly
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start app here
    app(debug=True)

def watch_and_reload():
    # Run the process and restart it when changes are detected
    run_process('./', target=dev)

if __name__ == '__main__':
    watch_and_reload()
    