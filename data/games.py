#!/usr/env/bin python

"""Create games.json using ID's in idlist.csv."""

import csv
import json


def id_reader():
    """Read the previous created idlist.csv."""
    print("Reading idlist.csv")
    with open("idlist.csv") as basefile:
        reader = csv.DictReader(basefile)
        for row in reader:
            yield row


def main():
    """Entry point."""
    print("Opening games.json")
    with open("games.json", "w") as f:
        count = 0
        for idinfo in id_reader():
            # TODO: actual get
            f.write(json.dumps({
                'id': idinfo.get('id', 'MISSING'),
                'name': idinfo.get('idname', 'MISSING'),
                'TODO': True
            }))
            count += 1
    print("Game records written: %d" % count)


if __name__ == "__main__":
    main()
