import speech_recognition as sr

r = sr.Recognizer()

# ALC245 Analog Mikrofon
mic = sr.Microphone(device_index=2)  # Achtung: Device index = Liste von sr.Microphone.list_microphone_names()
# Optional: List all devices
print(sr.Microphone.list_microphone_names())

with mic as source:
    print("🎤 Listening...")
    r.adjust_for_ambient_noise(source, duration=1)
    audio = r.listen(source)

try:
    text = r.recognize_google(audio)
    print("You said:", text)
except sr.UnknownValueError:
    print("Arti could not understand you 😅")
except sr.RequestError as e:
    print("Google API error:", e)

