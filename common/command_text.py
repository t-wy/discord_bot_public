from discord.app_commands import locale_str as _

# Common Texts used in App Commands (Group Names / Command Names / Option Names)

class description:
    accessory_info = _("Accessory information", zh="飾品資訊")
    accessory_name = _('Accessory name', zh="飾品名稱", ja="アクセサリー名")
    accessory_mode = _('The item to fetch', zh="飾品資訊", ja="アクセサリー情報")
    all_ticks = _("Show hidden ticks", zh="顯示隱藏節點")
    another_notation = _('Use another notation', zh="使用其他譜面", ja="アナザー譜面の使用")
    asset_background_images = _("All background images", zh="所有背景圖")
    asset_name = _('Asset name', zh="素材名稱", ja="アセット名")
    asset_posters = _("All posters", zh="所有海報")
    asset_song_jackets = _("All song jackets", zh="所有歌曲封面")
    asset_stamps = _("All stamps", zh="所有貼圖")
    audio_video = _("Game audio / video", zh="遊戲音訊及影片")
    bar_mode = _("Show bars instead of seconds", zh="顯示小節而非秒數")
    bar_mode_experimental = _("Show bars instead of seconds (Experimental)", zh="顯示小節而非秒數 (測試中)")
    card_info = _("Card information", zh="卡面資訊")
    card_name = _('Card name', zh="卡面名稱", ja="カード名")
    card_mode = _('The item to fetch', zh="卡面資訊", ja="カード情報")
    character = _('Character Name', zh="角色名稱", ja="キャラクター名")
    character_info = _("Character Basic Information", zh="角色基本資料", ja="キャラクター設定")
    detail_player = _("Detailed player information", zh="詳細玩家資訊")
    diff = _('Chart difficulty', zh="譜面難度", ja="譜面難易度")
    difference = _("Difference between assets", zh="素材版本間的差異")
    duration_command = _("List of Longest and Shortest songs", zh="最長與最短的歌曲列表", ja="長い曲と短い曲の一覧")
    efficient_songs_command = _("Most time-efficient songs", zh="時間效率最高的歌曲", ja="一番時間効率の高い曲")
    event_borders = _("Event ranking borders", zh="活動排名榜線", ja="イベントボーダー")
    event_info = _("Event information", zh="活動資訊", ja="イベント情報")
    event_name = _('Event name', zh="活動名稱", ja="イベント名")
    event_ranking = _("Rankings of a event.", zh="活動排名")
    event_ranking_predict = _("Event ranking prediction", zh_TW="活動榜線預測", zh_CN="活动榜线预测", ja="イベントボーダー予測")
    game_file = _("Game files", zh="遊戲檔案")
    guess_jacket = _("Guess the song from the cropped jacket", zh="猜出封面的歌曲")
    guess_song = _("Guess the song from the given sample", zh="猜出樣本的歌曲")
    human_readable_size=_('Use file size units', zh="使用檔案大小單位")
    latest_batch_card = _("Latest card batch", zh="最新批卡面")
    latest_batch_poster = _("Latest poster batch", zh="最新批海報")
    master = _("Get master database", zh="取得 Master 資料庫的內容")
    mirror = _('Mirror mode', zh="鏡像模式", ja="ミラーモード")
    next_rank = _("Rankings 1 lower than each border", zh="榜線下一名的數字")
    order_0 = _('The release order of the card batch (0: All unreleased, 1: Latest)', zh="相關卡面的推出批次 (0 為所有未推出，1 為最近)")
    order_1 = _('The release order of the card batch (1: Latest)', zh="相關卡面的推出批次 (1 為最近)")
    order_0_poster = _('The release order of the card batch (0: All unreleased, 1: Latest)', zh="相關卡面的推出批次 (0 為所有未推出，1 為最近)")
    order_1_poster = _('The release order of the card batch (1: Latest)', zh="相關卡面的推出批次 (1 為最近)")
    player_id = _('Player id', zh="玩家 ID", ja="プレイヤー ID")
    poster_info = _("Poster information", zh="海報資訊")
    poster_name = _('Poster name', zh="海報名稱", ja="ポスター名")
    poster_mode = _('The item to fetch', zh="海報資訊", ja="ポスター情報")
    def rank(max: int):
        return _('Target rank (1 ~ {})'.format(max), zh="目標排名 (1 至 {})".format(max), ja="目標順位 (1 ～ {})".format(max))
    recent_songs = _("Recent Songs", zh="最近追加歌曲")
    reencode_audio = _("Reencode the audio file so that it does not take up much space", zh="重新編碼音檔以使其能佔據較小空間")
    reencode_video = _("Reencode the video file so that it is preview-able", zh="重新編碼影片以使其能被預覽")
    reencode = _("Reencode the file so that it can be sent and viewed", zh="重新編碼內容以使其能被傳送及預覽")
    score = _('Score', zh="分數", ja="スコア")
    secsep = _('No. of seconds per column (Default: 10)', zh="每行顯示秒數 (預設: 10)")
    song_chart = _("Chart image", zh="譜面圖片")
    song_info = _("Song basic information", zh="歌曲的基本資訊")
    song_stat = _("Chart note distribution", zh="譜面的各項分布數據")
    show_character = _("Show the character chosen", zh="顯示玩家選擇的角色")
    show_name = _("Display player names", zh="顯示玩家名稱")
    songname = _('Song name', zh="歌曲名稱", ja="曲名")
    table_name = _("Table name", zh="表格名稱")
    version_asset = _("Asset version", zh="資源版本", ja="アセットバージョン")
    zipped = _("Keep sending a zip file instead of separate files", zh="維持發送一個壓縮檔而非獨立檔案")

