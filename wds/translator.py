"""
This file is safe for hot reloading.
"""

from msgint import MsgInt
from typing import *

# regex to select the 3rd field from an array entry:
# \[(?:[^[,]+, ){2}"([^"]+)"

def user_locales(message: MsgInt) -> Tuple[str]:
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
    target: str, message: Union[MsgInt, List[str], Tuple[str], str],
    lookup_dict: Dict[str, Dict[str, str]],
    regex_lookup_dict: Dict[str, Dict[str, str]] = {}
) -> str:
    if type(message) is str:
        locales = [message]
    elif type(message) is list or type(message) is tuple:
        locales = message
    else:
        locales = user_locales(message)
    if target in lookup_dict:
        for locale in locales:
            if locale in lookup_dict[target]:
                return lookup_dict[target][locale]
        if "*" in lookup_dict[target]:
            return lookup_dict[target]["*"]
        return target
    else:
        import re
        from .const import sense_name_emote, sense_to_key
        from .const import type_emotes, type_names
        for regex in regex_lookup_dict:
            match = re.fullmatch(regex, target)
            if match:
                for locale in locales:
                    if locale in regex_lookup_dict[regex]:
                        translator = regex_lookup_dict[regex][locale]
                        temp_dict = match.groupdict()
                        if "company" in temp_dict:
                            temp_dict["company"] = company_translator(temp_dict["company"], locales)
                        if "company2" in temp_dict:
                            temp_dict["company2"] = company_translator(temp_dict["company2"], locales)
                        if "companies" in temp_dict:
                            temp_dict["companies"] = "・".join([company_translator(company, locales) for company in temp_dict["companies"].split("・")])
                        if "actor" in temp_dict:
                            temp_dict["actor"] = actor_translator(temp_dict["actor"], locales)
                        if "actors" in temp_dict:
                            temp_dict["actors"] = "・".join([actor_translator(actor, locales) for actor in temp_dict["actors"].split("・")])
                        if "sense_star_act" in temp_dict:
                            temp_dict["sense_star_act"] = sense_star_act_translator(temp_dict["sense_star_act"], locales)
                        if "sense_type" in temp_dict:
                            # handle emoji before translating text
                            if "{sense_emoji}" in translator:
                                temp_dict["sense_emoji"] = sense_name_emote.get(sense_to_key.get(temp_dict["sense_type"]), "❓")
                            temp_dict["sense_type"] = sense_type_translator(temp_dict["sense_type"], locales)
                        if "attribute" in temp_dict:
                            # handle emoji before translating text
                            if "{attribute_emoji}" in translator:
                                temp_dict["attribute_emoji"] = type_emotes[type_names.index(temp_dict["attribute"])] if temp_dict["attribute"] in type_names else "❓"
                            temp_dict["attribute"] = attribute_translator(temp_dict["attribute"], locales)
                        if "status" in temp_dict:
                            temp_dict["status"] = status_translator(temp_dict["status"], locales)
                        if "status2" in temp_dict:
                            temp_dict["status2"] = status_translator(temp_dict["status2"], locales)
                        if "ordinal" in temp_dict:
                            temp_dict["ordinal"] = ordinal_translator(temp_dict["ordinal"], locale) # need string or message
                        return translator.format(*match.groups(), **temp_dict)
                else:
                    if "*" in regex_lookup_dict[regex]:
                        return regex_lookup_dict[regex]["*"]
                    return target
        return target

available_translators = {}

def regex_lookup_translator_wrapper(
    label: str,
    lookup_dict: Dict[str, Dict[str, str]],
    regex_lookup_dict: Dict[str, Dict[str, str]] = {}
):
    available_translators[label] = {
        "simple": lookup_dict,
        "regex": regex_lookup_dict
    }
    def wrapper(target: str, message: Union[MsgInt, str]) -> str:
        return regex_lookup_translator(target, message, lookup_dict, regex_lookup_dict)
    return wrapper

actor_translator = regex_lookup_translator_wrapper("actor_translator", {
    "ここな": {
        "en": "Kokona",
        "zh": "心菜",
        "ko": "코코나",
        "th": "โคโคนะ",
    },
    "静香": {
        "en": "Shizuka",
        "zh_TW": "靜香",
        "ko": "시즈카",
        "th": "ชิซุกะ", # or ชิซึกะ
    },
    "カトリナ": {
        "en": "Kathrina",
        "zh": "卡特莉娜",
        "ko": "카트리나",
        "th": "แคทริน่า" # or คาทรีนา
    },
    "八恵": {
        "en": "Yae",
        "zh": "八惠",
        "ko": "야에",
        "th": "แพนด้า", # or พันดะ
    },
    "ぱんだ": {
        "en": "Panda",
        "zh_TW": "潘達",
        "zh_CN": "潘达",
        "ko": "판다",
        "th": "พันดะ",
    },
    "知冴": {
        "en": "Chisa",
        "ko": "치사",
        "th": "จิสะ",
    },

    "初魅": {
        "en": "Hatsumi",
        "ko": "하츠미",
        "th": "ฮัทสึมิ", # or ฮัตสึมิ
    },
    "大黒": {
        "en": "Daikoku",
        "zh": "大黑",
        "ko": "다이코쿠",
        "th": "ไดโคคุ",
    },
    "仁花子": {
        "en": "Nikako",
        "ko": "니카코",
        "th": "นิคาโกะ", # or นิกาโกะ
    },
    "容": {
        "en": "Iruru",
        "ko": "이루루",
        "th": "อิรุรุ",
    },
    "しぐれ": {
        "en": "Shigure",
        "zh_TW": "時雨",
        "zh_CN": "时雨",
        "ko": "시구레",
        "th": "ชิกุเระ",
    },

    "暦": {
        "en": "Koyomi",
        "zh_TW": "曆",
        "zh_CN": "历",
        "ko": "코요미",
        "th": "โคโยมิ",
    },
    "ラモーナ": {
        "en": "Ramona",
        "zh": "拉莫娜",
        "ko": "라모나",
        "th": "ราโมนา", # or โรมานา
    },
    "雪": {
        "en": "Xue",
        "ko": "슈에",
        "th": "เสวี่ย",
    },
    "リリヤ": {
        "en": "Lilja",
        "zh_TW": "莉莉亞",
        "zh_CN": "莉莉亚",
        "ko": "리리야",
        "th": "ลิเลีย",
    },
    "緋花里": {
        "en": "Hikari",
        "zh_CN": "绯花里",
        "ko": "히카리",
        "th": "ฮิคาริ",
    },

    "いろは": {
        "en": "Iroha",
        "zh_TW": "伊呂波",
        "zh_CN": "伊吕波",
        "ko": "이로하",
        "th": "อิโรฮะ",
    },
    "美兎": {
        "en": "Mito",
        "zh": "美兔",
        "ko": "미토",
        "th": "มิโตะ",
    },
    "カミラ": {
        "en": "Kamira",
        "zh_TW": "卡蜜拉",
        "zh_CN": "卡米拉",
        "ko": "카미라",
        "th": "คามิระ",
    },
    "蕾": {
        "en": "Tsubomi",
        "ko": "츠보미",
        "th": "สึโบมิ",
    },
    "叶羽": {
        "en": "Towa",
        "zh_TW": "葉羽",
        "ko": "토와",
        "th": "โทวะ",
    },

    "千歌": {
        "en": "Chika",
        "ko": "치카",
        "th": "จิกะ",
    },
    "梨子": {
        "en": "Riko",
        "ko": "리코",
        "th": "ริโกะ",
    },
    "果南": {
        "en": "Kanan",
        "ko": "카난",
        "th": "คานัน",
    },
    "ダイヤ": {
        "en": "Dia",
        "zh": "黛雅",
        "ko": "다이아",
        "th": "ไดยะ",
    },
    "曜": {
        "en": "You",
        "ko": "요우",
        "th": "โย",
    },
    "善子": {
        "en": "Yoshiko",
        "ko": "요시코",
        "th": "โยชิโกะ",
    },
    "花丸": {
        "en": "Hanamaru",
        "ko": "하나마루",
        "th": "ฮานะมารุ",
    },
    "鞠莉": {
        "en": "Mari",
        "ko": "마리",
        "th": "มาริ",
    },
    "ルビィ": {
        "en": "Ruby",
        "zh": "露比",
        "ko": "루비",
        "th": "รูบี้",
    },
})

