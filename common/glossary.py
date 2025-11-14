import discord

# This module is used for building localized outputs to interactions

from locale_str import locale_str_ex as _

class GrammarGlossary:
    connector = _("{0} {1}", ja="{0}{1}", zh="{0}{1}", th="{0}{1}")
    colon = _(": ", ja="：", zh="：")
    comma = _(", ", ja="、", zh="，")
    tilde = _(" ~ ", ja="〜", zh="〜")
    bracket = _(" ({})", ja="（{}）", zh="（{}）")

class GameNameGlossary:
    """
    Used for game name in outputs
    For command group name, check command_text.gamename
    """
    CG = _("Mobamas", zh="cg走路工", ja="モバマス")
    CGSS = _("CGSS", ja="デレステ")
    MLTD = _("MLTD", ja="ミリシタ")
    GKMS = _("GKMS", zh_TW="學園偶大", zh_CN="学园偶大", ja="学マス")
    IPR = _("IPR", zh_TW="偶像榮耀", zh_CN="偶像荣耀", ja="アイプラ")
    LLLL = _("LLLL", ja="リンクラ")
    PJSK = _("PJSK", ja="プロセカ", ko="프로세카")
    RST = _("RST", ja="リステップ")
    SC = _("SC", zh_TW="閃耀色彩", zh_CN="闪耀色彩", ja="シャニマス")
    SFP = _("SFP", ja="シャニソン")
    WDS = _("WDS", ja="ユメステ")

class GameColor:
    CG = 0x848ac4
    CGSS = 0x848ac4
    MLTD = 0xffc20b
    GKMS = 0xf39800
    LLLL = 0xfce8e6
    PJSK = 0x39c5bb
    RST = 0xee2288
    SC = 0x8adfff
    SFP = 0x8adfff
    WDS = 0xee5f5f
    IPR = 0x1428ff

# categorized glossary lists

class BasicGlossary:
    hidden = _("Hidden", ja="非表示", zh_TW="隱藏", zh_CN="隐藏")
    titles = _("Title(s)", ja="称号", zh_TW="稱號", zh_CN="称号")
    none = _("None", ja="なし", zh_TW="無", zh_CN="无")
    label = _("Label", ja="ラベル", zh_TW="標籤", zh_CN="标签")
    stated = _("Stated", ja="記載", zh_TW="標示", zh_CN="标示")
    actual = _("Actual", ja="実際", zh_TW="實際", zh_CN="实际")
    guessed = _("Guessed", ja="推測", zh_TW="猜測", zh_CN="猜测")

class CardGlossary:
    ability = _("Ability", ja="アビリティ", zh="能力")
    abilities = _("Abilit(y/ies)", ja="アビリティ", zh="能力")
    """allow plural"""
    accessory_search = _("Accessory Search", ja="アクセサリー検索", zh_TW="飾品搜尋", zh_CN="饰品搜索")
    """used as embed title"""
    additional_ability = _("Additional Ability", ja="追加アビリティ", zh="追加能力")
    appearing_actors = _("Appearing Actors", ja="登場アクター", zh_TW="登場演員", zh_CN="登场演员")
    available_from = _("Available From", ja="登場日時", zh_TW="登場日期", zh_CN="登场日期")
    card_search = _("Card Search", ja="カード検索", zh_TW="卡片搜尋", zh_CN="卡片搜索")
    """used as embed title"""
    leader_abilities = _("Leader Abilit(y/ies)", ja="リーダーアビリティ", zh_TW="隊長能力", zh_CN="队长能力")
    main_acquisition_method = _("Main Acquisition Method", ja="主な獲得条件", zh="主要取得方式")
    poster_search = _("Poster Search", ja="ポスター検索", zh_TW="海報搜尋", zh_CN="海报搜索")
    """used as embed title"""
    pronunciation = _("Pronunciation", ja="読み方", zh_TW="讀法", zh_CN="读法")
    """check also SongGlossary.pronunciation"""
    rarity = _("Rarity", ja="レア度", zh="稀有度")
    unlock_at_level = _("(🔒 Unlock at Lv. {})\n", ja="（🔒 レベル{}で解放）\n", zh_TW="（🔒 於 Lv. {} 解鎖）\n", zh_CN="（🔒 于 Lv. {} 解锁）\n")
    using_items_to_unlock_levels = _("Using Items to Unlock Levels", ja="アイテムを使用して上限解放", zh="使用物品解放上限")

