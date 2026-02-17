import os


PROMPT = "Prompts/arti_prompt.txt"
FEEDBACK = "Feedback/session_report.txt"


def main():

    if not os.path.exists(FEEDBACK):
        print("No feedback.")
        return

    with open(PROMPT) as f:
        prompt = f.read()

    with open(FEEDBACK) as f:
        feedback = f.read()

    if "too long" in feedback.lower():

        prompt += "\nKeep answers short.\n"

    with open(PROMPT, "w") as f:
        f.write(prompt)

    print("Prompt improved.")


if __name__ == "__main__":
    main()
