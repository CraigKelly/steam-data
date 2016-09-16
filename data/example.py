"""Quick example of reading games.json."""

import json


def read_games():
    """Simple generator to yield everything in games.json as Python dicts."""
    with open("games.json") as f:
        for line in f:
            if line:
                yield json.loads(line)


def main():
    """Entry point - main logic."""
    good, bad, error, total = 0, 0, 0, 0

    for game in read_games():
        total += 1
        s = game.get("success", None)
        if s is None:
            error += 1  # success isn't even in the stupid object
        elif s:
            good += 1   # success is a boolean, so we got our results
        else:
            bad += 1    # success == False

    print("Good Records Seen:  %8d" % good)
    print("Bad Records Seen:   %8d" % bad)
    print("Error Records Seen: %8d" % error)
    print("                    --------")
    print("Total Records Seen: %8d" % total)
    print("                    --------")
    print("Sanity Check Total: %8d" % (good+bad+error,))

if __name__ == "__main__":
    main()
