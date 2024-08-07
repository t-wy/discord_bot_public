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

class GameNameGlossary:
    PJSK = _("プロセカ", en="PJSK", zh="PJSK")
    WDS = _("ユメステ", en="WDS", zh="WDS")

# categorized glossary lists

class BasicGlossary:
    hidden = _("非表示", en="Hidden", zh="隱藏")
    titles = _("称号", en="Title(s)", zh="稱號")
    none = _("なし", en="None", zh="無")

class CardGlossary:
    ability = _("アビリティ", en="Ability", zh="能力")
    abilities = _("アビリティ", en="Abilit(y/ies)", zh="能力") # allow plural
    accessory_search = _("アクセサリー検索", en="Accessory Search", zh="飾品搜尋") # used as embed title
    additional_ability = _("追加アビリティ", en="Additional Ability", zh="追加能力")
    appearing_actors = _("登場アクター", en="Appearing Actors", zh="登場演員")
    available_from = _("登場日時", en="Available From", zh="登場日期")
    card_search = _("カード検索", en="Card Search", zh="卡片搜尋") # used as embed title
    leader_abilities = _("リーダーアビリティ", en="Leader Abilit(y/ies)", zh="隊長能力")
    main_acquisition_method = _("主な獲得条件", en="Main Acquisition Method", zh="主要取得方式")
    poster_search = _("ポスター検索", en="Poster Search", zh="海報搜尋") # used as embed title
    pronunciation = _("読み方", en="Pronunciation", zh="讀法") # check also SongGlossary.pronunciation
    rarity = _("レア度", en="Rarity", zh="稀有度")
    unlock_at_level = _("（🔒 レベル{}で解放）\n", en="(🔒 Unlock at Lv. {})\n", zh="（🔒 於 Lv. {} 解鎖）\n")
    using_items_to_unlock_levels = _("アイテムを使用して上限解放", en="Using Items to Unlock Levels", zh="使用物品解放上限")

class EventGlossary:
    aggregate_period = _("集計期間", en="Aggregate Period", zh="結算時間")
    bonus_actors = _("対象アクター", en="Bonus Actors", zh="對象演員") # a variant of bonus_members
    bonus_category = _("対象カテゴリ", en="Bonus Category", zh="對象分類") # bonus type, but used the term 属性 instead
    bonus_type = _("タイプボーナス", en="Bonus Type", zh="Bonus 類型", ko="타입 보너스")
    bonus_type_element = _("対象属性", en="Bonus Type", zh="對象屬性") # bonus type, but used the term 属性 instead
    bonus_members = _("キャラクターボーナス", en="Bonus Members", zh="Bonus 角色", ko="캐릭터 보너스") # actually referring to the character
    character_bonus = _("メンバーボーナス", en="Character Bonus", zh="Bonus 成員", ko="보너스 멤버") # actually referring to a card instance
    distribution_of_ranking_rewards = _("報酬配布期間", en="Distribution of Ranking Rewards", zh="報酬發送時間", ko="보상 지급 기간")
    elapsed_time = _("経過時間", en="Elapsed Time", zh="經過時間")
    event_duration = _("イベント期間", en="Event Duration", zh="活動時數")
    event_period = _("開催期間", en="Event Period", zh="活動時間", ko="개최 기간")
    event_results = _("結果発表", en="Event Results", zh="結果發表", ko="결과 발표")
    new_event_characters = _("イベントで登場する新メンバー", en="New Event Characters", zh="活動登場新成員", ko="이벤트에서 등장하는 신규 멤버")
    notice_period = _("予告期間", en="Notice Period", zh="預告時間")
    remaining_time = _("残り時間", en="Remaining Time", zh="剩餘時間")
    second_half = _("後半戦", en="Second Half", zh="後半戰")
    type = _("タイプ", en="Type", zh="類型")

class PlayerGlossary:
    basic_info = _("基本情報", en="Basic Info")
    comment = _("コメント", en="Comment", zh="留言")
    last_login = _("最終ログイン", en="Last Login", zh="最近登入")
    player_search = _("プレーヤー検索", en="Player Search", zh="玩家搜尋")
    rank = _("ランク", en="Rank", zh="等級")
    rate = _("レート", en="Rate", zh="Rate")

class CircleGlossary:
    circle_comment = _("サークル説明", en="Circle Comment", zh="社團說明")
    circle_info = _("サークル情報", en="Circle Info")
    circle_search = _("サークル検索", en="Circle Search", zh="社團搜尋")

class RankingGlossary:
    unit_details = _("編成詳細", en="Unit Details", zh="詳細編成")
    unit_info = _("編成確認", en="Unit Info", zh="編成確認")

class ReleaseGlossary:
    recently_released = _("公開済み", en="Recently released", zh="已公開")
    release_time = _("追加日時", en="Release Time", zh="追加時間")
    to_be_released = _("公開予定", en="To be released", zh="即將公開")

class SongGlossary:
    arrangement = _("編曲", en="Arrangement", zh="編曲") # refer to the arranger(s) of the song
    base_consumption = _("ベース消費", en="Base Consumption", zh="基礎消耗")
    cover_song = _("カバー楽曲", en="Cover Song", zh="翻唱歌曲") # use 〇 / ○ / × as the value
    duration = _("長さ", en="Duration", zh="長度") # refer to the duration of the music file
    efficient_songs = _("効率曲", en="Efficient Songs", zh="效率曲")
    menu_time = _("曲間の時間", en="Menu Time", zh="過場時間")
    lyrics = _("作詞", en="Lyrics", zh="作詞") # refer to the lyricist(s) of the song
    music = _("作曲", en="Music", zh="作曲") # refer to the composer(s) of the song
    pronunciation = _("読み方", en="Pronunciation", zh="讀法") # check also CardGlossary.pronunciation
    recent_song_list = _("最近楽曲リスト", en="Recent Song List", zh="最近歌曲列表")
    recent_vocal_list = _("最近ボーカルリスト", en="Recent Vocal List", zh="最近 Vocal 列表")
    seconds = _("秒", en="s")
    song_duration = _("楽曲の長さ", en="Song Duration", zh="歌曲長度") # use this as column label, use "duration" instead as field
    song_info = _("楽曲情報", en="Song Information", zh="歌曲資訊"
    )
    stated_duration = _("記載の長さ", en="Stated Duration", zh="標示長度") # if the data provide some rounded value for the duration

# game-specific glossary

class WDSGlossary:
    recent_clears = _("直近クリア編成", en="Recent Clears", zh="最近通關編成")
    sense_activation_timing = _("センス発動タイミング", en="Sense Activation Timing", zh="Sense 發動時間")
    star_rank = _("スターランク", en="Star Rank", zh="Star Rank")
    status_bonus = _("演技力ボーナス：", en="Status Bonus: ", zh="演技力加成：")
    theater_league = _("演劇リーグ", en="Theater League", zh="演劇聯賽")