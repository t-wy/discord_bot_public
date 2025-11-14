# Put translated FULL name here if it is not the best match
# We have variant character (異[体體]字) matching, so probably need not handle CJK variants (i.e. Japanese Kanji / Korean Hanja / Trad. Chi. / Simp. Chi.)
# Take care of katakana songs which EN version is not yet released.
# If the translated song name can be found in the lyrics, it can also be included.
# "of" reversal may be considered if the Japanese title appears like "AのB" or compound noun "AB" but is translated as "B of A" in EN version (not for JP song with it's original title already in English)
# Reload pjsk.song after reload this file to refresh the cache if needed

# Official Translation References (e.g.):
# - Youtube bilingual title / region-specific title
# - Bilibili Official Upload Title
# - Authorised Derivative Comic / Novel / Book
# - Self-explanatory Lyrics

# Extra Reliable Translation / Abbreviation References (e.g.):
# - https://home.gamer.com.tw/ (Fanmade lyrics translations)
# - https://moegirl.org.cn (Backup: https://moegirl.icu)
#   - https://zh.moegirl.org.cn/世界计划虚拟歌手演唱歌曲/原创歌曲
#   - https://zh.moegirl.org.cn/世界计划虚拟歌手演唱歌曲/原创歌曲2
#   - https://zh.moegirl.org.cn/世界计划虚拟歌手演唱歌曲/原创歌曲3
#   - https://zh.moegirl.org.cn/世界计划虚拟歌手演唱歌曲/收录歌曲 (~4)
#   - https://zh.moegirl.org.cn/Leo/need演唱歌曲/原创歌曲 (~2)
#   - https://zh.moegirl.org.cn/MORE_MORE_JUMP!演唱歌曲/原创歌曲 (~2)
#   - https://zh.moegirl.org.cn/Vivid_BAD_SQUAD演唱歌曲/原创歌曲 (~2)
#   - https://zh.moegirl.org.cn/Wonderlands×Showtime演唱歌曲/原创歌曲 (~2)
#   - https://zh.moegirl.org.cn/25点，Nightcord见。演唱歌曲/原创歌曲 (~2)
#   - https://zh.moegirl.org.cn/世界计划其他歌曲 (~2)
#   - https://zh.moegirl.org.cn/Leo/need演唱歌曲/收录歌曲 (~3)
#   - https://zh.moegirl.org.cn/MORE_MORE_JUMP!演唱歌曲/收录歌曲 (~3)
#   - https://zh.moegirl.org.cn/Vivid_BAD_SQUAD演唱歌曲/收录歌曲 (~3)
#   - https://zh.moegirl.org.cn/Wonderlands×Showtime演唱歌曲/收录歌曲 (~3)
#   - https://zh.moegirl.org.cn/25点，Nightcord见。演唱歌曲/收录歌曲 (~3)
#   - https://zh.moegirl.org.cn/世界计划其他服务器独占歌曲
# - https://pjsekai.fandom.com
# - https://viewer.unipjsk.com/musics/
# - https://assets.unipjsk.com/logs/202511.html (If ever accessible)

# Last Update: Song before 2025-11-01

from typing import *
if TYPE_CHECKING:
    import bot_client

