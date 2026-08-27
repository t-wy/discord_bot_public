def get_tweet_legacy(tweet_id):
    from .api import twitter
    api = twitter.from_guest()
    # api = twitter.from_const() # "You currently have access to a subset of X API V2 endpoints and limited v1.1 endpoints (e.g. media post, oauth) only. If you need access to this endpoint, you may need a different access level. You can learn more here: https://developer.x.com/en/portal/product"
    params = {"include_my_retweet":"false", "tweet_mode":"extended"}
    return api.get_raw("statuses/show/{}.json".format(tweet_id), params)

def get_tweet_syndication(tweet_id, show_stat=True):
    import requests
    url = "https://cdn.syndication.twimg.com/tweet-result?id={}&token=token".format(tweet_id) # they just want a token, put a random string there
    r = requests.get(url = url)
    if r.status_code == 404:
        from .utility import placeholder_404
        return placeholder_404
    tweet = r.json()
    # print(tweet)
    return tweet

def get_tweet_graphql(tweet_id: int):
    from .api import twitter_graphql
    def _internal(api: twitter_graphql):
        params = {
            "variables": {
                "tweetId": str(tweet_id),
                "withCommunity": False,
                "includePromotedContent": False,
                "withVoice": False
            },
            "features": {
                "creator_subscriptions_tweet_preview_api_enabled": True,
                # "communities_web_enable_tweet_community_results_fetch": True,"c9s_tweet_anatomy_moderator_badge_enabled": True,"articles_preview_enabled": True,
                "tweetypie_unmention_optimization_enabled": True,
                "responsive_web_edit_tweet_api_enabled": True,
                "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                "view_counts_everywhere_api_enabled": True,
                "longform_notetweets_consumption_enabled": True,
                "responsive_web_twitter_article_tweet_consumption_enabled": False, # True
                "tweet_awards_web_tipping_enabled": False,
                # "creator_subscriptions_quote_tweet_preview_enabled": False,
                "freedom_of_speech_not_reach_fetch_enabled": True,
                "standardized_nudges_misinfo": True,
                "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                # "rweb_video_timestamps_enabled": True,
                "longform_notetweets_rich_text_read_enabled": True,
                "longform_notetweets_inline_media_enabled": True,
                # "rweb_tipjar_consumption_enabled": True,
                "responsive_web_graphql_exclude_directive_enabled": True,
                "verified_phone_label_enabled": False,
                "responsive_web_media_download_video_enabled": False,
                "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                "responsive_web_graphql_timeline_navigation_enabled": True,
                "responsive_web_enhance_cards_enabled": False,
            },
            "fieldToggles": {
                "withArticleRichContentState": False,
                "withAuxiliaryUserLabels": False,
                # "withArticlePlainText": False,
                # "withGrokAnalyze": False,
            }
        }
        result = api.get_raw("0hWvDhmW8YQ-S_ib3azIrw", "TweetResultByRestId", params)
        # result = api.get_raw("2ICDjqPd81tulZcYrtpTuQ", "TweetResultByRestId", params)
        # result = api.get_raw("mbnjGF4gOwo5gyp9pe5s4A", "TweetResultByRestId", params) # needs responsive_web_home_pinned_timelines_enabled
        # result = api.get_raw("Xl5pC_lBk_gcO2ItU39DQw", "TweetResultByRestId", params) # needs c9s_tweet_anatomy_moderator_badge_enabled, creator_subscriptions_quote_tweet_preview_enabled, articles_preview_enabled, rweb_video_timestamps_enabled, rweb_tipjar_consumption_enabled, communities_web_enable_tweet_community_results_fetch
        from .utility import conv_tweet_graphql
        return conv_tweet_graphql(result["data"]["tweetResult"]["result"])
    try:
        # more modern
        return get_tweet_detail_graphql(tweet_id)
    except:
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

