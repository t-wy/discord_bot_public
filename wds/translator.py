from discord_msgint import MsgInt
import discord
from typing import *

# regex to select the 3rd field from an array entry:
# \[(?:[^[,]+, ){2}"([^"]+)"

def user_locales(message: MsgInt) -> str:
    if message is None:
        return ()
    candidates = []
    for locale in [message.locale, message.guild_locale]:
        if locale is None:
            continue
        if "-" in locale.value:
            candidates.append(locale.value.replace("-", "_"))
            candidates.append(locale.value.split("-")[0])
        else:
            candidates.append(locale.value)
    return tuple(candidates)

def ordinal_translator(target: str, message: Union[MsgInt, str]) -> str:
    value = int(target)
    if type(message) is str:
        locales = [message]
    else:
        locales = user_locales(message)
    for locale in locales:
        if locale == "en":
            if value % 100 in range(10, 20):
                return target + "th"
            if value % 10 == 1:
                return target + "st"
            if value % 10 == 2:
                return target + "nd"
            if value % 10 == 3:
                return target + "rd"
            return target + "th"
    return target

def regex_lookup_translator(
    target: str, message: Union[MsgInt, str],
    lookup_dict: Dict[str, Dict[str, str]],
    regex_lookup_dict: Dict[str, Dict[str, str]] = {}
) -> str:
    if type(message) is str:
        locales = [message]
    else:
        locales = user_locales(message)
    if target in lookup_dict:
        for locale in locales:
            if locale in lookup_dict[target]:
                return lookup_dict[target][locale]
        return target
    else:
        import re
        for regex in regex_lookup_dict:
            match = re.fullmatch(regex, target)
            if match:
                for locale in locales:
                    if locale in regex_lookup_dict[regex]:
                        translator = regex_lookup_dict[regex][locale]
                        temp_dict = match.groupdict()
                        if "company" in temp_dict:
                            temp_dict["company"] = company_translator(temp_dict["company"], locale)
                        if "actor" in temp_dict:
                            temp_dict["actor"] = actor_translator(temp_dict["actor"], locale)
                        if "sense_star_act" in temp_dict:
                            temp_dict["sense_star_act"] = sense_star_act_translator(temp_dict["sense_star_act"], locale)
                        if "sense_type" in temp_dict:
                            temp_dict["sense_type"] = sense_type_translator(temp_dict["sense_type"], locale)
                        if "status" in temp_dict:
                            temp_dict["status"] = status_translator(temp_dict["status"], locale)
                        if "ordinal" in temp_dict:
                            temp_dict["ordinal"] = ordinal_translator(temp_dict["ordinal"], locale)
                        return translator.format(*match.groups(), **temp_dict)
                else:
                    return target
        return target

def regex_lookup_translator_wrapper(
    lookup_dict: Dict[str, Dict[str, str]],
    regex_lookup_dict: Dict[str, Dict[str, str]] = {}
):
    def wrapper(target: str, message: Union[MsgInt, str]) -> str:
        return regex_lookup_translator(target, message, lookup_dict, regex_lookup_dict)
    return wrapper

actor_translator = regex_lookup_translator_wrapper({
    "ここな": {
        "en": "Kokona",
        "zh": "心菜",
    },
    "静香": {
        "en": "Shizuka",
        "zh": "靜香",
    },
    "カトリナ": {
        "en": "Kathrina",
        "zh": "卡特莉娜",
    },
    "八恵": {
        "en": "Yae",
        "zh": "八惠",
    },
    "ぱんだ": {
        "en": "Panda",
        "zh": "潘達",
    },
    "知冴": {
        "en": "Chisa",
    },

    "初魅": {
        "en": "Hatsumi",
    },
    "大黒": {
        "en": "Daikoku",
        "zh": "大黑",
    },
    "仁花子": {
        "en": "Nikako",
    },
    "容": {
        "en": "Iruru",
    },
    "しぐれ": {
        "en": "Shigure",
        "zh": "時雨",
    },

    "暦": {
        "en": "Koyomi",
        "zh": "曆",
    },
    "ラモーナ": {
        "en": "Ramona",
        "zh": "拉莫娜",
    },
    "雪": {
        "en": "Xue",
    },
    "リリヤ": {
        "en": "Lilja",
        "zh": "莉莉亞",
    },
    "緋花里": {
        "en": "Hikari",
    },

    "いろは": {
        "en": "Iroha",
        "zh": "伊呂波",
    },
    "美兎": {
        "en": "Mito",
        "zh": "美兔",
    },
    "カミラ": {
        "en": "Kamira",
        "zh": "卡蜜拉", # also known as "卡米拉"
    },
    "蕾": {
        "en": "Tsubomi",
    },
    "叶羽": {
        "en": "Towa",
        "zh": "葉羽",
    },
})

