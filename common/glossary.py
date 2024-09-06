import discord
from typing import *
from discord_msgint import MsgInt

# This module is used for building localized outputs to interactions

def create_translator(default_locale: discord.Locale):
    def translate(default: str, /, *, fallback: str = None, **kwargs) -> Callable[[MsgInt], str]:
        """
        default: text in default locale
        fallback: match every locale except default
        """
        def call(target: MsgInt) -> str:
            if target is None:
                return default
            locales: List[discord.Locale] = [target.locale, target.guild_locale]
            for locale in locales:
                if locale is None:
                    continue
                if locale == default_locale:
                    return default
                else:
                    shortname = locale.value.split("-")[0]
                    longname = locale.value.replace("-", "_")
                    if longname in kwargs:
                        return kwargs[longname]
                    elif shortname in kwargs:
                        return kwargs[shortname]
            if fallback is not None:
                return fallback
            return default
        return call
    return translate

_ = create_translator(discord.Locale.japanese)

class GrammarGlossary:
    connector = _("{0}{1}", en="{0} {1}")

class GameNameGlossary:
    PJSK = _("プロセカ", en="PJSK", zh="PJSK")
    WDS = _("ユメステ", en="WDS", zh="WDS")

# categorized glossary lists

class BasicGlossary:
    hidden = _("非表示", en="Hidden", zh_TW="隱藏", zh_CN="隐藏")
    titles = _("称号", en="Title(s)", zh_TW="稱號", zh_CN="称号")
    none = _("なし", en="None", zh_TW="無", zh_CN="无")

class CardGlossary:
    ability = _("アビリティ", en="Ability", zh="能力")
    abilities = _("アビリティ", en="Abilit(y/ies)", zh="能力") # allow plural
    accessory_search = _("アクセサリー検索", en="Accessory Search", zh_TW="飾品搜尋", zh_CN="饰品搜寻") # used as embed title
    additional_ability = _("追加アビリティ", en="Additional Ability", zh="追加能力")
    appearing_actors = _("登場アクター", en="Appearing Actors", zh_TW="登場演員", zh_CN="登场演员")
    available_from = _("登場日時", en="Available From", zh_TW="登場日期", zh_CN="登场日期")
    card_search = _("カード検索", en="Card Search", zh_TW="卡片搜尋", zh_CN="卡片搜寻") # used as embed title
    leader_abilities = _("リーダーアビリティ", en="Leader Abilit(y/ies)", zh_TW="隊長能力", zh_CN="队长能力")
    main_acquisition_method = _("主な獲得条件", en="Main Acquisition Method", zh="主要取得方式")
    poster_search = _("ポスター検索", en="Poster Search", zh_TW="海報搜尋", zh_CN="海报搜寻") # used as embed title
    pronunciation = _("読み方", en="Pronunciation", zh_TW="讀法", zh_CN="读法") # check also SongGlossary.pronunciation
    rarity = _("レア度", en="Rarity", zh="稀有度")
    unlock_at_level = _("（🔒 レベル{}で解放）\n", en="(🔒 Unlock at Lv. {})\n", zh_TW="（🔒 於 Lv. {} 解鎖）\n", zh_CN="（🔒 于 Lv. {} 解锁）\n")
    using_items_to_unlock_levels = _("アイテムを使用して上限解放", en="Using Items to Unlock Levels", zh="使用物品解放上限")

class EventGlossary:
    aggregate_period = _("集計期間", en="Aggregate Period", zh_TW="結算時間", zh_CN="结算时间")
    bonus_actors = _("対象アクター", en="Bonus Actors", zh_TW="對象演員", zh_CN="对象演员") # a variant of bonus_members
    bonus_category = _("対象カテゴリ", en="Bonus Category", zh_TW="對象分類", zh_CN="对象分类") # bonus type, but used the term 属性 instead
    bonus_type = _("タイプボーナス", en="Bonus Type", zh_TW="Bonus 類型", zh_CN="Bonus 类型", ko="타입 보너스")
    bonus_type_element = _("対象属性", en="Bonus Type", zh_TW="對象屬性", zh_CN="对象属性") # bonus type, but used the term 属性 instead
    bonus_members = _("キャラクターボーナス", en="Bonus Members", zh="Bonus 角色", ko="캐릭터 보너스") # actually referring to the character
    character_bonus = _("メンバーボーナス", en="Character Bonus", zh_TW="Bonus 成員", zh_CN="Bonus 成员", ko="보너스 멤버") # actually referring to a card instance
    distribution_of_ranking_rewards = _("報酬配布期間", en="Distribution of Ranking Rewards", zh_TW="報酬發送時間", zh_CN="报酬发送时间", ko="보상 지급 기간")
    elapsed_time = _("経過時間", en="Elapsed Time", zh_TW="經過時間", zh_CN="经过时间")
    event_duration = _("イベント期間", en="Event Duration", zh_TW="活動時數", zh_CN="活动时数")
    event_period = _("開催期間", en="Event Period", zh_TW="活動時間", zh_CN="活动时间", ko="개최 기간")
    event_results = _("結果発表", en="Event Results", zh_TW="結果發表", zh_CN="结果发表", ko="결과 발표")
    new_event_characters = _("イベントで登場する新メンバー", en="New Event Characters", zh_TW="活動登場新成員", zh_CN="活动登场新成员", ko="이벤트에서 등장하는 신규 멤버")
    notice_period = _("予告期間", en="Notice Period", zh_TW="預告時間", zh_CN="预告时间")
    remaining_time = _("残り時間", en="Remaining Time", zh_TW="剩餘時間", zh_CN="剩余时间")
    second_half = _("後半戦", en="Second Half", zh_TW="後半戰", zh_CN="后半战")
    type = _("タイプ", en="Type", zh_TW="類型", zh_CN="类型")