def get_tweet_detail_graphql(tweet_id: int):
    from .api import twitter_graphql
    def _internal(api: twitter_graphql):
        params = {
            "variables": {
                "focalTweetId": str(tweet_id),
                "with_rux_injections": False,
                "rankingMode":"Relevance",
                "includePromotedContent": True,
                "withCommunity": True,
                "withQuickPromoteEligibilityTweetFields": True,
                "withBirdwatchNotes": True,
                "withVoice": True,
            },
            "features":  {
                "rweb_video_screen_enabled": False,
				"profile_label_improvements_pcf_label_in_post_enabled": True,
				"rweb_tipjar_consumption_enabled": True,
				"verified_phone_label_enabled": False,
				"creator_subscriptions_tweet_preview_api_enabled": True,
				"responsive_web_graphql_timeline_navigation_enabled": True,
				"responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
				"premium_content_api_read_enabled": False,
				"communities_web_enable_tweet_community_results_fetch": True,
				"c9s_tweet_anatomy_moderator_badge_enabled": True,
				"responsive_web_grok_analyze_button_fetch_trends_enabled": False,
				"responsive_web_grok_analyze_post_followups_enabled": True,
				"responsive_web_jetfuel_frame": False,
				"responsive_web_grok_share_attachment_enabled": True,
				"articles_preview_enabled": True,
				"responsive_web_edit_tweet_api_enabled": True,
				"graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
				"view_counts_everywhere_api_enabled": True,
				"longform_notetweets_consumption_enabled": True,
				"responsive_web_twitter_article_tweet_consumption_enabled": True,
				"tweet_awards_web_tipping_enabled": False,
				"responsive_web_grok_show_grok_translated_post": False,
				"responsive_web_grok_analysis_button_from_backend": True,
				"creator_subscriptions_quote_tweet_preview_enabled": False,
				"freedom_of_speech_not_reach_fetch_enabled": True,
				"standardized_nudges_misinfo": True,
				"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
				"longform_notetweets_rich_text_read_enabled": True,
				"longform_notetweets_inline_media_enabled": True,
				"responsive_web_grok_image_annotation_enabled": True,
				"responsive_web_enhance_cards_enabled": False,
            },
            "fieldToggles": {
                "withArticleRichContentState": True,
                "withArticlePlainText": False,
                "withGrokAnalyze": False,
                "withDisallowedReplyControls": False,
            }
        }
        # result = api.get_raw("Ez6kRPyXbqNlhBwcNMpU-Q", "TweetDetail", params)
        result = api.get_raw("_8aYOgEDz35BrBcBal1-_w", "TweetDetail", params)
        # print(result)
        # from pprint import pprint
        # pprint(result)
        assert "data" in result
        for instruction in result["data"]["threaded_conversation_with_injections_v2"]["instructions"]:
            if instruction["type"] != "TimelineAddEntries":
                continue
            for entry in instruction["entries"]:
                if "content" not in entry:
                    continue
                if entry["content"]["entryType"] != "TimelineTimelineItem":
                    continue
                if len(entry["content"]["itemContent"]["tweet_results"]) == 0:
                    continue
                if int(entry["content"]["itemContent"]["tweet_results"]["result"]["legacy"]["id_str"]) != tweet_id:
                    continue
                from .utility import conv_tweet_graphql
                return conv_tweet_graphql(entry["content"]["itemContent"]["tweet_results"]["result"])
        from .utility import placeholder_404
        return placeholder_404
    # def _internal2(api: twitter_graphql):
    #     from json import loads
    #     result = api.get_raw("0aTrQMKgj95K791yXeNDRA", "TweetResultByRestId", {
    #         "variables": {
    #             "tweetId": str(tweet_id),
    #             "includePromotedContent": True,
    #             "withBirdwatchNotes": True,
    #             "withVoice": True,
    #             "withCommunity": True
    #         },
    #         "features": loads('{"creator_subscriptions_tweet_preview_api_enabled":true,"premium_content_api_read_enabled":false,"communities_web_enable_tweet_community_results_fetch":true,"c9s_tweet_anatomy_moderator_badge_enabled":true,"responsive_web_grok_analyze_button_fetch_trends_enabled":false,"responsive_web_grok_analyze_post_followups_enabled":true,"responsive_web_jetfuel_frame":true,"responsive_web_grok_share_attachment_enabled":true,"responsive_web_grok_annotations_enabled":false,"articles_preview_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"responsive_web_grok_show_grok_translated_post":true,"responsive_web_grok_analysis_button_from_backend":true,"post_ctas_fetch_enabled":true,"creator_subscriptions_quote_tweet_preview_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"profile_label_improvements_pcf_label_in_post_enabled":true,"responsive_web_profile_redirect_enabled":false,"rweb_tipjar_consumption_enabled":false,"verified_phone_label_enabled":false,"responsive_web_grok_image_annotation_enabled":true,"responsive_web_grok_imagine_annotation_enabled":true,"responsive_web_grok_community_note_auto_translation_is_enabled":false,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_enhance_cards_enabled":false}')
    #     })
    #     print(result)
    try:
        return _internal(twitter_graphql.from_guest())
    except Exception as e:
        for _ in range(3):
            try:
                return _internal(twitter_graphql.from_random_account())
            except:
                import traceback
                traceback.print_exc()
                pass
        else:
            raise e

def get_tweet_html(tweet_id: int):
    import requests
    url = f"https://x.com/i/status/{tweet_id}"
    html_content = requests.get(url).text
    from extractors.tanstack import parse_html
    matches, records = parse_html(html_content)
    assert len(records)
    content = records[0]
    assert content["__typename"] == "__Root"
    tweet_result = next(
        value
        for key, value in content.items()
        if key.startswith(f'tweet_result_by_rest_id(rest_id:"{tweet_id}"')
        and isinstance(value, dict)
    )
    assert tweet_result["__typename"] == "TweetResults"
    if tweet_result["result"] is None:
        from .utility import placeholder_404
        return placeholder_404
    from .utility import conv_tweet_graphql
    return conv_tweet_graphql(tweet_result["result"])

def get_tweet(tweet_id):
    try:
        return get_tweet_html(int(tweet_id))
    except Exception as e:
        try:
            return get_tweet_graphql(int(tweet_id))
        except:
            try:
                return get_tweet_syndication(int(tweet_id))
            except:
                raise e