class CharacterGlossary:
    age = _("Age", ja="年齢", zh_TW="年齡", zh_CN="年龄")
    birthplace = _("Birthplace", ja="出身地", zh="出生地") # Notice the meaning between 出生地 (place of birth) vs 出身地 (hometown) in Japanese
    blood_type = _("Blood Type", ja="血液型", zh="血型")
    dislikes = _("Dislikes", ja="苦手", zh_TW="不擅長、害怕", zh_CN="不擅长、害怕", ko="싫어하는 것")
    dominant_hand = _("Dominant Hand", ja="利き手", zh_TW="慣用手", zh_CN="惯用手") # aka. Handedness
    dob = _("DOB", ja="誕生日", zh="生日", ko="생일")
    favorite_food = _("Favorite Food", en_GB = "Favourite Food", ja="好きな食べ物", zh_TW="喜歡的食物", zh="喜欢的食物", ko="좋아하는 음식")
    height = _("Height", ja="身長", zh="身高", ko="키")
    hobbies = _("Hobbies", ja="趣味", zh_TW="興趣", zh_CN="兴趣", ko="취미")
    introduction = _("Introduction", ja="紹介", zh_TW="介紹", zh_CN="介绍", ko="소개")
    least_favorite_food = _("Least Favorite Food", en_GB = "Least Favourite Food", ja="嫌いな食べ物", zh_TW="討厭的食物", zh_CN="讨厌的食物", ko="싫어하는 음식")
    profiles = _("Profiles", ja = "プロフィール", zh_TW = "角色個人資料", zh_CN = "角色个人资料", ko = "캐릭터 프로필")
    pronunciation = _("Pronunciation", ja="読み方", zh_TW="讀法", zh_CN="读法")
    school = _("School", ja="学校", zh_TW="學校", zh_CN="学校", ko="학교")
    school_year = _("School Year", ja="学年", zh_TW="年級", zh_CN="年级", ko="학년")
    speciality = _("Speciality", ja="特技", zh="特技", ko="특기")
    unit = _("Unit", ja = "ユニット")
    va = _("VA", ja="CV", zh="CV", ko="CV")
    weight = _("Weight", ja="体重", zh_TW="體重", zh_CN="体重", ko="체중")
    zodiac_sign = _("Zodiac Sign", ja="星座", zh="星座")

class EventGlossary:
    aggregate_period = _("Aggregate Period", ja="集計期間", zh_TW="結算時間", zh_CN="结算时间")
    bonus_actors = _("Bonus Actors", ja="対象アクター", zh_TW="對象演員", zh_CN="对象演员")
    """a variant of bonus_members"""
    bonus_category = _("Bonus Category", ja="対象カテゴリ", zh_TW="對象分類", zh_CN="对象分类")
    """bonus type, but used the term 属性 instead"""
    bonus_posters = _("Bonus Posters", ja="対象ポスター", zh_TW="對象海報", zh_CN="对象海报")
    
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
    player_search = _("Player Search", ja="プレーヤー検索", zh_TW="玩家搜尋", zh_CN="玩家搜索")
    rank = _("Rank", ja="ランク", zh_TW="等級", zh_CN="等级")
    rate = _("Rate", ja="レート", zh_TW="Rate", zh_CN="Rate")

