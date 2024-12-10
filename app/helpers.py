import os

def get_env_name():
    return os.getenv("ENV_NAME", "dev")