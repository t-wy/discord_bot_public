# Put translated FULL name here if it is not the best match
# We have variant character (異[体體]字) matching, so probably need not handle CJK variants (i.e. Japanese Kanji / Korean Hanja / Trad. Chi. / Simp. Chi.)
# Take care of katakana songs which EN version is not yet released.
# If the translated song name can be found in the lyrics, it can also be included.
# "of" reversal may be considered if the Japanese title appears like "AのB" or compound noun "AB" but is translated as "B of A" in EN version (not for JP song with it's original title already in English)
# Reload pjsk.song after reload this file to refresh the cache if needed

# Last Update: Song before 2025-11-01

from typing import *
if TYPE_CHECKING:
    import bot_client

song_alias_list: Dict[int, List[str]] = {
    8: [ # タイムマシン
        "時光機", # well known translation
    ],
    18: [ # アスノヨゾラ哨戒班 (Check WDS 86 Also)
        "Night Sky Patrol of Tomorrow", # Official English Title
        "明日の夜空哨戒班",
    ],
    21: [ # 脱法ロック
        "脱法 Rock",
    ],
    46: [ # グリーンライツ・セレナーデ
        "綠光小夜曲",
        "綠燈小夜曲",
    ],
    47: [
        "融化", # Supercell Album China Official Title
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
    ],
    71: [ # ツギハギスタッカート
        "継ぎ接ぎスタッカート"
        "Tsugihagi Staccato"
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
    78: [ # ぼうけんのしょがきえました！
        "冒険の書が消えました！",
    ],
    81: [ # 夜咄ディセイブ
        "夜咄 Deceive",
    ],
    90: [ # 限りなく灰色へ
        "向著無限的灰色", # https://www.bilibili.com/video/BV1kyKtzmE9Z/
        "向著無盡之灰",
    ],
    91: [ # ドラマツルギー
        "擬劇論", # Unofficial
    ],
    98: [ # ロストワンの号哭
        "Lost One の号哭",
    ],
    104: [ # サンドリヨン 10th Anniversary
        "灰姑娘 十周年", # direct translation to Chinese
        "灰姑娘 10周年", # direct translation to Chinese
    ],
    112: [ # 天使のクローバー
        "天使の Clover",
    ],
    113: [ # ローリンガール
        "滾女", # ???
    ],
    131: [ # 初音ミクの激唱 (The Intense Voice of Hatsune Miku)
        "Hatsune Miku's Intense Voice", # processive noun "of" reversal
    ],
    132: [ # 「１」 (One)
        "1",
    ],
    136: [ # チルドレンレコード
        "孩童記錄", # Unofficial translation
    ],
    146: [ # リモコン
        "Remo Con",
    ],
    158: [ # ナンセンス文学
        "Nonsense 文学",
    ],
    162: [ # エンドマークに希望と涙を添えて
        "End Mark に希望と涙を添えて",
    ],
    173: [ # 流星のパルス (Pulse of the Meteor)
        "Meteor Pulse", # compound noun "of" reversal
    ],
    175: [ # 拝啓ドッペルゲンガー
        "拝啓 Doppelganger",
    ],
    176: [ # マシンガンポエムドール
        "機關槍", # Common chinese abbreviation
    ],
    178: [ # にっこり^^調査隊のテーマ (Theme of Niccori Survey Team)
        "にっこり^^調査隊の Theme",
        "Niccori Survey Team Theme", # compound noun "of" reversal
        "Niccori", # short match
        "Nikkori", # short match
    ],
    187: [ # ロウワー (Lower)
        "Lower", # EN name: Lower one's eyes (Lost One's Weeping steal the best match)
    ],
    190: [ # 悪ノ娘 (The Daughter of Evil)
        "The Evil Daughter", # processive noun "of" reversal
    ],
    191: [ # 悪ノ召使 (The Servant of Evil)
        "The Evil Servant", # processive noun "of" reversal
    ],
    192: [ # 去り人達のワルツ (Waltz of the Deceased)
        "the Deceased's Waltz", # processive noun "of" reversal
    ],
    193: [ # ワールドワイドワンダー
        "World Wide Wonder", # as Worldwide is a single word in Japanese
    ],
    194: [ # 妄想感傷代償連盟
        "Delusion Sentiment Compensation Federation", # Only DSCF in EN Server
    ],
    196: [ # オーダーメイド
        "Ordermade",
        "Order Made",
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
    206: [ # 君色マリンスノウ
        "君色 Marine Snow",
    ],
    208: [ # 僕らまだアンダーグラウンド
        "僕らまだ Underground",
    ],
    210: [ # 雨とペトラ
        "雨と Petra",
    ],
    212: [ # 星空のメロディー
        "星空の Melody",
    ],
    214: [ # パレットには君がいっぱい
        "Palette には君がいっぱい",
    ],
    229: [ # 脳漿炸裂ガール
        "脳漿炸裂 Girl",
    ],
    230: [ # サラマンダー
        "沙羅曼蛇",
    ],
    234: [ # 徳川カップヌードル禁止令
        "徳川 Cup Noodle 禁止令",
    ],
    238: [ # ブラック★ロックシューター
        "黑岩★射手", # Supercell Album China Official Title
    ],
    240: [ # 踊れオーケストラ
        "踊れOrchestra",
    ],
    241: [ # アサガオの散る頃に (Removed)
        "アサガオの散る頃に",
        "あさがおのちるころに",
        "Asagao no Chiru Koro ni",
        "When the Morning Glory Falls",
    ],
    245: [ # 阿吽のビーツ
        "阿吽の Beats",
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
    ],
    251: [ # フロイライン＝ビブリォチカ
        "Fraulein=Biblioteca",  # Fräulein=библиотека in EN Server
    ],
    261: [ # 星屑ユートピア
        "星屑 Utopia",
    ],
    266: [ # YY
        "丫丫",
        "ㄚㄚ",
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
    275: [ # パラジクロロベンゼン
        "Benzene", # Paradichlorobenzene is too long that Benzene get matched to Bad End Night (BEN)
    ],
    281: [ # 気まぐれメルシィ
        "気まぐれ Mercy",
    ],
    282: [ # 星空オーケストラ
        "星空Orchestra",
    ],
    285: [ # ÅMARA(大未来電脳)
        "AMARA", # without bracket or character modifiers
        "大未来電脳", # only bracket contents
    ],
    290: [ # どんな結末がお望みだい？ (Removed)
        "どんな結末がお望みだい？",
        "どんなけつまつがおのぞみだい?",
        "Donna Ketsu Matu ga Onozomidai?",
        "What Sort of Ending Are You Wishing For?"
    ],
    296: [ # カンタレラ
        "坎特雷拉", # Unofficial
    ],
    298: [ # ネトゲ廃人シュプレヒコール
        "Net Game 廃人 Sprechchor"
    ],
    299: [ # エゴイスト
        "利己主義", # JP term
        "利己主義者", # literal translation
    ],
    301: [ # 私の恋はヘルファイア
        "私の恋は Hellfire",
        "私の恋は Hell Fire",
    ],
    314: [ # 陽だまりのセツナ
        "陽黙りの刹那", # kanji
        "向陽處的剎那", # some chinese translaton
    ],
    316: [ # ひつじがいっぴき
        "羊が一匹",
        "一匹羊",
        "一隻羊",
    ],
    317: [ # 魔法みたいなミュージック！
        "魔法みたいな Music ！",
    ],
    324: [ # 箱庭のコラル
        "箱庭の Coral",
    ],
    332: [ # エピローグに君はいない (Epilogue without you)
        "Epilogue に君はいない",
        "Epilog に君はいない",
        "Epilog without you",
    ],
    340: [ # とても素敵な六月でした
        "とても素敵な6月でした",
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
    ],
    349: [ # 悪食娘コンチータ
        "悪食娘 Conchita",
    ],
    354: [ # セツナトリップ
        "刹那トリップ",
        "刹那 Trip",
        "剎那旅程",
    ],
    355: [ # 白い雪のプリンセスは (The Snow White Princess Is...)
        "白い雪の Princess は",
        "THE STORY OF THE GIRL AND HER...", # subtitle
    ],
    360: [ # 太陽系デスコ
        "太陽系 Disco",
    ],
    365: [ # 恋は戦争
        "戀愛是場戰爭", # Supercell Album Taiwan Title
        "愛是戰爭", # Supercell Album China Official Title
    ],
    377: [ # 悪役にキスシーンを
        "悪役に Kiss Scene を",
    ],
    382: [ # 心拍ペアリング
        "心拍 Pairing",
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
    396: [ # 東京テディベア
        "東京Teddy Bear",
    ],
    400: [ # 我らステインバスターズ！
        "我らStain Busters！"
    ],
    402: [ # エンヴィーベイビー
        "Envy Baby",
    ],
    407: [ # 初めての恋が終わる時
        "第一次戀情結束時", # Supercell Album Taiwan Title
        "初戀終結之時", # Supercell Album China Official Title
    ],
    410: [ # マーシャル・マキシマイザー
        "Marshall Maximizer",
        "Marshall Maximiser",
    ],
    411: [ # 世界を照らすテトラッド
        "世界を照らすTetrad",
    ],
    412: [ # デビルじゃないもん
        "Devil じゃないもん",
    ],
    413: [ # さよならプリンセス
        "さよなら Princess",
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
    428: [ # ときめきジェットコースター
        "ときめき Jet Coaster",
        "Tokimeki Jet Coaster",
    ],
    432: [ # 強風オールバック
        "強風All Back",
    ],
    435: [ # リレイアウター
        "Relay Outer",
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
    446: [ # オーバーコード
        "O-Barcode",
        "Overcode",
    ],
    452: [ # サイバーパンクデッドボーイ
        "Cyberpunk Dead Boy",
    ],
    454: [ # えれくとりっく・えんじぇぅ
        "Electric Angel",
    ],
    462: [ # レッドランドマーカー
        "Red Land Marker",
    ],
    463: [ # ハッピーチートデー
        "Happy Cheat Day",
    ],
    466: [ # ガーネットの涙
        "Garnet の涙",
        "Tears of Garnet", # Official English Name
        "Garnet Tears", # compound noun "of" reversal
    ],
    468: [ # 十六歳の心臓
        "16歳の心臓",
    ],
    473: [ # マインドブランド
        "Mind Brand",
    ],
    474: [ # キラー
        "Killer",
    ],
    477: [ # モザイクロール (Reloaded)
        "Mosaic Roll (Reloaded)",
        "馬賽克卷 (Reloaded)", # Doesn't seem to be official anyways
    ],
    482: [ # だめにんげんだ!
        "だめ人間だ!",
        "dame 人間 da!",
        "打咩人間噠!",
    ],
    487: [ # ダイジョブですか？
        "大丈夫ですか？",
    ],
    490: [ # ルーマー
        "Rumor",
        "Rumour",
    ],
    491: [ # キャットラビング
        "Cat Loving",
    ],
    494: [ # ポッピンキャンディ☆フィーバー！
        "Poppin' Candy Fever!",
    ],
    495: [ # スーパーヒーロー
        "Superhero",
        "Super Hero",
    ],
    496: [ # シルバーコレクター
        "Silver Collector",
    ],
    503: [ # 超最終鬼畜妹フランドール・Ｓ
        "超最終鬼畜妹Flandre-S",
    ],
    505: [ # コールボーイ
        "Call Boy",
    ],
    507: [ # エンパープル
        "Empurple",
    ],
    508: [ # ヘイヴン
        "Haven",
        "避風港", # Unofficial
    ],
    509: [ # ライアーダンサー
        "Liar Dancer",
    ],
    511: [ # 如月アテンション
        "如月Attention",
    ],
    513: [ # CH4NGE
        "CHANGE",
    ],
    515: [ # イガク
        "醫學",
    ],
    516: [ # あちこちデートさん
        "あちこち Date さん",
    ],
    517: [ # メリーゴーラウンド
        "Merry Go Round",
    ],
    520: [ # 透明エレジー
        "透明 Elegy",
    ],
    521: [ # オーバーライド
        "Override",
    ],
    523: [ # きみとぼくのレゾナンス
        "きみとぼくのResonance",
    ],
    525: [ # アンテナ39
        "Antenna 39",
    ],
    529: [ # カルチャ
        "Culture",
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
    ],
    537: [ # 花に風
        "風拂花", # Doesn't seem official anyways
    ],
    538: [ # オールセーブチャレンジ
        "All-Save Challenge",
        "All Save Challenge",
    ],
    539: [ # イレヴンス
        "Eleventh",
    ],
    541: [ # メインキャラクター
        "Main Character",
    ],
    543: [ # 生命性シンドロウム
        "生命性Syndrome",
    ],
    544: [ # 妄想アスパルテーム
        "妄想Aspartame",
    ],
    551: [ # ロストアンブレラ
        "Lost Umbrella",
    ],
    553: [ # パリィ
        "Parry",
    ],
    555: [ # フュージョン
        "Fusion",
    ],
    556: [ # サイハテ
        "Reprise",
    ],
    560: [ # アイリッド
        "Eyelid",
    ],
    561: [ # プロトディスコ 
        "Proto Disco",
    ],
    562: [ # アンヘル
        "Ángel", # Spanish
        "Angel",
    ],
    566: [ # パンダヒーロー
        "Panda Hero",
    ],
    569: [ # シークレット・シーカー
        "Secret Seeker",
    ],
    570: [ # スター
        "Star",
    ],
    576: [ # ファイアダンス
        "Fire Dance",
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
    ],
    582: [ # アンチユー
        "Antiyou",
    ],
    583: [ # アクセラレイト
        "Accelerate",
        "加速", # Literal Chinese translation
    ],
    585: [ # ペンタトニック
        "Pentatonic",
    ],
    587: [ # ルルブ
        "Rule Book",
        "法則書", # as appearing in Lyrics corr. to the song name
    ],
    588: [ # プラネットヒーロー
        "Planet Hero",
    ],
    591: [ # 吉原ラメント 再来盤
        "吉原 Lament 再来盤",
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
    595: [ # エンヴィキャットウォーク
        "Envy Catwalk",
        "Envy Cat Walk",
    ],
    606: [ # スーサイドパレヱド
        "Suicide Parade",
    ],
    608: [ # 星宙メランコリア
        "星宙 Melancholia",
    ],
    621: [ # 東京サマーセッション
        "東京 Summer Session",
        "Tokyo Summer Session",
    ],
    622: [ # 超ナイト・オブ・ナイツ
        "超 Night of Knights",
    ],
    623: [ # とうほう☆ワンダーランド
        "とうほう☆Wonderland",
        "Touhou☆Wonderland",
    ],
    624: [ # チルノのパーフェクトさんすう学園
        "Cirno の Perfect さんすう学園",
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
    ],
    628: [ # モニタリング
        "Monitoring",
    ],
    635: [ # ありのままのストーリーを
        "ありのままの Story を",
    ],
    636: [ # エクスプロウル
        "Explore",
    ],
    639: [ # マリオネットダンサー
        "Marionette Dancer",
    ],
    645: [ # 深海シティアンダーグラウンド
        "深海 City Underground",
    ],
    646: [ # 透明なパレット
        "透明なPalette",
    ],
    650: [ # あの夏が飽和する。 (Check WDS 118 Also)
        "那个夏日已然饱和。", # https://www.bilibili.com/video/BV1CGdAYoEJJ
        "那個已然飽和的夏天。", # / 尖端出版社 ISBN 978-626-338-374-6
    ],
    651: [ # ホワイトハッピー
        "White Happy",
    ],
    652: [ # カレシのジュード
        "カレシのJude",
        "彼氏のジュード",
        "彼氏のJude",
        "男朋友Jude", # Don't get users confused from "男朋友" matching the "女朋友" song
    ],
    653: [ # パメラ
        "Pamela",
    ],
    655: [ # リリィララ
        "lily-lala",
    ],
    656: [ # ブラッドドール
        "Blood Doll",
    ],
    663: [ # ヴィーナス
        "Venus",
    ],
    664: [ # 人マニア
        "人 Mania",
    ],
    665: [ # ロケットサイダー
        "Rocket Cider",
    ],
    667: [# ㋰責任集合体
        "ム責任集合体",
        "無責任集合体",
    ],
    668: [ # ネクラチューンサーカス
        "Nekuratune Circus",
    ],
    669: [ # げんてん
        "原点", # kanji
    ],
    672: [ # ハウトゥー世界征服
        "How to 世界征服",
    ],
    677: [ # アベリア
        "Abelia",
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