class CircleGlossary:
    circle_comment = _("Circle Comment", ja="サークル説明", zh_TW="社團說明", zh_CN="社团说明")
    circle_info = _("Circle Info", ja="サークル情報", zh_TW="社團情報", zh_CN="社团情报")
    circle_search = _("Circle Search", ja="サークル検索", zh_TW="社團搜尋", zh_CN="社团搜索")

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
    artist = _("Artist", ja="アーティスト", zh="演出者")
    """アーティスト\n\nrefer to the artist(s) featured in the song"""

    arrangement = _("Arrangement", ja="編曲", zh_TW="編曲", zh_CN="编曲", ko="편곡")
    """編曲\n\nrefer to the arranger(s) of the song"""

    base_consumption = _("Base Consumption", ja="ベース消費", zh_TW="基礎消耗", zh_CN="基础消耗")

    category = _("Categor(y/ies)", ja="カテゴリ", zh_TW="類別", zh_CN="类别")
    
    chart = _("Chart", ja="譜面", zh_TW="譜面", zh_CN="谱面")
    """譜面\n\nused as embed field text"""
    
    chart_search = _("Chart Search", ja="譜面検索", zh_TW="譜面搜尋", zh_CN="谱面搜索")
    """譜面検索\n\nused as embed title"""

    cover_song = _("Cover Song", ja="カバー曲", zh="翻唱歌曲")
    """use ○ / × as the value"""

    duration = _("Duration", ja="長さ", zh_TW="長度", zh_CN="长度")
    """長さ\n\nrefer to the duration of the music file"""

    difficulty = _("Difficulty", ja="難易度", zh_TW="難度", zh_CN="难度")
    """難易度\n\nrefer to the difficulty name of the chart"""

    difficulties = _("Difficulties", ja="難易度", zh_TW="難度", zh_CN="难度")
    """難易度\n\nrefer to the difficulty list of the song"""

    duration_song = _("Duration (Song)", ja="長さ（楽曲）", zh_TW="長度（歌曲）", zh_CN="长度（歌曲）")
    """長さ（楽曲）\n\nrefer to the duration of the music file, shown in song difficulty"""

    duration_last_note = _("Duration (Last Note)", ja="長さ（最後のノート）", zh_TW="長度（最後的 Note）", zh_CN="长度（最后的 Note）")
    """長さ（最後のノート）\n\nrefer to the time of the last note of the chart, shown in song difficulty"""

    efficiency_coef = _("Efficiency Coef.", ja="効率係数", zh="效率係數", zh_CN="效率系数")

    efficient_songs = _("Efficient Songs", ja="効率曲", zh="效率曲")

    event_p_coef = _("Event P Coef.", ja="イベントP係数", zh_TW="活動P係數", zh_CN="活动P系数")

    live = _("Live", ja="ライブ", zh="公演")
    """ライブ\n\nNaming of a specific entry with charts of different difficulties"""

    lyrics = _("Lyrics", ja="作詞", zh_TW="作詞", zh_CN="作词", ko="작사")
    """作詞\n\nrefer to the lyricist(s) of the song"""

    menu_time = _("Menu Time", ja="曲間の時間", zh_TW="過場時間", zh_CN="过场时间")

    music = _("Music", ja="作曲", zh="作曲", ko="작곡")
    """作曲\n\nrefer to the composer(s) of the song"""

    note_count = _("Note Count", ja="ノーツ数", zh_TW="Note 數", zh_CN="Note 数")
    """ノーツ数"""

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

    song_level = _("Song Lv.", ja="楽曲 Lv.", zh="歌曲 Lv.")
    """楽曲 Lv.\n\nrefer to the difficulty level of the chart"""

    song_name = _("Song Name", ja="曲名", zh="歌名")
    """曲名\n\nrefer to the song name"""

    stated_duration = _("Stated Duration", ja="記載の長さ", zh_TW="標示長度", zh_CN="标示长度")
    """記載の長さ\n\nused when the data source provides some rounded value for the duration"""

    target_score = _("Target Score", ja="目標スコア", zh_TW="目標分數", zh_CN="目标分数") 

    reward_multiplier = _("Reward Multiplier", ja="報酬倍率", zh_TW="報酬倍率", zh_CN="报酬倍率")

    unit = _("Unit", ja="ユニット", zh_TW="團體", zh_CN="团体")

    versions = _("Version(s)", ja="バージョン", zh="版本")
    """
    Refer to different soundtracks of the same song
    """

# game-specific glossary

class WDSGlossary:
    recent_clears = _("Recent Clears", ja="直近クリア編成", zh_TW="最近通關編成", zh_CN="最近通关编成")
    sense_activation_timing = _("Sense Activation Timing", ja="センス発動タイミング", zh_TW="Sense 發動時間", zh_CN="Sense 发动时间")
    star_rank = _("Star Rank", ja="スターランク", zh_TW="Star Rank", zh_CN="Star Rank")
    status_bonus = _("Status Bonus: ", ja="演技力ボーナス：", zh="演技力加成：")
    theater_league = _("Theater League", ja="演劇リーグ", zh_TW="演劇聯賽", zh_CN="演剧联赛")

class RSTGlossary:
    maker = _("Chart Maker", ja="譜面メーカー", zh_TW="譜面製作器", zh_CN="谱面制作器")

class SFPGlossary:
    focus_camera = _("Focus Mode", ja="フォーカスモード")
    song_parts = _("歌い分け", ja="歌い分け")