actor_full_translator = regex_lookup_translator_wrapper("actor_full_translator", {
    "鳳ここな": {
        "en": "Kokona Otori",
        "zh_TW": "鳳心菜",
        "zh_CN": "凤心菜",
        "ko": "오오토리 코코나",
        "th": "โอโทริ โคโคนะ", # or โอโตริ โคโคนะ
    },
    "静香": {
        "en": "Shizuka",
        "zh_TW": "靜香",
        "ko": "시즈카",
        "th": "ชิซุกะ", # or ชิซึกะ
    },
    "カトリナ・グリーベル": {
        "en": "Kathrina Griebel",
        "zh": "卡特莉娜·格利貝爾",
        "zh_CN": "卡特莉娜·格利贝尔",
        "ko": "카트리나 그리벨",
        "th": "แคทริน่า กรีเบล" # or คาทรีนา กรีเบล
    },
    "新妻八恵": {
        "en": "Yae Niizuma",
        "zh": "新妻八惠",
        "ko": "니이즈마 야에",
        "th": "นีซึมะ ยาเอะ",
    },
    "柳場ぱんだ": {
        "en": "Panda Yanagiba",
        "zh_TW": "柳場潘達",
        "zh_CN": "柳场潘达",
        "ko": "야나기바 판다",
        "th": "ยานากิบะ แพนด้า", # or ยานางิบะ พันดะ
    },
    "流石知冴": {
        "en": "Chisa Sasuga",
        "ko": "사스가 치사",
        "th": "ซาสึกะ จิสะ", # or ซาสึงะ จิสะ
    },

    "連尺野初魅": {
        "en": "Hatsumi Renjakuno",
        "zh_CN": "连尺野初魅",
        "ko": "렌쟈쿠노 하츠미",
        "th": "เรนจาคุโนะ ฮัทสึมิ", # or เร็นจากุโนะ ฮัตสึมิ
    },
    "烏森大黒": {
        "en": "Daikoku Karasumori",
        "zh_TW": "烏森大黑",
        "zh_CN": "乌森大黑",
        "ko": "카라스모리 다이코쿠",
        "th": "คาราสึโมริ ไดโคคุ",
    },
    "舎人仁花子": {
        "en": "Nikako Toneri",
        "zh": "舍人仁花子",
        "ko": "토네리 니카코",
        "th": "โทเนริ นิคาโกะ", # or โทเนริ นิกาโกะ
    },
    "萬容": {
        "en": "Iruru Yorozu",
        "zh_CN": "万容",
        "ko": "요로즈 이루루",
        "th": "โยโรซุ อิรุรุ",
    },
    "筆島しぐれ": {
        "en": "Shigure Fudeshima",
        "zh_TW": "筆島時雨",
        "zh_CN": "笔岛时雨",
        "ko": "후데시마 시구레",
        "th": "ฟุเดชิมะ ชิกุเระ", # or ฟุเดชิมา ชิกุเระ
    },

    "千寿暦": {
        "en": "Koyomi Senju",
        "zh_TW": "千壽曆",
        "zh_CN": "千寿历",
        "ko": "센쥬 코요미",
        "th": "เซ็นจู โคโยมิ", # or เซ็นจุ โคโยมิ
    },
    "ラモーナ・ウォルフ": {
        "en": "Ramona Wolf",
        "zh_TW": "拉莫娜·沃爾芙",
        "zh_CN": "拉莫娜·沃尔芙",
        "ko": "라모나 울프",
        "th": "ราโมนา วูล์ฟ", # or โรมานา วอล์ฟ
    },
    "王雪": {
        "en": "Xue Wang",
        "ko": "왕 슈에",
        "th": "หวัง เสวี่ย",
    },
    "リリヤ・クルトベイ": {
        "en": "Lilja Kurtbay",
        "zh_TW": "莉莉亞·庫爾特貝",
        "zh_CN": "莉莉亚·库尔特贝",
        "ko": "리리야 쿠르트베이",
        "th": "ลิเลีย เคิร์ทเบย์",
    },
    "与那国緋花里": {
        "en": "Hikari Yonaguni",
        "zh_TW": "與那國緋花里",
        "zh_CN": "与那国绯花里",
        "ko": "요나구니 히카리",
        "th": "โยนะกุนิ ฮิคาริ",
    },

    "千寿いろは": {
        "en": "Iroha Senju",
        "zh_TW": "千壽伊呂波",
        "zh_CN": "千寿伊吕波",
        "ko": "센쥬 이로하",
        "th": "เซ็นจู อิโรฮะ", # or เซ็นจุ อิโรฮะ
    },
    "白丸美兎": {
        "en": "Mito Shiromaru",
        "zh": "白丸美兔",
        "ko": "시로마루 미토",
        "th": "ชิโระมารุ มิโตะ", # or ชิโรมารุ มิโตะ
    },
    "阿岐留カミラ": {
        "en": "Kamira Akiru",
        "zh_TW": "阿岐留卡蜜拉",
        "zh_CN": "阿伎留卡米拉",
        "ko": "아키루 카미라",
        "th": "อากิรุ คามิระ", # or อะกิรุ คามิระ
    },
    "猫足蕾": {
        "en": "Tsubomi Nekoashi",
        "zh_TW": "貓足蕾",
        "ko": "네코아시 츠보미",
        "th": "เนโกะอาชิ สึโบมิ",
    },
    "本巣叶羽": {
        "en": "Towa Motosu",
        "zh_TW": "本巢葉羽",
        "zh_CN": "本巢叶羽",
        "ko": "모토스 토와",
        "th": "โมโตสึ โทวะ",
    },

    "高海千歌": {
        "en": "Chika Takami",
        "ko": "타카미 치카",
        "th": "ทาคามิ จิกะ",
    },
    "桜内梨子": {
        "en": "Riko Sakurauchi",
        "zh_TW": "櫻內梨子",
        "zh_CN": "樱内梨子",
        "ko": "사쿠라우치 리코",
        "th": "ซากุระอุจิ ริโกะ",
    },
    "松浦果南": {
        "en": "Kanan Matsuura",
        "ko": "마츠우라 카난",
        "th": "มัตซึอุระ คานัน",
    },
    "黒澤ダイヤ": {
        "en": "Dia Kurosawa",
        "zh_TW": "黑澤黛雅",
        "zh_CN": "黑泽黛雅",
        "ko": "쿠로사와 다이아",
        "th": "คุโรซาว่า ไดยะ",
    },
    "渡辺曜": {
        "en": "You Watanabe",
        "zh_TW": "渡邊曜",
        "zh_CN": "渡边曜",
        "ko": "쿠로사와 요우",
        "th": "วาตานาเบะ โย",
    },
    "津島善子": {
        "en": "Yoshiko Tsushima",
        "zh_CN": "津岛善子",
        "ko": "츠시마 요시코",
        "th": "ซึชิมะ โยชิโกะ",
    },
    "国木田花丸": {
        "en": "Hanamaru Kunikida",
        "zh_TW": "國木田花丸",
        "ko": "쿠니키타 하나마루",
        "th": "คุนิคิดะ ฮานามารุ",
    },
    "小原鞠莉": {
        "en": "Mari Ohara",
        "ko": "오하라 마리",
        "th": "โอฮาระ มาริ",
    },
    "黒澤ルビィ": {
        "en": "Ruby Kurosawa",
        "zh_TW": "黑澤露比",
        "zh_CN": "黑泽露比",
        "ko": "쿠로사와 루비",
        "th": "คุโรซาว่า รูบี้",
    },
})

company_translator = regex_lookup_translator_wrapper("company_translator", {
    "シリウス": {
        "en": "Sirius",
        "zh": "天狼星",
        "ko": "시리우스",
        "ja": "シリウス",
        "*": "Sirius",
    },
    "Eden": {
        "*": "Eden",
    },
    "銀河座": {
        "en": "Gingaza",
        "zh_TW": "銀河座",
        "zh_CN": "银河座",
        "ko": "은하자리",
        "ja": "銀河座",
        "*": "Gingaza",
    },
    "劇団電姫": {
        "en": "Gekidan Denki",
        "zh_TW": "劇團電姬",
        "zh_CN": "剧团电姬",
        "ko": "극단 전자공주",
        "ja": "劇団電姫",
        "*": "Gekidan Denki",
    },
    "ラブライブサンシャイン": {
        "ja": "ラブライブサンシャイン",
        "ko": "러브 라이브 선샤인",
        "th": "เลิฟไลฟ์ ซันไชน์",
        "*": "LoveLive Sunshine",
    }
})

sense_type_translator = regex_lookup_translator_wrapper("sense_type_translator", {
    "支援": {
        "en": "Support",
        "th": "ดาวสีเขียว", # "green"
    },
    "支配": {
        "en": "Control",
        "th": "ดาวสีแดง", # "red"
    },
    "増幅": {
        "en": "Amplification",
        "zh": "增幅",
        "th": "ดาวสีเหลือง", # "yellow"
    },
    "特殊": {
        "en": "Special",
        "th": "ดาวสีน้ำเงิน", # "blue"
    },
})

attribute_translator = regex_lookup_translator_wrapper("attribute_translator", {
    "憐": {
        "en": "Cute",
        "zh_CN": "怜",
    },
    "凛": {
        "en": "Cool",
        "zh_TW": "凜",
        "zh_CN": "凛",
    },
    "彩": {
        "en": "Colorful",
        "zh_CN": "彩",
    },
    "陽": {
        "en": "Cheerful",
        "zh_CN": "阳",
    },
})

sense_star_act_translator = regex_lookup_translator_wrapper("sense_star_act_translator", {
    "センス": {
        "en": "Sense",
        "ko": "센스",
        "th": "เซนส์",
        "ja": "センス",
        "*": "Sense",
    },
    "スターアクト": {
        "en": "Star Act",
        "ko": "스타 액트",
        "ja": "スターアクト",
        "*": "Star Act",
    },
})

