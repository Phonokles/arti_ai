import os


DATA = "Data"


def find_relevant(text):

    paths = []

    for root, dirs, files in os.walk(DATA):

        for d in dirs:
            if d.lower() in text.lower():
                paths.append(os.path.join(root, d))

        for f in files:
            if f.lower().replace(".txt", "") in text.lower():
                paths.append(os.path.join(root, f))

    return paths


def main():

    text = input("Input: ")

    res = find_relevant(text)

    print("Relevant files:")

    for r in res:
        print("-", r)


if __name__ == "__main__":
    main()
