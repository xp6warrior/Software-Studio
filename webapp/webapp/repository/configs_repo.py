import os

def get_policy() -> str:
    filepath = os.getenv("CONFIGS_PATH") + "/policy.txt"
    if not os.path.exists(filepath):
        return False
    with open(filepath, "r") as f:
        return f.read()

def write_policy(policy: str) -> bool:
    filepath = os.getenv("CONFIGS_PATH") + "/policy.txt"
    with open(filepath, "w") as f:
        f.write(policy)