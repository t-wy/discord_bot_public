import discord

# This module is used for building localized outputs to interactions

from locale_str import locale_str_ex as _

class GrammarGlossary:
    connector = _("{0} {1}", ja="{0}{1}")

class GameNameGlossary:
    CGSS = _("CGSS", ja="デレステ")
    MLTD = _("MLTD", ja="ミリシタ")
    PJSK = _("PJSK", ja="プロセカ")
    RST = _("RST", ja="リステップ")
    SC = _("SC", ja="シャニマス")
    SFP = _("SFP", ja="シャニソン")
    WDS = _("WDS", ja="ユメステ")

# categorized glossary lists

class BasicGlossary:
    hidden = _("Hidden", ja="非表示", zh_TW="隱藏", zh_CN="隐藏")
    titles = _("Title(s)", ja="称号", zh_TW="稱號", zh_CN="称号")
    none = _("None", ja="なし", zh_TW="無", zh_CN="无")

class CardGlossary:
    ability = _("Ability", ja="アビリティ", zh="能力")
    abilities = _("Abilit(y/ies)", ja="アビリティ", zh="能力")
    """allow plural"""
    accessory_search = _("Accessory Search", ja="アクセサリー検索", zh_TW="飾品搜尋", zh_CN="饰品搜寻")
    """used as embed title"""
    additional_ability = _("Additional Ability", ja="追加アビリティ", zh="追加能力")
    appearing_actors = _("Appearing Actors", ja="登場アクター", zh_TW="登場演員", zh_CN="登场演员")
    available_from = _("Available From", ja="登場日時", zh_TW="登場日期", zh_CN="登场日期")
    card_search = _("Card Search", ja="カード検索", zh_TW="卡片搜尋", zh_CN="卡片搜寻")
    """used as embed title"""
    leader_abilities = _("Leader Abilit(y/ies)", ja="リーダーアビリティ", zh_TW="隊長能力", zh_CN="队长能力")
    main_acquisition_method = _("Main Acquisition Method", ja="主な獲得条件", zh="主要取得方式")
    poster_search = _("Poster Search", ja="ポスター検索", zh_TW="海報搜尋", zh_CN="海报搜寻")
    """used as embed title"""
    pronunciation = _("Pronunciation", ja="読み方", zh_TW="讀法", zh_CN="读法")
    """check also SongGlossary.pronunciation"""
    rarity = _("Rarity", ja="レア度", zh="稀有度")
    unlock_at_level = _("(🔒 Unlock at Lv. {})\n", ja="（🔒 レベル{}で解放）\n", zh_TW="（🔒 於 Lv. {} 解鎖）\n", zh_CN="（🔒 于 Lv. {} 解锁）\n")
    using_items_to_unlock_levels = _("Using Items to Unlock Levels", ja="アイテムを使用して上限解放", zh="使用物品解放上限")

class EventGlossary:
    aggregate_period = _("Aggregate Period", ja="集計期間", zh_TW="結算時間", zh_CN="结算时间")
    bonus_actors = _("Bonus Actors", ja="対象アクター", zh_TW="對象演員", zh_CN="对象演员")
    """a variant of bonus_members"""
    bonus_category = _("Bonus Category", ja="対象カテゴリ", zh_TW="對象分類", zh_CN="对象分类")
    """bonus type, but used the term 属性 instead"""
    bonus_type = _("Bonus Type", ja="タイプボーナス", zh_TW="Bonus 類型", zh_CN="Bonus 类型", ko="타입 보너스")
    bonus_type_element = _("Bonus Type", ja="対象属性", zh_TW="對象屬性", zh_CN="对象属性")
    """bonus type, but used the term 属性 instead"""
    bonus_members = _("Bonus Members", ja="キャラクターボーナス", zh="Bonus 角色", ko="캐릭터 보너스")
    """actually referring to the character"""
    character_bonus = _("Character Bonus", ja="メンバーボーナス", zh_TW="Bonus 成員", zh_CN="Bonus 成员", ko="보너스 멤버")
    """actually referring to a card instance"""
    distribution_of_ranking_rewards = _("Distribution of Ranking Rewards", ja="報酬配布期間", zh_TW="報酬發送時間", zh_CN="报酬发送时间", ko="보상 지급 기간")
    elapsed_time = _("Elapsed Time", ja="経過時間", zh_TW="經過時間", zh_CN="经过时间")
    event_duration = _("Event Duration", ja="イベント期間", zh_TW="活動時數", zh_CN="活动时数")
    event_period = _("Event Period", ja="開催期間", zh_TW="舉辦時間", zh_CN="举办时间", ko="개최 기간")
    event_results = _("Event Results", ja="結果発表", zh_TW="結果發表", zh_CN="结果发表", ko="결과 발표")
    new_event_characters = _("New Event Characters", ja="イベントで登場する新メンバー", zh_TW="活動登場新成員", zh_CN="活动登场新成员", ko="이벤트에서 등장하는 신규 멤버")
    notice_period = _("Notice Period", ja="予告期間", zh_TW="預告時間", zh_CN="预告时间")
    remaining_time = _("Remaining Time", ja="残り時間", zh_TW="剩餘時間", zh_CN="剩余时间")
    second_half = _("Second Half", ja="後半戦", zh_TW="後半戰", zh_CN="后半战")
    type = _("Type", ja="タイプ", zh_TW="類型", zh_CN="类型")

