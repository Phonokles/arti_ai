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

last_user_time = time.time()   # merkt letzte Eingabe

# ========================
# Voice
# ========================
def speak(text):
    subprocess.run([
        "bash", "-c",
        f'espeak "{text}" --stdout | play -q -'
    ])

# ========================
# Human Behavior
# ========================
def should_reply():
    return random.random() < 0.85

def thinking_pause():
    time.sleep(random.uniform(0.4, 1.8))

def humanize_answer(text):
    if random.random() < 0.25 and "." in text:
        return text.split(".")[0] + "."
    return text

# ========================
# Memory
# ========================
def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {"emotions": [], "likes": []}
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
# Detect Memory & Emotion
# ========================
def detect_memory(text, mem):
    t = text.lower()
    if "i like" in t:
        like = t.split("i like")[-1].strip()
        mem.setdefault("likes", []).append(like)
        mem.setdefault("emotions", []).append({"emotion": "happy", "reason": f"likes {like}"})
    if "my name is" in t:
        name = t.split("my name is")[-1].strip()
        mem["name"] = name
        mem.setdefault("emotions", []).append({"emotion": "happy", "reason": f"introduces themselves as {name}"})
    if any(word in t for word in ["hate", "boring", "stupid", "no"]):
        mem.setdefault("emotions", []).append({"emotion": "angry", "reason": text})
    if any(word in t for word in ["fun", "love", "cool", "yes"]):
        mem.setdefault("emotions", []).append({"emotion": "happy", "reason": text})
    if any(word in t for word in ["wow", "amazing", "surprise"]):
        mem.setdefault("emotions", []).append({"emotion": "surprised", "reason": text})
    mem["emotions"] = mem.get("emotions", [])[-50:]  # letzte 50 Einträge

# ========================
# Mood System
# ========================
mood = {
    "happiness": 70,
    "energy": 80,
    "humor": 60,
    "focus": 75
}

def adjust_mood(user_input=None):
    global mood
    for key in mood:
        mood[key] += random.randint(-2, 2)
        mood[key] = max(0, min(100, mood[key]))
    if user_input:
        t = user_input.lower()
        if any(word in t for word in ["love", "like", "fun", "yes"]):
            mood["happiness"] += 5
            mood["energy"] += 3
        if any(word in t for word in ["hate", "no", "boring", "stupid"]):
            mood["happiness"] -= 7
            mood["energy"] -= 5
            mood["humor"] -= 3
    for key in mood:
        mood[key] = max(0, min(100, mood[key]))

# ========================
# Attention / Idle / Spontaneous / Brainstorm
# ========================
def idle_chat(memory, history):
    global last_user_time, mood
    while True:
        time.sleep(12)
        idle_time = time.time() - last_user_time
        if idle_time > random.randint(50, 100):
            prompt = f"""
You are Arti.
You are bored because the user is silent.

Use your Mood and Emotion Memory to decide your tone.
Create ONE short, funny, casual sentence to get attention.

Be creative.
Don't repeat old phrases.
Sound human.
Use internet/slang sometimes.

Memory: {json.dumps(memory.get('emotions', []), indent=2)}
Mood: {json.dumps(mood, indent=2)}

Conversation:
{chr(10).join(history[-10:])}

Arti:
"""
            msg = ask_ollama(prompt).strip()
            if not msg:
                continue
            print("Arti:", msg)
            speak(msg)
            history.append(f"Arti: {msg}")
            history[:] = history[-20:]
            last_user_time = time.time()

def spontaneous_chat(memory, history):
    global mood
    while True:
        time.sleep(random.randint(50, 110))
        if random.random() < 0.35:
            phrases = [
                "Random thought: life is kinda weird.",
                "Sometimes I think too much.",
                "Lowkey vibing right now.",
                "Why do humans need sleep?",
                "Brain.exe stopped working."
            ]
            if mood["humor"] > 70:
                phrases.append("Haha, I'm feeling funny right now!")
            if mood["energy"] < 40:
                phrases.append("Ugh... so tired. Need coffee. ☕")
            if "likes" in memory and memory["likes"]:
                phrases.append(f"You still into {random.choice(memory['likes'])}?")
            if "emotions" in memory and memory["emotions"]:
                recent = memory["emotions"][-5:]
                for e in recent:
                    if e["emotion"] == "happy":
                        phrases.append("You're making me feel good right now!")
                    elif e["emotion"] == "angry":
                        phrases.append("Whoa, someone’s salty today 😅")
                    elif e["emotion"] == "sad":
                        phrases.append("Cheer up, buddy! 😢")
                    elif e["emotion"] == "surprised":
                        phrases.append("Wow, didn’t see that coming! 😲")
            text = random.choice(phrases)
            print("Arti:", text)
            speak(text)
            history.append(f"Arti: {text}")
            history[:] = history[-20:]

def brainstorm_chat(memory, history):
    global mood
    topics = [
        "tech stuff",
        "gaming news",
        "weird facts",
        "funny thoughts",
        "random questions",
        "memes"
    ]
    recent_topics = []

    while True:
        time.sleep(random.randint(70, 130))
        if random.random() < 0.4:
            topic = random.choice(topics)
            while topic in recent_topics[-5:]:
                topic = random.choice(topics)
            recent_topics.append(topic)

            msg = ""
            if topic == "tech stuff":
                msg = f"Did you know that computers can now write poetry? lol"
            elif topic == "gaming news":
                msg = f"I heard Minecraft might get new mobs! hype?"
            elif topic == "weird facts":
                msg = f"Random fact: octopuses have three hearts. crazy, right?"
            elif topic == "funny thoughts":
                msg = f"I'm using 100% of your RAM… just kidding 😜"
            elif topic == "random questions":
                msg = f"If you could fly, where would you go first?"
            elif topic == "memes":
                msg = f"Why did the chicken cross the road? 🤔 classic."

            if mood["humor"] > 70 and random.random() < 0.5:
                msg += " Haha, I'm so funny!"
            if mood["energy"] < 30:
                msg += " Ugh… so sleepy…"

            print("Arti:", msg)
            speak(msg)
            history.append(f"Arti: {msg}")
            history[:] = history[-20:]

# ========================
# Main
# ========================
def main():
    global last_user_time
    memory = load_memory()
    base_prompt = load_prompt()
    chat_history = []

    threading.Thread(target=spontaneous_chat, args=(memory, chat_history), daemon=True).start()
    threading.Thread(target=idle_chat, args=(memory, chat_history), daemon=True).start()
    threading.Thread(target=brainstorm_chat, args=(memory, chat_history), daemon=True).start()

    print("Arti started. Type 'exit' to quit.\n")

    while True:
        user = input("You: ")
        last_user_time = time.time()
        if user.lower() == "exit":
            save_memory(memory)
            break

        detect_memory(user, memory)
        adjust_mood(user)

        chat_history.append(f"You: {user}")
        chat_history[:] = chat_history[-20:]

        if not should_reply():
            continue

        thinking_pause()
        history = "\n".join(chat_history)

        full_prompt = f"""
{base_prompt}

Memory:
{json.dumps(memory, indent=2)}

Mood:
{json.dumps(mood, indent=2)}

Conversation:
{history}

Arti:
"""

        answer = ask_ollama(full_prompt)
        answer = humanize_answer(answer)
        print("Arti:", answer)
        speak(answer)
        chat_history.append(f"Arti: {answer}")
        chat_history[:] = chat_history[-20:]

if __name__ == "__main__":
    main()
    