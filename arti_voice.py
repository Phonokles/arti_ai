import subprocess

def speak(text):
    subprocess.run([
        "bash", "-c",
        f'espeak "{text}" --stdout | play -q -'
    ])
