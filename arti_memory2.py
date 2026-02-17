import os
import json
import random
import threading
import time
import subprocess
import requests

MODEL = "arti"

MEMORY_FILE = "Memory/memory.json"
PROMPT_FILE = "Prompts/arti_prompt.txt"
OLLAMA_URL = "http://localhost:11434/api/generate"

# ========================
# Voice
# ========================
def speak(text):
    subprocess.run([
        "bash", "-c",
        f'espeak "{text}" --stdout | play -q -'
    ])


# ========================
# Memory
# ========================
def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


def save_memory(mem):
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
    with open(MEMORY_FILE, "w") as f:
        json.dump(mem, f, indent=4)


# ========================
# Prompt
# ========================
def load_prompt():
    if not os.path.exists(PROMPT_FILE):
        return ""
    with open(PROMPT_FILE) as f:
        return f.read()


# ========================
# Ollama API
# ========================
def ask_ollama(prompt):
    data = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }
    r = requests.post(OLLAMA_URL, json=data)
    if r.status_code != 200:
        print("API Error:", r.text)
        return ""
    return r.json()["response"]


# ========================
# Memory erkennen
# ========================
def detect_memory(text, mem):
    t = text.lower()
    if "i like" in t:
        like = t.split("i like")[-1].strip()
        mem.setdefault("likes", []).append(like)
    if "my name is" in t:
        name = t.split("my name is")[-1].strip()
        mem["name"] = name


# ========================
# Proaktives Labern
# ========================
def spontaneous_chat(memory, chat_history):
    while True:
        time.sleep(random.randint(30, 90))
        if random.random() > 0.5:
            phrases = [
                "I was just thinking about something fun...",
                "Did you know I love chatting about games?",
                "Hmm, I wonder what Papa is up to...",
                "Sometimes I just like to think out loud 😎"
            ]
            if "likes" in memory and memory["likes"]:
                phrases.append(f"You really like {random.choice(memory['likes'])}, right?")
            text = random.choice(phrases)
            print("Arti:", text)
            speak(text)
            chat_history.append(f"Arti: {text}")
            # Limit auf 20 Nachrichten
            if len(chat_history) > 20:
                chat_history[:] = chat_history[-20:]


# ========================
# Main
# ========================
def main():
    memory = load_memory()
    base_prompt = load_prompt()
    chat_history = []  # speichert letzten 20 Nachrichten

    # Starte Hintergrund-Thread für proaktives Labern
    threading.Thread(target=spontaneous_chat, args=(memory, chat_history), daemon=True).start()

    print("Arti gestartet. 'exit' = beenden\n")

    while True:
        user = input("You: ")
        if user.lower() == "exit":
            save_memory(memory)
            break

        detect_memory(user, memory)
        chat_history.append(f"You: {user}")
        if len(chat_history) > 20:
            chat_history = chat_history[-20:]

        history_for_prompt = "\n".join(chat_history)

        full_prompt = f"""
{base_prompt}

Memory:
{json.dumps(memory, indent=2)}

{history_for_prompt}

Arti:
"""
        answer = ask_ollama(full_prompt)
        print("Arti:", answer)
        speak(answer)
        chat_history.append(f"Arti: {answer}")
        if len(chat_history) > 20:
            chat_history = chat_history[-20:]


if __name__ == "__main__":
    main()
