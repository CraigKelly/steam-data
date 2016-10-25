#!/usr/env/bin python

"""Create games-features.csv from games.json."""

import csv
import json


def game_reader():
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


COLUMNS = ["ID", "Name"]  # TODO: make sure matches record() func below


def record(raw):
    """Convert the raw JSON dict to our CSV record."""
    data = raw["data"]  # NOQA  (TODO: actually use this)
    return {
        "ID": raw["query_appid"],
        "Name": raw["query_appname"]
        # TODO: all the other columns
    }


def main():
    """Entry point."""
    print("Creating games-features.csv")
    with open("games-features.csv", "w") as basefile:
        writer = csv.writer(basefile)
        writer.writerow(COLUMNS)
        count = 0
        for game in game_reader():
            writer.writerow(record(game))
            count += 1
    print("Game Records Written: %d" % count)


if __name__ == "__main__":
    main()