status_translator = regex_lookup_translator_wrapper("status_translator", {
    "演技力": {
        "en": "Total Status",
        "th": "ความสามารถการแสดง",
    },
    "演技力上限": {
        "en": "Status Cap",
        "zh": "演技力上限",
        "th": "ความสามารถการแสดงสูงสุด",
    },
    "演技力の上限": {
        "en": "Status Cap",
        "zh": "演技力的上限",
        "th": "ความสามารถการแสดงสูงสุด",
    },
    "歌唱力": {
        "en": "Vocal Status",
        "th": "การร้องเพลง",
    },
    "表現力": {
        "en": "Expression Status",
        "zh_CN": "表现力",
        "th": "การแสดงออก",
    },
    "集中力": {
        "en": "Concentration Status",
        "th": "สมาธิ",
    },
})

unlock_text_translator = regex_lookup_translator_wrapper("unlock_text_translator", {
    "初期から所持": {
        "en": "Owned Initially",
        "zh_TW": "從一開始就持有",
        "zh_CN": "从一开始就持有",
    },
    "ガチャで入手": {
        "en": "Obtain via Gacha",
        "zh_TW": "從抽獎取得",
        "zh_CN": "从抽奖取得",
    },
    "ガチャ(期間限定)で入手": {
        "en": "Obtain via Gacha (Time-Limited)",
        "zh_TW": "從抽獎 (期間限定) 取得",
        "zh_CN": "从抽奖 (期间限定) 取得",
    },
    "ガチャ(ユメフェス)で入手": {
        "en": "Obtain via Gacha (Yume Fes)",
        "zh_TW": "從抽獎 (Yume Fes) 取得",
        "zh_CN": "从抽奖 (Yume Fes) 取得",
    },
    "ガチャ(コラボ限定)で入手": {
        "en": "Obtain via Gacha (Collab-Limited)",
        "zh_TW": "從抽獎 (聯動限定) 取得",
        "zh_CN": "从抽奖 (联动限定) 取得",
    },
    "メインストーリー読了、/n、またはガチャで入手": {
        "en": "Obtain by finishing reading Main Story,/nor via Gacha",
        "zh_TW": "閱畢主線劇情，/n或從抽獎取得",
        "zh_CN": "阅毕主线剧情，/n或从抽奖取得",
    },
    "イベントで入手": {
        "en": "Obtain via Event",
        "zh_TW": "從活動取得",
        "zh_CN": "从活动取得",
    },
    "イベント(コラボ)で入手": {
        "en": "Obtain via Event (Collab)",
        "zh_TW": "從活動 (聯動) 取得",
        "zh_CN": "从活动 (联动) 取得",
    },
    "特別な方法で入手": {
        "en": "Obtain via Special Method",
        "zh_TW": "從特殊方式取得",
        "zh_CN": "从特殊方式取得",
    },
    "初心者ミッションで入手": {
        "en": "Obtain via Beginner Missions",
        "zh_TW": "從新手任務取得",
        "zh_CN": "从新手任务取得",
    },
    "劇団ミッションで入手": {
        "en": "Obtain via Company Missions",
        "zh_TW": "從劇團任務取得",
        "zh_CN": "从剧团任务取得",
    },
    "メダル交換で入手": {
        "en": "Obtain via Medal Exchange",
        "zh_TW": "透過交換獎章取得",
        "zh_CN": "透过交换奖章取得",
    },
})

trophy_description_translator = regex_lookup_translator_wrapper("trophy_description_translator", {
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
        "en": "Clear {0} Multi-player Performances with 4 Players in the Circle",
        "zh": "Circle 4 人完成 {0} 次協力公演",
    },
    r"協力公演で4人全員(.+)を達成しよう": {
        "en": "Achieve {0} by all 4 Players in a Multi-player Performance",
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
        "en": "Read All of {company} Main Stories, Chapter {1}",
        "zh": "閱畢 {company} 主線劇情第 {1} 章",
    },
})

single_star_act_translator = regex_lookup_translator_wrapper("single_star_act_translator", {
    "総演技力の[:score]倍のスコアを獲得": {
        "en": "Gain a Score of [:score] Times the Total Status",
        "zh_TW": "獲得總演技力 [:score] 倍的分數",
        "zh_CN": "获得总演技力 [:score] 倍的分数",
        "th": "ได้รับคะแนน [:score] เท่าของความสามารถการแสดงทั้งหมด",
    },
    "ライフが多いほどスコア獲得量UP効果（最大＋[:pre1]%）": {
        "en": "The More the Life Value is, the More Score Gain UP is Resulted in from so (+[:pre1]% at Most)",
        "zh_TW" : "生命值愈多，分數獲得量 UP 效果愈強（最多 +[:pre1]%）",
        "zh_CN" : "生命值愈多，分数获得量 UP 效果愈强（最多 +[:pre1]%）",
        "th" : "ยิ่งเลือดมากเท่าไหร่ยิ่งได้รับคะแนนมากเท่านั้น (สูงสุด +[:pre1]%)",
    },
}, {
    r"付与されているライフガード1回につきスコア獲得量(\d+)％上昇（最大＋(\d+)％）": {
        "en": "Score Gain is Increased by {0}% for each Attached Life Guard (+{1}% at Most)",
        "zh_TW": "附帶 Life Guard 每剩餘 1 次，分數獲得量增加{0}%（最多 +{1}%）",
        "zh_CN": "附带 Life Guard 每剩余 1 次，分数获得量增加{0}%（最多 +{1}%）",
        "th": "ได้รับคะแนนเพิ่มขึ้น {0}% ต่อ Life Guard 1 ครั้ง (สูงสุด {1}%)",
    },
    r"編成されている属性1種類につきスコア獲得量(\d+)％上昇（最大＋(\d+)％）": {
        "en": "For each Attribute there is in the Unit, Score Gain is Increased by {0}% (+{1}% at Most)",
        "zh_TW": "每 1 個編成的屬性能使分數獲得量增加{0}%（最多 +{1}%）",
        "zh_CN": "每 1 个编成的属性能使分数获得量增加{0}%（最多 +{1}%）",
        "th": "ได้รับคะแนนเพิ่มขึ้น {0}% ต่อคุณสมบัติของนักแสดงที่แตกต่างกัน (สูงสุด {1}%)",
    },
    r"ストックされている全ての光1個につき総演技力の\[:param11\]倍のスコアを獲得\(最大(\d+)個\)": {
        "en": "For each Stocked Light, Gain a Score of [:param11] Times the Total Status ({0} Lights at Most)",
        "zh_TW": "每儲藏 1 個光，獲得總演技力 [:param11] 倍的分數 (最多 {0} 個)",
        "zh_CN": "每储藏 1 个光，获得总演技力 [:param11] 倍的分数 (最多 {0} 个)",
        "th": "ได้รับคะแนนเพิ่มเติม [:param11] เท่าของความสามารถการแสดงของดาวแต่ละดวงสูงสุด {0} ดวง",
    },
    r"ストックされている(?P<sense_type>.{2})系の光1個につき総演技力の\[:param11\]倍のスコアを獲得\(最大(\d+)個\)": {
        "ja": "ストックされている{sense_type}系の光「{sense_emoji}」1個につき総演技力の[:param11]倍のスコアを獲得(最大{1}個)",
        "en": "For each Stocked {sense_type} Light ({sense_emoji}), Gain a Score of [:param11] Times the Total Status ({1} Lights at Most)",
        "zh_TW": "每儲藏 1 個{sense_type}系光「{sense_emoji}」，獲得總演技力 [:param11] 倍的分數 (最多 {1} 個)",
        "zh_CN": "每储藏 1 个{sense_type}系光「{sense_emoji}」，获得总演技力 [:param11] 倍的分数 (最多 {1} 个)",
        "th": "ได้รับคะแนนเพิ่มเติม [:param11] เท่าของความสามารถการแสดงของ{sense_type} ({sense_emoji}) ดาวแต่ละดวงสูงสุด {1} ดวง",
    },
    r"ストックされている(?P<sense_type>.{2})系の光1個につき総演技力の\[:param11\]倍のスコアを追加で獲得\(最大(\d+)個\)": {
        "ja": "ストックされている{sense_type}系の光「{sense_emoji}」1個につき総演技力の[:param11]倍のスコアを追加で獲得(最大{1}個)",
        "en": "For each Stocked {sense_type} Light ({sense_emoji}), Gain an Additional Score of [:param11] Times the Total Status ({1} Lights at Most)",
        "zh_TW": "每儲藏 1 個{sense_type}系光「{sense_emoji}」，額外獲得總演技力 [:param11] 倍的分數 (最多 {1} 個)",
        "zh_CN": "每储藏 1 个{sense_type}系光「{sense_emoji}」，额外获得总演技力 [:param11] 倍的分数 (最多 {1} 个)",
        "th": "ได้รับคะแนนเพิ่มเติม [:param11] เท่าของความสามารถการแสดงของ{sense_type} ({sense_emoji}) แต่ละดวงสูงสุด {1} ดวง",
    },
    r"プリンシパルゲージの上限を編成されている(?P<company>.+)アクターの人数×\[:param11\]上昇させる": {
        "en": 'Principal Gauge Cap Increased by the Number of {company} Actors in Unit × [:param11]',
        "zh_TW": "Principal Gauge 的上限值提升隊伍內{company}演員人數 × [:param11]",
        "zh_CN": "Principal Gauge 的上限值提升队伍内{company}演员人数 × [:param11]",
    },
    r"編成されている(?P<company>.+)アクターの(?P<status>.+?)と(?P<status2>.+?)を、編成されている\1アクターの人数×(\d+)%上昇させる\(この効果は重複する\)": {
        "en": "The {status} and {status2} of each {company} Actor in the Unit Increased by the Number of {company} Actors in Unit × {3}% (This Effect can be Stacked)",
        "zh_TW": "{company}演員的 {status} 及 {status2} 提升隊伍內{company}演員人數 × {3}% (此效果可疊加)",
        "zh_CN": "{company}演员的 {status} 及 {status2} 提升队伍内{company}演员人数 × {3}% (此效果可叠加)",
    },
})

