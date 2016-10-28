#!/usr/env/bin python

# pylama:ignore=E501

"""Create games-features.csv from games.json."""

import csv
import json
import re
import unicodedata


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


html_tags = re.compile('<[^<]+?>')


def txt(t):
    """Return filtered text."""
    # Ascii-compatible UTF8 string
    s = unicodedata.normalize('NFKD', str(t)).encode('ascii', 'ignore').decode('utf-8')
    # No html tags
    s = html_tags.sub('', s).strip()
    # Just kill any troublesome characters
    for c in ",'\"\r\n\t":
        s = s.replace(c, '')
    return s.strip()


def num(n):
    """Return correctly interpreted number (current assume ints)."""
    n = str(n).strip() if n else None
    if not n:
        return ""
    try:
        return int(n)
    except:
        return ""


# List of columns in the order we want them in the file
# If you change the function `record`, you probably want to change
# this list
# TODO: make sure matches record() func below
COLUMNS = [
    "QueryID", "ResponseName", "QueryName", "ResponseName",

    "RequiredAge",

    # Achivements
    "AchievementCount", "AchievementHighlightedCount",

    # Categories
    "CategorySinglePlayer", "CategoryMultiplayer", "CategoryCoop", "CategoryMMO",
    "CategoryInAppPurchase",
    "CategoryIncludeSrcSDK", "CategoryIncludeLevelEditor",
    "CategoryVRSupport",

    # Text fields (potentially long)
    "ResponseName",
    "AboutText",
    "Background",
    "ShortDescrip",
    "DetailedDescrip",
    "DRMNotice",
    "ExtUserAcctNotice",
    "HeaderImage",
    "LegalNotice",
    "Reviews",
    "SupportedLanguages",
    "Website",
]


def record(raw):
    """Convert the raw JSON dict to our CSV record."""
    data = raw["data"]

    # Categories
    cats = set()
    for d in data.get('categories', []):
        c = d.get('description', '').strip().lower()
        if c:
            cats.add(c)

    return {
        "QueryID": raw["query_appid"],

        # Text fields
        "QueryName": raw["query_appname"],
        "ResponseName": txt(data.get('name', '')),
        "AboutText": txt(data.get('about_the_game', '')),
        "Background": txt(data.get('background', '')),
        "ShortDescrip": txt(data.get('short_description', '')),
        "DetailedDescrip": txt(data.get('detailed_description', '')),
        "DRMNotice": txt(data.get('drm_notice', '')),
        "ExtUserAcctNotice": txt(data.get('ext_user_account_notice', '')),
        "HeaderImage": txt(data.get('header_image', '')),
        "LegalNotice": txt(data.get('legal_notice', '')),
        "Reviews": txt(data.get('reviews', '')),
        "SupportedLanguages": txt(data.get('supported_languages', '')),
        "Website": txt(data.get('website', '')),

        # Numeric fields
        "ResponseID": num(data.get('steam_appid', None)),
        "RequiredAge": num(data.get('required_age', None)),

        # Achivements
        "AchievementCount": num(data.get('achievements', {}).get('total', 0)),
        "AchievementHighlightedCount": len(data.get('achievements', {}).get('highlighted', [])),

        # Categories
        "CategoryMultiplayer": any(i in cats for i in [
            "cross-platform multiplayer", "local multi-player", "multi-player",
            "online multi-player", "shared/split screen"
        ]),
        "CategoryCoop": any(i in cats for i in [
            "co-op", "local co-op", "online co-op"
        ]),
        "CategoryInAppPurchase": "in-app purchases" in cats,
        "CategoryIncludeSrcSDK": "includes source sdk" in cats,
        "CategoryIncludeLevelEditor": "includes level editor" in cats,
        "CategoryMMO": "mmo" in cats,
        "CategorySinglePlayer": "single-player" in cats,
        "CategoryVRSupport": "vr support" in cats,
    }

    """ TODO
    controller_support	3391	1	either ‘full’ or missing – boolean
    demos	1134	1	List – use count (DemoCount)
    developers	11402	1	List of strings – 3 field: MainDev, OtherDevs, DevCount = d[0], d[1:], len(d)
    dlc	2076	1	List of ID’s – use count
    genres	11294	1	List of dict’s – use description to discretize: see notebook
    is_free	12037	2	boolean
    linux_requirements	12037	2	Requirements – see nb for description
    mac_requirements	12037	2	Requirements – see nb for description
    metacritic	2263	1	Dict – extract key ‘score’ as int – blank on missing/failure
    movies	10429	1	Turn list of dict’s into count
    package_groups	12037	1	3 bool columns – see code in nb
    packages	10193	1	PackageCount – from len of list
    pc_requirements	12037	2	Requirements – see nb for description
    platforms	12037	1	3 bool columns from dict: Windows, Linux, Mac – keys are (“windows”, “linux”, “mac”)
    price_overview	10008	1	Dict – get PriceCurrency, PriceInitial, PriceFinal from keys “currency”, “initial”, “final”
    publishers	12037	1	List – make PublishersCount, but drop blanks and uniq-ify
    recommendations	4832	1	Use key ‘total’ to get RecommendationCount
    release_date	12037	1	ReleaseDate using key “date”
    screenshots	11336	1	ScreenshotCount is len of list
    support_info	12037	1	SupportEmail and SupportURL from keys “email” and “url”
    type	12037	1	ignore
    """


def main():
    """Entry point."""
    print("Creating games-features.csv")
    with open("games-features.csv", "w") as basefile:
        writer = csv.writer(basefile)
        writer.writerow(COLUMNS)
        count = 0
        for game in game_reader():
            rec = record(game)
            writer.writerow([rec[c] for c in COLUMNS])
            count += 1
    print("Game Records Written: %d" % count)


if __name__ == "__main__":
    main()
