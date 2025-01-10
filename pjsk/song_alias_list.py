# Put translated FULL name here if it is not the best match
# We have variant character (異[体體]字) matching, so probably need not handle CJK variants (i.e. Japanese Kanji / Korean Hanja / Trad. Chi. / Simp. Chi.)
# Take care of katakana songs which EN version is not yet released.
# Reload pjsk.song after reload this file to refresh the cache if needed
from typing import *
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
    74: [ # 独りんぼエンヴィー
        "孑然妒火",
        "充滿嫉妒的一人捉迷藏",
    ],
    132: [ # 「１」
        "1"
    ],
    187: [ # ロウワー
        "Lower", # EN name: Lower one's eyes (Lost One's Weeping steal the best match)
    ],
    193: [ # ワールドワイドワンダー
        "World Wide Wonder", # as Worldwide is a single word in Japanese
    ],
    194: [ # 妄想感傷代償連盟
        "Delusion Sentiment Compensation Federation",
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
    275: [ # パラジクロロベンゼン
        "Benzene", # Paradichlorobenzene is too long that Benzene get matched to Bad End Night (BEN)
    ],
    290: [ # どんな結末がお望みだい？ (Removed)
        "どんな結末がお望みだい？",
        "どんなけつまつがおのぞみだい?",
        "Donna Ketsu Matu ga Onozomidai?",
        "What Sort of Ending Are You Wishing For?"
    ],
    354: [ # セツナトリップ
        "剎那旅程",
    ],
    365: [ # 恋は戦争
        "戀愛是場戰爭", # Supercell Album Taiwan Title
        "愛是戰爭", # Supercell Album China Official Title
    ],
    391: [ # キュートなカノジョ
        "Cute Girlfriend",
        "可愛女友",  
    ],
    396: [ # 東京テディベア
        "東京Teddy Bear",
    ],
    400: [ # 我らステインバスターズ！
        "我らSteinbusters！"
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
    511: [ # 如月アテンション
        "如月Attention",
    ],
    515: [ # イガク
        "醫學",
    ],
    517: [ # メリーゴーラウンド
        "Merry Go Round",
    ],
    523: [ # きみとぼくのレゾナンス
        "きみとぼくのResonance",
    ],
    529: [ # カルチャ
        "Culture",
    ],
    531: [ # メズマライザー
        "Mesmeriser",
        "Mesmerizer",
    ],
    532: [ # レイヤーノート
        "Layer Note",
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
    553: [ # パリィ
        "Parry",
    ]
}