class locale:
    accessory = _('accessory', zh="飾品", ja="アクセサリー")
    all_ticks = _("all_ticks", zh="全節點")
    another_notation = _('another_notation', zh="其他譜面", ja="アナザー譜面")
    asset = _("asset", zh="素材", ja="アセット")
    asset_name = _('asset_name', zh="素材名稱", ja="アセット名")
    audio_video = _('audio_video', zh="影音")
    background_images = _('background_images', zh="背景圖片") # for asset command (implying plural)
    bar_mode = _("bar_mode", zh="小節模式")
    card = _('card', zh="卡面", ja="カード") # as group name and argument name
    cards = _("cards", zh="卡面", ja="カード") # for asset command (implying plural)
    character = _("character", zh="角色", ja="キャラクター")
    chart = _("chart", zh="譜面")
    detail = _("detail", zh="詳細", ja="詳細")
    diff = _("diff", zh="難度", ja="難易度")
    difference = _('diff', zh="差異")
    duration = _("duration", zh="長度", ja="長さ")
    efficient_songs = _("efficient_songs", zh="效率曲", ja="効率曲")
    event = _("event", zh="活動", ja="イベント")
    event_borders = _("event_borders", zh="活動榜線", ja="イベントボーダー")
    event_name = _('event_name', zh="活動名稱", ja="イベント名")
    file = _('file', zh="檔案")
    guess_jacket = _("guess_jacket", zh="猜封面")
    guess_song = _("guess_song", zh="猜歌曲")
    info = _("info", zh="資訊", ja="情報")
    latest = _('latest', zh="最近", ja="最近")
    latest_batch = _("latest_batch", zh="最新批次")
    master = _('master', zh="master")
    mirror = _("mirror", zh="鏡像", ja="ミラー")
    mode = _("mode", zh="模式", ja="モード")
    name = _('name', zh="名稱", ja="名")
    next_rank = _("next_rank", zh="下一名", ja="次の順位")
    player = _("player", zh="玩家")
    poster = _('poster', zh="海報", ja="ポスター")
    posters = _('posters', zh="海報", ja="ポスター") # for asset command (implying plural)
    predict = _("predict", zh_TW="預測", zh_CN="预测", ja="予測")
    order = _('order', zh="次序")
    rank = _('rank', zh="排名", ja="順位") # as field name
    ranking = _("ranking", zh="排名", ja="ランキング") # as group name
    recent = _("recent", zh="最近", ja="最近")
    reencode = _("reencode", zh="重新編碼")
    score = _('score', zh="分數", ja="スコア")
    secsep = _('secsep', zh="秒數分隔")
    show_character = _("show_character", zh="顯示角色")
    show_name = _("show_name", zh="顯示名稱")
    song = _("song", zh="歌曲", ja="楽曲")
    song_jackets = _('song_jackets', zh="歌曲封面") # for asset command (implying plural)
    songname = _("song_name", zh="歌名", ja="曲名")
    stamps = _('stamps', zh="貼圖") # as asset command name (plural)
    stat = _("stat", zh="統計")
    table_name = _("table_name", zh="表格名稱")
    version = _("version", zh="版本", ja="バージョン")
    zipped = _("zipped", zh="壓縮")