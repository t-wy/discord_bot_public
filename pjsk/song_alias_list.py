# Put translated FULL name here if it is not the best match
# We have variant character (異[体體]字) matching, so probably need not handle CJK variants (i.e. Japanese Kanji / Korean Hanja / Trad. Chi. / Simp. Chi.)
# Take care of katakana songs which EN version is not yet released.
# If the translated song name can be found in the lyrics, it can also be included.
# "of" reversal may be considered if the Japanese title appears like "AのB" or compound noun "AB" but is translated as "B of A" in EN version (not for JP song with it's original title already in English)
# Reload pjsk.song after reload this file to refresh the cache if needed

# Last Update: Song before yyyy-mm-dd

from typing import *
if TYPE_CHECKING:
    import bot_client

song_alias_list: Dict[int, List[str]] = {
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
    131: [ # 初音ミクの激唱 (The Intense Voice of Hatsune Miku)
        "Hatsune Miku's Intense Voice", # processive noun "of" reversal
    ],
    132: [ # 「１」 (One)
        "1",
    ],
    173: [ # 流星のパルス (Pulse of the Meteor)
        "Meteor Pulse", # compound noun "of" reversal
    ],
    178: [ # にっこり^^調査隊のテーマ (Theme of Niccori Survey Team)
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
        "再見宣言",
    ],
    199: [ # ゴーストルール
        "幽靈法則",
        "鬼法",
    ],
    238: [ # ブラック★ロックシューター
        "黑岩★射手", # Supercell Album China Official Title
    ],
    241: [ # アサガオの散る頃に (Removed)
        "アサガオの散る頃に",
        "あさがおのちるころに",
        "Asagao no Chiru Koro ni",
        "When the Morning Glory Falls",
    ],
    246: [ # エイリアンエイリアン
        "外星人",
    ],
    251: [ # フロイライン＝ビブリォチカ
        "Fraulein=Biblioteca",  # Fräulein=библиотека in EN Server
    ],
    266: [ # YY
        "丫丫",
        "ㄚㄚ",
    ],
    275: [ # パラジクロロベンゼン
        "Benzene", # Paradichlorobenzene is too long that Benzene get matched to Bad End Night (BEN)
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
    354: [ # セツナトリップ
        "剎那旅程",
    ],
    355: [ # 白い雪のプリンセスは (The Snow White Princess Is...)
        "THE STORY OF THE GIRL AND HER...", # subtitle
    ],
    365: [ # 恋は戦争
        "戀愛是場戰爭", # Supercell Album Taiwan Title
        "愛是戰爭", # Supercell Album China Official Title
    ],
    388: [ # 初音ミクの激唱 (FULL) (The Intense Voice of Hatsune Miku (FULL))
        "Hatsune Miku's Intense Voice (FULL)",
    ],
    391: [ # キュートなカノジョ
        "Cute Girlfriend",
        "可愛女友",  
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
        "Tears of Garnet", # Official English Name
        "Garnet Tears", # compound noun "of" reversal
    ],
    473: [ # マインドブランド
        "Mind Brand",
    ],
    474: [ # キラー
        "Killer",
    ],
    477: [ # モザイクロール (Reloaded)
        "Mosaic Roll (Reloaded)",
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
    ],
    509: [ # ライアーダンサー
        "Liar Dancer",
    ],
    511: [ # 如月アテンション
        "如月Attention",
    ],
    515: [ # イガク
        "醫學",
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
    ],
    532: [ # レイヤーノート
        "Layer Note",
    ],
    534: [ # ワールド・ランプシェード [reunion]
        "reunion", # the only English substring
        "World Lampshade [reunion]",
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
    651: [ # ホワイトハッピー
        "White Happy",
    ],
    652: [ # カレシのジュード
        "カレシのJude",
        "彼氏のジュード",
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
    668: [ # ネクラチューンサーカス
        "Nekuratune Circus",
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