company_translator = regex_lookup_translator_wrapper({
    "シリウス": {
        "en": "Sirius",
        "zh": "天狼星",
    },
    "Eden": {},
    "銀河座": {
        "en": "Gingaza",
    },
    "劇団電姫": {
        "en": "Gekidan Denki",
        "zh": "劇團電姬",
    },
})

sense_type_translator = regex_lookup_translator_wrapper({
    "支援": {
        "en": "Support",
    },
    "支配": {
        "en": "Control",
    },
    "増幅": {
        "en": "Amplification",
    },
    "特殊": {
        "en": "Special",
    },
})

sense_star_act_translator = regex_lookup_translator_wrapper({
    "センス": {
        "en": "Sense",
        "zh": "Sense",
    },
    "スターアクト": {
        "en": "Star Act",
        "zh": "Star Act",
    },
})

status_translator = regex_lookup_translator_wrapper({
    "演技力": {
        "en": "Total Status",
    },
    "歌唱力": {
        "en": "Vocal Status",
    },
    "表現力": {
        "en": "Expression Status",
    },
    "集中力": {
        "en": "Concentration Status",
    },
})

trophy_description_translator = regex_lookup_translator_wrapper({
    "スコアの下３桁が「７７７」で公演をクリアしよう": {
        "en": "Clear a Live with \"777\" as the Last 3 Digits of the Score",
        "zh": "以末 3 位為「777」的分數完成公演",
    },
    "物語の舞台・浅草を巡るデジタルスタンプラリーに参加しよう": {
        "en": "Participate in Digital Rally of Visiting the Stage of the Story, Asakusa",
        "zh": "參加周遊物語的舞台——浅草的數碼集印活動",
    },
    "期間限定ミッションをクリアしよう": {
        "en": "Clear the Time-Limited Mission",
        "zh": "完成期間限定任務",
    },
}, {
    r"(?P<actor>.+)のスターランクを(\d+)以上にしよう": {
        "en": "Raise the Star Rank of {actor} to {1} or above",
        "zh": "提升 {actor} 的 Star Rank 到 {1} 或以上",
    },
    r"イベント「(.+)」で(\d+)位以内に入賞": {
        "en": "Rank among the Top {1} in the Event \"{0}\"",
        "zh": "於活動「{0}」取得前 {1} 名",
    },
    r"イベント「(.+)」で(?P<ordinal>\d+)位に入賞": {
        "en": "Rank {ordinal} in the Event \"{0}\"",
        "zh": "於活動「{0}」取得第 {ordinal} 名",
    },
    r"イベント「(.+)」で(?P<actor>.+)応援ランキングの(\d+)位以内に入賞": {
        "en": "Rank among the Top {2} of the Support Ranking of {actor} in the Event \"{0}\"",
        "zh": "於活動「{0}」取得 {actor} 應援排行榜的前 {2} 名",
    },
    r"プレイヤーランクを(\d+)以上にしよう": {
        "en": "Raise Player Rank to {0} or above",
        "zh": "提升玩家等級到 {0} 或以上",
    },
    r"サークルメンバー4人で協力公演を(\d+)回クリアしよう": {
        "en": "Clear {0} Multi-player Lives with 4 Players in the Circle",
        "zh": "Circle 4 人完成 {0} 次協力公演",
    },
    r"協力公演で4人全員(.+)を達成しよう": {
        "en": "Achieve {0} by all 4 Players in a Multi-player Live",
        "zh": "於協力公演中 4 人全都達成 {0}",
    },
    r"公演を(\d+)回クリアしよう": {
        "en": "Clear {0} Lives",
        "zh": "完成 {0} 次公演",
    },
    r"ライフ(\d+)以上で公演をクリアしよう": {
        "en": "Clear a Live with at Least {0} Life",
        "zh": "以 {0} 以上的生命值完成公演",
    },
    r"累計で(\d+)日以上ログインしよう": {
        "en": "Log in for at Least {0} Days in Total",
        "zh": "累積登入 {0} 天或以上",
    },
    r"スタミナを累計(\d+)消費しよう": {
        "en": "Consume {0} Stamina in Total",
        "zh": "累計消耗 {0} 體力",
    },
    r"ノーツを累計(\d+)回タップしよう": {
        "en": "Tap {0} Notes in Total",
        "zh": "累計點擊 {0} 次節奏圖示",
    },
    r"コインを(\d+)枚入手しよう": {
        "en": "Obtain {0} Coins",
        "zh": "取得 {0} 枚金幣",
    },
    r"スタンプを(\d+)種類入手しよう": {
        "en": "Obtain {0} Kinds of Stamps",
        "zh": "取得 {0} 款貼圖",
    },
    r"衣装を(\d+)種類入手しよう": {
        "en": "Obtain {0} Kinds of Costumes",
        "zh": "取得 {0} 款服裝",
    },
    r"アクセサリーを(\d+)種類入手しよう": {
        "en": "Obtain {0} Kinds of Accessories",
        "zh": "取得 {0} 款飾品",
    },
    r"シークレットアクセサリーを(\d+)種類入手する": {
        "en": "Obtain {0} Kinds of Secret Accessories",
        "zh": "取得 {0} 款神秘飾品",
    },
    r"ジュゴンの勲章を(\d+)個入手する": {
        "en": "Obtain {0} Dugong Medals",
        "zh": "取得 {0} 個儒艮勳章",
    },
    r"難易度(.+)で(\d+)曲(.+)を達成しよう": {
        "en": "Get {2} on {1} Songs in {0} Difficulty",
        "zh": "在 {0} 難度取得 {1} 首歌曲的 {2}",
    },
    r"(\d+)人とフレンドになろう": {
        "en": "Become Friends with {0} Players",
        "zh": "與 {0} 人成為朋友",
    },
    r"スターアクトを累計(\d+)回発動しよう": {
        "en": "Trigger {0} Star Acts in Total",
        "zh": "累計發動 {0} 次 Star Act",
    },
    r"オーディションで★★★クリアを(\d+)ステージで達成しよう": {
        "en": "Complete {0} Audition Stage(s) with ★★★ Clear",
        "zh": "在試鏡達成 {0} 階段的★★★通關",
    },
    r"(?P<actor>.+)誕生日記念パック(\d+)を購入しよう": {
        "en": "Purchase {actor} Birthday Memorial Pack {1}",
        "zh": "購買{actor}生日限定禮包{1}",
    },
    r"スポットストーリーを(\d+)種類読もう": {
        "en": "Read {0} Kinds of Spot Stories",
        "zh": "閱讀 {0} 種類場景劇情",
    },
    r"(?P<company>.+)のメインストーリー(\d+)章を全て読もう": {
        "en": "Read all of {company} Main Stories, Chapter {1}",
        "zh": "閱畢 {company} 主線劇情第 {1} 章",
    },
})