class PlayerGlossary:
    basic_info = _("Basic Info", ja="基本情報", zh_CN="基本情报")
    comment = _("Comment", ja="コメント", zh="留言")
    last_login = _("Last Login", ja="最終ログイン", zh="最近登入")
    player_search = _("Player Search", ja="プレーヤー検索", zh_TW="玩家搜尋", zh_CN="玩家搜寻")
    rank = _("Rank", ja="ランク", zh_TW="等級", zh_CN="等级")
    rate = _("Rate", ja="レート", zh_TW="Rate", zh_CN="Rate")

class CircleGlossary:
    circle_comment = _("Circle Comment", ja="サークル説明", zh_TW="社團說明", zh_CN="社团说明")
    circle_info = _("Circle Info", ja="サークル情報", zh_TW="社團情報", zh_CN="社团情报")
    circle_search = _("Circle Search", ja="サークル検索", zh_TW="社團搜尋", zh_CN="社团搜寻")

class RankingGlossary:
    unit_details = _("Unit Details", ja="編成詳細", zh_TW="詳細編成", zh_CN="详细编成")
    unit_info = _("Unit Info", ja="編成確認", zh_TW="編成確認", zh_CN="编成确认")

class ReleaseGlossary:
    recently_released = _("Recently released", ja="公開済み", zh_TW="已公開", zh_CN="已公开")
    "公開済み"
    release_time = _("Release Time", ja="実装日時", zh_TW="實裝時間", zh_CN="实装时间")
    "実装日時"
    to_be_released = _("To be released", ja="公開予定", zh_TW="即將公開", zh_CN="即将公开")
    "公開予定"
    posting_time = _("Posting Time", ja="投稿日時", zh_TW="投稿時間", zh_CN="投稿时间")
    "投稿日時"

class SongGlossary:
    arrangement = _("Arrangement", ja="編曲", zh_TW="編曲", zh_CN="编曲", ko="편곡")
    """編曲\n\nrefer to the arranger(s) of the song"""

    base_consumption = _("Base Consumption", ja="ベース消費", zh_TW="基礎消耗", zh_CN="基础消耗")

    cover_song = _("Cover Song", ja="カバー楽曲", zh="翻唱歌曲")
    """use 〇 / ○ / × as the value"""

    duration = _("Duration", ja="長さ", zh_TW="長度", zh_CN="长度")
    """長さ\n\nrefer to the duration of the music file"""

    efficient_songs = _("Efficient Songs", ja="効率曲", zh="效率曲")
    menu_time = _("Menu Time", ja="曲間の時間", zh_TW="過場時間", zh_CN="过场时间")

    lyrics = _("Lyrics", ja="作詞", zh_TW="作詞", zh_CN="作词", ko="작사")
    """作詞\n\nrefer to the lyricist(s) of the song"""

    music = _("Music", ja="作曲", zh="作曲", ko="작곡")
    """作曲\n\nrefer to the composer(s) of the song"""

    original = _("Orig.", ja="原曲", zh="原曲", ko="원곡")
    """原曲\n\nrefer to the video URL to the song"""

    original_song = _("Original Song", ja="書き下ろし楽曲", zh="活動創作歌曲", ko="오리지널 악곡")
    """書き下ろし楽曲\n\nindicator for whether the song is original or not"""

    pronunciation = _("Pronunciation", ja="読み方", zh_TW="讀法", zh_CN="读法")
    """読み方\n\ncheck also CardGlossary.pronunciation"""

    recent_song_list = _("Recent Song List", ja="最近楽曲リスト", zh="最近歌曲列表")
    recent_vocal_list = _("Recent Vocal List", ja="最近ボーカルリスト", zh="最近 Vocal 列表")
    seconds = _("s", ja="秒")

    song_duration = _("Song Duration", ja="楽曲の長さ", zh_TW="歌曲長度", zh_CN="歌曲长度")
    """楽曲の長さ\n\nuse this as column label, use "duration" instead as field"""

    song_info = _("Song Information", ja="楽曲情報", zh_TW="歌曲資訊", zh_CN="歌曲资讯")
    """楽曲情報"""

    stated_duration = _("Stated Duration", ja="記載の長さ", zh_TW="標示長度", zh_CN="标示长度")
    """記載の長さ\n\nused when the data source provides some rounded value for the duration"""

    unit = _("Unit", ja="ユニット", zh_TW="團體", zh_CN="团体")

# game-specific glossary

class WDSGlossary:
    recent_clears = _("Recent Clears", ja="直近クリア編成", zh_TW="最近通關編成", zh_CN="最近通关编成")
    sense_activation_timing = _("Sense Activation Timing", ja="センス発動タイミング", zh_TW="Sense 發動時間", zh_CN="Sense 发动时间")
    star_rank = _("Star Rank", ja="スターランク", zh_TW="Star Rank", zh_CN="Star Rank")
    status_bonus = _("Status Bonus: ", ja="演技力ボーナス：", zh="演技力加成：")
    theater_league = _("Theater League", ja="演劇リーグ", zh_TW="演劇聯賽", zh_CN="演剧联赛")

class RSTGlossary:
    maker = _("Chart Maker", ja="譜面メーカー", zh_TW="譜面製作器", zh_CN="谱面制作器")