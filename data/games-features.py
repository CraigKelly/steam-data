#!/usr/env/bin python

# pylama:ignore=E501,C901

"""Create games-features.csv from games.json."""

import csv
import json
import re
import html

from unidecode import unidecode


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


def txt(t, defval=' '):
    """Return filtered text."""
    # Ascii-compatible UTF8 string
    s = unidecode(str(t)).strip()
    # s = unicodedata.normalize('NFKD', str(t)).encode('ascii', 'ignore').decode('utf-8')
    # No html tags
    s = html_tags.sub('', s)
    # No unescape any html entities (like &gt; or &quot;)
    s = html.unescape(s)
    # And now we need to kill any HTML tags we re-introduced
    s = html_tags.sub('', s)
    # And finally kill any troublesome characters
    for c in ",'\"\r\n\t":
        s = s.replace(c, '')
    return s.strip() or defval


def num(s, defval=0):
    """Return correctly interpreted number (current assume ints)."""
    n = str(s).strip() if s else None
    if not n:
        return defval
    try:
        return int(n)
    except:
        print("Could not int(%s)" % (n,))
        return defval


def numf(s, defval=0.0):
    """Return interpreted float - unlike num default is 0.0."""
    f = str(s).strip() if s else None
    if not f:
        return defval
    try:
        return float(f)
    except:
        print("Could not float(%s)" % (f,))
        return defval


def txt_count(lst):
    """Return count of unique, non-empty strings in the list/iterable."""
    uniq = set([str(i).strip().lower() for i in lst])
    return len(uniq - set(['']))


# List of columns in the order we want them in the file
# If you change the function `record`, you probably want to change
# this list
COLUMNS = [
    # Identifying fields
    "QueryID", "ResponseID", "QueryName", "ResponseName", "ReleaseDate",

    # Numerics
    "RequiredAge",
    "DemoCount",
    "DeveloperCount",
    "DLCCount",
    "Metacritic",
    "MovieCount",
    "PackageCount",
    "RecommendationCount",
    "PublisherCount",
    "ScreenshotCount",

    # Numerics from SteamSpy JSON
    "SteamSpyOwners",
    "SteamSpyOwnersVariance",
    "SteamSpyPlayersEstimate",
    "SteamSpyPlayersVariance",

    # Achievements (numeric)
    "AchievementCount", "AchievementHighlightedCount",

    # Bools
    "ControllerSupport",
    "IsFree",
    "FreeVerAvail", "PurchaseAvail", "SubscriptionAvail",
    "PlatformWindows", "PlatformLinux", "PlatformMac",

    # Requirements (bool)
    "PCReqsHaveMin", "PCReqsHaveRec",
    "LinuxReqsHaveMin", "LinuxReqsHaveRec",
    "MacReqsHaveMin", "MacReqsHaveRec",

    # Categories (bool)
    "CategorySinglePlayer", "CategoryMultiplayer", "CategoryCoop", "CategoryMMO",
    "CategoryInAppPurchase",
    "CategoryIncludeSrcSDK", "CategoryIncludeLevelEditor",
    "CategoryVRSupport",

    # Genres (bool)
    "GenreIsNonGame",
    "GenreIsIndie", "GenreIsAction", "GenreIsAdventure", "GenreIsCasual",
    "GenreIsStrategy", "GenreIsRPG", "GenreIsSimulation", "GenreIsEarlyAccess",
    "GenreIsFreeToPlay", "GenreIsSports", "GenreIsRacing",
    "GenreIsMassivelyMultiplayer",

    # Pricing
    "PriceCurrency", "PriceInitial", "PriceFinal",

    # Text fields (potentially long)
    "SupportEmail",
    "SupportURL",
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
    "PCMinReqsText",
    "PCRecReqsText",
    "LinuxMinReqsText",
    "LinuxRecReqsText",
    "MacMinReqsText",
    "MacRecReqsText",
]


def steam_spy_read(appid, *field_names):
    """Read the given fields from steam spy JSON."""
    if not steam_spy_read.steam_spy:
        with open("steamspy.json") as inp:
            steam_spy_read.steam_spy = json.load(inp)
        if not steam_spy_read.steam_spy:
            raise Exception("Could not read steamspy.json")

    rec = steam_spy_read.steam_spy.get(str(appid), dict())
    return tuple([num(rec.get(f, 0)) for f in field_names])


steam_spy_read.steam_spy = dict()


