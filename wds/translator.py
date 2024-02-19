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

def lookup_translator(lookup_dict: Dict[str, Dict[str, str]], target: str, message: MsgInt) -> str:
    locales = user_locales(message)
    for locale in locales:
        if locale in lookup_dict:
            if target in lookup_dict[locale]:
                return lookup_dict[locale][target]
            elif "\0" in lookup_dict[locale]:
                return target
    return target

def lookup_translator_wrapper(lookup_dict: Dict[str, Dict[str, str]]):
    def wrapper(target: str, message: MsgInt) -> str:
        return lookup_translator(lookup_dict, target, message)
    return wrapper

actor_translator = lookup_translator_wrapper({
    "en": {
        "ここな": "Kokona",
        "静香": "Shizuka",
        "カトリナ": "Kathrina",
        "八恵": "Yae",
        "ぱんだ": "Panda",
        "知冴": "Chisa",

        "初魅": "Hatsumi",
        "大黒": "Daikoku",
        "仁花子": "Nikako",
        "容": "Iruru",
        "しぐれ": "Shigure",

        "暦": "Koyomi",
        "ラモーナ": "Ramona",
        "雪": "Xue",
        "リリヤ": "Lilja",
        "緋花里": "Hikari",

        "いろは": "Iroha",
        "美兎": "Mito",
        "カミラ": "Kamira",
        "蕾": "Tsubomi",
        "叶羽": "Towa",
        "\0": "*",
    },
    "zh": {
        "ここな": "心菜",
        "静香": "靜香",
        "カトリナ": "卡特莉娜",
        "八恵": "八惠",
        "ぱんだ": "潘達",

        "初魅": "初魅",
        "大黒": "大黑",
        "容": "容",
        "しぐれ": "時雨",

        "暦": "曆",
        "ラモーナ": "拉莫娜",
        "リリヤ": "莉莉亞",

        "いろは": "伊呂波",
        "美兎": "美兔",
        "カミラ": "卡蜜拉",
        "叶羽": "葉羽",
        "\0": "*",
    },
})
"""
    "<dummy>": {
        "ここな": "ここな",
        "静香": "静香",
        "カトリナ": "カトリナ",
        "八恵": "八恵",
        "ぱんだ": "ぱんだ",
        "知冴": "知冴",

        "初魅": "初魅",
        "大黒": "大黒",
        "仁花子": "仁花子",
        "容": "容",
        "しぐれ": "しぐれ",

        "暦": "暦",
        "ラモーナ": "ラモーナ",
        "雪": "雪",
        "リリヤ": "リリヤ",
        "緋花里": "緋花里",

        "いろは": "いろは",
        "美兎": "美兎",
        "カミラ": "カミラ",
        "蕾": "蕾",
        "叶羽": "叶羽",
        "\0": "*",
    },
"""

company_translator = lookup_translator_wrapper({
    "en": {
        "シリウス": "Sirius",
        "Eden": "Eden",
        "銀河座": "Gingaza",
        "劇団電姫": "Gekidan Denki",
    },
    "zh": {
        "シリウス": "天狼星",
        "Eden": "Eden",
        "銀河座": "銀河座",
        "劇団電姫": "劇團電姬",
    },
})

sense_type_translator = lookup_translator_wrapper({
    "en": {
        "支援": "Support",
        "支配": "Control",
        "増幅": "Amplification",
        "特殊": "Special",
    },
})

sense_star_act_translator = lookup_translator_wrapper({
    "en": {
        "センス": "Sense",
        "スターアクト": "Star Act",
    },
    "zh": {
        "センス": "Sense",
        "スターアクト": "Star Act",
    },
})

