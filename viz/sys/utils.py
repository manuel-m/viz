import os


def dump_environment_variables() -> None:
    print("=== environment variables ===")
    for key, value in os.environ.items():
        print(f"{key}: {value}")
