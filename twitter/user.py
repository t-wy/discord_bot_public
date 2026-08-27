
def conv_user_result(user_result):
    """
    Basic requirements:
    name, screen_name, profile_image_url_https
    """
    if "legacy" in user_result:
        legacy = user_result["legacy"]
        del user_result["legacy"]
        user_result.update(legacy)
        """
        Leagcy:
        blocked_by, blocking, can_dm, can_media_tag, created_at, default_profile, default_profile_image, description, entities, fast_followers_count, favourites_count, follow_request_sent, followed_by, followers_count, following, friends_count, has_custom_timelines, is_translator, listed_count, location, media_count, muting, name, needs_phone_verification, normal_followers_count, notifications, pinned_tweet_ids_str, possibly_sensitive, profile_banner_url, profile_image_url_https, profile_interstitial_type, protected, screen_name, statuses_count, time_zone, translator_type, url, utc_offset, verified, want_retweets, withheld_description, withheld_scope
        Not legacy:
        is_blue_verified, has_graduated_access, affiliates_highlighted_label, parody_commentary_fan_label, profile_image_shape, rest_id, super_follow_eligible, super_followed_by, super_following, tipjar_settings
        """
        return user_result
    """
    Fields:
    __typename, rest_id, id, core, avatar, relationship_counts, tweet_counts, privacy, professional, verification, super_follow_eligible, profile_image_shape, identity_profile_labels_highlighted_label
    """
    return {
        **user_result.get("core", {}), # name, screen_name
        **user_result.get("privacy", {}), # protected
        **user_result.get("verification", {}), # is_blue_verified, verified_type
        "followers_count": user_result.get("relationship_counts", {}).get("followers"),
        "friends_count": user_result.get("relationship_counts", {}).get("following"),
        "profile_image_url_https": user_result.get("avatar", {}).get("image_url"),
        "statuses_count": user_result.get("user_result", {}).get("tweets"),
        **user_result
        # "__typename": user_result["__typename"],
    }

def user_id_graphql(ac: str):
    """
    Get user id from screen name
    """
    from .api import twitter_graphql
    def _internal(api: twitter_graphql):
        params = {
            "variables": {
                "screen_name": ac,
                "withSafetyModeUserFields": True,
            },
            "features": {
                "hidden_profile_likes_enabled": False,
                "hidden_profile_subscriptions_enabled": False,
                "responsive_web_graphql_exclude_directive_enabled": True,
                "verified_phone_label_enabled": False,
                "subscriptions_verification_info_verified_since_enabled": True,
                "highlights_tweets_tab_ui_enabled": True,
                "creator_subscriptions_tweet_preview_api_enabled": True,
                "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                "responsive_web_graphql_timeline_navigation_enabled": True
            },
            "fieldToggles": {
                "withAuxiliaryUserLabels": False
            }
        }
        result = api.get_raw("xc8f1g7BYqr6VTzTbvNlGw", "UserByScreenName", params)
        return result["data"]["user"]["result"]["rest_id"]
    try:
        return _internal(twitter_graphql.from_guest())
    except Exception as e:
        for _ in range(3):
            try:
                return _internal(twitter_graphql.from_random_account())
            except:
                pass
        else:
            raise e

def user_iter_legacy(ac):
    from .api import twitter
    if ac[0] == "@":
        ac = ac[1:]
    api = twitter.from_guest() # from_const()
    params = {'screen_name':ac, "count":"200", "include_rts":"false", "tweet_mode":"extended"}
    while len(temp := api.get_raw("statuses/user_timeline.json", params)):
        for t in temp:
            yield t
        params["max_id"] = str(temp[-1]['id'] - 1)


def user_iter_syndication(ac):
    import requests
    if ac[0] == "@":
        ac = ac[1:]
    url = "https://syndication.twitter.com/srv/timeline-profile/screen-name/{}".format(ac)
    r = requests.get(url = url)
    if r.status_code != 200:
        raise StopIteration
    data = r.text.split('<script id="__NEXT_DATA__" type="application/json">')[1].split("</script>")[0]
    import json
    data = json.loads(data)
    if data['props']['pageProps']['contextProvider']['hasResults']:
        for t in data['props']['pageProps']['timeline']['entries']:
            yield t['content']['tweet']

