# Put translated FULL name here if it is not the best match
# We have variant character (異[体體]字) matching, so probably need not handle CJK variants (i.e. Japanese Kanji / Korean Hanja / Trad. Chi. / Simp. Chi.)
# Take care of katakana songs
# Since WDS does not put katakana version in pronunciation for songs with English title, the katakana pronunciation can also be included
# If the translated song name can be found in the lyrics, it can also be included.
# "of" reversal may be considered if the Japanese title appears like "AのB" or compound noun "AB" but is translated as "B of A" in EN version (not for JP song with it's original title already in English)
# Reload wds.song after reload this file to refresh the cache if needed

# Last Update: Song before 2025-08-19

from typing import *
if TYPE_CHECKING:
    import bot_client

song_alias_list: Dict[int, List[str]] = {
    1: [ # ワナビスタ！
        "Wanna Be Star!", # as in song name, JASRAC Database
        "Wanna Be a Star!", # in lyrics
    ],
    2: [ # トゥ・オブ・アス
        "Two of Us",
    ],
    6: [ # ダイヤモンドの誓い
        "Diamondの誓い",
        "Diamond no Chikai", # JASRAC Database
    ],
    7: [ # 魔法のラストノート
        "魔法のLast Note",
        "Maho no Last Note", # JASRAC Database
    ],
    8: [ # New Nostalgic Friend
        "ニュー・ノスタルジック・フレンド",
    ],
    9: [ # Drawing World
        "ドローイング・ワールド", # JASRAC Database
    ],
    11: [ # Etoile
        "エトワール", # French, JASRAC Database
    ],
    12: [ # Masquerade
        "マスカレード", # JASRAC Database
    ],
    13: [ # Farewell song
        "フェアウェル・ソング", # JASRAC Database
    ],
    14: [ # Eternity
        "エタニティ", # JASRAC Database
        "エタニティー",
        "エターニティー",
    ],
    15: [ # Decide
        "ディサイド", # JASRAC Database, More Phonetically Matched
        "デサイド", # More Common
    ],
    16: [ # ウタカタメロディ
        "ウタカタMelody",
        "Utakata Melody", # JASRAC Database
    ],
    17: [ # シリウスの輝きのように
        "Siriusの輝きのように",
        "Sirius no Kagayaki no you ni", # JASRAC Database
    ],
    19: [ # Faith in Expression
        "フェイス・イン・エクスプレッション", # JASRAC Database
    ],
    21: [ # プラネタリウム・レヴュー,
        "Planetarium Revue", # As in album art (https://world-dai-star.com/product/2639)
        "Planetarium Review", # As in digital release, JASRAC Database
    ],
    23: [ # デアエ・エクス・マキナ！,
        "Deae Ex Machina!", # JASRAC Database
    ],
    25: [ # Binary Star
        "バイナリー・スター", # JASRAC Database
    ],
    26: [ # 暁星アストレーション,
        "暁星Astration",
        "Gyosei Astration", # JASRAC Database
    ],
    27: [ # 情熱リベレイション,
        "情熱Liberation",
        "Jonetsu Liberation", # JASRAC Database
    ],
    28: [ # プレイ・マイ・フェイバリット!!
        "Play My Favorite!!", # JASRAC Database
        "Play My Favourite!!",
    ],
    33: [ # Snow halation
        "スノー・ハレーション",
        "スノーハレーション",
    ],
    34: [ # フォニイ
        "Phony",
    ],
    35: [ # チューリングラブ
        "Turing Love",
    ],
    37: [ # Shiny Smily Story
        "シャイニー・スマイリー・ストーリー",
    ],
    39: [ # Realize
        "リアライズ",
    ],
    40: [ # 魔法少女とチョコレゐト
        "魔法少女とChocolate",
        "Magical Girl and Chocolate", # On Jacket
    ],
    42: [ # 六兆年と一夜物語
        "Six Trillion Years and Overnight Story", # Official title
    ],
    45: [ # Blondie Revenge Tragedy
        "ブロンディ・リベンジ・トラジェディー", # JASRAC Database
        "ブロンディー・リベンジ・トラジェディー",
    ],
    46: [ # Fernweh
        "フェルンヴェー", # German, JASRAC Database
        "フェアンヴェー",
    ],
    47: [ # サマーバカンス☆アクトレス！
        "Summer Vacances☆Actress!", # JASRAC Database
    ],
    48: [ # I Wanna
        "アイ・ワナ",
    ],
    49: [ # パーティー・ジョーク・シンデレラ
        "Party Joke Cinderella", # On Jacket, JASRAC Database
    ],
    53: [ # 電脳スペクタクル
        "電脳Spectacle",
        "Denno Spectacle", # JASRAC Database
    ],
    54: [ # ひとりの夜のフィルモグラフィー
        "ひとりの夜のFilmography",
        "Hitori no yoru no Filmography", # JASRAC Database
    ],
    55: [ # ANIMA
        "アニマ",
    ],
    56: [ # フレーフレー・ファンファーレ！
        "Hurray Hurray Fanfare!", # JASRAC Database
    ],
    57: [ # Black Diary
        "ブラック・ダイアリー", # JASRAC Database
    ],
    58: [ # Pandastic Stage!
        "パンダスティック・ステージ！", # JASRAC Database
    ],
    60: [ # シル・ヴ・プレジデント
        "S'il Vous President", # JASRAC Database
    ],
    62: [ # 革命ダンス
        "革命Dance",
        "Kakumei Dance", # JASRAC Database
        "REVOLUTION DANCE", # Shown on Jacket
    ],
    63: [ # マイ・ピクチャー・ストーリー
        "My Picture Story",
    ],
    64: [ # きらり！マジカリュー・スマイル！
        "きらり！マジカリュー Smile!",
        "KIRARI! MAJICAREW SMILE!", # JASRAC Database
    ],
    65: [ # adrenaline!!!
        "アドレナリン!!!",
    ],
    66: [ # Forbidden Fruit Addiction
        "フォービドゥン・フルーツ・アディクション", # JASRAC Database
    ],
    67: [ # So long, Say Goodbye
        "ソー・ロング、セイ・グッバイ", # JASRAC Database
    ],
    68: [ # 夢のステラリウム
        "夢のStellarium",
        "Yume no Stellarium", # JASRAC Database
    ],
    69: [ # トゥインクル・トゥインクル・スクールデイズ！
        "Twinkle Twinkle School Days!",
    ],
    71: [ # いろはうたBLOOMING
        "いろはうたブルーミング", # JASRAC Database
        "IROHAUTA BLOOMING", # JASRAC Database
    ],
    72: [ # DAYBREAK FRONTLINE
        "デイブレイク・フロントライン",
    ],
    73: [ # フタリノスタルジア
        "フタリNostalgia",
        "Futari Nostalgia", # JASRAC Database
    ],
    74: [ # Get to Act Life♡
        "ゲット・トゥ・アクト・ライフ♡", # JASRAC Database
        "ゲット・トゥー・アクト・ライフ♡",
    ],
    76: [ # 不可逆的運命ディストピア
        "不可逆的運命Dystopia",
        "Fukagrakuteki unmei Dystopia", # JASRAC Database
    ],
    78: [ # トウキョウ・シャンディ・ランデヴ
        "Tokyo Shandy Rendez‐vous",
    ],
    79: [ # HAPPY NEW SHOW TIME!
        "ハッピー・ニュー・ショー・タイム！", # JASRAC Database
    ],
    81: [ # アンプレザント・ライン
        "Unpleasant Line",
    ],
    82: [ # アイ・ウィル！
        "I Will!",
    ],
    83: [ # Rolling Stone
        "ローリング・ストーン",
    ],
    85: [ # Surges
        "サージズ",
        "サージス",
    ],
    86: [ # アスノヨゾラ哨戒班 (Check PJSK 18 Also)
        "Night Sky Patrol of Tomorrow", # Official English Title
        "明日の夜空哨戒班",
    ],
    88: [ # 幻日ミステリウム
        "幻日Mysterium",
        "Genjitsu Mysterium", # JASRAC Database
    ],
    89: [ # ウタカタララバイ
        "Utakata Lullaby", # JASRAC Database
        "ウタカタLullaby",
        "Fleeting Lullaby", # From Jacket
    ],
    90: [ # NEO SKY, NEO MAP!
        "ネオ・スカイ、ネオ・マップ！",
    ],
    91: [ # ミックス・アップ・インタレスト！
        "Mix Up Interest!", # JASRAC Database
    ],
    92: [ # Crystal Bell
        "クリスタル・ベル",
    ],
    93: [ # St. Bitter Sweet
        "セント・ビター・スウィート",
        "セント・ビター・スイート", # JASRAC Database
        "セイント・ビター・スイート", # Jacket
    ],
    95: [ # ふぁうすと・いんぷれっしょん！！
        "Faust Impression!!", # JASRAC Database
    ],
    96: [ # ハチメンロッピング！
        "八面六臂ing！",
        "HACHIMENROPPING!", # JASRAC Database
    ],
    97: [ # To B-eat, or not to B-eat!
        "トゥー・ビー・イート、オア・ノット・トゥー・ビー・イート！",
        "トゥ・ビート、オア・ノット・トゥ・ビート！", # JASRAC Database
    ],
    98: [ # MY FIRST ACT！
        "マイ・ファースト・アクト！", # JASRAC Database
    ],
    100: [ # Singin' little blue bird
        "シンギン・リトル・ブルー・バード", # JASRAC Database
    ],
    101: [ # ハートフル・レシピ
        "Heartful Recipe",
    ],
    102: [ # Friends Per Second
        "フレンズ・パー・セカンド", # JASRAC Database
    ],
    106: [ # アクト・レゾナンス
        "Act Resonance",
    ],
    108: [ # Thirsty Soul
        "サースティ・ソウル", # JASRAC Database
        "サースティー・ソウル",
    ],
    109: [ # Wish upon a star
        "ウィッシュ・アポン・ア・スター",
    ],
    110: [ # ワンダフル・フラワー・ガーデン！
        "Wonderful Flower Garden!",
    ],
    111: [ # リアルタイム・リプライ！
        "Real Time Reply!", # as seen on jacket
    ],
    112: [ # マン・ハン・チュエンシー!!
        "満漢全席!!",
        "MAN HAN QUAN XI!!", # JASRAC Database
    ],
    115: [ # 惑う星達のダンスホール
        "惑う星達のDance Hall",
        "DANCE HALL OF THE PUZZLED STARS", # Shown on Jacket
    ],
    116: [ # Like Blooming Flowers
        "ライク・ブルーミング・フラワーズ",
    ],
    117: [ # 水際PARTY、水着でFUNNY
        "水際パーティー、水着でファニー",
    ],
    118: [ # あの夏が飽和する。 (Check PJSK 650 Also)
        "那个夏日已然饱和。", # https://www.bilibili.com/video/BV1CGdAYoEJJ
        "那個已然飽和的夏天。", # / 尖端出版社 ISBN 978-626-338-374-6
    ],
    119: [ # Stellar Stellar
        "ステラ・ステラ",
    ],
    120: [ # Nameless Story
        "ネームレス・ストーリー",
    ],
    121: [ # Another colony
        "アナザー・コロニー",
    ],
    122: [ #  ただ声一つ
        "One Voice", # Official title
    ],
    123: [ # ヴァンパイア
        "Vampire",
    ],
    124: [ # エジソン
        "Edison",
    ],
    125: [ # 強風オールバック
        "強風All Back",
    ],
    128: [ # オドループ
        "Oddloop",
    ],
    130: [ # Virtual to LIVE
        "バーチャル・トゥ・ライブ",
    ],
    135: [ # INTERNET YAMERO
        "インターネット・ヤメロ",
    ],
    136: [ # TOMORROW
        "トゥモロー",
    ],
    137: [ # インフェルノ
        "Inferno",
    ],
    140: [ # ミックスナッツ
        "Mix Nuts",
        "Mixed Nuts", # JASRAC Database
    ],
    141: [ # Transcend Lights
        "トランセンド・ライツ",
    ],
    142: [ # 絆はずっとGrowing Up!!!
        "絆はずっとグローイング・アップ!!!",
    ],
    143: [ # give it up to you
        "ギブ・イット・アップ・トゥー・ユー",
    ],
    144: [ # Y.Y.Y.計画!!!!
        "ヤバイクライヨノナカヲワイワイサセチャウゾケイカク", # As stated on jacket
    ],
    145: [ # STARTLINER
        "スタートライナー",
    ],
    146: [ # 進め！マイウェイ！
        "進め！My Way!",
    ],
    149: [ # GODLINESS
        "ゴッドリネス",
    ],
    150: [ # 粛聖!!ロリ神レクイエム☆
        "粛聖!!ロリ神Requiem☆",
    ],
    152: [ # シャルル
        "Charles",
    ],
    153: [ # DISCOTHEQUE
        "ディスコテーク",
        "ディスコティーク", # French
    ],
    155: [ # リライト
        "Rewrite",
    ],
    156: [ # COLORS
        "カラーズ",
    ],
    162: [ # Neustart
        "ノイシュタルト", # German
    ],
    163: [ # Original Scene
        "オリジナル・シーン", # JASRAC Database
    ],
    164: [ # 色即是空卍Trick is Treat！
        "シキソクゼクウトリック・イズ・トリート！", # JASRAC Database
        "シキソクゼクウマンジトリック・イズ・トリート！", # JASRAC Database
        "色即是空卍トリック・イズ・トリート！",
    ],
    165: [ # Sweet Memories
        "スウィート・メモリーズ", # JASRAC Database
        "スイート・メモリーズ",
    ],
    166: [ # 史上最幸NEW YEAR!
        "史上最幸ニュー・イヤー！",
    ],
    167: [ # プリズム△▽リズム
        "Prism△▽Rhythm",
    ],
    169: [ # 花と、雪と、ドラムンベース。
        "花と、雪と、Drum'n' Bass."
    ],
    170: [ # Starry Colors
        "スターリー・カラーズ",
    ],
    172: [ # 青空Jumping Heart
        "青空ジャンピング・ハート",
    ],
    173: [ # 恋になりたいAQUARIUM
        "恋になりたいアクアリウム",
    ],
    174: [ # Landing action Yeah!!
        "ランディング・アクション・イエー！！",
    ],
    175: [ # Believe again
        "ビリーブ・アゲイン",
    ],
    176: [ # いーあるふぁんくらぶ (Check PJSK 174 Also)
        "一二Fanclub",
        "1, 2, Fanclub", # JASRAC Database
    ],
    179: [ # ヱテルナ・ガラクシア
        "Eterna Galaxia", # JASRAC Database
    ],
    180: [ # いこうよ！ネバーランドへ
        "いこうよ！Neverlandへ",
        "Ikou yo! Neverland e", # JASRAC Database
        "LET'S GO TO NEVER LAND", # Shown on Jacket
    ],
    181: [ # トーキョー・ウィンター・ミュージック
        "Tokyo Winter Music", # JASRAC Database
    ],
    182: [ # 絶対！ニーデリッヒ宣言♡
        "絶対！Niedlich宣言♡",
        "Zettai! Niedlich Sengen♡", # JASRAC Database
    ],
    183: [ # Act on my feelings.
        "アクト・オン・マイ・フィーリングス。", # JASRAC Database
    ],
    185: [ # マッピング・マイ・ワールド
        "Mapping My World", # JASRAC Database
    ],
    187: [ # ティンクル・ティンクル・ティンク！
        "Tinkle Tinkle Tink!",
        "Twinkle Twinkle Twink!", # JASRAC Database
    ],
    188: [ # 君というメソッドへ
        "君というMethodへ",
        "Kimi to iu Method e", # JASRAC Database
    ],
    189: [ # 想い出はリタルダンド
        "想い出はRitardando",
        "Omoide wa Ritardando", # JASRAC Database
    ],
    190: [ # ビビデバ
        "BIBBIDIBA", # JASRAC Database
    ],
    191: [ # 愛包ダンスホール
        "愛包Dancehall",
    ],
    193: [ # 1・2・3
        "One Two Three", # JASRAC Database
        "ワン・ツー・スリー", # JASRAC Database
    ],
    194: [ # オーバーライド
        "Override",
    ],
    195: [ # シャイニングスター
        "Shining Star",
    ],
    198: [ # 青春サイダー
        "青春Cider",
    ],
    199: [ # SHINY DAYS
        "シャイニー・デイズ",
    ],
    200: [ # レイドバックジャーニー
        "Laid Back Journey",
    ],
    201: [ # Worlds Dye Star
        "ワールズ・ダイ・スター", # JASRAC Database
    ],
    202: [ # シャボンに浮かぶセカイであおう
        "Sabãoに浮かぶセカイであおう", # Old Portuguese
        "Sabaoに浮かぶセカイであおう", # Old Portuguese
        "Sabõに浮かぶセカイであおう", # Old Portuguese
        "Saboに浮かぶセカイであおう", # Old Portuguese
        "Sabonに浮かぶセカイであおう", # Old Portuguese
        "Sabunに浮かぶセカイであおう", # Malay
    ],
    204: [ # Dear My Eden
        "ディア・マイ・エデン", # JASRAC Database
    ],
    205: [ # Sunny day in June.
        "サニー・デイ・イン・ジューン",
    ],
    206: [ # SECRET TRAINING!!!!
        "シークレット・トレーニング!!!!",
    ],
    208: [ # アンチ・サニーデイズ・カレンダー
        "Anti Sunny Days Calendar",
    ],
    209: [ # RAREFIED HEIGHTS
        "レアファイド・ハイツ", # JASRAC Database
        "レアリファイド・ハイツ",
    ],
    210: [ # グローリー・ワンダーランド
        "Glory Wonderland",
    ],
    212: [ # ファンサ
        "Fanservice", # Full form of Fansa
    ],
    215: [ # Invitation
        "インビテーション",
    ],
    216: [ # Blazing Break
        "ブレイジング・ブレイク",
    ],
    217: [ # 光線チューニング
        "光線Tuning",
    ],
    218: [ # 〚隔絶〛～Flame of Determination
        "〚隔絶〛～フレイム・オブ・ディターミネーション",
    ],
    219: [ # 蜘蛛の糸
        "Spider's Thread", # Shown in Arcaea
    ],
    220: [ # ロマンスの神様
        "Romance の神様",
        "Romance no Kamisama",
        "The Cupid of Romance", # Official English Title
    ],
    221: [ # DreamRiser
        "ドリームライザー",
    ],
    222: [ # Enter Enter MISSION！
        "エンター・エンター・ミッション！",
    ],
    225: [ # VIVID BIT AT HOME！
        "ビビッド・ビット・アット・ホーム！",
    ],
    236: [ # カルペ・ディエム
        "Carpe diem",
    ],
    249: [ # Stellarium Collection Vol.1
        "ステラリウム・コレクション・ボリューム・ワン",
    ],
}

def setup(client: 'bot_client.BotClient'):
    # reload whatever creates the Song instances
    # from basic_utility import full_reload
    # full_reload("wds.song", message_client = client)
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