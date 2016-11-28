# Column Descriptions for games-features.csv

The file games-features.csv is created from the raw data file games.json
(which contains a JSON object per line).

## Data Types

When a column is listed below, it is one of a few data types:

* Text - string value, sanitized for processing. See below
* TextualCount - the number of unique, non-empty strings in the original list
* Integer - integral value, missing values are 0
* Float - floating point value, missing values are 0.0
* Boolean - field has one of two literal values: True or False

## Text processing

Unless otherwise specified, any string checks/comparisons below are done are
stripping leading/trailing whitespace *and* converting the string to lowercase.

Fields of type text are also "cleaned up" for easier processing. Note that the
JSON data is processed in UTF-8, so all text is initially encoded as UTF-8
unicode. The processing steps are:


1. Unicode sequences that are not in ASCII are transliterated via the library
   `unidecode` (see https://pypi.python.org/pypi/Unidecode).
2. HTML tags are stripped out using a regular expression.
3. Any HTML entities (e.g. &gt; or &quot;) are unescaped using the Python
   standard library (`html.unescape`).
4. The HTML tag stripping routine from #2 above is *re-run* to strip out any
   HTML tags introduced via the unescaping in step #3.
5. Comma's, single-quotes, double-quotes, tabs, and line break characters are
   all removed from the string.
6. All leading and trailing whitespace is stripped
7. If the final string is empty, a default value is returned. Currently the
   default value is a single space, which insures that libraries like `pandas`
   treat the field as text when the CSV is loaded (instead of assuming a missing
   numeric value).


## Field list

* QueryID - (Integer) The original ID in idlist.csv
* ResponseID - (Integer) The ID returned in the Steam response (should equal QueryID)
* QueryName - (Text) The original name in idlist.csv
* ResponseName - (Text) The name returned in the Steam response (should equal QueryName)
* ReleaseDate - (Text) Appears to the be the initial release date for the game


* RequiredAge - (Integer) list named `required_age` in JSON
* DemoCount - (TextualCount) list named `demos` in JSON
* DeveloperCount - (TextualCount) list named `developers` in JSON
* DLCCount - (TextualCount) list named `dlc` in JSON
* Metacritic - (Integer) numeric score from metacritic object in JSON
* MovieCount - (TextualCount) list named `movies` in JSON (used object `id` for unique count)
* PackageCount  - (TextualCount) list named `packages` in JSON
* RecommendationCount  - (Integer) from `recommendations.total` in JSON
* PublisherCount  - (TextualCount) list named `publishers` in JSON
* ScreenshotCount  - (TextualCount) list named `screenshots` in JSON


* AchievementCount - (Integer) `achievements.total` in JSON
* AchievementHighlightedCount - (TextualCount) for `achievements.highlighted` in JSON


* ControllerSupport - (Boolean) True if `controller_support` was `full`
* IsFree - (Boolean) `is_free` in JSON
* FreeVerAvail - (Boolean) True if `is_free_license` is True in `package_groups` list
* PurchaseAvail - (Boolean) True if `price_in_cents_with_discount` greater than 0 in `package_groups` list
* SubscriptionAvail - (Boolean) True if `is_recurring_subscription` is True in `package_groups`
* PlatformWindows - (Boolean) True if `platforms.windows` is True
* PlatformLinux - (Boolean) True if `platforms.linux` is True
* PlatformMac - (Boolean) True if `platforms.mac` is True


* PCReqsHaveMin - (Boolean) True if `pc_requirements.minimum` is non-empty string
* PCReqsHaveRec - (Boolean) True if `pc_requirements.recommended` is non-empty string
* LinuxReqsHaveMin - (Boolean) True if `linux_requirements.minimum` is non-empty string
* LinuxReqsHaveRec - (Boolean) True if `linux_requirements.recommended` is non-empty string
* MacReqsHaveMin - (Boolean) True if `mac_requirements.minimum` is non-empty string
* MacReqsHaveRec - (Boolean) True if `mac_requirements.recommended` is non-empty string


* CategorySinglePlayer - (Boolean) True if for any i, `categories[i].description` is "single-player"
* CategoryMultiplayer - (Boolean) True if for any i, `categories[i].description` is one of: "cross-platform multiplayer", "local multi-player", "multi-player", "online multi-player", "shared/split screen"
* CategoryCoop - (Boolean) True if for any i, `categories[i].description` is one of: "co-op", "local co-op", "online co-op"
* CategoryMMO - (Boolean) True if for any i, `categories[i].description` is "mmo"
* CategoryInAppPurchase - (Boolean) True if for any i, `categories[i].description` is "in-app purchases"
* CategoryIncludeSrcSDK - (Boolean) True if for any i, `categories[i].description` is "includes source sdk"
* CategoryIncludeLevelEditor - (Boolean) True if for any i, `categories[i].description` is "includes level editor"
* CategoryVRSupport - (Boolean) True if for any i, `categories[i].description` is "vr support"


* GenreIsNonGame - (Boolean) True if for any i, `genres[i].description` is one of: "utilities", "design & illustration", "animation & modeling", "software training", "education", "audio production", "video production", "web publishing", "photo editing", "accounting"
* GenreIsIndie - (Boolean) True if for any i, `genres[i].description` is "indie"
* GenreIsAction - (Boolean) True if for any i, `genres[i].description` is "action"
* GenreIsAdventure - (Boolean) True if for any i, `genres[i].description` is "adventure"
* GenreIsCasual - (Boolean) True if for any i, `genres[i].description` is "casual"
* GenreIsStrategy - (Boolean) True if for any i, `genres[i].description` is "strategy"
* GenreIsRPG - (Boolean) True if for any i, `genres[i].description` is "rpg"
* GenreIsSimulation - (Boolean) True if for any i, `genres[i].description` is "simulation"
* GenreIsEarlyAccess - (Boolean) True if for any i, `genres[i].description` is "early access"
* GenreIsFreeToPlay - (Boolean) True if for any i, `genres[i].description` is "free to play"
* GenreIsSports - (Boolean) True if for any i, `genres[i].description` is "sports"
* GenreIsRacing - (Boolean) True if for any i, `genres[i].description` is "racing"
* GenreIsMassivelyMultiplayer - (Boolean) True if for any i, `genres[i].description` is "massively multiplayer"


* PriceCurrency - (Text) `price_overview.currency` in JSON
* PriceInitial - (Float) `price_overview.initial` in JSON, divided by 100.0 to converts cents to currency
* PriceFinal - (Float) `price_overview.final` in JSON, divided by 100.0 to converts cents to currency


* SteamSpyOwners - (steamspy.com) total owners, which includes free weekend trials and other possibly spurious numbers.
* SteamSpyOwnersVariance - (steamspy.com) total owners, which includes free weekend trials and other possibly spurious numbers. Note that this is not technically variance: according to steamspy.com, "the real number... lies somewhere on... [value +/- variance]"
* SteamSpyPlayersEstimate - (steamspy.com) best estimate of total number of people who have played the game since March 2009
* SteamSpyPlayersVariance - (steamspy.com) errors bounds on SteamSpyPlayersEstimate. Note that this is not technically variance: according to steamspy.com, "the real number... lies somewhere on... [value +/- variance]"


* SupportEmail - (Textual) `support_info.email` in JSON
* SupportURL - (Textual) `support_info.url` in JSON
* AboutText - (Textual) `about_the_game` in JSON
* Background - (Textual) `background` in JSON
* ShortDescrip - (Textual) `short_description` in JSON
* DetailedDescrip - (Textual) `detailed_description` in JSON
* DRMNotice - (Textual) `drm_notice` in JSON
* ExtUserAcctNotice - (Textual) `ext_user_account_notice` in JSON
* HeaderImage - (Textual) `header_image` in JSON
* LegalNotice - (Textual) `legal_notice` in JSON
* Reviews - (Textual) `reviews` in JSON
* SupportedLanguages - (Textual) `supported_languages` in JSON
* Website - (Textual) `website` in JSON
* PCMinReqsText - (Textual) text of `pc_requirements.minimum`
* PCRecReqsText - (Textual) text of `pc_requirements.recommended`
* LinuxMinReqsText - (Textual) text of `linux_requirements.minimum`
* LinuxRecReqsText - (Textual) text of `linux_requirements.recommended`
* MacMinReqsText - (Textual) text of `mac_requirements.minimum`
* MacRecReqsText - (Textual) text of `mac_requirements.recommended`