def user_iter_graphql(ac: str):
    from .api import twitter_graphql
    def _internal(api: twitter_graphql):
        params = {
            "variables": {
                "userId": str(user_id_graphql(ac)),
                "count": 20,
                "includePromotedContent": True,"withQuickPromoteEligibilityTweetFields": True,"withVoice": True,
                "withV2Timeline": True
            },
            "features": {
                "rweb_lists_timeline_redesign_enabled": True,
                "responsive_web_graphql_exclude_directive_enabled": True,
                "verified_phone_label_enabled": False,
                "creator_subscriptions_tweet_preview_api_enabled": True,
                "responsive_web_graphql_timeline_navigation_enabled": True,
                "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                "tweetypie_unmention_optimization_enabled": True,
                "responsive_web_edit_tweet_api_enabled": True,
                "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                "view_counts_everywhere_api_enabled": True,
                "longform_notetweets_consumption_enabled": True,
                "responsive_web_twitter_article_tweet_consumption_enabled": False,
                "tweet_awards_web_tipping_enabled": False,
                "freedom_of_speech_not_reach_fetch_enabled": True,
                "standardized_nudges_misinfo": True,
                "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                "longform_notetweets_rich_text_read_enabled": True,
                "longform_notetweets_inline_media_enabled": True,
                "responsive_web_media_download_video_enabled": False,
                "responsive_web_enhance_cards_enabled": False
            },
            "fieldToggles": {
                "withAuxiliaryUserLabels": False,
                "withArticleRichContentState": False
            }
        }
        result = api.get_raw("XicnWRbyQ3WgVY__VataBQ", "UserTweets", params)
        entries = result["data"]["user"]["result"]["timeline_v2"]["timeline"]["instructions"][2]["entries"]
        from .utility import conv_tweet_graphql
        for t in entries:
            yield conv_tweet_graphql(t['content']['itemContent']['tweet_results']['result'])
    try:
        yield from _internal(twitter_graphql.from_guest())
    except Exception as e:
        for _ in range(3):
            try:
                yield from _internal(twitter_graphql.from_random_account())
            except:
                pass
        else:
            raise e

def user_iter_html(ac: str):
    """
    This method does not need login, but can only get 4 posts at most
    """
    import requests
    url = f"https://x.com/{ac}"
    html_content = requests.get(url).text
    from extractors.tanstack import parse_html
    matches, records = parse_html(html_content)
    assert len(records)
    target_user_key = f'user_result_by_screen_name(safety_level:"UserProfileHeader",screen_name:"{ac}")'
    match_user_entry = next(
        (
            record[target_user_key]
            for record in records
            if target_user_key in record
        ), None
    )
    if match_user_entry is None:
        from common.exception import UserNotFoundException
        raise UserNotFoundException()
    target_key = f'user_result_by_screen_name(safety_level:"UserScopedTimeline",screen_name:"{ac}")'
    # print(list(record.keys() for record in records))
    match_entry = next(
        (
            record[target_key]["result"]["profile_user_originals_timeline"]
            for record in records
            if target_key in record
        ), None
    )
    if match_entry is None:
        return
    for key, value in match_entry.items():
        if key.startswith('timeline('):
            instructions = value["instructions"]
            break
    else:
        return
    for instruction in instructions:
        if instruction["__typename"] == "TimelineAddEntries":
            entries = instruction["entries"]
            break
    else:
        return
    for entry in entries:
        if entry["__typename"] != "TimelineTimelineEntry":
            continue
        if entry["content"]["__typename"] != "TimelineTimelineItem":
            continue
        from .utility import conv_tweet_graphql
        yield conv_tweet_graphql(entry["content"]["content"]["tweet_results"]["result"])

def user_iter(ac: str):
    """
    Try all current working user_iter methods
    """
    yield from user_iter_html(ac)