star_act_translator = regex_lookup_translator_wrapper({
    "総演技力の[:score]倍のスコアを獲得": {
        "en": "Gain a Score of [:score] Times the Total Status",
        "zh": "獲得總演技力 [:score] 倍的分數",
    }
})

single_sense_translator = regex_lookup_translator_wrapper({
    "[:score]倍のスコアを獲得": {
        "en": "Gain [:score]x Score",
        "zh": "獲得 [:score] 倍的分數",
    },
    "[:gauge]のプリンシパルゲージを獲得": {
        "en": "Gain [:gauge] Principal Gauge",
        "zh": "獲得 [:gauge] Principal Gauge",
    },
    "ライフを[:param11]回復": {
        "en": "Recover Life by [:param11]",
        "zh": "回復 [:param11] 生命值",
    },
    "ライフを[:param11]": {
        "en": "Change Life by [:param11]",
        "zh": "[:param11] 生命值",
    },
    "効果無し（所持している「光」は維持される）": {
        "en": "No Effect (Possessed \"Lights\" are Kept as is)",
        "zh": "沒有效果 (所持的「光」得以保留)",
    },
    "センス発動後、追加で[:param11]のプリンシパルゲージを獲得": {
        "en": "Gain Additional [:param11] Principal Gauge After Sense Activation",
        "zh": "Sense 發動後，追加獲得 [:param11] Principal Gauge",
    },
    "センス発動後、プリンシパルゲージの上限値が[:param11]上昇": {
        "en": "Raise the Cap of Principal Gauge by [:param11] After Sense Activation",
        "zh": "Sense 發動後，Principal Gauge 的上限提升 [:param11]",
    },
}, {
    r"(?P<actor>.+)編成時、(?P=actor)が代わりにセンスを発動し、(?P=actor)のスコア獲得量\[:pre1\]％UP": {
        "en": "When {actor} is Present, Sense will be Activated by {actor} Instead, and {actor} Gains [:pre1]% UP Score from so",
        "zh": "當{actor}在隊伍時，{actor}代為發動 Sense，且{actor}獲得的分數 [:pre1]% UP",
    },
    r"ライフが多いほど(?P<actor>.+)のスコア獲得量UP（最大＋(\d+)％）": {
        "en": "The More the Life value is, {actor} Gains More Score Gain UP from so (+{1}% at Most)",
        "zh" : "生命值愈多，{actor}的分數獲得量 UP 愈多（最多 +{1}%）",
    },
    r"ライフが少ないほど(?P<actor>.+)のスコア獲得量UP（最大＋(\d+)％）": {
        "en": "The Less the Life value is, {actor} Gains More Score Gain UP from so (+{1}% at Most)",
        "zh": "生命值愈少，{actor}的分數獲得量 UP 愈多（最多 +{1}%）",
    },
    r"\[:sec\]秒間、(?P<company>.+)のアクターに(?P<sense_star_act>センス|スターアクト)スコア\[:param11\]％UP効果": {
        "en": "For [:sec] seconds, {company} Actors Gain [:param11]% UP Score from {sense_star_act}",
        "zh": "[:sec]秒內，{company}演員附帶 {sense_star_act} 分數 [:param11]% UP 效果",
    },
    r"(?P<company>.+)のアクターのCTを(\d+)秒短縮": {
        "en": "CT of {company} Actor Reduced by {1}s for the Next Sense",
        "zh": "{company}演員的 CT 縮短 {1} 秒",
    },
    r"センス発動直後、自身の(?P<status>.+)の\[:param11\]倍のスコアを獲得": {
        "en": "Gain a Score of [:param11] Times the Actor's own {status} After Sense Activation",
        "zh": "Sense 發動後，獲得自身{status} [:param11] 倍的分數",
    },
})