def star_act_translator(description: str, message: MsgInt) -> str:
    import re
    # remove size tag
    description = re.sub(
        r"<size=\d+[%％]?>(.+?)<\/size>",
        r"\1",
        description
    )
    return "／".join([
        single_star_act_translator(part, message)
    for part in description.strip().split("／")])

single_sense_translator = regex_lookup_translator_wrapper("single_sense_translator", {
    "[:score]倍のスコアを獲得": {
        "en": "Gain [:score]x Score",
        "zh_TW": "獲得 [:score] 倍的分數",
        "zh_CN": "获得 [:score] 倍的分数",
        "th": "เพิ่มคะแนน [:score] เท่า",
    },
    "[:gauge]のプリンシパルゲージを獲得": {
        "en": "Gain [:gauge] Principal Gauge",
        "zh_TW": "獲得 [:gauge] Principal Gauge",
        "zh_CN": "获得 [:gauge] Principal Gauge",
        "th": "ได้รับ Principal gauge เพิ่มขึ้น [:gauge]",
    },
    "ライフを[:param11]回復": {
        "en": "Recover Life by [:param11]",
        "zh_TW": "回復 [:param11] 生命值",
        "zh_CN": "回复 [:param11] 生命值",
        "th": "ฟื้นฟูเลือด [:param11]",
    },
    "ライフを[:param11]": {
        "en": "Change Life by [:param11]",
        "zh": "[:param11] 生命值",
        "th": "เปลี่ยนเลือดของคุณ [:param11]",
    },
    "効果無し（所持している「光」は維持される）": {
        "en": "No Effect (Possessed \"Lights\" are Kept as is)",
        "zh_TW": "沒有效果 (所持的「光」得以保留)",
        "zh_CN": "没有效果 (所持的「光」得以保留)",
    },
    "センス発動後、追加で[:param11]のプリンシパルゲージを獲得": {
        "en": "After Sense Activation, Gain Additional [:param11] Principal Gauge",
        "zh_TW": "Sense 發動後，額外獲得 [:param11] Principal Gauge",
        "zh_CN": "Sense 发动后，额外获得 [:param11] Principal Gauge",
        "th": "ได้รับ Principal gauge เพิ่มขึ้น [:param11] หลังจากเปิดใช้งานเซนส์",
    },
    "センス発動後、プリンシパルゲージの上限値が[:param11]上昇": {
        "en": "After Sense Activation, Increase Principal Gauge Cap by [:param11]",
        "zh_TW": "Sense 發動後，Principal Gauge 的上限值提升 [:param11]",
        "zh_CN": "Sense 发动后，Principal Gauge 的上限值提升 [:param11]",
        "th": "หลังจากเปิดใช้งานเซนส์ Principal gauge สูงสุดจะเพิ่มขึ้น [:param11]",
    },
    "センス発動後、追加で獲得しているプリンシパルゲージ[:param11]%を獲得": {
        "en": "After Sense Activation, Additionally Gain [:param11]% of the Amount of Gained Principal Gauge",
        "zh_TW": "Sense 發動後，額外獲得已獲得的 Principal Gauge 的 [:param11]%",
        "zh_CN": "Sense 发动后，额外获得已获得的 Principal Gauge 的 [:param11]%",
    },
    "センス発動後、現在のプリンシパルゲージ[:param11]%分のプリンシパルゲージを追加で獲得する": {
        "en": "After Sense Activation, Gain Additional Principal Gauge of [:param11]% of the Current Principal Gauge",
        "zh_TW": "Sense 發動後，額外獲得目前 Principal Gauge 的 [:param11]% 份量的 Principal Gauge",
        "zh_CN": "Sense 发动后，额外获得目前 Principal Gauge 的 [:param11]% 份量的 Principal Gauge",
    },
    "ライフが多いほどスコア獲得量UP効果（最大＋[:pre1]%）": {
        "en": "The More the Life value is, the More Score Gain UP is resulted in from so (+[:pre1]% at Most)",
        "zh_TW" : "生命值愈多，分數獲得量 UP 效果愈強（最多 +[:pre1]%）",
        "zh_CN" : "生命值愈多，分数获得量 UP 效果愈强（最多 +[:pre1]%）",
        "th": "ยิ่งเลือดน้อยเท่าไหร่ยิ่งได้รับคะแนนมากเท่านั้น (สูงสุด +[:pre1]%)",
    },
}, {
    r"(?P<actor>.+)編成時、(?P=actor)が代わりにセンスを発動し、(?P=actor)のスコア獲得量\[:pre1\]％UP": {
        "en": "When {actor} is Present, Sense is Activated by {actor} Instead, and {actor} Gains [:pre1]% UP Score from so",
        "zh_TW": "當{actor}在隊伍時，{actor}代為發動 Sense，且{actor}獲得的分數 [:pre1]% UP",
        "zh_CN": "当{actor}在队伍时，{actor}代为发动 Sense，且{actor}获得的分数 [:pre1]% UP",
        "th": "เมื่อ{actor}อยู่ในทีม {actor}จะเปิดใช้งานเซนส์แทนและคะแนนจะเพิ่มขึ้น [:pre1]%",
    },
    r"ライフが多いほど(?P<actor>.+)のスコア獲得量UP（最大＋(\d+)％）": {
        "en": "The More the Life value is, {actor} Gains More Score Gain UP from so (+{1}% at Most)",
        "zh_TW" : "生命值愈多，{actor}的分數獲得量 UP 效果愈強（最多 +{1}%）",
        "zh_CN" : "生命值愈多，{actor}的分数获得量 UP 效果愈强（最多 +{1}%）",
        "th" : "ยิ่งเลือดมากเท่าไหร่ยิ่งได้รับคะแนนมากเท่านั้น (สูงสุด +{1}%)",
    },
    r"ライフが少ないほど(?P<actor>.+)のスコア獲得量UP（最大＋(\d+)％）": {
        "en": "The Less the Life value is, {actor} Gains More Score Gain UP from so (+{1}% at Most)",
        "zh_TW": "生命值愈少，{actor}的分數獲得量 UP 效果愈強（最多 +{1}%）",
        "zh_CN": "生命值愈少，{actor}的分数获得量 UP 效果愈强（最多 +{1}%）",
        "th": "ยิ่งเลือดน้อยเท่าไหร่ยิ่งได้รับคะแนนมากเท่านั้น (สูงสุด +{1}%)",
    },
    r"\[:sec\]秒間、(?P<company>.+)のアクターに(?P<sense_star_act>センス|スターアクト)スコア\[:param11\]％UP効果": {
        "en": "For [:sec] seconds, {company} Actors Gain [:param11]% UP Score from {sense_star_act}",
        "zh_TW": "[:sec]秒內，{company}演員附帶 {sense_star_act} 分數 [:param11]% UP 效果",
        "zh_CN": "[:sec]秒内，{company}演员附带 {sense_star_act} 分数 [:param11]% UP 效果",
        "th": "คะแนน{sense_star_act}ของ {company} เพิ่มขึ้น [:param11]% เป็นเวลา [:sec] วินาที",
    },
    r"(?P<company>.+)のアクターのCTを(\d+)秒短縮": {
        "en": "CT of {company} Actor Reduced by {1}s for the Next Sense",
        "zh_TW": "{company}演員的 CT 縮短 {1} 秒",
        "zh_CN": "{company}演员的 CT 缩短 {1} 秒",
        "th": "CT ของ {company} ลดลง {1} วินาที",
    },
    r"付与されているライフガード1回につきスコア獲得量(\d+)％上昇（最大＋(\d+)％）": {
        "en": "For each Attached Life Guard, Score Gain is Increased by {0}% (+{1}% at Most)",
        "zh_TW": "附帶 Life Guard 每剩餘 1 次，分數獲得量增加{0}%（最多 +{1}%）",
        "zh_CN": "附带 Life Guard 每剩余 1 次，分数获得量增加{0}%（最多 +{1}%）",
        "th": "ได้รับคะแนนเพิ่มขึ้น {0}% ต่อ Life Guard 1 ครั้ง (สูงสุด {1}%)",
    },
    r"付与されているライフガード1回につきプリンシパルゲージの上限値が(\d+)上昇（最大\+(\d+)）": {
        "en": "Increase Principal Gauge Cap by {0} for each Attached Life Guard (+{1} at Most)",
        "zh_TW": "附帶 Life Guard 每剩餘 1 次，Principal Gauge 的上限值提升{0}（最多 +{1}）",
        "zh_CN": "附带 Life Guard 每剩余 1 次，Principal Gauge 的上限值提升{0}（最多 +{1}）",
        "th": "Principal gauge สูงสุดจะเพิ่มขึ้น {0} ต่อ Life Guard 1 ครั้ง (สูงสุด {1})",
    },
    r"編成されている属性1種類につきスコア獲得量(\d+)％上昇（最大＋(\d+)％）": {
        "en": "For each Attribute there is in the Unit, Score Gain is Increased by {0}% (+{1}% at Most)",
        "zh_TW": "每 1 個編成的屬性能使分數獲得量增加{0}%（最多 +{1}%）",
        "zh_CN": "每 1 个编成的属性能使分数获得量增加{0}%（最多 +{1}%）",
        "th": "ได้รับคะแนนเพิ่มขึ้น {0}% ต่อคุณสมบัติของนักแสดงที่แตกต่างกัน (สูงสุด {1}%)",
    },
    r"センス発動直後、自身の(?P<status>.+)の\[:param11\]倍のスコアを獲得": {
        "en": "Right After Sense Activation, Gain a Score of [:param11] Times the Actor's own {status}",
        "zh_TW": "Sense 發動後，獲得自身{status} [:param11] 倍的分數",
        "zh_CN": "Sense 发动后，获得自身{status} [:param11] 倍的分数",
        "th": "หลังจากเปิดใช้งานเซนส์จะได้รับคะแนน [:param11] เท่าของ{status}",
    },
    r"センス発動時、追加で「(?P<sense_type>.{2})の光」を(\d+)個獲得する": {
        "ja": "センス発動時、追加で「{sense_type}の光{sense_emoji}」を{1}個獲得する",
        "en": 'When Sense Activates, Gain {1} Additional "{sense_type} Light(s){sense_emoji}"',
        "zh_TW": "Sense 發動時，額外獲得 {1} 個「{sense_type}系光{sense_emoji}」",
        "zh_CN": "Sense 发动时，额外获得 {1} 个「{sense_type}系光{sense_emoji}」",
    },
    r"センス発動時、編成されている(?P<company>.+)アクターの(?P<status>.+?)と(?P<status2>.+?)を、編成されている\1アクターの人数×(\d+)%上昇させる\(この効果は重複する\)": {
        "en": "When Sense Activates, the {status} and {status2} of each {company} Actor in the Unit Increased by the Number of {company} Actors in Unit × {3}% (This Effect can be Stacked)",
        "zh_TW": "Sense 發動時，{company}演員的 {status} 及 {status2} 提升隊伍內{company}演員人數 × {3}% (此效果可疊加)",
        "zh_CN": "Sense 發動時，{company}演员的 {status} 及 {status2} 提升队伍内{company}演员人数 × {3}% (此效果可叠加)",
    },
})