def user_timeline_legacy(ac, max_id=-1):
    from .api import twitter
    api = twitter.from_guest() # from_const()
    params = {'screen_name':ac, "count":"1", "include_rts":"false", "tweet_mode":"extended"}
    max_id = int(max_id)
    if max_id > -1:
        params['max_id'] = str(max_id)
    return api.get_raw("statuses/user_timeline.json", params)

def get_latest_tweet_legacy(ac: str, cnt: int = 1):
    max_allowed = 200
    if ac[0] == "@":
        ac = ac[1:]
    if cnt < 1:
        return None, "Count Invalid: " + str(cnt)
    if cnt > max_allowed:
        return None, "Count Invalid: " + str(cnt) + ", max allowed: " + str(max_allowed)
    total = 0
    max_id = -1
    while True:
        data = user_timeline_legacy(ac, max_id)
        if "errors" in data:
            return None, "Error:\n" + "\n".join([i['message'] + " (" + str(i['code']) + ")" for i in data['errors']])
        else:
            if type(data) == type([]):
                if cnt <= total + len(data):
                    return data[cnt - total - 1], None
                else:
                    total += len(data)
                    max_id = int(data[-1]['id_str']) - 1
            else:
                return None, "No tweets found."

def get_latest_tweet_syndication(ac: str, cnt: int = 1):
    if cnt < 1:
        return None, "Count Invalid: " + str(cnt)
    lst = list(user_iter_syndication(ac))
    if cnt <= len(lst):
        return lst[cnt - 1], None
    return None, "No tweets found."

def get_latest_tweet_graphql(ac: str, cnt: int = 1): # not latest anymore
    if cnt < 1:
        return None, "Count Invalid: " + str(cnt)
    lst = list(user_iter_graphql(ac))
    if cnt <= len(lst):
        return lst[cnt - 1], None
    return None, "No tweets found."

def get_latest_tweet_html(ac: str, cnt: int = 1):
    if cnt < 1:
        return None, "Count Invalid: " + str(cnt)
    lst = list(user_iter_html(ac))
    if cnt <= len(lst):
        return lst[cnt - 1], None
    return None, "No tweets found."

def get_latest_tweet(ac: str, cnt: int = 1):
    if cnt < 1:
        return None, "Count Invalid: " + str(cnt)
    lst = list(user_iter(ac))
    if cnt <= len(lst):
        return lst[cnt - 1], None
    return None, "No tweets found."

def get_latest_tweet(ac: str, cnt: int = 1): # temporary measure
    return get_latest_tweet_html(ac, cnt)

async def post_latest_tweet(message, ac: str, cnt: int = 1):
    tweet, errormsg = get_latest_tweet(ac, cnt)
    if errormsg is not None:
        await message.reply(errormsg)
    else:
        from .utility import reply_twitter_embed, discord_embeds_from_tweet
        await reply_twitter_embed(message, *discord_embeds_from_tweet(tweet))


def get_user_pin_html(ac: str):
    import requests
    url = f"https://x.com/{ac}"
    html_content = requests.get(url).text
    from extractors.tanstack import parse_html
    matches, records = parse_html(html_content)
    assert len(records)
    target_user_key = f'user_result_by_screen_name(safety_level:"UserProfileHeader",screen_name:"{ac}")'
    match_user_entry = next(
        (
            record[target_user_key]
            for record in records
            if target_user_key in record
        ), None
    )
    if match_user_entry is None:
        from common.exception import UserNotFoundException
        raise UserNotFoundException()
    target_key = f'user_result_by_screen_name(safety_level:"UserScopedTimeline",screen_name:"{ac}")'
    match_entry = next(
        (
            record[target_key]["result"]["profile_user_originals_timeline"]
            for record in records
            if target_key in record
        ), None
    )
    if match_entry is None:
        return None
    for key, value in match_entry.items():
        if key.startswith('timeline('):
            instructions = value["instructions"]
            break
    else:
        return None
    for instruction in instructions:
        if instruction["__typename"] == "TimelinePinEntry":
            entry = instruction["entry"]
            break
    else:
        return None
    from .utility import conv_tweet_graphql
    return conv_tweet_graphql(entry["content"]["content"]["tweet_results"]["result"])