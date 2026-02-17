import os
import re
from datetime import datetime


BASE = "Data"


# =========================
# Helper
# =========================

def safe_name(text):
    return re.sub(r"[^a-zA-Z0-9_-]", "", text)


def write_file(path, text):

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "a") as f:
        f.write(text + "\n")


# =========================
# Memory Parser
# =========================

def parse_memory(user, memory):

    t = user.lower()

    name = memory.get("name", "Moritz")


    # Likes
    if "ich mag" in t:

        thing = t.split("ich mag")[-1].strip().title()

        folder = f"{BASE}/Games/{safe_name(thing)}"
        file = f"{folder}/likes.txt"

        line = f"{name} likes {thing}"

        write_file(file, line)

        return f"Saved: {file}"


    # Name
    if "mein name ist" in t:

        name2 = user.split("ist")[-1].strip().title()

        folder = f"{BASE}/Persons/{safe_name(name2)}"
        file = f"{folder}/profile.txt"

        line = f"Name: {name2}"

        write_file(file, line)

        return f"Saved: {file}"


    # General topic
    words = user.split()

    if len(words) == 1:

        topic = words[0].title()

        folder = f"{BASE}/Topics/{safe_name(topic)}"
        file = f"{folder}/notes.txt"

        line = f"Mentioned: {topic}"

        write_file(file, line)

        return f"Saved: {file}"


    return None


# =========================
# Main
# =========================

def main():

    import json

    memfile = "Memory/memory.json"

    if os.path.exists(memfile):
        with open(memfile) as f:
            memory = json.load(f)
    else:
        memory = {}


    print("File-Memory Agent ready. exit = quit\n")


    while True:

        user = input("Input: ")

        if user == "exit":
            break

        res = parse_memory(user, memory)

        if res:
            print(res)
        else:
            print("No memory stored.")


if __name__ == "__main__":
    main()
