import discord
from typing import *
from discord_msgint import MsgInt

async def wds_efficient_song(message: MsgInt, ver="production"):
    from .wds_file import wds_master, wds_song_duration
    from .wds_master_models import MusicMaster
    from common.rate_limiter import rate_limiter
    from discord_utility import progress_bar
    from common.glossary import SongGlossary
    music_master: List[MusicMaster] = await wds_master("MusicMaster", as_array=True, ver=ver)
    reply_message = await message.reply("Calculating... Please Wait...")
    callback = rate_limiter(lambda index: reply_message.edit(content="Calculating Songs...\n" + progress_bar((index + 1) / len(music_master))))
    stamina_best = {}
    # O(n), with k unique elements
    for index, entry in enumerate(music_master):
        if entry.id < 1000:
            duration = await wds_song_duration(entry.id, ver=ver)
            qualified = True
            if entry.staminaConsumption in stamina_best:
                if duration >= stamina_best[entry.staminaConsumption][1]:
                    qualified = False
            if qualified:
                stamina_best[entry.staminaConsumption] = (entry.staminaConsumption, duration, entry.name)
        await callback(index)
    # O(k log k)
    stamina_best = [stamina_best[k] for k in sorted(stamina_best)]
    stamina_best.sort(key=lambda x: (x[1] / x[0], x[0]))
    # O(k)
    # Maximum number of pops = k
    # Maximum number of non-pop each iteration = 1
    parts = []
    for entry in stamina_best:
        current_consumption, current_duration, current_name = entry
        best_from = 0
        while len(parts) > 0:
            last_best_from, (last_consumption, last_duration, last_name) = parts[-1]
            if current_consumption < last_consumption:
                # impossible to chase
                best_from = None
                break
            intersection = (last_consumption * current_duration - current_consumption * last_duration) / (current_consumption - last_consumption)
            if intersection > last_best_from:
                best_from = intersection
                break
            else:
                parts.pop()
        if best_from is not None:
            parts.append((best_from, entry))
    embed = discord.Embed(
        title=SongGlossary.efficient_songs(message), color=0xee5f5f
    )
    second_str = SongGlossary.seconds(message)
    infinity = "∞"
    parts.append((infinity, None))
    embed.description = "**{}**\n{}".format(
        SongGlossary.menu_time(message),
        "\n".join([
            "**{:.2f}{} ~ {}{}**: {}".format(
                entry[0],
                second_str,
                infinity if next_entry[0] == infinity else "{:.2f}".format(next_entry[0]),
                second_str,
                entry[1][2], # song name
            )
        for index, (entry, next_entry) in enumerate(zip(parts, parts[1:]))])
    )
    await reply_message.edit(content="", embed=embed)