def sense_translator(description: str, message: MsgInt) -> str:
    import re
    # remove size tag
    description = re.sub(
        r"<size=\d+[%％]?>(.+?)<\/size>",
        r"\1",
        description
    )
    return "／".join([
        single_sense_translator(part, message)
    for part in description.strip().split("／")])

single_leader_sense_translator = regex_lookup_translator_wrapper("single_leader_sense_translator", {}, {
    r"「(.+?)」カテゴリの(?P<status>.+?)(\d+)[%％]上昇・(?P<status2>.+?)(が?)(\d+)[%％]上昇": {
        "en": 'Category "{0}" {status} Increased by {2}%, {status2} Increased by {5}%',
        "zh_TW": "「{0}」分類的{status}提升 {2}%・{status2}提升 {5}%",
        "zh_CN": "「{0}」分类的{status}提升 {2}%・{status2}提升 {5}%",
    },
    r"「(.+?)」カテゴリの(?P<status>.+?)(が?)(\d+)[%％]上昇": {
        "en": 'Category "{0}" {status} Increased by {3}%',
        "zh_TW": "「{0}」分類的{status}提升 {3}%",
        "zh_CN": "「{0}」分类的{status}提升 {3}%",
    },
    r"「(.+?)」カテゴリを持つアクターの数に応じて初期プリンシパルゲージが(\d+)上昇": {
        "en": 'Initial Principal Gauge Increased by {1} for each actor having Category "{0}"',
        "zh_TW": "根據持有「{0}」分類的演員數量，初始 Principal Gauge 各提升 {1}",
        "zh_CN": "根据持有「{0}」分类的演员数量，初始 Principal Gauge 各提升 {1}",
    },
    r"「(.+?)」カテゴリのCTを(\d+)秒短縮する": {
        "en": 'Category "{0}" CT Reduced by {1}s',
        "zh_TW": "「{0}」分類的 CT 縮短 {1} 秒",
        "zh_CN": "「{0}」分类的 CT 缩短 {1} 秒",
    }
})

def leader_sense_translator(description: str, message: MsgInt) -> str:
    return "\n".join([
        single_leader_sense_translator(part, message)
    for part in description.strip().replace("\t", "").replace("、「", "\n「").split("\n")])

bloom_translator = regex_lookup_translator_wrapper("bloom_translator", {
    "公演開始時に自身と同系統の光を獲得": {
        "en": "When the Performance Starts, Gain a Light with the same System as oneself",
        "zh_TW": "公演開始時，獲得與自身同系統的光",
        "zh_CN": "公演开始时，获得与自身同系统的光",
    }
}, {
    r"演技力(\d+)[%％]UP": {
        "en": "Status {}% UP",
        "zh": "演技力 {}% UP",
        "th": "การแสดงเพิ่มขึ้น {}%",
    },
    r"演技力上限が(\d+)%上昇": {
        "en": "Status Cap increased by {}%",
        "zh": "演技力上限提升 {}%",
        "th": "ความสามารถการแสดงสูงสุด {}%",
    },
    r"センスのCTが(\d+)秒減少": {
        "en": "Sense CT Reduced by {}s",
        "zh": "Sense 的 CT 減少{}秒",
        "th": "CT ลดลง {} วินาที",
    },
    r"基礎スコアが(\d+)％上昇": {
        "en": "Base Score Increased by {}%",
        "zh_TW": "基礎分數提升 {}%",
        "zh_CN": "基础分数提升 {}%",
        "th": "คะแนนพื้นฐานเพิ่มขึ้น {}%",
    },
    r"基礎ステータスの(?P<status>.+)が(\d+)上昇": {
        "en": "Base {status} Increased by {1}",
        "zh_TW": "基礎{status}提升 {1}",
        "zh_CN": "基础{status}提升 {1}",
        "th": "สถานะ{status}พื้นฐานเพิ่มขึ้น {1}",
    },
    r"初期ライフが(\d+)上昇": {
        "en": "Initial Life Increased by {}",
        "zh": "起始生命值提升 {}",
        "th": "เลือดเริ่มต้นเพิ่มขึ้น {}",
    },
    r"初期プリンシパルゲージが(\d+)上昇": {
        "en": "Initial Principal Gauge Increased by {}",
        "zh": "起始 Principal Gauge 提升 {}",
        "th": "Principal gauge เริ่มต้นเพิ่มขึ้น {}",
    },
    r"公演での報酬量が(\d+)％上昇": {
        "en": "Live Rewards Increased by {}%",
        "zh_TW": "公演報酬量提升 {}%",
        "zh_CN": "公演报酬量提升 {}%",
        "th": "ดรอปไอเทมเพิ่มขึ้น {}%",
    },
    r"スターアクト発動に必要な(?P<sense_type>.{2})の光の個数が(\d+)個減少": {
        "ja": "スターアクト発動に必要な{sense_type}の光「{sense_emoji}」の個数が{1}個減少",
        "en": "Number of {sense_type} Lights ({sense_emoji}) Required to Trigger Star Act Reduced by {1}",
        "zh_TW": "Star Act 發動所需的{sense_type}系光「{sense_emoji}」數量減少 {1} 個",
        "zh_CN": "Star Act 发动所需的{sense_type}系光「{sense_emoji}」数量减少 {1} 个",
        "th": "จำนวน{sense_type} ({sense_emoji}) ที่ใช้ในการเปิด Star Act ลดลง {1} ดวง",
    },
    r"公演開始時、ライフガードを(\d+)付与": {
        "en": "When the Performance Starts, Attach {} Life Guard(s)",
        "zh_TW": "公演開始時，給予 {} 個 Life Guard",
        "zh_CN": "公演开始时，给予 {} 个 Life Guard",
        "th": "เมื่อเริ่มเพลงจะได้ Life Guard {} ครั้ง",
    },
    r"(?P<sense_type>.{2})の光追加": {
        "ja": "{sense_type}の光「{sense_emoji}」追加",
        "en": "Additional {sense_type} Light ({sense_emoji})",
        "zh": "追加{sense_type}系光「{sense_emoji}」",
    },
    r"公演開始時に(?P<sense_type>.{2})の光を獲得": {
        "ja": "公演開始時に{sense_type}の光「{sense_emoji}」を獲得",
        "en": "When the Performance Starts, Gain {sense_type} Light ({sense_emoji})",
        "zh_TW": "公演開始時，獲得{sense_type}系光「{sense_emoji}」",
        "zh_CN": "公演开始时，获得{sense_type}系光「{sense_emoji}」",
    },
})

