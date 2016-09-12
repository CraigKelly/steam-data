#!/usr/env/bin python

"""Create games.json using ID's in idlist.csv."""

# pylama:ignore=E501

import csv
import json
import requests
import time


def id_reader():
    """Read the previous created idlist.csv."""
    print("Reading idlist.csv")
    with open("idlist.csv") as basefile:
        reader = csv.DictReader(basefile)
        for row in reader:
            yield row['ID']


def main():
    """Entry point."""
    defaults = {
        'cc': 'US',
        'l': 'english',
        'v': '1',
    }
    print("Default parameters: %s" % repr(defaults))

    URL = "http://store.steampowered.com/api/appdetails/"
    LIMIT = 190
    WAIT_TIME = 5 * 60  # 5 minutes

    print("Opening games.json")

    import logging
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('requests').setLevel(logging.DEBUG)

    with open("games.json", "w") as f:
        count = 0
        batch_count = 0
        for appid in id_reader():
            req_data = dict(defaults)
            req_data['appids'] = str(appid)

            resp_data = requests.get(URL, params=req_data)

            for appid, game in resp_data.json().items():
                f.write(json.dumps(game) + '\n')
                count += 1

            batch_count += 1
            if batch_count >= LIMIT:
                print("batch count is %d, waiting for %d secs" % (batch_count, WAIT_TIME))
                time.sleep(WAIT_TIME)
                batch_count = 0

    print("Game records written: %d" % count)


if __name__ == "__main__":
    main()