def record(raw):
    """Convert the raw JSON dict to our CSV record."""
    data = raw["data"]

    # Categories
    cats = set()
    for d in data.get('categories', []):
        c = d.get('description', '').strip().lower()
        if c:
            cats.add(c)

    # Genres
    genres = set()
    non_game_genres = set([
        "utilities", "design & illustration", "animation & modeling",
        "software training", "education", "audio production",
        "video production", "web publishing", "photo editing", "accounting",
    ])
    for d in data.get('genres', []):
        g = d.get('description', '').strip().lower()
        if g:
            if g in non_game_genres:
                genres.add('nongame')
            else:
                genres.add(g)

    # Package groups
    pgs = data.get("package_groups", [])
    pg_free, pg_purchase, pg_subscript = False, False, False
    for pg in pgs:
        if pg.get('is_recurring_subscription', '') == 'true':
            pg_subscript = True
        for s in pg.get('subs', list()):
            if s.get('is_free_license', None):
                pg_free = True
            elif s.get('price_in_cents_with_discount', 0) > 0:
                pg_purchase = True

    # Requirements
    # The extra "or {}" check is because some empty requirements get interpreted
    # as an empty list...
    linux_req = data.get('linux_requirements', {}) or {}
    mac_req = data.get('mac_requirements', {}) or {}
    pc_req = data.get('pc_requirements', {}) or {}

    # SteamSpy.com owner/player data
    ss_owners, ss_owners_var, ss_players, ss_players_var = steam_spy_read(
        raw['query_appid'],
        'owners',
        'owners_variance',
        'players_forever',
        'players_forever_variance',
    )

    return {
        "QueryID": raw['query_appid'],

        # Text fields
        "QueryName": raw['query_appname'],
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
        "ReleaseDate": txt(data.get('release_date', {}).get('date', '')),
        "SupportEmail": txt(data.get('support_info', {}).get('email', '')),
        "SupportURL": txt(data.get('support_info', {}).get('url', '')),

        # Numeric fields
        "ResponseID": num(data.get('steam_appid', None)),
        "RequiredAge": num(data.get('required_age', None)),
        "DemoCount": txt_count(data.get('demos', [])),
        "DeveloperCount": txt_count(data.get('developers', [])),
        "DLCCount": txt_count(data.get('dlc', [])),
        "Metacritic": num(data.get('metacritic', {}).get('score', '')),
        "MovieCount": txt_count([num(d.get('id', '')) for d in data.get('movies', [])]),
        "PackageCount": txt_count(data.get('packages', [])),
        "PublisherCount": txt_count(data.get('publishers', [])),
        "RecommendationCount": num(data.get('recommendations', {}).get('total', 0)),
        "ScreenshotCount": txt_count(data.get('screenshots', [])),

        # Steam Spy numeric fields
        "SteamSpyOwners": ss_owners,
        "SteamSpyOwnersVariance": ss_owners_var,
        "SteamSpyPlayersEstimate": ss_players,
        "SteamSpyPlayersVariance": ss_players_var,

        # Achivements
        "AchievementCount": num(data.get('achievements', {}).get('total', 0)),
        "AchievementHighlightedCount": txt_count(data.get('achievements', {}).get('highlighted', [])),

        # "Easy" Boolean fields
        "ControllerSupport": data.get("controller_support", "").strip().lower() == "full",
        "IsFree": data.get("is_free", False),
        "FreeVerAvail": pg_free,
        "PurchaseAvail": pg_purchase,
        "SubscriptionAvail": pg_subscript,
        "PlatformWindows": data.get("platforms", {}).get("windows", False),
        "PlatformLinux": data.get("platforms", {}).get("linux", False),
        "PlatformMac": data.get("platforms", {}).get("mac", False),

        # Categories (Bool)
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

        # Genres (Bool)
        "GenreIsNonGame": "nongame" in genres,
        "GenreIsIndie": "indie" in genres,
        "GenreIsAction": "action" in genres,
        "GenreIsAdventure": "adventure" in genres,
        "GenreIsCasual": "casual" in genres,
        "GenreIsStrategy": "strategy" in genres,
        "GenreIsRPG": "rpg" in genres,
        "GenreIsSimulation": "simulation" in genres,
        "GenreIsEarlyAccess": "early access" in genres,
        "GenreIsFreeToPlay": "free to play" in genres,
        "GenreIsSports": "sports" in genres,
        "GenreIsRacing": "racing" in genres,
        "GenreIsMassivelyMultiplayer": "massively multiplayer" in genres,

        # Requirements (Bool)
        "LinuxReqsHaveMin": True if linux_req.get('minimum', '') else False,
        "LinuxReqsHaveRec": True if linux_req.get('recommended', '') else False,
        "MacReqsHaveMin": True if mac_req.get('minimum', '') else False,
        "MacReqsHaveRec": True if mac_req.get('recommended', '') else False,
        "PCReqsHaveMin": True if pc_req.get('minimum', '') else False,
        "PCReqsHaveRec": True if pc_req.get('recommended', '') else False,

        # Requirements (Text)
        "PCMinReqsText": txt(pc_req.get('minimum', '')),
        "PCRecReqsText": txt(pc_req.get('recommended', '')),
        "LinuxMinReqsText": txt(linux_req.get('minimum', '')),
        "LinuxRecReqsText": txt(linux_req.get('recommended', '')),
        "MacMinReqsText": txt(mac_req.get('minimum', '')),
        "MacRecReqsText": txt(mac_req.get('recommended', '')),

        # Pricing (prices are in pennies and we convert to dollars)
        "PriceCurrency": txt(data.get("price_overview", {}).get("currency", "")),
        "PriceInitial": numf(data.get("price_overview", {}).get("initial", 0.0)) / 100.0,
        "PriceFinal": numf(data.get("price_overview", {}).get("final", 0.0)) / 100.0,
    }


def sanity_check():
    """Make sure COLUMNS and a default record match up."""
    blank = record({'query_appid': '', 'query_appname': '', 'data': {}})
    keys = set(blank.keys())
    cols = set(COLUMNS)
    if len(cols) != len(keys):
        print("Column mismatch: expected %d but found %d in blank record" % (
            len(cols), len(keys)
        ))
        print("In COLUMNS, but not in rec: %s" % repr(cols-keys))
        print("In rec, but not in COLUMNS: %s" % repr(keys-cols))
        raise Exception("Failed column check")
    if len(COLUMNS) != len(cols):
        print("Check failed: duplicate columns!")
        from collections import Counter
        print([k for k, c in Counter(COLUMNS).items() if c > 1])
        raise Exception("Duplicate columns found")


def main():
    """Entry point."""
    sanity_check()

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