condition_text_translator = regex_lookup_translator_wrapper("condition_text_translator", {
    "発動条件：": {
        "en": "Activation Condition: ",
        "zh_TW": "發動條件：",
        "zh_CN": "发动条件：",
        "th": "เงื่อนไข: ",
    },
})

condition_translator = regex_lookup_translator_wrapper("condition_translator", {}, {
    "(?P<companies>.+)に所属するアクターが装備": {
        "en": "Equipped by a(n) {companies} actor",
        "zh_TW": "由{companies}演員裝備",
        "zh_CN": "由{companies}演员装备",
        "th": "นักแสดง {companies} เท่านั้น",
    },
    r"<color=#(.{6})>(?P<attribute>.)属性<\/color>のアクターが装備": {
        "ja": "{attribute_emoji} {attribute}属性のアクターが装備",
        "en": "Equipped by an Actor of {attribute_emoji} {attribute} Attribute",
        "zh_TW": "由 {attribute_emoji} {attribute}屬性演員裝備",
        "zh_CN": "由 {attribute_emoji} {attribute}属性演员装备",
        "th": "นักแสดงที่มีคุณสมบัติ {attribute_emoji} {attribute} เท่านั้น",
    },
    "(?P<attribute>.)属性のアクターが装備": {
        "ja": "{attribute_emoji} {attribute}属性のアクターが装備",
        "en": "Equipped by an Actor of {attribute_emoji} {attribute} Attribute",
        "zh_TW": "由 {attribute_emoji} {attribute}屬性演員裝備",
        "zh_CN": "由 {attribute_emoji} {attribute}属性演员装备",
        "th": "นักแสดงที่มีคุณสมบัติ {attribute_emoji} {attribute} เท่านั้น",
    },
    r"<color=#(.{6})>(?P<attribute>.)属性<\/color>の(?P<actor>.+)が装備": {
        "ja": "{attribute_emoji} {attribute}属性の{actor}が装備",
        "en": "Equipped by {actor} of {attribute_emoji} {attribute} Attribute",
        "zh_TW": "由 {attribute_emoji} {attribute}屬性{actor}裝備",
        "zh_CN": "由 {attribute_emoji} {attribute}属性{actor}装备",
        "th": "การ์ด {actor} ที่มีคุณสมบัติ {attribute_emoji} {attribute} เท่านั้น",
    },
    "(?P<actors>.+)が装備": {
        "en": "Equipped by {actors}",
        "zh_TW": "由{actors}裝備",
        "zh_CN": "由{actors}装备",
        "th": "{actors} เท่านั้น",
    },
    "(?P<actor>.+)が装備かつ(?P<company>.+)に所属しているアクターのみで編成": {
        "en": "Equipped by {actor}, and the Unit only Consists of {company} Actors",
        "zh_TW": "由{actor}裝備且隊伍只由{company}所屬演員組成",
        "zh_CN": "由{actor}装备且队伍只由{company}所属演员组成",
        "th": "ใส่โดย {actor} และต้องมีนักแสดง {company} อยู่ในทีมเท่านั้น",
    }
})

