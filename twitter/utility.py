from typing import *

placeholder_404 = {
    "errors": [
        {
            "code": 404,
            "message": "Tweet not Found"
        }
    ]
}

async def reply_twitter_embed(message, embeds, msg: str):
    """
    msg: platform-compatible message content (allow markdown)
    """
    if embeds is not None and len(embeds):
        content = "\n".join(e.author.url for e in embeds if e.author.url is not None if e.author.url.startswith("https://twitter.com/"))
        await message.reply(embeds=embeds, content=content)
    if msg is not None and msg.strip() != "":
        await message.reply(content=msg)

def conv_tweet_graphql(tweet):
    if tweet['__typename'] == 'TweetTombstone':
        from common.exception import APIFailException
        raise APIFailException("**{}**\n{}".format(tweet['__typename'], tweet["tombstone"]["text"]["text"]))
    if tweet['__typename'] not in ('Tweet', 'TweetWithVisibilityResults'):
        from common.exception import APIFailException
        raise APIFailException("**{}**\n{}".format(tweet['__typename'], tweet['reason']))
    if "tweet" in tweet:
        tweet = tweet["tweet"]
    temp = tweet["legacy"]
    del tweet["legacy"]
    temp.update(tweet)
    user_result = tweet["core"]["user_results"]["result"]
    # add user data back
    from .user import conv_user_result
    temp.update({
        "user": conv_user_result(user_result),
    })
    if "counts" in tweet:
        # bookmark_count, favorite_count, reply_count, retweet_count, quote_count
        temp.update(tweet["counts"]) 
    if "details" in tweet:
        # conversation_control, created_at_ms, display_text_range, self_thread_metadata, full_text, hashtag_entities, cashtag_entities, smarttags
        temp.update(tweet["details"])
    if "card" in tweet and tweet["card"] is not None:
        temp.update({
            "card": tweet["card"]["legacy"],
        })
    if "quoted_status_result" in tweet:
        # force add quoted tweet
        temp.update({
            "quoted_status_result": conv_tweet_graphql(tweet["quoted_status_result"]["result"]),
        })
    if "id_str" not in temp:
        if "rest_id" in temp:
            temp["id_str"] = temp["rest_id"]
    return temp

