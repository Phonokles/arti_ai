from datetime import datetime


FILE = "Feedback/session_report.txt"


def main():

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    report = f"""
SESSION REPORT
Date: {now}

Naturalness: 7/10
Helpfulness: 7/10
Personality: 7/10
Relevance: 7/10

Problems:
- Sometimes too long answers

Improvements:
- Shorter messages
"""

    with open(FILE, "w") as f:
        f.write(report)

    print("Session rated.")


if __name__ == "__main__":
    main()