poster_ability_translator = regex_lookup_translator_wrapper("poster_ability_translator", {
    "センス発動直後、その時のスコアの[:param11]％のスコアを獲得": {
        "en": "Right After Sense Activation, Gain a Score of [:param11]% of the Score at That Moment",
        "zh_TW": "Sense 發動後，獲得當時分數 [:param11]% 的分數",
        "zh_CN": "Sense 发动后，获得当时分数 [:param11]% 的分数",
        "th": "หลังจากเปิดใช้งานเซนส์จะได้รับคะแนน [:param11]% ของคะแนนในขณะนั้น",
    },
    "公演開始時、P.ゲージが[:param11]上昇": {
        "en": "When the Performance Starts, P. Gauge Increased by [:param11]",
        "zh_TW": "公演開始時，P. Gauge 提升 [:param11]",
        "zh_CN": "公演开始时，P. Gauge 提升 [:param11]",
        "th": "ในช่วงเริ่มเพลงเพิ่มขีดจำกัดของ Principal gauge จะเพิ่มขึ้น [:param11]",
    },
    "センス発動直後、ライフを[:param11]回復": {
        "en": "Right After Sense Activation, Life Value Recovered by [:param11]",
        "zh_TW": "Sense 發動後，生命值回復 [:param11]",
        "zh_CN": "Sense 发动后，生命值回复 [:param11]",
        "th": "หลังจากเปิดใช้งานเซนส์จะฟื้นฟูเลือด [:param11]",
    },
    "公演開始時、ライフが[:param11]上昇": {
        "en": "When the Performance Starts, Life Value Increased by [:param11]",
        "zh_TW": "公演開始時，生命值提升 [:param11]",
        "zh_CN": "公演开始时，生命值提升 [:param11]",
        "th": "เมื่อเริ่มเพลงจะได้รับเลือดเพิ่ม [:param11]",
    },
    "公演開始時、Pゲージの上限が[:param11]上昇": {
        "en": "When the Performance Starts, P. Gauge Cap Increased by [:param11]",
        "zh_TW": "公演開始時，P. Gauge 的上限值提升 [:param11]",
        "zh_CN": "公演开始时，P. Gauge 的上限值提升 [:param11]",
        "th": "เมื่อเริ่มเพลงเพิ่มขีดจำกัดของ P. Gauge เพิ่มขึ้น [:param11]",
    },
    "P.ゲージの上限が[:param11]上昇": {
        "en": "P. Gauge Cap Increased by [:param11]",
        "zh_TW": "P. Gauge 的上限值提升 [:param11]",
        "zh_CN": "P. Gauge 的上限值提升 [:param11]",
        "th": "เพิ่มขีดจำกัดของ P. Gauge เพิ่มขึ้น [:param11]",
    },
    "センス発動直後、P.ゲージの上限が[:param11]上昇": {
        "en": "Right After Sense Activation, P. Gauge Cap Increased by [:param11]",
        "zh_TW": "Sense 發動後，P. Gauge 的上限值提升 [:param11]",
        "zh_CN": "Sense 发动后，P. Gauge 的上限值提升 [:param11]",
        "th": "หลังจากเปิดใช้งานเซนส์จะเพิ่มขีดจำกัดของ P. Gauge เพิ่มขึ้น [:param11]",
    },
    "センスを発動しなくなるが、自身の演技力が2倍": {
        "en": 'Sense can no Longer Activate, but one\'s own Total Status doubled',
        "zh_TW": "Sense 無法發動，但自身演技力 2 倍",
        "zh_CN": "Sense 无法发动，但自身演技力 2 倍",
        "th": "เซนส์จะไม่ถูกเปิดใช้งานแต่ความสามารถการแสดงจะเพิ่มเป็น 2 เท่า",
    },
    "センス発動時、SP光を追加で付与": {
        "en": 'When Sense Activates, Gain an Additional SP Light',
        "zh_TW": "Sense 發動時，額外獲得 SP 光",
        "zh_CN": "Sense 发动时，额外获得 SP 光",
    },
    "センスで付与する「光」の付与数が[:param11]個増加": {
        "en": "The Number of \"Lights\" Gained by Sense Increased by [:param11]",
        "zh_TW": "自 Sense 獲得的「光」的數量增加 [:param11] 個",
        "zh_CN": "自 Sense 获得的「光」的数量增加 [:param11] 个",
        "th": "จำนวนดาวที่ได้รับจากเซนส์ +[:param11]",
    },
    "公演開始時、ライフガードを[:param11]付与": {
        "en": "When the Performance Starts, Attach [:param11] Life Guard(s)",
        "zh_TW": "公演開始時，給予 [:param11] 個 Life Guard",
        "zh_CN": "公演开始时，给予 [:param11] 个 Life Guard",
        "th": "เมื่อเริ่มเพลงจะได้ Life Guard [:param11] ครั้ง",
    },
}, {
    r"センス発動直後、現在のスコアの\[:param11\][%％]のスコアを獲得": {
        "en": "Right After Sense Activation, Gain a Score of [:param11]% of the Current Score",
        "zh_TW": "Sense 發動後，獲得目前分數 [:param11]% 的分數",
        "zh_CN": "Sense 发动后，获得目前分数 [:param11]% 的分数",
        "th": "หลังจากเปิดใช้งานเซนส์จะได้รับคะแนน [:param11]% ของคะแนนปัจจุบัน",
    },
    r"<color=#.{6}>(?P<attribute>.)属性<\/color>のアクターの演技力が\[:param11\]([%％])上昇": {
        "ja": "{attribute_emoji} {attribute}属性のアクターの演技力が[:param11]{1}上昇",
        "en": "Total Status of Actors with {attribute_emoji} {attribute} Attribute Increased by [:param11]%",
        "zh_TW": "{attribute_emoji} {attribute}屬性演員的演技力提升[:param11]%",
        "zh_CN": "{attribute_emoji} {attribute}属性演员的演技力提升[:param11]%",
        "th": "การแสดงของนักแสดงที่มีคุณสมบัติ {attribute_emoji} {attribute} เพิ่มขึ้น [:param11] %",
    },
    r"公演開始時、(?P<sense_type>.{2})系の光「<color=#.{6}>\*<\/color>」を\[:param11\](個?)付与（効果は公演開始時1回のみ発動する）": {
        "ja": "公演開始時、{sense_type}系の光「{sense_emoji}」を[:param11]{1}付与（効果は公演開始時1回のみ発動する）",
        "en": "When the Performance Starts, Attach [:param11] {sense_type} Light(s) ({sense_emoji}) (The Effect only Activates once when the Performance Starts)",
        "zh_TW": "公演開始時，給予 [:param11] 個{sense_type}系光「{sense_emoji}」（效果僅於公演開始時發動 1 次）",
        "zh_CN": "公演开始时，给予 [:param11] 个{sense_type}系光「{sense_emoji}」（效果仅于公演开始时发动 1 次）",
        "th": "เมื่อเริ่มเพลงจะได้รับ{sense_type} ({sense_emoji}) [:param11] ดวง",
    },
    r"公演開始時、SP光を\[:param11\](個?)付与": {
        "en": "When the Performance Starts, Attach [:param11] SP Light(s)",
        "zh_TW": "公演開始時，給予 [:param11] 個 SP 光",
        "zh_CN": "公演开始时，给予 [:param11] 个 SP 光",
        "th": "เมื่อเริ่มเพลงจะได้รับดาว SP [:param11] ดวง",
    },
    r"公演開始時、SP光を\[:param11\](個?)付与（効果は公演開始時1回のみ発動する）": {
        "en": "When the Performance Starts, Attach [:param11] SP Light(s) (The Effect only Activates once when the Performance Starts)",
        "zh_TW": "公演開始時，給予 [:param11] 個 SP 光（效果僅於公演開始時發動 1 次）",
        "zh_CN": "公演开始时，给予 [:param11] 个 SP 光（效果仅于公演开始时发动 1 次）",
        "th": "เมื่อเริ่มเพลงจะได้รับดาว SP [:param11] ดวง",
    },
    r"センス発動時、(?P<sense_type>.{2})系の光「<color=#.{6}>\*<\/color>」を追加で\[:param11\]個付与": {
        "ja": "センス発動時、{sense_type}系の光「{sense_emoji}」を追加で[:param11]個付与",
        "en": 'When Sense Activates, Gain [:param11] Additional "{sense_type} Light(s){sense_emoji}"',
        "zh_TW": "Sense 發動時，獲得額外 [:param11] 個「{sense_type}系光{sense_emoji}」",
        "zh_CN": "Sense 发动时，获得额外 [:param11] 个「{sense_type}系光{sense_emoji}」",
    },
    r"(?P<company>.+)または(?P<company2>.+)に所属するアクターの(?P<status>.+?)が\[:param11\][%％]上昇": {
        "en": "{status} of {company} or {company2} Actors Increased by [:param11]%",
        "zh_TW": "{company} 或 {company2} 演員的 {status} 提升[:param11]%",
        "zh_CN": "{company} 或 {company2} 演员的 {status} 提升[:param11]%",
        "th": "{status} {company} หรือ {company2} เพิ่มขึ้น [:param11] %",
    },
    r"(?P<company>.+)に所属するアクターの(?P<status>.+?)が\[:param11\][%％]上昇": {
        "en": "{status} of {company} Actors Increased by [:param11]%",
        "zh_TW": "{company}演員的 {status} 提升[:param11]%",
        "zh_CN": "{company}演员的 {status} 提升[:param11]%",
        "th": "{status} {company} เพิ่มขึ้น [:param11] %",
    },
    r"(?P<company>.+)に所属しているアクターのみで編成している場合、追加で全アクターの(?P<status>.+?)が\[:param11\]％上昇": {
        "en": "When the Unit only Consists of {company} Actors, {status} of All Actors Increased Additionally by [:param11]%",
        "zh_TW": "當隊伍只由{company}所屬演員組成時，全部演員的 {status} 額外提升[:param11]%",
        "zh_CN": "当队伍只由{company}所属演员组成时，全部演员的 {status} 额外提升[:param11]%",
        "th": "หากจัดทีมด้วย {company} เท่านั้น {status}ทุกคนจะเพิ่มขึ้น [:param11]%",
    },
    r"(?P<company>.+)に所属しているアクターのみで編成している場合、追加で(?P<status>.+?)が\[:param11\]％上昇": {
        "en": "When the Unit only Consists of {company} Actors, {status} Increased Additionally by [:param11]%",
        "zh_TW": "當隊伍只由{company}所屬演員組成時，{status} 額外提升[:param11]%",
        "zh_CN": "当队伍只由{company}所属演员组成时，{status} 额外提升[:param11]%",
        "th": "หากจัดทีมด้วย {company} เท่านั้น {status}จะเพิ่มขึ้น [:param11]%",
    },
    r"全アクターの演技力が\[:param11\][%％]上昇": {
        "en": "Total Status of All Actors Increased by [:param11]%",
        "zh_TW": "全部演員的演技力提升[:param11]%",
        "zh_CN": "全部演员的演技力提升[:param11]%",
        "th": "การแสดงของนักแสดงทุกคนเพิ่มขึ้น [:param11] %",
    },
    r"自身のセンスのCT[がを]\[:param11\]秒短縮": {
        "en": "CT of one's Sense Reduced by [:param11]s",
        "zh_TW": "自身的 Sense 的 CT 縮短 [:param11] 秒",
        "zh_CN": "自身的 Sense 的 CT 缩短 [:param11] 秒",
        "th": "CT เซนส์ลดลง [:param11] วินาที",
    },
    r"自身の(?P<status>.+?)が\[:param11\][%％]上昇": {
        "en": "One's {status} Increased by [:param11]%",
        "zh": "自身的{status}提升 [:param11]%",
        "th": "{status}ของตัวเองเพิ่มขึ้น [:param11] %",
    },
    r"編成されている属性数が多いほど自身の(?P<status>.+?)が上昇（4属性：\[:param11\][%％]／3属性：\[:param21\][%％]／2属性：\[:param31\][%％]／1属性：\[:param41\][%％]）": {
        "en": "The more Attributes there are in the Unit, the more One's {status} is Increased (4 Attributes: [:param11]% / 3 Attributes: [:param21]% / 2 Attributes: [:param31]% / 1 Attribute: [:param41]%)",
        "zh_TW": "編成的屬性數量愈多，自身的{status}上升愈多（4屬性：[:param11]%／3屬性：[:param21]%／2屬性：[:param31]%／1屬性：[:param41]%）",
        "zh_CN": "编成的属性数量愈多，自身的{status}上升愈多（4属性：[:param11]%／3属性：[:param21]%／2属性：[:param31]%／1属性：[:param41]%）",
        "th": "ยิ่งคุณสมบัตินักแสดงแตกต่างกัน ความสามารถ{status}ยิ่งสูงขึ้น (4 คุณสมบัติ: [:param11]% / 3 คุณสมบัติ: [:param21]% / 2 คุณสมบัติ: [:param31]% / 1 คุณสมบัติ: [:param41]%)",
    },
    r"編成されている属性数が少ないほど自身の(?P<status>.+?)が上昇（1属性：\[:param11\][%％]／2属性：\[:param21\][%％]／3属性：\[:param31\][%％]／4属性：\[:param41\][%％]）　*": {
        "en": "The fewer Attributes there are in the Unit, the more One's {status} is Increased (1 Attribute: [:param11]% / 2 Attributes: [:param21]% / 3 Attributes: [:param31]% / 4 Attributes: [:param41]%)",
        "zh_TW": "編成的屬性數量愈少，自身的{status}上升愈多（1屬性：[:param11]%／2屬性：[:param21]%／3屬性：[:param31]%／4屬性：[:param41]%）",
        "zh_CN": "编成的属性数量愈少，自身的{status}上升愈多（1属性：[:param11]%／2属性：[:param21]%／3属性：[:param31]%／4属性：[:param41]%）",
        "th": "ยิ่งคุณสมบัตินักแสดงแตกต่างกัน ความสามารถ{status}ยิ่งต่ำลง (1 คุณสมบัติ: [:param11]% / 2 คุณสมบัติ: [:param21]% / 3 คุณสมบัติ: [:param31]% / 4 คุณสมบัติ: [:param41]%)",
    },
    r"公演開始時、ライフが(\d+)上昇": {
        "en": "When the Performance Starts, Life Value Increased by {}",
        "zh_TW": "公演開始時，生命值提升 {}",
        "zh_CN": "公演开始时，生命值提升 {}",
        "th": "เมื่อเริ่มเพลงจะได้รับเลือดเพิ่ม {}",
    },
    r"公演開始時、ライフを(\d+)回復": {
        "en": "When the Performance Starts, Life Value Recovered by {}",
        "zh_TW": "公演開始時，生命值回復 {}",
        "zh_CN": "公演开始时，生命值回复 {}",
        "th": "เมื่อเริ่มเพลงจะฟื้นฟูเลือดเพิ่ม {}",
    },
    r"公演開始時、ライフを(\d+)減少": {
        "en": "When the Performance Starts, Life Value Reduced by {}",
        "zh_TW": "公演開始時，生命值減少 {}",
        "zh_CN": "公演开始时，生命值減少 {}",
        "th": "เมื่อเริ่มเพลงเลือดจะลดลง {}",
    },
    r"センス発動直後、自身の(?P<status>.+?)の\[:param11\]倍のスコアを獲得": {
        "en": "Right After Sense Activation, Gain a Score of [:param11] Times one's own {status}",
        "zh_TW": "Sense 發動後，獲得自身{status} [:param11] 倍的分數",
        "zh_CN": "Sense 发动后，獲得自身{status} [:param11] 倍的分数",
        "th": "หลังจากเปิดใช้งานเซนส์จะได้รับคะแนน [:param11] ของ{status}",
    },
    r"センス発動直後、P(\.?)ゲージを\[:param11\]獲得": {
        "en": "Right After Sense Activation, Gain [:param11] P. Gauge",
        "zh_TW": "Sense 發動後，獲得 [:param11] P. Gauge",
        "zh_CN": "Sense 发动后，獲得 [:param11] P. Gauge",
        "th": "หลังจากเปิดใช้งานเซนส์จะได้รับ P. Gauge [:param11]",
    },
    r"プリンシパルゲージの上限を(\d+)上昇": {
        "en": "Principal Gauge Cap Increased by {}",
        "zh_TW": "Principal Gauge 的上限值提升 {}",
        "zh_CN": "Principal Gauge 的上限值提升 {}",
        "th": "เมื่อเริ่มเพลงปริมาณ Principal gauge สูงสุดจะเพิ่มขึ้น {}",
    },
    r"センスによるP.ゲージの獲得量が\[:param11\][%％]UP": {
        "en": "The Amount of P. Gauge Gained by Sense [:param11]% UP",
        "zh_TW": "自 Sense 獲得的 P. Gauge 量 [:param11]%UP",
        "zh_CN": "自 Sense 获得的 P. Gauge 量 [:param11]%UP",
        "th": "ปริมาณ P. gauge ที่ได้รับจากเซนส์เพิ่มขึ้น [:param11] %",
    },
    r"公演開始時、ライフガード（(\d+)回）を付与": {
        "en": "When the Performance Starts, Attach Life Guard(s) ({} Times)",
        "zh_TW": "公演開始時，給予 Life Guard（{} 次）",
        "zh_CN": "公演开始时，给予 Life Guard（{} 次）",
        "th": "เมื่อเริ่มเพลงจะได้ Life Guard {} ครั้ง",
    },
    r"公演と協力公演の公演報酬が\[:param11\][%％]増加（アクセサリーを除く）": {
        "en": "Rewards from Performances and Multi-player Performances Increased by [:param11]% (Except Accessories)",
        "zh_TW": "公演及協力公演的公演報酬增加[:param11]%（飾品除外）",
        "zh_CN": "公演及协力公演的公演报酬增加[:param11]%（饰品除外）",
        "th": "จำนวนไอเทมที่ได้รับจากการแสดงโซโล่และมัลติเพิ่มขึ้น [:param11] % ( ไม่รวม Accessory )",
    },
})