def trophy_description_translator(description: str, message: MsgInt) -> str:
    import re
    locales = user_locales(message)
    for locale in locales:
        if locale == "en":
            description = re.sub(
				r"([^　]+)のスターランクを(\d+)以上にしよう",
                lambda match: "Raise the Star Rank of {} to {} or above".format(actor_translator(match.group(1), message), match.group(2)),
                description
            )
            description = re.sub(
				r"イベント「(.+)」で(\d+)位以内に入賞",
				lambda match: "Getting Top {1} in Event \"{0}\"".format(match.group(1), match.group(2)),
				description
			)
            description = re.sub(
				r"イベント「(.+)」で(\d+)位に入賞",
				lambda match: "Getting {1} place in Event \"{0}\"".format(match.group(1), match.group(2) + ["st", "nd", "rd", "th"][min(int(match.group(2)) - 1, 3)]),
				description
			)
            description = re.sub(
				r"イベント「(.+)」で(.+)応援ランキングの(\d+)位以内に入賞",
				lambda match: "Getting Top {2} of the support ranking of {1} in Event \"{0}\"".format(match.group(1), actor_translator(match.group(2), message), match.group(3)),
				description
			)
            description = re.sub(
				r"プレイヤーランクを(\d+)以上にしよう",
				r"Raise Player Rank to \1 or above",
				description
			)
            description = re.sub(
				r"サークルメンバー4人で協力公演を(\d+)回クリアしよう",
				r"Clear \1 Lives with 4 Players in the Circle",
				description
			)
            description = re.sub(
				r"公演を(\d+)回クリアしよう",
				r"Clear \1 Lives",
				description
			)
            description = re.sub(
				r"ライフ(\d+)以上で公演をクリアしよう",
				r"Clear a Live with at Least \1 Life",
				description
			)
            description = re.sub(
				r"スコアの下３桁が「７７７」で公演をクリアしよう",
				r"Clear a Live with Last 3 Digits of Score being \"777\"",
				description
			)
            description = re.sub(
				r"物語の舞台・浅草を巡るデジタルスタンプラリーに参加",
				r"Participate in Digital Rally of Visiting the Stage of the Story, Asakusa",
				description
			)
            description = re.sub(
				r"累計で(\d+)日以上ログインしよう",
				r"Log in for at Least \1 Days",
				description
			)
            description = re.sub(
				r"スタミナを累計(\d+)消費しよう",
				r"Consume \1 Stamina in Total",
				description
			)
            description = re.sub(
				r"コインを(\d+)枚入手しよう",
				r"Obtain \1 Coins",
				description
			)
            description = re.sub(
				r"ノーツを累計(\d+)回タップしよう",
				r"Tap \1 Notes in Total",
				description
			)
            description = re.sub(
				r"スタンプを(\d+)種類入手しよう\n",
				r"Obtain \1 Kinds of Stamps",
				description
			)
            description = re.sub(
				r"衣装を(\d+)種類入手しよう\n",
				r"Obtain \1 Kinds of Costumes",
				description
			)
            description = re.sub(
				r"アクセサリーを(\d+)種類入手しよう",
				r"Obtain \1 Kinds of Accessories",
				description
			)
            description = re.sub(
				r"シークレットアクセサリーを(\d+)種類入手する",
				r"Obtain \1 Kinds of Secret Accessories",
				description
			)
            description = re.sub(
				r"ジュゴンの勲章を(\d+)個入手する",
				r"Obtain \1 Dugong Medals",
				description
			)
            description = re.sub(
				r"難易度(.+)で(\d+)曲(.+)を達成しよう",
				r"Get \3 on \2 Songs in \1 Difficulty",
				description
			)
            description = re.sub(
				r"協力公演で4人全員(.+)を達成しよう",
				r"Achieve \1 by all 4 Players in Multiplayer Live",
				description
			)
            description = re.sub(
				r"(\d+)人とフレンドになろう",
				r"Become Friends with \1 Players",
				description
			)
            description = re.sub(
				r"スターアクトを累計(\d+)回発動しよう",
				r"Trigger \1 Star Acts in Total",
				description
			)
            description = re.sub(
				r"オーディションで★★★クリアを(\d+)ステージで達成しよう",
				r"Complete \1 Audition Stage(s) with ★★★ Clear",
				description
			)
            description = re.sub(
				r"期間限定ミッションをクリアしよう",
				r"Clear the Time-Limited Mission",
				description
			)
            description = re.sub(
				r"([^　]+)誕生日記念パック(\d+)を購入しよう",
                lambda match: r"Purchase {} Birthday Memorial Pack {}".format(actor_translator(match.group(1), message), match.group(2)),
				description
			)
            description = re.sub(
				r"スポットストーリーを(\d+)種類読もう",
				r"Read \1 Kinds of Spot Stories",
				description
			)
            description = re.sub(
				r"([^　]+)のメインストーリー(\d+)章を全て読もう",
				lambda match: "Read all of {} Main Stories, Chapter {}".format(company_translator(match.group(1), message), match.group(2)),
				description
			)
            return description
        elif locale == "zh":
            description = re.sub(
                r"([^　]+)のスターランクを(\d+)以上にしよう",
                lambda match: "提升 {} 的 Star Rank 到 {} 或以上".format(actor_translator(match.group(1), message), match.group(2)),
                description
            )
            description = re.sub(
				r"イベント「(.+)」で(\d+)位以内に入賞",
				lambda match: "於活動「{}」取得前 {} 名".format(match.group(1), match.group(2)),
				description
			)
            description = re.sub(
				r"イベント「(.+)」で(\d+)位に入賞",
				lambda match: "於活動「{}」取得第 {} 名".format(match.group(1), match.group(2)),
				description
			)
            description = re.sub(
				r"イベント「(.+)」で(.+)応援ランキングの(\d+)位以内に入賞",
				lambda match: "於活動「{}」取得 {} 應援排行榜的前 {} 名".format(match.group(1), actor_translator(match.group(2), message), match.group(3)),
				description
			)
            description = re.sub(
				r"プレイヤーランクを(\d+)以上にしよう",
				r"提升玩家等級到\1或以上",
				description
			)
            description = re.sub(
				r"サークルメンバー4人で協力公演を(\d+)回クリアしよう",
				r"Circle 4 人完成 \1 次公演",
				description
			)
            description = re.sub(
				r"公演を(\d+)回クリアしよう",
				r"完成 \1 次公演",
				description
			)
            description = re.sub(
				r"ライフ(\d+)以上で公演をクリアしよう",
				r"以 \1 以上的生命值完成公演",
				description
			)
            description = re.sub(
				r"スコアの下３桁が「７７７」で公演をクリアしよう",
				r"以末 3 位為「777」的分數完成公演",
				description
			)
            description = re.sub(
				r"物語の舞台・浅草を巡るデジタルスタンプラリーに参加",
				r"參加周遊物語的舞台——浅草的數碼集印活動",
				description
			)
            description = re.sub(
				r"累計で(\d+)日以上ログインしよう",
				r"累積登入 \1 天或以上",
				description
			)
            description = re.sub(
				r"スタミナを累計(\d+)消費しよう",
				r"累計消耗 \1 體力",
				description
			)
            description = re.sub(
				r"ノーツを累計(\d+)回タップしよう",
				r"累計點擊 \1 次節奏圖示",
				description
			)
            description = re.sub(
				r"コインを(\d+)枚入手しよう",
				r"取得 \1 枚金幣",
				description
			)
            description = re.sub(
				r"スタンプを(\d+)種類入手しよう\n",
				r"取得 \1 款貼圖",
				description
			)
            description = re.sub(
				r"衣装を(\d+)種類入手しよう\n",
				r"取得 \1 款服裝",
				description
			)
            description = re.sub(
				r"アクセサリーを(\d+)種類入手しよう",
				r"取得 \1 款飾品",
				description
			)
            description = re.sub(
				r"シークレットアクセサリーを(\d+)種類入手する",
				r"取得 \1 款神秘飾品",
				description
			)
            description = re.sub(
				r"ジュゴンの勲章を(\d+)個入手する",
				r"取得 \1 個儒艮勳章",
				description
			)
            description = re.sub(
				r"難易度(.+)で(\d+)曲(.+)を達成しよう",
				r"在 \1 難度取得 \2 首歌曲的 \3",
				description
			)
            description = re.sub(
				r"協力公演で4人全員(.+)を達成しよう",
				r"全部 4 人於協力公演達成 \1",
				description
			)
            description = re.sub(
				r"(\d+)人とフレンドになろう",
				r"與 \1 人成為朋友",
				description
			)
            description = re.sub(
				r"スターアクトを累計(\d+)回発動しよう",
				r"累計發動 \1 次 Star Act",
				description
			)
            description = re.sub(
				r"オーディションで★★★クリアを(\d+)ステージで達成しよう",
				r"在試鏡達成 \1 階段的★★★通關",
				description
			)
            description = re.sub(
				r"期間限定ミッションをクリアしよう",
				r"完成期間限定任務",
				description
			)
            description = re.sub(
				r"([^　]+)誕生日記念パック(\d+)を購入しよう",
                lambda match: r"購買{}生日限定禮包{}".format(actor_translator(match.group(1), message), match.group(2)),
				description
			)
            description = re.sub(
				r"スポットストーリーを(\d+)種類読もう",
				r"閱讀 \1 種類場景劇情",
				description
			)
            description = re.sub(
				r"([^　]+)のメインストーリー(\d+)章を全て読もう",
				lambda match: "閱畢 {} 主線劇情第 {} 章".format(company_translator(match.group(1), message), match.group(2)),
				description
			)
            return description
        """
        elif locale == "<dummy>":
            description = re.sub(
                r"([^　]+)のスターランクを(\d+)以上にしよう",
				lambda match: "{}のスターランクを{}以上にしよう".format(actor_translator(match.group(1), message), match.group(2)),
				description
			)
            description = re.sub(
                r"イベント「(.+)」で(\d+)位以内に入賞",
				lambda match: "イベント「{}」で{}位以内に入賞".format(match.group(1), match.group(2)),
				description
			)
            description = re.sub(
                r"イベント「(.+)」で(\d+)位に入賞",
				lambda match: "イベント「{}」で{}位に入賞".format(match.group(1), match.group(2)),
				description
			)
            description = re.sub(
                r"イベント「(.+)」で(.+)応援ランキングの(\d+)位以内に入賞",
				lambda match: "イベント「{}」で{}応援ランキングの{}位以内に入賞".format(match.group(1), actor_translator(match.group(2), message), match.group(3)),
				description
			)
            description = re.sub(
                r"プレイヤーランクを(\d+)以上にしよう",
				r"プレイヤーランクを\1以上にしよう",
				description
			)
            description = re.sub(
                r"サークルメンバー4人で協力公演を(\d+)回クリアしよう",
				r"サークルメンバー4人で協力公演を\1回クリアしよう",
				description
			)
            description = re.sub(
                r"公演を(\d+)回クリアしよう",
                r"公演を\1回クリアしよう",
				description
			)
            description = re.sub(
                r"ライフ(\d+)以上で公演をクリアしよう",
                r"ライフ\1以上で公演をクリアしよう",
				description
			)
            description = re.sub(
                r"スコアの下３桁が「７７７」で公演をクリアしよう",
                r"スコアの下３桁が「７７７」で公演をクリアしよう",
				description
			)
            description = re.sub(
                r"物語の舞台・浅草を巡るデジタルスタンプラリーに参加",
                r"物語の舞台・浅草を巡るデジタルスタンプラリーに参加",
				description
			)
            description = re.sub(
                r"累計で(\d+)日以上ログインしよう",
                r"累計で\1日以上ログインしよう",
				description
			)
            description = re.sub(
                r"スタミナを累計(\d+)消費しよう",
                r"スタミナを累計\1消費しよう",
				description
			)
            description = re.sub(
                r"ノーツを累計(\d+)回タップしよう",
                r"ノーツを累計\1回タップしよう",
				description
			)
            description = re.sub(
                r"コインを(\d+)枚入手しよう",
                r"コインを\1枚入手しよう",
				description
			)
            description = re.sub(
                r"スタンプを(\d+)種類入手しよう\n",
                r"スタンプを\1種類入手しよう\n",
				description
			)
            description = re.sub(
                r"衣装を(\d+)種類入手しよう\n",
                r"衣装を\1種類入手しよう\n",
				description
			)
            description = re.sub(
                r"アクセサリーを(\d+)種類入手しよう",
                r"アクセサリーを\1種類入手しよう",
				description
			)
            description = re.sub(
                r"シークレットアクセサリーを(\d+)種類入手する",
                r"シークレットアクセサリーを\1種類入手する",
				description
			)
            description = re.sub(
                r"ジュゴンの勲章を(\d+)個入手する",
                r"ジュゴンの勲章を\1個入手する",
				description
			)
            description = re.sub(
                r"難易度(.+)で(\d+)曲(.+)を達成しよう",
                r"難易度\1で\2曲\3を達成しよう",
				description
			)
            description = re.sub(
                r"協力公演で4人全員(.+)を達成しよう",
                r"協力公演で4人全員\1を達成しよう",
				description
			)
            description = re.sub(
                r"(\d+)人とフレンドになろう",
                r"\1人とフレンドになろう",
				description
			)
            description = re.sub(
                r"スターアクトを累計(\d+)回発動しよう",
                r"スターアクトを累計\1回発動しよう",
				description
			)
            description = re.sub(
                r"オーディションで★★★クリアを(\d+)ステージで達成しよう",
                r"オーディションで★★★クリアを\1ステージで達成しよう",
				description
			)
            description = re.sub(
                r"期間限定ミッションをクリアしよう",
                r"期間限定ミッションをクリアしよう",
				description
			)
            description = re.sub(
                r"([^　]+)誕生日記念パック(\d+)を購入しよう",
                lambda match: r"{}誕生日記念パック{}を購入しよう".format(actor_translator(match.group(1), message), match.group(2)),
				description
			)
            description = re.sub(
                r"スポットストーリーを(\d+)種類読もう",
                r"スポットストーリーを\1種類読もう",
				description
			)
            description = re.sub(
                r"([^　]+)のメインストーリー(\d+)章を全て読もう",
				lambda match: "{}のメインストーリー{}章を全て読もう".format(company_translator(match.group(1), message), match.group(2)),
				description
			)
            return description
        """

