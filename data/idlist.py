#!/usr/env/bin python

"""Create idlist.csv."""

import csv
import requests


def idreader():
    """Get all ID's from Steam."""
    URL = "http://api.steampowered.com/ISteamApps/GetAppList/v2"
    print("GET", URL)
    data = requests.get(URL).json()
    for a in data.get("applist", dict()).get("apps", dict()):
        appid = a.get('appid', None)
        name = a.get('name', '')
        if not appid:
            print("Skipping mising appid: %s" % repr(a))
            continue
        if not name:
            print("AUDIT: missing name in record: %s" % repr(a))
        yield appid, name


def main():
    """Entry point."""
    print("Creating idlist.csv")
    with open("idlist.csv", "w") as basefile:
        writer = csv.writer(basefile)
        writer.writerow(["ID", "Name"])
        count = 0
        for appid, name in idreader():
            writer.writerow([appid, name])
            count += 1
    print("ID Records Written: %d" % count)


if __name__ == "__main__":
    main()