accessory_effect_translator = regex_lookup_translator_wrapper("accessory_effect_translator", {
    "公演開始時、ライフが[:param1]上昇": {
        "en": "When the Performance Starts, Life Value Increased by [:param1]",
        "zh_TW": "公演開始時，生命值提升 [:param1]",
        "zh_CN": "公演开始时，生命值提升 [:param1]",
        "th": "เมื่อเริ่มเพลงจะได้รับเลือดเพิ่ม [:param1]",
    },
    "センス発動により光を付与するとき、同系統の光を追加で1個付与する。": {
        "en": "When Lights are Attached by Sense Activation, Attach 1 additional Light of the same System",
        "zh_TW": "當 Sense 發動給予光的時候，額外給予 1 個同系統的光",
        "zh_CN": "当 Sense 发动给予光的时候，额外给予 1 个同系统的光",
        "th": "จำนวนดาวที่ได้รับจากเซนส์ +1",
    },
    "基礎スコアが[:param1]％上昇": {
        "en": "Base Score Increased by [:param1]%",
        "zh_TW": "基礎分數提升 [:param1]%",
        "zh_CN": "基础分数提升 [:param1]%",
        "th": "คะแนนพื้นฐานเพิ่มขึ้น [:param1]%",
    },
}, {
    r"自身の(?P<status>.+?)が?\[:param1\]上昇": {
        "en": "One's {status} Increased by [:param1]",
        "zh": "自身的{status}提升 [:param1]",
        "th": "{status}ของตัวเองเพิ่มขึ้น [:param1]",
    },
    r"自身の(?P<status>.+?)が?\[:param1\][%％]上昇": {
        "en": "One's {status} Increased by [:param1]%",
        "zh": "自身的{status}提升 [:param1]%",
        "th": "{status}ของตัวเองเพิ่มขึ้น [:param1]%",
    },
    r"自身のセンスのCTが\[:param1\]秒短縮": {
        "en": "CT of one's Sense Reduced by [:param1]s",
        "zh_TW": "自身的 Sense 的 CT 縮短 [:param1] 秒",
        "zh_CN": "自身的 Sense 的 CT 缩短 [:param1] 秒",
        "th": "CT เซนส์ลดลง [:param1] วินาที",
    },
    r"初期プリンシパルゲージが\[:param1\]上昇": {
        "en": "Initial Principal Gauge Increased by [:param1]",
        "zh": "起始 Principal Gauge 提升 [:param1]",
        "th": "Principal gauge เริ่มต้นเพิ่มขึ้น [:param1]",
    },
    r"公演と協力公演の公演報酬が\[:param1\][%％]増加（アクセサリーを除く）": {
        "en": "Rewards from Performances and Multi-player Performances Increased by [:param1]% (Except Accessories)",
        "zh_TW": "公演及協力公演的公演報酬增加[:param1]%（飾品除外）",
        "zh_CN": "公演及协力公演的公演报酬增加[:param1]%（饰品除外）",
        "th": "จำนวนไอเทมที่ได้รับจากการแสดงโซโล่และมัลติเพิ่มขึ้น [:param1] % ( ไม่รวม Accessory )",
    },
    r"公演開始時、「SP光」を\[:param1\]付与（SP光はどの系統の光としても扱われる）": {
        "en": "When the Performance Starts, Attach [:param1] \"SP Light(s)\" (SP Light(s) can be treated as Light(s) of any system)",
        "zh_TW": "公演開始時，給予 [:param1] 個「SP 光」（SP 光能被視為任何系統的光）",
        "zh_CN": "公演开始时，给予 [:param1] 个「SP 光」（SP 光能被视为任何系统的光）",
        "th": "มื่อเริ่มเพลงจะได้รับดาว SP สีไหนก็ได้ [:param1] ดวง",
    },
    r"センスによるP.ゲージの獲得量が\[:param1\][%％]UP": {
        "en": "The Amount of P. Gauge Gained by Sense [:param1]% UP",
        "zh_TW": "自 Sense 獲得的 P. Gauge 量 [:param1]%UP",
        "zh_CN": "自 Sense 获得的 P. Gauge 量 [:param1]%UP",
        "th": "ปริมาณ P. gauge ที่ได้รับจากเซนส์เพิ่มขึ้น [:param1] %",
    },
})

def full_poster_ability_translator(description: str, message: MsgInt) -> str:
    if "◆発動条件：" in description:
        effect_text, condition_text = description.split("◆発動条件：")
        return poster_ability_translator(effect_text.rstrip("　"), message) + "　◆" + condition_text_translator("発動条件：", message) + condition_translator(condition_text, message)
    else:
        return poster_ability_translator(description, message)

def full_accessory_effect_translator(description: str, message: MsgInt) -> str:
    if "◆発動条件：" in description:
        effect_text, condition_text = description.split("◆発動条件：")
        return accessory_effect_translator(effect_text.rstrip("　"), message) + "　◆" + condition_text_translator("発動条件：", message) + condition_translator(condition_text, message)
    else:
        return accessory_effect_translator(description, message)