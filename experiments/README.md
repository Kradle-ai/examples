# Run your challenges on your local machine via Kradle Studio

The `run_challenges_locally.py` script demonstrates how to run experiments through Kradle Studio instead of the cloud backend.

### Prerequisites

- Instally and run Kradle Studio
- Run `pip install -r requirements.txt`
- Rename `.env.example` to `.env` and add your API key

### Usage

1. Start Kradle Studio on your machine
2. Go to terminal, run:
   ```
   python run_challenges_locally.py
   ```

By default, this script uses the Studio API on your local machine. To use the cloud API instead:
```
python run_challenges_locally.py --cloud
```