def discord_embeds_from_tweet(tweet, show_stat=True):
    if "errors" in tweet:
        return None, "\n".join(["{} (Code: {})".format(err["message"], err["code"]) for err in tweet["errors"]])
    if "tombstone" in tweet:
        if "text" in tweet["tombstone"]:
            temp = tweet["tombstone"]["text"]["text"]
            try:
                for entity in sorted(
                    tweet["tombstone"]["text"]["entities"],
                    key = lambda e: (e['from_index'], e['to_index']),
                    reverse = True
                ):
                    if entity["ref"]["__typename"] == "TimelineUrl":
                        from_index, to_index = entity["from_index"], entity["to_index"]
                        before_text = temp[:from_index]
                        between_text = temp[from_index:to_index]
                        after_text = temp[to_index:] 
                        between_url = entity["ref"]["url"]
                        temp = before_text + f"[{between_text}](<{between_url}>)" + after_text
            except:
                pass
            return None, temp
        return None, "The tweet cannot be displayed."
    from datetime import datetime
    import discord
    embed_list: List[discord.Embed] = []
    embed = discord.Embed(color=0x1da0f2)
    tweet_url = f'https://twitter.com/{tweet["user"]["screen_name"]}/status/{tweet["id_str"]}'
    embed.set_author(name=f'{tweet["user"]["name"]} (@{tweet["user"]["screen_name"]})', icon_url=tweet["user"]["profile_image_url_https"], url=tweet_url)
    embed.description = tweet.get("full_text", tweet.get("text"))[slice(*tweet['display_text_range'])]
    if "quoted_status_result" in tweet:
        append_tweet = tweet["quoted_status_result"]
        append_description = append_tweet.get("full_text", append_tweet.get("text"))[slice(*append_tweet['display_text_range'])]
        append_url = f'https://twitter.com/{append_tweet["user"]["screen_name"]}/status/{append_tweet["id_str"]}'
        append_name = f'{append_tweet["user"]["name"]} ([@{append_tweet["user"]["screen_name"]}]({append_url}))'
        lines = append_description.split("\n")
        embed.description += "\n" + f"\n> **{append_name}**\n> \n" + "\n".join(["> " + line for line in lines])
    if show_stat:
        embed.add_field(name="Likes", value=tweet["favorite_count"], inline=True)
        embed.add_field(name="Retweets", value=tweet.get("retweet_count", "Unavailable"), inline=True)
    # embed.set_footer(text="Twitter", icon_url="https://abs.twimg.com/favicons/twitter.2.ico")
    embed.set_footer(text="Twitter", icon_url="https://abs.twimg.com/icons/apple-touch-icon-192x192.png")
    if "created_at_ms" in tweet:
        embed.timestamp = datetime.fromtimestamp(tweet["created_at_ms"] // 1000)
    elif " " in tweet["created_at"]:
        embed.timestamp = datetime.strptime(tweet["created_at"], "%a %b %d %H:%M:%S %z %Y")
    else:
        # expected to be ISO format (e.g. from syndication API)
        # Python cannot understand Z pre version 3.11
        embed.timestamp = datetime.fromisoformat(tweet["created_at"].replace('Z', '+00:00'))
    embed.url = tweet_url

    media_urls = []
    contents = []

    seen_entities = set()
    extended_entities = []
    if "entities" in tweet:
        extended_entities.append(tweet["entities"])
    if "extended_entities" in tweet:
        extended_entities.append(tweet["extended_entities"])
    if "media_entities2" in tweet:
        extended_entities.append({
            "media": tweet["media_entities2"]
        })
    if "quoted_status_result" in tweet:
        append_tweet = tweet["quoted_status_result"]
        if "extended_entities" in append_tweet:
            extended_entities.append(append_tweet["extended_entities"])
    for extended_entity in extended_entities:
        for media in extended_entity["media"]:
            if "id_str" not in media:
                continue
            if media["id_str"] in seen_entities:
                continue
            seen_entities.add(media["id_str"])
            if media["type"] in ["photo"]:
                url = media["media_url_https"] + ":orig"
                media_urls.append(url)
            elif media["type"] in ["video", "animated_gif"]:
                url = None
                max_bitrate = -1
                for v in media["video_info"]["variants"]:
                    if v["content_type"] == "video/mp4":
                        bitrate = v.get("bitrate", 0)
                        if bitrate > max_bitrate:
                            url, max_bitrate = v["url"], bitrate
                contents.append(url)
    if "video" in tweet:
        url = None
        max_resolution = -1
        for v in tweet["video"]["variants"]:
            if v["type"] == "video/mp4":
                src = v["src"]
                parts = src.split("/")
                resolution = next(
                    (
                        int(part.split("x")[0]) * int(part.split("x")[1])
                        for part in parts
                        if part.count('x') == 1 and all(c in '0123456789x' for c in part)
                    ), 0
                )
                if resolution > max_resolution:
                    url, max_resolution = src, resolution
        contents.append(url)
    if len(media_urls) == 0:
        embed_list.append(embed)
    else:
        media_embeds: List[discord.Embed] = []
        is_first = True
        for url in media_urls:
            if is_first:
                real_embed = embed
                is_first = False
            else:
                real_embed = discord.Embed(color=embed.color)
            real_embed.url = embed.url
            real_embed.set_image(url=url)
            media_embeds.append(real_embed)
        embed_list.extend(media_embeds)
    if "card" in tweet:
        card = tweet["card"]
        if card is not None and card["name"] == "unified_card":
            import json
            if isinstance(card["binding_values"], dict):
                # e.g. from syndication
                binding_values = card["binding_values"]
            else:
                binding_values = {
                    entry["key"]: entry["value"]
                for entry in card["binding_values"]}
            card_embed = discord.Embed(color=0x1da0f2)
            embed_url = binding_values["card_url"]["string_value"]
            card_embed.url = embed_url
            content = json.loads(binding_values["unified_card"]["string_value"])
            component = content["component_objects"]["details_1"]
            card_media_urls = []
            if component["type"] == "grok_share":
                component_data = component["data"]
                profile_user = component_data["profile_user"]
                card_embed.set_author(name="{} (@{})".format(profile_user["name"], profile_user["screen_name"]), icon_url=profile_user["profile_image_url_https"], url=embed_url)
                component_lines = []
                for entry in component_data["conversation_preview"]:
                    if entry["sender"] == "USER":
                        component_lines.append(entry["message"])
                    elif entry["sender"] == "AGENT":
                        component_lines.append("> " + entry["message"])
                    else:
                        component_lines.append("? " + entry["message"])
                    card_media_urls.extend(entry.get("mediaUrls", []))
                card_embed.description = "\n".join(component_lines)
            card_embed_list: List[discord.Embed] = []
            if len(card_media_urls) == 0:
                card_embed_list.append(card_embed)
            else:
                is_first = True
                for url in card_media_urls:
                    if is_first:
                        real_card_embed = card_embed
                        is_first = False
                    else:
                        real_card_embed = discord.Embed(color=card_embed.color)
                    real_card_embed.url = card_embed.url
                    real_card_embed.set_image(url=url)
                    card_embed_list.append(real_card_embed)
            embed_list.extend(card_embed_list)
    return embed_list, "\n".join(contents)