song_alias_list: Dict[int, List[str]] = {
    2: [ # ロキ
        '洛基',
    ],
    3: [ # テオ
        '將手緊握',
    ],
    6: [ # ヒバナ -Reloaded-
        '火花',
    ],
    8: [ # タイムマシン
        "時光機", # well known translation
    ],
    11: [ # ビバハピ
        "匕八八匕",
        "比八哈皮",
        "比八八比",
    ],
    18: [ # アスノヨゾラ哨戒班 (Check WDS 86 Also)
        "Night Sky Patrol of Tomorrow", # Official English Title
        "明日の夜空哨戒班",
        '明日的夜空巡邏班',
    ],
    19: [ # シャルル (Check WDS 152 Also)
        '夏露露',
        '下陸路',
    ],
    21: [ # 脱法ロック
        "脱法 Rock",
        '脱法搖滾',
        '枉法搖滾',
    ],
    22: [ # 命に嫌われている
        '被生命厭惡著',
    ],
    28: [ # ドクター＝ファンクビート
        '不幸癒醫＝恐懼擊敗',
    ],
    36: [ # ミラクルペイント
        '奇蹟畫筆',
        '魔法畫筆',
        '奇蹟筆刷',
    ],
    41: [ # スイートマジック
        '甜蜜魔法',
    ],
    46: [ # グリーンライツ・セレナーデ
        "綠光小夜曲",
        "綠燈小夜曲",
    ],
    47: [
        "融化", # Supercell Album China Official Title
        'メノレト',
        '咩路透',
    ],
    48: [ # ワールドイズマイン
        "世界第一的公主殿下", # Supercell Album Taiwan Title
        "世界屬於我", # Supercell Album China Official Title
    ],
    49: [ # 初音ミクの消失 (THE END OF HATSUNE MIKU)
        "初音ミクの消失 -DEAD END-", # don't let the full name loses similarity score
        "DEAD END", # as in the subtitle of "初音ミクの消失 -DEAD END-"
        "Hatsune Miku's end", # processive noun "of" reversal
        "The Disappearance of Hatsune Miku", # alternative title
        "Hatsune Miku's Disappearance", # processive noun "of" reversal
        '消失',
    ],
    51: [ # セカイはまだ始まってすらいない
        "世界はまだ始まってすらいない", # kanji
        '世界甚至尚未開始',
        '「世界」還沒開始',
    ],
    52: [ # potatoになっていく
        '變成馬鈴薯',
        '變成薯仔',
        '變成土豆',
        '變身馬鈴薯',
        '變身薯仔',
    ],
    60: [ # 悔やむと書いてミライ
        "悔やむと書いて未来", # kanji
    ],
    66: [ # ハロ／ハワユ
        "哈囉/你好嗎", # direct translation
    ],
    68: [ # ダンスロボットダンス
        '跳舞機器人跳舞',
    ],
    69: [ # フラジール
        '易碎',
        '肥宅', # ?
    ],
    70: [ # メルティランドナイトメア
        '惡夢',
    ],
    71: [ # ツギハギスタッカート
        "継ぎ接ぎスタッカート",
        "Tsugihagi Staccato",
        '拼湊出的斷音',
    ],
    72: [ # ブレス・ユア・ブレス
        '祝福你的呼吸',
    ],
    74: [ # 独りんぼエンヴィー
        "エビ",
        "えび",
        "海老",
        "蝦",
        "🦐",
        "孑然妒火",
        "充滿嫉妒的一人捉迷藏",
    ],
    75: [ # ウミユリ海底譚 (Tale of the Deep-sea Lily)
        "Deep-sea Lily Tale", # compound noun "of" reversal
    ],
    77: [ # ワーワーワールド
        '嘩嘩世界',
    ],
    78: [ # ぼうけんのしょがきえました！
        "冒険の書が消えました！",
    ],
    81: [ # 夜咄ディセイブ
        "夜咄 Deceive",
        '夜談欺騙',
    ],
    84: [ # ジャンキーナイトタウンオーケストラ
        '癮者之夜城鎮樂隊',
    ],
    88: [ # チュルリラ・チュルリラ・ダッダッダ！
        '告老師',
    ],
    89: [ # Color of Drops
        '淚滴',
    ],
    90: [ # 限りなく灰色へ
        "向著無限的灰色", # https://www.bilibili.com/video/BV1kyKtzmE9Z/
        "向著無盡之灰",
    ],
    91: [ # ドラマツルギー
        "擬劇論", # Unofficial
    ],
    93: [ # 青く駆けろ！
        '奔跑吧！藍色！',
    ],
    94: [ # とても痛い痛がりたい
        '痛且渴望疼痛',
    ],
    97: [ # 霽れを待つ
        '等待天晴',
    ],
    98: [ # ロストワンの号哭
        "Lost One の号哭",
        '迷失一人的號哭',
        '被遺留一人的號哭',
        '最後一名的號哭',
        '失去一人的號哭',
    ],
    99: [ # モア！ジャンプ！モア！
        '多跳多',
        '更多！跳！更多！',
        '再多！跳！再多！',
    ],
    101: [ # RAD DOGS
        '狗',
    ],
    103: [ # ニジイロストーリーズ
        '虹色故事',
        '虹色Stories',
        '虹色ストーリーズ',
    ],
    104: [ # サンドリヨン 10th Anniversary
        "灰姑娘 十周年", # direct translation to Chinese
        "灰姑娘 10周年", # direct translation to Chinese
    ],
    105: [ # ワンスアポンアドリーム
        '從前的一個夢',
        '曾經的夢想',
    ],
    107: [ # ミルククラウン・オン・ソーネチカ
        '牛奶皇冠',
        '索涅奇卡的牛奶皇冠',
    ],
    108: [ # 愛されなくても君がいる
        '即使不被愛著也沒關係，因為有你在',
    ],
    109: [ # ヒビカセ
        '匕匕力乜',
        '匕匕力也',
    ],
    111: [ # カトラリー
        '餐具',
    ],
    112: [ # 天使のクローバー
        "天使の Clover",
        '天使的四葉草',
    ],
    113: [ # ローリンガール
        "滾女", # ???
        '翻滾少女',
        'Rolling Girl', # in ending
    ],
    114: [ # 裏表ラバーズ
        '裏表情人',
        '表裏情人',
    ],
    115: [ # アンノウン・マザーグース
        '鵝媽媽',
        '不為人知的鵝媽媽童謠',
        '未知鵝媽媽',
    ],
    116: [ # アイディスマイル
        'id',
    ],
    119: [ # ワールズエンド・ダンスホール
        '舞廳',
    ],
    120: [ # いかないで
        '別走',
        '咪走',
    ],
    121: [ # ロミオとシンデレラ
        '羅密歐與灰姑娘',
    ],
    123: [ # どりーみんチュチュ
        '啾啾',
    ],
    124: [ # みくみくにしてあげる♪【してやんよ】
        '把你MIKUMIKU掉♪【MIKU掉喔～】',
        '把你給MIKUMIKU掉♪【MIKU掉喔～】',
    ],
    126: [ # シネマ
        "電影",
        '電影院',
    ],
    127: [ # トンデモワンダーズ
        '不可思議的Wonders',
        '意想不到的wonders',
        '不可思議的奇蹟',
    ],
    129: [ # ビターチョコデコレーション
        '苦巧',
    ],
    130: [ # フロムトーキョー
        '來自東京',
    ],
    131: [ # 初音ミクの激唱 (The Intense Voice of Hatsune Miku)
        "Hatsune Miku's Intense Voice", # processive noun "of" reversal
        '激唱',
    ],
    132: [ # 「１」 (One)
        "1",
    ],
    133: [ # 悪魔の踊り方
        '惡魔的舞蹈方式',
    ],
    134: [ # テレキャスタービーボーイ
        'bboy',
    ],
    136: [ # チルドレンレコード
        "孩童記錄", # Unofficial translation
    ],
    137: [ # 花を唄う
        '歌頌花束',
    ],
    139: [ # 夜に駆ける
        '夜仁駆什歹', # ？？？
    ],
    140: [ # アイスドロップ
        '冰滴',
    ],
    143: [ # トラフィック・ジャム
        '堵車',
        '交通擠塞',
        '交通堵塞',
        '塞車',
    ],
    144: [ # アイノマテリアル
        '愛的材料',
    ],
    145: [ # ベノム
        '猛毒',
    ],
    146: [ # リモコン
        "Remo Con",
    ],
    147: [ # からくりピエロ
        '活動小丑',
    ],
    149: [ # カナデトモスソラ
        '奏響點亮天空',
    ],
    150: [ # トキヲ・ファンカ
        '東京不夜城',
    ],
    152: [ # だれかの心臓になれたなら
        '若能成為某人的心臟的話',
    ],
    153: [ # Miku
        '咪哭',
    ],
    158: [ # ナンセンス文学
        "Nonsense 文学",
        '荒謬文學',
        '廢話文學',
        '屁話文學',
        '無厘頭文學',
    ],
    159: [ # STAGE OF SEKAI
        '「世界」的舞台',
    ],
    160: [ # ショウタイム・ルーラー
        '尺子',
        '開演時刻的支配者',
    ],
    162: [ # エンドマークに希望と涙を添えて
        "End Mark に希望と涙を添えて",
        '希望淚',
    ],
    163: [ # the EmpErroR
        '皇帝',
    ],
    164: [ # Don't Fight The Music
        '別打音樂',
    ],
    165: [ # そうだった！！
        '這樣啊',
        '原來如此',
        '是的是的！！',
    ],
    167: [ # オルターエゴ
        '另我',
    ],
    169: [ # 少女レイ
        '少女靈',
    ],
    170: [ # ヴィラン
        "糜爛", # appeared in lyrics
        "びらん", # pronunciation of the kanji
        "biran", # pronunciation of the kanji
    ],
    171: [ # カゲロウデイズ
        "カゲロウdays",
        "陽炎デイズ",
        "陽炎days",
        "陽炎日",
        'カゲロウdaze',
        '陽炎daze',
        '陽炎眩亂',
    ],
    173: [ # 流星のパルス (Pulse of the Meteor)
        "流星の Pulse",
        "流星的脉搏", # https://www.bilibili.com/video/BV1ZPdfY6Eif/
        "流星的脈動",
        "Meteor Pulse", # compound noun "of" reversal
        '流星Pulse',
    ],
    174: [ # いーあるふぁんくらぶ (Check WDS 176 Also)
        '1 2 粉絲俱樂部',
        '一二粉絲俱樂部',
    ],
    175: [ # 拝啓ドッペルゲンガー
        "拝啓 Doppelganger",
        '敬啟分身',
        '敬啟 我的分身',
    ],
    176: [ # マシンガンポエムドール
        "機關槍", # Common chinese abbreviation
    ],
    177: [ # 右肩の蝶
        '右肩之蝶',
    ],
    178: [ # にっこり^^調査隊のテーマ (Theme of Niccori Survey Team)
        "にっこり^^調査隊の Theme",
        "Niccori Survey Team Theme", # compound noun "of" reversal
        "Niccori", # short match
        "Nikkori", # short match
        '笑容滿面^^調查隊的主題曲',
    ],
    181: [ # 愛して愛して愛して
        '愛我愛我愛我',
        '深愛著深愛著深愛著',
    ],
    186: [ # 初音天地開闢神話
        '開天闢地',
    ],
    187: [ # ロウワー (Lower)
        "Lower", # EN name: Lower one's eyes (Lost One's Weeping steal the best match)
    ],
    189: [ # ノマド
        '游牧者',
        '流浪者',
        '游居者',
    ],
    190: [ # 悪ノ娘 (The Daughter of Evil)
        "The Evil Daughter", # processive noun "of" reversal
        '惡之娘',
    ],
    191: [ # 悪ノ召使 (The Servant of Evil)
        "The Evil Servant", # processive noun "of" reversal
        '惡之召使',
    ],
    192: [ # 去り人達のワルツ (Waltz of the Deceased)
        "the Deceased's Waltz", # processive noun "of" reversal
        '去人達',
        '離去之人們的華爾滋',
    ],
    193: [ # ワールドワイドワンダー
        "World Wide Wonder", # as Worldwide is a single word in Japanese
        'www', # beware of wah-wah world
        '世界環遊',
    ],
    194: [ # 妄想感傷代償連盟
        "Delusion Sentiment Compensation Federation", # Only DSCF in EN Server
    ],
    195: [ # PaⅢ.SENSATION
        'passionate three dot sensation',
    ],
    196: [ # オーダーメイド
        "Ordermade",
        "Order Made",
    ],
    197: [ # ラストスコア
        '最後的總譜',
    ],
    198: [ # グッバイ宣言
        "Goodbye 宣言",
        "Good Bye 宣言",
        "再見宣言",
    ],
    199: [ # ゴーストルール
        "幽靈法則",
        "鬼法",
    ],
    200: [ # ガランド
        '傻瓜',
    ],
    201: [ # 神のまにまに
        '隨神之側',
        '神錢錢',
        '神的隨之任之',
    ],
    203: [ # トリコロージュ
        '特等俘虜',
    ],
    204: [ # うっせぇわ
        '吵死了',
    ],
    206: [ # 君色マリンスノウ
        "君色 Marine Snow",
    ],
    208: [ # 僕らまだアンダーグラウンド
        "僕らまだ Underground",
        '我們仍位於地面之下',
    ],
    210: [ # 雨とペトラ
        "雨と Petra",
    ],
    211: [ # イフ
        '衣服', # ？
        '依附', # ？
        '義父', # ？
        '姨夫', # ？
        '伊芙', # ？
    ],
    212: [ # 星空のメロディー
        "星空の Melody",
    ],
    214: [ # パレットには君がいっぱい
        "Palette には君がいっぱい",
        '調色盤上裝滿了你',
    ],
    216: [ # ルカルカ★ナイトフィーバー
        '流歌流歌★晚上發燒',
        '流歌流歌★晚上狂熱',
        '流歌流歌★深夜狂熱',
    ],
    219: [ # 砂の惑星
        '砂之行星',
    ],
    220: [ # ドーナツホール 2024
        '甜甜圈洞',
    ],
    221: [ # マトリョシカ
        '俄羅斯套娃',
    ],
    222: [ # ピアノ×フォルテ×スキャンダル
        '凌亂不堪的鋼琴現場',
    ],
    225: [ # エゴロック
        '自我搖滾',
    ],
    226: [ # ロストエンファウンド
        "大臉", # Popular alias
        "你排名掉了", # Popular alias
        '失物招領',
    ],
    229: [ # 脳漿炸裂ガール
        "脳漿炸裂 Girl",
        '脳漿炸裂女孩',
    ],
    230: [ # サラマンダー
        "沙羅曼蛇",
        '火蠑螈',
    ],
    232: [ # 青色絵具
        '蔚藍畫具',
    ],
    233: [ # コスモスパイス
        '宇宙辛香料',
    ],
    234: [ # 徳川カップヌードル禁止令
        "徳川 Cup Noodle 禁止令",
        '德川杯麵禁止令',
    ],
    235: [ # Journey
        '旅行',
        '旅途',
    ],
    237: [ # 君の夜をくれ
        '給我你的夜晚',
    ],
    238: [ # ブラック★ロックシューター
        "黑岩★射手", # Supercell Album China Official Title
    ],
    240: [ # 踊れオーケストラ
        "踊れOrchestra",
        '起舞吧管弦樂',
    ],
    241: [ # アサガオの散る頃に (Removed)
        "アサガオの散る頃に",
        "あさがおのちるころに",
        "Asagao no Chiru Koro ni",
        "When the Morning Glory Falls",
        "牽牛花凋謝之時",
    ],
    242: [ # トリノコシティ
        '孤雛市',
    ],
    244: [ # Awake Now
        '醒醒',
    ],
    245: [ # 阿吽のビーツ
        "阿吽の Beats",
        '阿吽的節拍',
        '契合的節奏',
        '契合的節拍',
        '阿吽的節奏',
    ],
    246: [ # エイリアンエイリアン
        "外星人",
    ],
    248: [ # バグ
        "故障", # translation
        "八股", # common abbreviation
    ],
    250: [ # 腐れ外道とチョコレゐト
        "腐れ外道と Chocolate",
        '腐敗的邪門歪道與巧克力',
    ],
    251: [ # フロイライン＝ビブリォチカ
        "Fraulein=Biblioteca",  # Fräulein=библиотека in EN Server
    ],
    253: [ # DAYBREAK FRONTLINE (Check WDS 72 Also)
        '黎明前線',
    ],
    255: [ # 夜もすがら君想ふ
        "夜裡也始終想著你",
        '夜裡也一直想著你',
    ],
    256: [ # ダブルラリアット
        '雙重套索踢',
    ],
    257: [ # てらてら
        '熠熠闪光',
    ],
    260: [ # ラブカ？
        '是愛嗎？',
        '皺鰓鯊？',
    ],
    261: [ # 星屑ユートピア
        "星屑 Utopia",
        '星屑烏托邦',
        '星屑下的理想鄉',
    ],
    266: [ # YY
        "丫丫",
        "ㄚㄚ",
    ],
    269: [ # ロンリーユニバース
        '孤獨宇宙',
    ],
    270: [ # 泥中に咲く
        '在泥濘中綻放',
        '花出淤泥',
    ],
    271: [ # あったかいと
        '暖暖KAITO',
    ],
    272: [ # ジェヘナ (Gehenna)
        "גיא בן הינום",
        "γέεννα",
        "ゲヘナ",
        "ヒンノムの谷",
        "欣嫩子谷",
        "火の池",
        "煉獄",
        "地獄", # New testament translation
    ],
    273: [ # フューチャー・イヴ
        '未來前夜',
    ],
    274: [ # それでもいいんだよ
        '即使是那樣也沒關係的',
        '即便如此也沒關係',
    ],
    275: [ # パラジクロロベンゼン
        "Benzene", # Paradichlorobenzene is too long that Benzene get matched to Bad End Night (BEN)
    ],
    277: [ # フォニイ (Check WDS 34 Also)
        '佛你',
    ],
    280: [ # 虚ろを扇ぐ
        '扇動虛空',
    ],
    281: [ # 気まぐれメルシィ
        "気まぐれ Mercy",
        "3D大臉", # Popular alias
        '反覆無常的寬赦',
        '隨心所欲的寬赦',
        '反覆無常Mercy',
    ],
    282: [ # 星空オーケストラ
        "星空Orchestra",
        "星空管弦樂",
        "星空交響樂團", # https://www.bilibili.com/video/BV1T8411P7Bu/
        '星空管弦樂團',
    ],
    285: [ # ÅMARA(大未来電脳)
        "AMARA", # without bracket or character modifiers
        "大未来電脳", # only bracket contents
    ],
    290: [ # どんな結末がお望みだい？ (Removed)
        "どんな結末がお望みだい？",
        "どんなけつまつがおのぞみだい?",
        "Donna Ketsu Matu ga Onozomidai?",
        "What Sort of Ending Are You Wishing For?",
        "你期望著怎樣的結局？",
    ],
    291: [ # フェレス
        '菲蜆蝶',
    ],
    292: [ # いちにのさんで
        "一二の三で",
        "1 2の3で",
        '從一到三',
    ],
    294: [ # それがあなたの幸せとしても
        '即便那就是你的幸福',
        '即使這就是你的幸福',
    ],
    295: [ # フロート・プランナー
        '空姐',
    ],
    296: [ # カンタレラ
        "坎特雷拉", # Unofficial
    ],
    298: [ # ネトゲ廃人シュプレヒコール
        "Net Game 廃人 Sprechchor",
        '網路遊戲廢人合唱曲',
    ],
    299: [ # エゴイスト
        "利己主義", # JP term
        "利己主義者", # literal translation
    ],
    300: [ # ザムザ
        '炸母炸',
        '薩姆沙',
    ],
    301: [ # 私の恋はヘルファイア
        "私の恋は Hellfire",
        "私の恋は Hell Fire",
        '我的戀情是hellfire',
        '我的戀情是地獄的業火',
        '地獄火',
    ],
    303: [ # リンちゃんなう！
        '鈴醬鬧',
        'rinchan',
        'rin',
    ],
    304: [ # Iなんです
        '這就是I',
    ],
    308: [ # ももいろの鍵
        '桃色鑰匙',
        '粉紅色鑰匙',
        '桃色鎖匙',
    ],
    311: [ # 夜明けと蛍
        '黎明與螢火蟲',
    ],
    314: [ # 陽だまりのセツナ
        "陽黙りの刹那", # kanji
        "向陽處的剎那", # some chinese translaton
        '向陽的那瞬間',
    ],
    316: [ # ひつじがいっぴき
        "羊が一匹",
        "一匹羊",
        "一隻羊",
    ],
    317: [ # 魔法みたいなミュージック！
        "魔法みたいな Music ！",
        '音樂就像魔法一樣！',
        '像是魔法一般的音樂！',
    ],
    322: [ # 絶え間なく藍色
        '無盡的藍色',
    ],
    324: [ # 箱庭のコラル
        "箱庭の Coral",
        '箱庭的珊瑚',
    ],
    326: [ # 天使の翼。
        '天使的翼',
        '天使之翼。',
    ],
    328: [ # 星界ちゃんと可不ちゃんのおつかい合騒曲
        '星界ちゃんと可不ちゃんのおつかい合奏曲',
        '星界ちゃん與可不ちゃん的跑腿合奏曲',
        '星界醬和可不醬的採購合奏曲',
        '星界醬和可不醬的跑腿合奏曲',
    ],
    329: [ # ヤミナベ!!!!
        '闇鍋!!!!',
    ],
    332: [ # エピローグに君はいない (Epilogue without you)
        "Epilogue に君はいない",
        "Epilog に君はいない",
        "Epilog without you",
        '後記里沒有你的身影',
    ],
    335: [ # トラッシュ・アンド・トラッシュ！
        '垃圾',
    ],
    340: [ # とても素敵な六月でした
        "とても素敵な6月でした",
    ],
    343: [ # スノーマン
        '雪人',
    ],
    344: [ # 脳内革命ガール
        "脳内革命 Girl",
    ],
    347: [ # 円尾坂の仕立屋 (The Tailor of Enbizaka)
        "The Enbizaka's Tailor", # processive noun "of" reversal
    ],
    348: [ # 悪徳のジャッジメント (Judgment of Corruption)
        "悪徳のJudgment",
        "Corruption's Judgment", # processive noun "of" reversal
        "Judgement of Corruption", # Accepted spelling in British English
        "悪徳のJudgement", # ^
        "Corruption's Judgement", # ^
        '惡貫滿盈的法官',
    ],
    349: [ # 悪食娘コンチータ
        "悪食娘 Conchita",
        '惡食娘康奇塔',
    ],
    353: [ # キティ
        '吉蒂', # Hello Kitty?
        '凱蒂', # Hello Kitty?
    ],
    354: [ # セツナトリップ
        "刹那トリップ",
        "刹那 Trip",
        "剎那旅程",
        '旅程',
    ],
    355: [ # 白い雪のプリンセスは (The Snow White Princess Is...)
        "白い雪の Princess は",
        "THE STORY OF THE GIRL AND HER...", # subtitle
        '白雪公主',
        '白如雪的公主啊',
    ],
    358: [ # 心做し
        '心理作用',
    ],
    359: [ # 名も無き革命
        '無名革命',
    ],
    360: [ # 太陽系デスコ
        "太陽系 Disco",
        '太陽系迪斯科',
        '太陽系的士高',
        '太陽系迪斯可',
    ],
    361: [ # きゅうくらりん
        '心動不已',
    ],
    364: [ # エターナルアリア
        '永恆的詠嘆調',
    ],
    365: [ # 恋は戦争
        "戀愛是場戰爭", # Supercell Album Taiwan Title
        "愛是戰爭", # Supercell Album China Official Title
        '戀愛戰爭',
    ],
    368: [ # アイムマイン(I'm Mine)
        "我就是我", # Unofficial
        "我是地雷", # ???
    ],
    369: [ # メランコリック
        '憂鬱的心情',
        '抑鬱的心情',
    ],
    374: [ # チームメイト
        "隊友", # translation
    ],
    375: [ # 星を繋ぐ
        '繋星',
        '連繫繁星',
    ],
    376: [ # 我儘姫
        '任性公主',
        '任性姬',
    ],
    377: [ # 悪役にキスシーンを
        "悪役に Kiss Scene を",
        '給反派的吻戲',
        '与反派的吻戏',
    ],
    378: [ # スロウダウナー
        '減速',
        '減速者',
        '減速器',
    ],
    379: [ # ずんだパーリナイ
        '毛豆泥派對夜',
        '俊達萌派對夜',
        '俊達派對之夜',
    ],
    380: [ # スターダストメドレー
        '星塵組曲',
    ],
    382: [ # 心拍ペアリング
        "心拍 Pairing",
        'ABC',
        '心拍配對',
        '心跳配對',
    ],
    384: [ # トワイライトライト
        '微明暮光',
    ],
    388: [ # 初音ミクの激唱 (FULL) (The Intense Voice of Hatsune Miku (FULL))
        "Hatsune Miku's Intense Voice (FULL)",
    ],
    391: [ # キュートなカノジョ
        "キュートな彼女",
        "Cuteなカノジョ",
        "Cuteな彼女",
        "Cute Girlfriend",
        "可愛女友",
        "可愛女朋友",
    ],
    392: [ # 春嵐
        '春日風暴',
    ],
    395: [ # サマータイムレコード
        '夏時記錄',
        '夏令時記錄',
    ],
    396: [ # 東京テディベア
        "東京Teddy Bear",
        '東京泰迪熊',
    ],
    397: [ # フィラメントフィーバー
        "燈絲 Fever", # Seems like 燈絲 is a common guess
        '燈絲狂熱',
    ],
    399: [ # Disco No.39
        '迪斯可 No.39',
        '迪斯科 No.39',
        '的士高 No.39',
        '三十九號迪斯可',
        '三十九號迪斯科',
        '三十九號的士高',
        '39號的士高',
        '39號迪斯可',
        '39號迪斯科',
    ],
    400: [ # 我らステインバスターズ！
        "我らStain Busters！",
        '我們是污漬剋星！',
    ],
    401: [ # まにまに
        '錢錢',
        '隨之任之',
    ],
    402: [ # エンヴィーベイビー
        "Envy Baby",
    ],
    405: [ # MOTTO!!!
        '摸頭',
    ],
    407: [ # 初めての恋が終わる時
        "第一次戀情結束時", # Supercell Album Taiwan Title
        "初戀終結之時", # Supercell Album China Official Title
    ],
    408: [ # CIRCUS PANIC!!!
        '慌亂馬戲團!!!',
        '马戏团恐慌！！！',
    ],
    409: [ # 25時の情熱
        '25點的情熱',
        '25時的情熱',
        '25時的熱情',
    ],
    410: [ # マーシャル・マキシマイザー
        "Marshall Maximizer",
        "Marshall Maximiser",
        '馬歇爾最大化器',
    ],
    411: [ # 世界を照らすテトラッド
        "世界を照らすTetrad",
    ],
    412: [ # デビルじゃないもん
        "Devil じゃないもん",
    ],
    413: [ # さよならプリンセス
        "さよなら Princess",
        '再見公主',
    ],
    417: [ # くうになる
        '成为空',
        '空になる',
        '變成空',
    ],
    422: [ # JUMPIN’ OVER !
        'JUMPING OVER !', # IN ending
    ],
    423: [ # レグルス (Regulus)
        # as star name
        "Alpha Leonis",
        "Cor Leonis",
        "Καρδια Λεοντος",
        "Kardia Leontos",
        "α Leo",
        "alpha Leo",
        "a Leo",
        "しし座α星",
        "しし座 alpha 星",
        "しし座a星",
        "獅子座α",
        "獅子座alpha",
        "獅子座a",
        "軒轅十四",
        "軒轅14",
    ],
    424: [ # インテグラル
        '積分',
        '缺一不可',
    ],
    427: [ # 幽光、1/fのゆらめき
        '幽光，1/f的波動',
    ],
    428: [ # ときめきジェットコースター
        "ときめき Jet Coaster",
        "Tokimeki Jet Coaster",
        '心跳不止的過山車',
    ],
    430: [ # 『んっあっあっ。』
        '嗯啊啊',
        '嗯呀呀',
    ],
    431: [ # flos
        '花兒們',
        '花',
    ],
    432: [ # 強風オールバック
        "強風All Back",
    ],
    433: [ # ヒアソビ
        '火遊び',
    ],
    435: [ # リレイアウター
        "Relay Outer",
    ],
    436: [ # 古書屋敷殺人事件
        '古書宅邸殺人事件',
    ],
    437: [ # え？あぁ、そう。
        '咦？啊啊，是喔。',
    ],
    438: [ # ハイドアンド・シーク
        "Hide and Seek",
    ],
    440: [ # ショウタイム×オーディエンス
        "Showtime x Audience",
    ],
    434: [ # 1000年生きてる
        "存活1000年", # Don't want to override the "千年の独奏歌" or "一千光年"
    ],
    441: [ # 酔いどれ知らず
        '不知醉',
    ],
    442: [ # すれすれ
        '若即若离',
        '擦肩而過',
    ],
    446: [ # オーバーコード
        "O-Barcode",
        "Overcode",
        '條碼',
    ],
    447: [ # folern
        '否冷',
    ],
    449: [ # MarbleBlue.
        "媽寶藍", # Sound-alike abbre.
    ],
    452: [ # サイバーパンクデッドボーイ
        "Cyberpunk Dead Boy",
        '賽博龐克死男孩',
    ],
    454: [ # えれくとりっく・えんじぇぅ
        "Electric Angel",
        '電子天使',
    ],
    456: [ # 幾望の月
        '幾望之月',
    ],
    458: [ # 抜錨
        '拋錨',
        '拔毛',
        '起航',
    ],
    461: [ # おどロボ
        '舞蹈機器人',
    ],
    462: [ # レッドランドマーカー
        "Red Land Marker",
    ],
    463: [ # ハッピーチートデー
        "Happy Cheat Day",
    ],
    465: [ # 嬢王
        '女王',
    ],
    466: [ # ガーネットの涙
        "Garnet の涙",
        "Tears of Garnet", # Official English Name
        "Garnet Tears", # compound noun "of" reversal
    ],
    467: [ # あいのうた
        '愛の歌',
        '愛の唄',
        '愛の詩',
        'AI之歌',
        '愛之歌',
    ],
    468: [ # 十六歳の心臓
        "16歳の心臓",
    ],
    469: [ # ラグトレイン
        '延誤列車',
        '迟延列车',
        '延遲列車',
    ],
    470: [ # ハジメテノオト
        '初めての音',
        '始めての音',
    ],
    473: [ # マインドブランド
        "Mind Brand",
    ],
    474: [ # キラー
        "Killer",
    ],
    475: [ # ちがう!!!
        '違う!!!',
        '不對的!!!',
        '錯誤的!!!',
        '不對!!!',
        '錯!!!',
    ],
    477: [ # モザイクロール (Reloaded)
        "Mosaic Roll (Reloaded)",
        "馬賽克卷 (Reloaded)", # Doesn't seem to be official anyways
        '瑞士捲 (Reloaded)',
        '馬賽克卷（重製版）',
    ],
    480: [ # おちゃめ機能
        '天真爛漫機能',
    ],
    482: [ # だめにんげんだ!
        "だめ人間だ!",
        "dame 人間 da!",
        "打咩人間噠!",
        '駄目人間だ!',
        '無用人類！',
    ],
    483: [ # アコトバ
        'ア言葉',
    ],
    485: [ # だんだん早くなる
        '逐漸變快',
    ],
    486: [ # おぎゃりないざー
        '寶寶',
        '返嬰者',
        '還嬰者',
    ],
    487: [ # ダイジョブですか？
        "大丈夫ですか？",
        '你沒事吧？',
    ],
    490: [ # ルーマー
        "Rumor",
        "Rumour",
    ],
    491: [ # キャットラビング
        "Cat Loving",
    ],
    493: [ # きょうもハレバレ
        '今日もハレバレ',
        '今日も晴々',
    ],
    494: [ # ポッピンキャンディ☆フィーバー！
        "Poppin' Candy Fever!",
        'Popping Candy Fever!', # in ending
    ],
    495: [ # スーパーヒーロー
        "Superhero",
        "Super Hero",
        '超級英雄',
    ],
    496: [ # シルバーコレクター
        "Silver Collector",
    ],
    498: [ # はしる! とおく! とどく!
        '奔跑向前!傳達到!遙遠彼方!',
        '走る! 遠く! 届く!',
        '奔跑！遠方！抵達！',
    ],
    499: [ # 混沌ブギ
        '混沌布吉',
    ],
    500: [ # 余花にみとれて
        '心醉余花',
    ],
    501: [ # Bad Apple!! feat.SEKAI
        '壞蘋果',
        'Bad Apple',
    ],
    503: [ # 超最終鬼畜妹フランドール・Ｓ
        "超最終鬼畜妹Flandre-S",
        '超最終鬼畜妹芙蘭朵露·S',
    ],
    505: [ # コールボーイ
        "Call Boy",
    ],
    507: [ # エンパープル
        "Empurple",
        '染上紫色',
    ],
    508: [ # ヘイヴン
        "Haven",
        "避風港", # Unofficial
    ],
    509: [ # ライアーダンサー
        "Liar Dancer",
        '謊言舞者',
        '騙子舞者',
    ],
    511: [ # 如月アテンション
        "如月Attention",
        '如月專注',
    ],
    512: [ # 合成するミライ
        "合成する未来", # kanji
        '合成的未來',
    ],
    513: [ # CH4NGE
        "CHANGE",
    ],
    515: [ # イガク
        "醫學",
    ],
    516: [ # あちこちデートさん
        "あちこち Date さん",
        '到處約會的人',
    ],
    517: [ # メリーゴーラウンド
        "Merry Go Round",
        '旋轉木馬',
    ],
    518: [ # みかぼし
        '甕星',
    ],
    519: [ # 夏夜ノ唄
        '夏夜之歌',
    ],
    520: [ # 透明エレジー
        "透明 Elegy",
        '透明哀歌',
    ],
    521: [ # オーバーライド
        "Override",
    ],
    523: [ # きみとぼくのレゾナンス
        "きみとぼくのResonance",
        '你我二人的共鳴',
    ],
    524: [ # それでも僕らは歌うことをやめない
        '即便如此我们也不会放弃歌唱',
    ],
    525: [ # アンテナ39
        "Antenna 39",
        '天線39',
        '在天之線的感謝',
    ],
    526: [ # 彗星ノ銀河
        '彗星的銀河',
    ],
    529: [ # カルチャ
        "Culture",
        '文化',
    ],
    530: [ # キャットフード
        "Cat Food",
    ],
    531: [ # メズマライザー
        "Mesmeriser",
        "Mesmerizer",
        "催眠者", # unofficial translated
    ],
    532: [ # レイヤーノート
        "Layer Note",
    ],
    534: [ # ワールド・ランプシェード [reunion]
        "reunion", # the only English substring
        "World Lampshade [reunion]",
        '世界燈罩',
        '世界燈罩（重製版）',
    ],
    537: [ # 花に風
        "風拂花", # Doesn't seem official anyways
    ],
    538: [ # オールセーブチャレンジ
        "All-Save Challenge",
        "All Save Challenge",
        '全部拯救挑戰',
    ],
    539: [ # イレヴンス
        "Eleventh",
        '第十一刻',
    ],
    540: [ # 虚無さん
        '虛無桑',
    ],
    541: [ # メインキャラクター
        "Main Character",
        '主角',
    ],
    543: [ # 生命性シンドロウム
        "生命性Syndrome",
        '生命性症候群',
    ],
    544: [ # 妄想アスパルテーム
        "妄想Aspartame",
        '妄想阿斯巴甜',
    ],
    545: [ # 脳天
        '頭頂',
    ],
    546: [ # その音が鳴るなら
        '若那聲音響起',
    ],
    548: [ # ぼくのかみさま
        '僕の神様',
        '我的神明大人',
    ],
    549: [ # 化けの花
        '矯飾之花',
        '詭化之花',
        '異類之花',
        '怪物之花',
    ],
    551: [ # ロストアンブレラ
        "Lost Umbrella",
        'Lost傘',
        'ロスト傘',
    ],
    553: [ # パリィ
        "Parry",
        '招架',
    ],
    555: [ # フュージョン
        "Fusion",
    ],
    556: [ # サイハテ
        "Reprise",
        '最終之所',
    ],
    557: [ # 花溺れ
        '沉溺於花中',
    ],
    558: [ # のだ
        '喏噠',
    ],
    559: [ # おどりゃんせ
        '來起舞吧',
        '踊りゃんせ',
    ],
    560: [ # アイリッド
        "Eyelid",
        '眼瞼',
    ],
    561: [ # プロトディスコ
        "Proto Disco",
        '原型的士高',
        '原型迪斯可',
        '原型迪斯科',
    ],
    562: [ # アンヘル
        "Ángel", # Spanish
        "Angel",
        '天使',
    ],
    563: [ # NAKAKAPAGPABAGABAG
        '焦慮不安',
    ],
    564: [ # そこに在る、光。
        '光芒，就在那裡。',
        '存在於那𥚃的光。',
    ],
    565: [ # 夏に透明
        '夏日透明',
    ],
    566: [ # パンダヒーロー
        "Panda Hero",
        '熊貓英雄',
    ],
    567: [ # 結ンデ開イテ羅刹ト骸
        '連起來又分開羅剎與骨骸',
        '分分合合的羅剎與骨骸',
    ],
    569: [ # シークレット・シーカー
        "Secret Seeker",
    ],
    570: [ # スター
        "Star",
    ],
    571: [ # 偽物人間40号
        '偽物人類40號',
        '偽人40',
    ],
    572: [ # 飾って
        '裝飾',
    ],
    573: [ # はじまりの未来
        '始まりの未来',
    ],
    576: [ # ファイアダンス
        "Fire Dance",
        '火之舞',
    ],
    577: [ # スマイル*シンフォニー
        "Smile* Symphony",
        "微笑*交響樂", # Unofficial
    ],
    578: [ # ハローセカイ
        "Hello Sekai",
    ],
    580: [ # 三日月ステップ
        "三日月 Step",
    ],
    581: [ # 厨病激発ボーイ
        "厨病激発 Boy",
        '厨病激発男孩',
    ],
    582: [ # アンチユー
        "Antiyou",
        '俺吃魚',
        '俺吃余',
    ],
    583: [ # アクセラレイト
        "Accelerate",
        "加速", # Literal Chinese translation
    ],
    585: [ # ペンタトニック
        "Pentatonic",
        '五聲音階',
    ],
    587: [ # ルルブ
        "Rule Book",
        "法則書", # as appearing in Lyrics corr. to the song name
        '規則書',
    ],
    588: [ # プラネットヒーロー
        "Planet Hero",
    ],
    589: [ # バレリーコ
        '芭蕾舞者',
    ],
    590: [ # マンハッタン
        '曼哈頓',
        '曼赫頓',
    ],
    591: [ # 吉原ラメント 再来盤
        "吉原 Lament 再来盤",
        '吉原哀歌再来盤',
    ],
    592: [ # クイーンオブハート
        "Queen of Heart",
        "Queen of Hearts",
        "Heart Queen",
        # Poker Card
        "♥Q",
        "Q♥",
        "🂽",
         # Alice in Wonderland
        "ハートの女王",
        "紅心王后",
        "紅心皇后",
        "紅心女王",
        "하트의 여왕",
    ],
    593: [ # クリスタルスノウ
        '水晶之雪',
    ],
    595: [ # エンヴィキャットウォーク
        "Envy Catwalk",
        "Envy Cat Walk",
        '令人嫉妒的貓步',
    ],
    597: [ # その絵の名前は
        '繪名',
        'ena',
        '那幅畫的名字是',
        '其繪名為',
    ],
    603: [ # ドレミファロンド
        '音階圓舞曲',
        'DoReMiFa圓舞曲',
    ],
    606: [ # スーサイドパレヱド
        "Suicide Parade",
        '自殺遊行',
        '拼死遊行',
        '決死行進',
    ],
    607: [ # 回る空うさぎ
        '回る空兎',
        '月兔迴旋於空中',
    ],
    608: [ # 星宙メランコリア
        "星宙 Melancholia",
        '星空憂鬱',
        '星宙',
        '星宙憂鬱',
        '星宙抑鬱',
        '星空抑鬱',
    ],
    621: [ # 東京サマーセッション
        "東京 Summer Session",
        "Tokyo Summer Session",
        '東京夏日相會',
    ],
    622: [ # 超ナイト・オブ・ナイツ
        "超 Night of Knights",
        '超騎士夜',
        '超夜騎士',
    ],
    623: [ # とうほう☆ワンダーランド
        "とうほう☆Wonderland",
        "Touhou☆Wonderland",
        '東方☆Wonderland',
        '東方☆幻想鄉', # appropriation?
    ],
    624: [ # チルノのパーフェクトさんすう学園
        "Cirno の Perfect さんすう学園",
        'チルノのパーフェクト算数学園',
        '⑨',
        '琪露諾的完美算術學園',
    ],
    625: [ # このふざけた素晴らしき世界は、僕の為にある
        "這個愚蠢而美好的世界是為我準備的", # https://www.bilibili.com/video/av456264266/
        "這可笑又美妙的世界、為我而存在", # Unofficial
        "This Silly Wonderful World Exists For Me",
    ],
    626: [ # フィッシュアンドTips
        "Fish and Tips",
    ],
    627: [ # テトリス
        "Tetris",
        "Tetoris",
        "Тетрис",
        '俄羅斯方塊',
    ],
    628: [ # モニタリング
        "Monitoring",
        '視奸',
        '監視',
    ],
    632: [ # Surges (Check WDS 85 Also)
        '被海放',
    ],
    633: [ # 庭師のおはなしによると
        '根據庭師的故事',
    ],
    635: [ # ありのままのストーリーを
        "ありのままの Story を",
        '這本色出演的故事',
    ],
    636: [ # エクスプロウル
        "Explore",
    ],
    637: [ # 笑えたらえーやん！
        '笑了不就好了！',
    ],
    638: [ # 花弁、それにまつわる音声
        '花瓣、與之相關的聲音',
    ],
    639: [ # マリオネットダンサー
        "Marionette Dancer",
        '木偶舞者',
    ],
    644: [ # 生きる
        '生',
        '活下去',
    ],
    645: [ # 深海シティアンダーグラウンド
        "深海 City Underground",
        '深海地下城市',
    ],
    646: [ # 透明なパレット
        "透明なPalette",
        "透明的調色盤", # Unofficial
        '透明調色板',
    ],
    648: [ # Life Will Change
        'persona5',
    ],
    649: [ # サヨナラ天国また来て地獄
        '再見天國再臨地獄',
    ],
    650: [ # あの夏が飽和する。 (Check WDS 118 Also)
        "那个夏日已然饱和。", # https://www.bilibili.com/video/BV1CGdAYoEJJ
        "那個已然飽和的夏天。", # / 尖端出版社 ISBN 978-626-338-374-6
    ],
    651: [ # ホワイトハッピー
        "White Happy",
        '白色幸福',
    ],
    652: [ # カレシのジュード
        "カレシのJude",
        "彼氏のジュード",
        "彼氏のJude",
        "男朋友Jude", # Don't get users confused from "男朋友" matching the "女朋友" song
        'Jude男朋友',
    ],
    653: [ # パメラ
        "Pamela",
        '帕梅拉',
        '怕沒啦',
        '怕滅啦',
        '怕咩啦',
    ],
    654: [ # ラストラス
        '星漢燦爛',
    ],
    655: [ # リリィララ
        "lily-lala",
    ],
    656: [ # ブラッドドール
        "Blood Doll",
    ],
    659: [ # あなたの空が泣くのなら
        '若你的天空在哭泣',
    ],
    663: [ # ヴィーナス
        "Venus",
        '維納斯',
        '金星',
    ],
    664: [ # 人マニア
        "人 Mania",
        '人狂熱症',
        '人際狂人',
        '人狂熱者',
    ],
    665: [ # ロケットサイダー
        "Rocket Cider",
        '火箭蘇打水',
    ],
    667: [# ㋰責任集合体
        "ム責任集合体",
        "無責任集合体",
    ],
    668: [ # ネクラチューンサーカス
        "Nekuratune Circus",
        '暗調馬戲團',
    ],
    669: [ # げんてん
        "原点", # kanji
    ],
    672: [ # ハウトゥー世界征服
        "How to 世界征服",
        '世征',
        '如何世界征服',
        '如何征服世界',
        '點樣征服世界',
    ],
    677: [ # アベリア
        "Abelia",
        '六道木',
    ],
    678: [ # 金時計
        '金時鐘',
    ],
    10001: [ # 장산범
        '萇山虎',
        '萇山범',
    ],
    10003: [ # 각개전투
        '各自的戰鬥',
    ],
    10004: [ # 벚꽃비
        '櫻花雨',
    ],
    10005: [ # 별빛 세레나데
        '星光小夜曲',
    ],
    10006: [ # 비밀 인형극 II
        '秘密人偶劇II',
        '秘密人偶劇二',
    ],
    10007: [ # Carpe Diem!
        '及時行樂！',
    ],
    10008: [ # 둔갑
        '替身',
    ],
}

def setup(client: 'bot_client.BotClient'):
    # reload whatever creates the Song instances
    # from basic_utility import full_reload
    # full_reload("pjsk.song", message_client = client)
    # call reload_lookup from all songlist in game_manager instead
    from .game_manager import managers
    from common.song import SongList
    from console_color import color_print
    for ver, manager in managers.items():
        if isinstance(manager.song_list, SongList):
            color_print(
                f"* Reload {manager.__class__.game_abbr.upper()} ({manager.game_version}) song alias list...",
                color = manager.__class__.color
            )
            manager.song_list.reload_lookup()