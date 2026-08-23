# Put translated FULL name here if it is not the best match
# We have variant character (異[体體]字) matching, so probably need not handle CJK variants (i.e. Japanese Kanji / Korean Hanja / Trad. Chi. / Simp. Chi.)
# Take care of katakana songs

# Last Update: --

from typing import *
if TYPE_CHECKING:
    import bot_client

song_alias_list: Dict[int, List[str]] = {
    103103: [ # フォーチュンムービー
        '포춘 무비', # AuroraCaelum/TakasakiInfo
        'Fortune Movie', # Suyooo/ll-heardle
    ],
    103105: [ # 謳歌爛漫
        '구가난만', # AuroraCaelum/TakasakiInfo
    ],
    103106: [ # 眩耀夜行
        '현요야행', # AuroraCaelum/TakasakiInfo
    ],
    103108: [ # ジブンダイアリー
        '자신 다이어리', # AuroraCaelum/TakasakiInfo
        'Jibun Diary', # rurimegu/MyPickHasunosora
    ],
    103109: [ # 永遠のEuphoria
        '영원의 유포리아', # AuroraCaelum/TakasakiInfo
        'Eien no Euphoria', # Suyooo/ll-heardle
    ],
    103110: [ # ハクチューアラモード
        'Hakuchu- à la Mode',
        '한낮 à la Mode', # AuroraCaelum/TakasakiInfo
        'Hakuchuu à la mode', # Suyooo/ll-heardle
    ],
    103111: [ # パラレルダンサー
        '패러렐 댄서', # AuroraCaelum/TakasakiInfo
        'Parallel Dancer', # Suyooo/ll-heardle
    ],
    103113: [ # アイデンティティ
        '아이덴티티', # AuroraCaelum/TakasakiInfo
        'Identity', # Suyooo/ll-heardle
    ],
    103115: [ # 千変万華
        '천변만화', # AuroraCaelum/TakasakiInfo
    ],
    103117: [ # シュガーメルト
        '슈가 멜트', # AuroraCaelum/TakasakiInfo
        'Sugar Melt', # Suyooo/ll-heardle
    ],
    103119: [ # ハッピー至上主義！
        'Happy Shijou Shugi!', # Suyooo/ll-heardle
    ],
    103120: [ # マハラジャンボリー
        'Mahara Jamboree', # Suyooo/ll-heardle
    ],
    103203: [ # ダンスロボットダンス
        'Dance Robot Dance',
    ],
    103205: [ # ダイヤモンドハッピー
        'Diamond Happy',
    ],
    103302: [ # 君のこころは輝いてるかい?
        'Kimi no Kokoro wa Kagayaiteru kai?', # hamproductions/llll-chart
    ],
    104102: [ # Sparkly Spot（104期NEW Ver.）
        'Sparkly Spot (104th Class NEW Ver.)', # rurimegu/MyPickHasunosora
    ],
    104109: [ # ファンファーレ！！！
        'Fanfare!!!', # Suyooo/ll-heardle
    ],
    104116: [ # ベジ・ラブ・ルー
        'Veggie・Love・Roux', # Suyooo/ll-heardle
    ],
    104117: [ # おいでよ！石川大観光
        'Oide yo! Ishikawa Daikankou', # Suyooo/ll-heardle
    ],
    104201: [ # ミラクルショッピング ～ドン・キホーテのテーマ～
        'MIRACLE SHOPPING〜ドン・キホーテのテーマ〜',
        'Miracle Shopping ~ Don Quijote Theme ~',
    ],
    104202: [ # ルージュの伝言
        'Rouge No Dengon',
        'Rūju no Dengon',
        'Rūju の伝言',
        'Rouge の伝言',
        'Message in Rouge',
        'Lipstick Message',
    ],
    104204: [ # コネクト
        'Connect',
    ],
    104301: [ # 夏色えがおで1,2,Jump!
        'Natsuiro Egao de 1,2,Jump!', # Suyooo/ll-heardle
    ],
    104302: [ # 常夏☆サンシャイン
        'Tokonatsu☆Sunshine', # Suyooo/ll-heardle
        '常夏☆Sunshine',
    ],
    105103: [ # チリコンカン
        'Chili Con Carne', # Suyooo/ll-heardle
    ],
    105105: [ # 幸せのリボン
        'Shiawase no Ribbon', # Suyooo/ll-heardle
        '幸せのRibbon',
    ],
    203102: [ # ツキマカセ
        '츠키마카세', # AuroraCaelum/TakasakiInfo
    ],
    203105: [ # 夏めきペイン
        '여름스런 페인', # AuroraCaelum/TakasakiInfo
        'Natsumeki Pain', # Suyooo/ll-heardle
    ],
    203106: [ # ド！ド！ド！
        '도! 도! 도!', # AuroraCaelum/TakasakiInfo
    ],
    203107: [ # 素顔のピクセル
        '맨얼굴의 픽셀', # AuroraCaelum/TakasakiInfo
        'Sugao no Pixel', # Suyooo/ll-heardle
    ],
    203108: [ # ノンフィクションヒーローショー
        '논픽션 히어로 쇼', # AuroraCaelum/TakasakiInfo
        'Non-fiction Hero Show', # Suyooo/ll-heardle
    ],
    203110: [ # 青春の輪郭
        '청춘의 윤곽', # AuroraCaelum/TakasakiInfo
    ],
    203111: [ # ツバサ・ラ・リベルテ
        'Tsubasa La Liberte', # Suyooo/ll-heardle
        'Tsubasa・La・Liberte', # rurimegu/MyPickHasunosora
    ],
    203112: [ # 天才なのかもしれない
        '천재일지도 몰라', # AuroraCaelum/TakasakiInfo
    ],
    203114: [ # ミルク
        'Milk', # Suyooo/ll-heardle
    ],
    203116: [ # BANG YOU グラビティ
        'BANG YOU Gravity', # Suyooo/ll-heardle
    ],
    203202: [ # ビバハピ
        'Viva Happy',
    ],
    203206: [ # ハッピーシンセサイザ
        'Happy Synthesizer',
        'Happy Synthesiser',
    ],
    203207: [ # 強風オールバック
        '強風All Back',
        'Kyoufuu All Back',
    ],
    203301: [ # 僕らのLIVE 君とのLIFE
        'Bokura no LIVE Kimi to no LIFE', # Suyooo/ll-heardle
    ],
    203302: [ # 始まりは君の空
        'Hajimari wa Kimi no Sora', # Suyooo/ll-heardle
    ],
    204101: [ # アイデンティティ（104期NEW Ver.）
        'Identity (104th Class NEW Ver.)', # rurimegu/MyPickHasunosora
    ],
    204104: [ # みらくりえーしょん
        'Miracreation', # Suyooo/ll-heardle
        'Mira-Creation', # rurimegu/MyPickHasunosora
    ],
    204112: [ # バアドケージ
        'Birdcage', # Suyooo/ll-heardle
    ],
    204118: [ # レム
        'Rem', # Suyooo/ll-heardle
    ],
    204121: [ # アステリズム
        'Asterism', # Suyooo/ll-heardle
    ],
    204201: [ # ビビデバ
        'BIBBIDIBA',
    ],
    205103: [ # 37.5℃のファンタジー
        '37.5°C no Fantasy', # Suyooo/ll-heardle
        '37.5℃ no Fantasy', # rurimegu/MyPickHasunosora
    ],
    205202: [ # ロミオとシンデレラ
        'Romeo and Cinderella',
        'Romeo to Cinderella',
        'Romeo と Cinderella',
    ],
    205301: [ # 青空Jumping Heart
        'Aozora Jumping Heart', # Suyooo/ll-heardle
    ],
    303102: [ # 水彩世界
        '수채화 세계', # AuroraCaelum/TakasakiInfo
    ],
    303105: [ # 希望的プリズム
        '희망적 프리즘', # AuroraCaelum/TakasakiInfo
        'Kibouteki Prism', # Suyooo/ll-heardle
    ],
    303106: [ # スケイプゴート
        '스케이프 고트', # AuroraCaelum/TakasakiInfo
        'Scapegoat', # Suyooo/ll-heardle
    ],
    303109: [ # ココン東西
        '고금동서', # AuroraCaelum/TakasakiInfo
    ],
    303110: [ # 残陽
        '잔양', # AuroraCaelum/TakasakiInfo
    ],
    303115: [ # 明日の空の僕たちへ
        '내일 하늘의 우리들에게', # AuroraCaelum/TakasakiInfo
    ],
    303116: [ # 飴色
        '조청빛', # AuroraCaelum/TakasakiInfo
    ],
    303202: [ # ロストワンの号哭
        "Lost One's Weeping",
        'Weeping of the Lost One',
        "The Lost One's Weeping",
    ],
    303204: [ # ヴィラン
        'Villain',
    ],
    303206: [ # 祝福
        'The Blessing',
    ],
    304102: [ # Reflection in the mirror（104期NEW Ver.）
        'Reflection in the mirror (104th Class NEW Ver.)', # rurimegu/MyPickHasunosora
    ],
    304105: [ # レディバグ
        'Ladybug', # Suyooo/ll-heardle
    ],
    304107: [ # 月夜見海月
        "つくよみくらげ", # Correct Pronunciation
        "Tsukuyomi Kurage", # Correct Pronunciation (Romaji)
        'Tsukuyomi Kurage', # Suki-Suki-Club/link-like-setlist-maker-backend
    ],
    304114: [ # ジョーショーキリュー
        'Joushou Kiryuu', # Suki-Suki-Club/link-like-setlist-maker-backend
    ],
    304121: [ # マハラジャンボリーⅡ
        'Mahara Jamboree II', # Suyooo/ll-heardle
    ],
    304122: [ # 恥は人生のかきすて
        'Haji wa Jinsei no Kakisute', # rurimegu/MyPickHasunosora
    ],
    305102: [ # アンペア
        'Ampere', # Suyooo/ll-heardle
    ],
    305105: [ # アイマイメーデー
        'I My Mayday', # rurimegu/MyPickHasunosora
    ],
    305106: [ # 十六夜セレーネ
        'Izayoi Selene', # Suyooo/ll-heardle
    ],
    305107: [ # アイドゥーミー！
        'I Do Me!', # Suyooo/ll-heardle
    ],
    405102: [ # フルーツパンチ
        'Fruit Punch', # Suyooo/ll-heardle
    ],
    405104: [ # とーひょー☆スター！
        'Tohyo☆Star!', # Suyooo/ll-heardle
    ],
    405105: [ # Very! Very! COCO夏っ
        'Very! Very! COCO Natsu', # Suyooo/ll-heardle
    ],
    405109: [ # ブルウモーメント
        'Blue Moment', # Suyooo/ll-heardle
    ],
    405110: [ # フュージョンクラスト
        'Fusion Crust', # Suyooo/ll-heardle
    ],
    405112: [ # ニャオシグニャル
        'Nyao Signyal', # Suyooo/ll-heardle
    ],
    405113: [ # ハートにQ
        'Heart ni Q', # Suyooo/ll-heardle
    ],
    405115: [ # ドライブ・スペード・クレイジー
        'Drive・Spade・Crazy', # Suyooo/ll-heardle
    ],
    405117: [ # 乙女詞華集
        'Otome Anthology', # Suyooo/ll-heardle
    ],
    405118: [ # バイタルサイン
        'Vital Sign', # Suyooo/ll-heardle
    ],
    405120: [ # ガランドFlash
        'Garando Flash', # Suyooo/ll-heardle
        'Garland Flash', # Suki-Suki-Club/link-like-setlist-maker-backend
    ],
    405121: [ # 平成ギャルズ!!!!
        'Heisei Galz!!!!', # Suyooo/ll-heardle
    ],
    405122: [ # ちょ、尊いLOVE
        'Cho, Toutoi LOVE', # Suyooo/ll-heardle
    ],
    405123: [ # シアター生き様
        'Theater Ikizama', # Suyooo/ll-heardle
    ],
    405126: [ # チャーミングな花束を！
        'Charming na Hanataba o!', # Suyooo/ll-heardle
    ],
    405128: [ # 令嬢モブ！
        'Reijou Mob!', # Suyooo/ll-heardle
    ],
    405131: [ # ハロめぐ讃歌
        'Hello Megu Sanka', # rurimegu/MyPickHasunosora
    ],
    405135: [ # リブウト
        'Reboot', # Suyooo/ll-heardle
    ],
    405137: [ # 不思議と君とライブラリー
        'Fushigi to Kimi to Library', # Suyooo/ll-heardle
    ],
    405138: [ # アイシイ
        'Icy', # Suyooo/ll-heardle
    ],
    405203: [ # もういちど ルミナス
        'Mou Ichido Luminous',
        'もういちど Luminous',
    ],
    405208: [ # 気まぐれロマンティック
        'Kimagure Romantic',
        '気まぐれ Romantic',
    ],
    405301: [ # 虹色Passions!
        'Nijiiro Passions!', # Suyooo/ll-heardle
    ],
    405302: [ # 愛♡スクリ～ム！
        'Ice Cream',
        'Ai♡Scream!', # Suyooo/ll-heardle
    ],
    405305: [ # 僕らは今のなかで
        'Bokura wa Ima no Naka de', # hamproductions/llll-chart
    ],
}

def setup(client: 'bot_client.BotClient'):
    # reload whatever creates the Song instances
    from .game_manager import manager
    from common.song import SongList
    from console_color import color_print
    if isinstance(manager.song_list, SongList):
        color_print(
            f"* Reload {manager.__class__.game_abbr.upper()} song alias list...",
            color = manager.__class__.color
        )
        manager.song_list.reload_lookup()