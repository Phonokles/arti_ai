import json
import os

MEMORY_FILE = "Memory/memory.json"


def main():

    if not os.path.exists(MEMORY_FILE):
        print("No memory found.")
        return

    with open(MEMORY_FILE) as f:
        mem = json.load(f)

    cleaned = {}

    for k, v in mem.items():

        if isinstance(v, list):
            cleaned[k] = list(set(v))
        else:
            cleaned[k] = v

    with open(MEMORY_FILE, "w") as f:
        json.dump(cleaned, f, indent=4)

    print("Memory cleaned.")


if __name__ == "__main__":
    main()