def sense_translator(description: str, message: MsgInt) -> str:
    return "／".join([
        single_sense_translator(part, message)
    for part in description.split("／")])

bloom_translator = regex_lookup_translator_wrapper({}, {
    r"演技力(\d+)％UP": {
        "en": "Status {}% UP",
        "zh": "演技力 {}% UP",
    },
    r"センスのCTが(\d+)秒減少": {
        "en": "Sense CT Reduced by {}s",
        "zh": "Sense 的 CT 減少{}秒",
    },
    r"基礎スコアが(\d+)％上昇": {
        "en": "Base Score Increased by {}%",
        "zh": "基礎分數提升 {}%",
    },
    r"初期ライフが(\d+)上昇": {
        "en": "Initial Life Increased by {}",
        "zh": "起始生命值提升 {}",
    },
    r"初期プリンシパルゲージが(\d+)上昇": {
        "en": "Initial Principal Gauge Increased by {}",
        "zh": "起始 Principal Gauge 提升 {}",
    },
    r"公演での報酬量が(\d+)％上昇": {
        "en": "Live Rewards Increased by {}%",
        "zh": "公演報酬量提升 {}%",
    },
    r"スターアクト発動に必要な(?P<sense_type>.{2})の光の個数が(\d+)個減少": {
        "en": "Number of {sense_type} Lights Required to Trigger Star Act Reduced by {1}",
        "zh": "Star Act 發動所需的{sense_type}系光數量減少 {1} 個",
    },
})