class PlayerGlossary:
    basic_info = _("基本情報", en="Basic Info", zh_CN="基本情报")
    comment = _("コメント", en="Comment", zh="留言")
    last_login = _("最終ログイン", en="Last Login", zh="最近登入")
    player_search = _("プレーヤー検索", en="Player Search", zh_TW="玩家搜尋", zh_CN="玩家搜寻")
    rank = _("ランク", en="Rank", zh_TW="等級", zh_CN="等级")
    rate = _("レート", en="Rate", zh_TW="Rate", zh_CN="Rate")

class CircleGlossary:
    circle_comment = _("サークル説明", en="Circle Comment", zh_TW="社團說明", zh="社团说明")
    circle_info = _("サークル情報", en="Circle Info", zh_TW="社團情報", zh_CN="社团情报")
    circle_search = _("サークル検索", en="Circle Search", zh_TW="社團搜尋", zh_CN="社团搜寻")

class RankingGlossary:
    unit_details = _("編成詳細", en="Unit Details", zh_TW="詳細編成", zh_CN="详细编成")
    unit_info = _("編成確認", en="Unit Info", zh_TW="編成確認", zh_CN="编成确认")

class ReleaseGlossary:
    recently_released = _("公開済み", en="Recently released", zh_TW="已公開", zh_CN="已公开")
    release_time = _("実装日時", en="Release Time", zh_TW="實裝時間", zh_CN="实装时间")
    to_be_released = _("公開予定", en="To be released", zh_TW="即將公開", zh_CN="即将公开")

class SongGlossary:
    arrangement = _("編曲", en="Arrangement", zh_TW="編曲", zh_CN="编曲") # refer to the arranger(s) of the song
    base_consumption = _("ベース消費", en="Base Consumption", zh_TW="基礎消耗", zh_CN="基础消耗")
    cover_song = _("カバー楽曲", en="Cover Song", zh="翻唱歌曲") # use 〇 / ○ / × as the value
    duration = _("長さ", en="Duration", zh_TW="長度", zh_CN="长度") # refer to the duration of the music file
    efficient_songs = _("効率曲", en="Efficient Songs", zh="效率曲")
    menu_time = _("曲間の時間", en="Menu Time", zh_TW="過場時間", zh_CN="过场时间")
    lyrics = _("作詞", en="Lyrics", zh_TW="作詞", zh_CN="作词") # refer to the lyricist(s) of the song
    music = _("作曲", en="Music", zh="作曲") # refer to the composer(s) of the song
    pronunciation = _("読み方", en="Pronunciation", zh_TW="讀法", zh_CN="读法") # check also CardGlossary.pronunciation
    recent_song_list = _("最近楽曲リスト", en="Recent Song List", zh="最近歌曲列表")
    recent_vocal_list = _("最近ボーカルリスト", en="Recent Vocal List", zh="最近 Vocal 列表")
    seconds = _("秒", en="s")
    song_duration = _("楽曲の長さ", en="Song Duration", zh_TW="歌曲長度", zh_CN="歌曲长度") # use this as column label, use "duration" instead as field
    song_info = _("楽曲情報", en="Song Information", zh_TW="歌曲資訊", zh_CN="歌曲资讯"
    )
    stated_duration = _("記載の長さ", en="Stated Duration", zh_TW="標示長度", zh_CN="标示长度") # if the data provide some rounded value for the duration

# game-specific glossary

class WDSGlossary:
    recent_clears = _("直近クリア編成", en="Recent Clears", zh_TW="最近通關編成", zh_CN="最近通关编成")
    sense_activation_timing = _("センス発動タイミング", en="Sense Activation Timing", zh_TW="Sense 發動時間", zh_CN="Sense 发动时间")
    star_rank = _("スターランク", en="Star Rank", zh_TW="Star Rank", zh_CN="Star Rank")
    status_bonus = _("演技力ボーナス：", en="Status Bonus: ", zh="演技力加成：")
    theater_league = _("演劇リーグ", en="Theater League", zh_TW="演劇聯賽", zh_CN="演剧联赛")