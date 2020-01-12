import json
import os


def load_secrets(env_name, secret_dir):
    # Secret file
    if not os.path.exists(secret_dir):
        raise FileNotFoundError(f"Secret data file not found. Please provide '.secrets/{env_name}_secrets.json' file.")
    else:
        with open(secret_dir, 'r') as f:
            return json.loads(f.read())
