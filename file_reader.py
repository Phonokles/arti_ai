import os
import re


BASE = "Data"


# =====================
# Helper
# =====================

def normalize(text):
    return re.sub(r"[^a-zA-Z0-9 ]", "", text.lower())


# =====================
# Finder
# =====================

def find_relevant_dirs(text):

    text = normalize(text)

    matches = []

    for root, dirs, files in os.walk(BASE):

        for d in dirs:

            name = normalize(d)

            if name in text:
                matches.append(os.path.join(root, d))

    return list(set(matches))


# =====================
# Reader
# =====================

def read_files(dirs):

    content = []

    for d in dirs:

        for f in os.listdir(d):

            if f.endswith(".txt"):

                path = os.path.join(d, f)

                with open(path, errors="ignore") as file:
                    content.append(file.read())

    return "\n".join(content)


# =====================
# Main API
# =====================

def load_memory_for_text(text):

    dirs = find_relevant_dirs(text)

    if not dirs:
        return ""

    data = read_files(dirs)

    return data


# =====================
# Test
# =====================

if __name__ == "__main__":

    q = input("Test: ")

    print("\nLoaded Memory:\n")
    print(load_memory_for_text(q))
