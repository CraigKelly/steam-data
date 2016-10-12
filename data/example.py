"""Quick example of reading games.json."""

import json


def read_games():
    """Simple generator to yield everything in games.json as Python dicts."""
    with open("games.json") as f:
        for line in f:
            if not line:
                continue
            rec = json.loads(line)
            if not rec.get('success', None):
                continue
            if 'game' != rec.get('data', {}).get('type', ''):
                continue

            yield rec


def main():
    """Entry point - main logic."""
    good, bad, error, total = 0, 0, 0, 0

    for game in read_games():
        total += 1
        d = game.get("data", None)
        if d is None:
            error += 1
        elif d.get('type', None):
            good += 1
        else:
            bad += 1

    print("Good Records Seen:  %8d" % good)
    print("Bad Records Seen:   %8d" % bad)
    print("Error Records Seen: %8d" % error)
    print("                    --------")
    print("Total Records Seen: %8d" % total)
    print("                    --------")
    print("Sanity Check Total: %8d" % (good+bad+error,))

if __name__ == "__main__":
    main()