def star_act_translator(description: str, message: MsgInt) -> str:
    locales = user_locales(message)
    for locale in locales:
        if locale == "en":
            description = description.replace(
                "総演技力の[:score]倍のスコアを獲得",
                "Gain a Score of [:score] Times the Total Status"
            )
            return description
        elif locale == "zh":
            description = description.replace(
                "総演技力の[:score]倍のスコアを獲得",
                "獲得總演技力 [:score] 倍的分數"
            )
            return description
        """
        elif locale == "<dummy>":
            description = description.replace(
                "総演技力の[:score]倍のスコアを獲得",
                "総演技力の[:score]倍のスコアを獲得",
            )
            return description
        """
    return description

def sense_translator(description: str, message: MsgInt) -> str:
    import re
    locales = user_locales(message)
    for locale in locales:
        if locale == "en":
            description = description.replace(
                "[:score]倍のスコアを獲得",
                "Gain [:score]x Score"
            )
            description = description.replace(
                "[:gauge]のプリンシパルゲージを獲得",
                "Gain [:gauge] Principal Gauge"
            )
            description = description.replace(
                "ライフを[:param11]回復",
                "Recover Life by [:param11]"
            )
            description = description.replace(
                "ライフを[:param11]",
                "Change Life by [:param11]"
            ) # placeholder
            description = description.replace(
                "効果無し（所持している「光」は維持される）",
                "No Effect (Possessed \"Lights\" are Kept as is)"
            )
            description = description.replace(
                "ここな編成時、ここなが代わりにセンスを発動し、ここなのスコア獲得量[:pre1]％UP",
                "When {0} is Present, Sense will be Activated by {0} Instead, and {0} Gains [:pre1]% UP Score from so".format(actor_translator("ここな", message))
            )
            description = description.replace(
                "センス発動後、追加で[:param11]のプリンシパルゲージを獲得",
                "Gain Additional [:param11] Principal Gauge After Sense Activation"
            )
            description = re.sub(
				r"ライフが多いほど(.+?)のスコア獲得量UP（最大＋(\d+)％）",
				lambda match: "The More the Life value is, {} Gains More Score Gain UP from so (+{}% at Most)".format(actor_translator(match.group(1), message), match.group(2)),
				description
			)
            description = re.sub(
				r"ライフが少ないほど(.+?)のスコア獲得量UP（最大＋(\d+)％）",
				lambda match: "The Less the Life value is, {} Gains More Score Gain UP from so (+{}% at Most)".format(actor_translator(match.group(1), message), match.group(2)),
				description
			)
            description = re.sub(
				r"\[:sec\]秒間、(.+?)のアクターに(センス|スターアクト)スコア\[:param11\]％UP効果",
				lambda match: "For [:sec] seconds, {} Actors Gain [:param11]% UP Score from {}".format(company_translator(match.group(1), message), sense_star_act_translator(match.group(2), message)),
				description
			)
            description = re.sub(
				r"(シリウス|Eden|銀河座|劇団電姫)のアクターのCTを(\d+)秒短縮",
				lambda match: "CT of {} Actor Reduced by {}s for the Next Sense".format(company_translator(match.group(1), message), match.group(2)),
				description
			)
            return description
        elif locale == "zh":
            description = description.replace(
                "[:score]倍のスコアを獲得",
                "獲得 [:score] 倍的分數"
            )
            description = description.replace(
                "[:gauge]のプリンシパルゲージを獲得",
                "獲得 [:gauge] Principal Gauge"
            )
            description = description.replace(
                "ライフを[:param11]回復",
                "回復 [:param11] 生命值"
            )
            description = description.replace(
                "ライフを[:param11]",
                "[:param11] 生命值"
            ) # placeholder
            description = description.replace(
                "効果無し（所持している「光」は維持される）",
                "沒有效果 (所持的「光」得以保留)"
            )
            description = description.replace(
                "ここな編成時、ここなが代わりにセンスを発動し、ここなのスコア獲得量[:pre1]％UP",
                "當{0}在隊伍時，{0}代為發動 Sense，且{0}獲得的分數 [:pre1]% UP".format(actor_translator("ここな", message))
            )
            description = description.replace(
                "センス発動後、追加で[:param11]のプリンシパルゲージを獲得",
                "Sense 發動後，追加獲得 [:param11] Principal Gauge"
            )
            description = re.sub(
				r"ライフが多いほど(.+?)のスコア獲得量UP（最大＋(\d+)％）",
				lambda match: "生命值愈多，{}的分數獲得量 UP 愈多（最多 +{}%）".format(actor_translator(match.group(1), message), match.group(2)),
				description
			)
            description = re.sub(
				r"ライフが少ないほど(.+?)のスコア獲得量UP（最大＋(\d+)％）",
				lambda match: "生命值愈少，{}的分數獲得量 UP 愈多（最多 +{}%）".format(actor_translator(match.group(1), message), match.group(2)),
				description
			)
            description = re.sub(
				r"\[:sec\]秒間、(.+?)のアクターに(センス|スターアクト)スコア\[:param11\]％UP効果",
				lambda match: "[:sec]秒內，{}演員附帶 {} 分數 [:param11]% UP 效果".format(company_translator(match.group(1), message), sense_star_act_translator(match.group(2), message)),
				description
			)
            description = re.sub(
				r"(シリウス|Eden|銀河座|劇団電姫)のアクターのCTを(\d+)秒短縮",
				lambda match: "{}演員的 CT 縮短 {} 秒".format(company_translator(match.group(1), message), match.group(2)),
				description
			)
            return description
        """
        elif locale == "<dummy>":
            description = description.replace(
                "[:score]倍のスコアを獲得",
                "[:score]倍のスコアを獲得",
            )
            description = description.replace(
                "[:gauge]のプリンシパルゲージを獲得",
                "[:gauge]のプリンシパルゲージを獲得",
            )
            description = description.replace(
                "ライフを[:param11]回復",
                "ライフを[:param11]回復",
            )
            description = description.replace(
                "ライフを[:param11]",
                "ライフを[:param11]",
            ) # placeholder
            description = description.replace(
                "効果無し（所持している「光」は維持される）",
                "効果無し（所持している「光」は維持される）",
            )
            description = description.replace(
                "ここな編成時、ここなが代わりにセンスを発動し、ここなのスコア獲得量[:pre1]％UP",
                "{0}編成時、{0}が代わりにセンスを発動し、{0}のスコア獲得量[:pre1]％UP".format(actor_translator("ここな", message)),
            )
            description = description.replace(
                "センス発動後、追加で[:param11]のプリンシパルゲージを獲得",
                "センス発動後、追加で[:param11]のプリンシパルゲージを獲得",
            )
            description = re.sub(
				r"ライフが多いほど(.+?)のスコア獲得量UP（最大＋(\d+)％）",
				lambda match: "ライフが多いほど{}のスコア獲得量UP（最大＋{}％）".format(actor_translator(match.group(1), message), match.group(2)),
				description
			)
            description = re.sub(
				r"ライフが少ないほど(.+?)のスコア獲得量UP（最大＋(\d+)％）",
				lambda match: "ライフが少ないほど{}のスコア獲得量UP（最大＋{}％）".format(actor_translator(match.group(1), message), match.group(2)),
				description
			)
            description = re.sub(
				r"\[:sec\]秒間、(.+?)のアクターに(センス|スターアクト)スコア\[:param11\]％UP効果",
				lambda match: "[:sec]秒間、{}のアクターに{}スコア[:param11]％UP効果".format(company_translator(match.group(1), message), sense_star_act_translator(match.group(2), message)),
				description
			)
            description = re.sub(
				r"(シリウス|Eden|銀河座|劇団電姫)のアクターのCTを(\d+)秒短縮",
				lambda match: "{}のアクターのCTを{}秒短縮".format(company_translator(match.group(1), message), match.group(2)),
				description
			)
            return description
        """
    else:
        return description

def bloom_translator(description: str, message: MsgInt) -> str:
    import re
    locales = user_locales(message)
    for locale in locales:
        if locale == "en":
            description = re.sub(
				r"演技力(\d+)％UP",
				r"Status \1% UP",
				description
			)
            description = re.sub(
				r"センスのCTが(\d+)秒減少",
				r"Sense CT Reduced by \1s",
				description
			)
            description = re.sub(
				r"基礎スコアが(\d+)％上昇",
				r"Base Score Increased by \1%",
				description
			)
            description = re.sub(
				r"初期ライフが(\d+)上昇",
				r"Initial Life Increased by \1",
				description
			)
            description = re.sub(
				r"初期プリンシパルゲージが(\d+)上昇",
				r"Initial Principal Gauge Increased by \1",
				description
			)
            description = re.sub(
				r"公演での報酬量が(\d+)％上昇",
				r"Rewards from Lives Increased by \1%",
				description
			)
            description = re.sub(
				r"スターアクト発動に必要な(.{2})の光の個数が(\d+)個減少",
				lambda match: "Number of {} Lights Required to Trigger Star Act Reduced by {}".format(sense_type_translator(match.group(1), message), match.group(2)),
				description
			)
            return description
        elif locale == "zh":
            description = re.sub(
				r"演技力(\d+)％UP",
				r"演技力 \1% UP",
				description
			)
            description = re.sub(
				r"センスのCTが(\d+)秒減少",
				r"Sense 的 CT 減少\1秒",
				description
			)
            description = re.sub(
				r"基礎スコアが(\d+)％上昇",
				r"基礎分數提升 \1%",
				description
			)
            description = re.sub(
				r"初期ライフが(\d+)上昇",
				r"起始生命值提升 \1",
				description
			)
            description = re.sub(
				r"初期プリンシパルゲージが(\d+)上昇",
				r"起始 Principal Gauge 提升 \1",
				description
			)
            description = re.sub(
				r"公演での報酬量が(\d+)％上昇",
				r"公演報酬量提升 \1%",
				description
			)
            description = re.sub(
				r"スターアクト発動に必要な(.{2})の光の個数が(\d+)個減少",
				lambda match: "Star Act 發動所需的{}系光數量減少 {} 個".format(sense_type_translator(match.group(1), message), match.group(2)),
				description
			)
            return description
        """
        elif locale == "<dummy>":
            description = re.sub(
				r"演技力(\d+)％UP",
				r"演技力\1％UP",
				description
			)
            description = re.sub(
				r"センスのCTが(\d+)秒減少",
				r"センスのCTが\1秒減少",
				description
			)
            description = re.sub(
				r"基礎スコアが(\d+)％上昇",
				r"基礎スコアが\1％上昇",
				description
			)
            description = re.sub(
				r"初期ライフが(\d+)上昇",
				r"初期ライフが\1上昇",
				description
			)
            description = re.sub(
				r"初期プリンシパルゲージが(\d+)上昇",
				r"初期プリンシパルゲージが\1上昇",
				description
			)
            description = re.sub(
				r"公演での報酬量が(\d+)％上昇",
				r"公演での報酬量が\1％上昇",
				description
			)
            description = re.sub(
				r"スターアクト発動に必要な(.{2})の光の個数が(\d+)個減少",
				lambda match: "スターアクト発動に必要な{}の光の個数が{}個減少".format(sense_type_translator(match.group(1), message), match.group(2)),
				description
			)
            return description
        """
    else:
        return description