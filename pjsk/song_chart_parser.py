from typing import *

if TYPE_CHECKING:
    from common.chart_factory import BPM

def build_beats_lookup(beat_table: Dict[int, float]) -> List[float]:
    """
    beat_table: {measure_num: number_of_beats}
    """
    beat_table = dict(sorted(beat_table.items()))
    max_beat_measure = max(beat_table)
    beats = [4] * (max_beat_measure + 1)
    for measure in range(max_beat_measure + 1):
        if measure in beat_table:
            beats[measure] = beat_table[measure]
        elif measure > 0:
            beats[measure] = beats[measure - 1]
    return beats


def parse_chart(content: str) -> Dict[str, Any]: #, min_num_measures: int = 0):
    import re
    def process_data(data):
        data = data.replace(" ", "")
        data_len = len(data)
        for i in range(0, data_len, 2):
            temp = data[i: i+2]
            if temp != '00':
                yield (i, data_len), temp

    def parse_speed(data):
        meas_tick, speed = data.split(":")
        meas, tick = tuple(map(int, meas_tick.split("'")))
        return {
            "measure": meas,
            "tick": tick,
            "speed": float(speed),
        }

    lines = content.split("\n") # most chart files use \r\n, though

    default_sort = lambda x: (x["measure"], x["tick"])
    ticks_per_beat = 480
    lines2 = []
    for ln in lines:
        ln = ln.strip()
        # match = re.fullmatch(r'^#(\w+)\s+(.*)$', ln) # space separated, without colon
        # if match:
        #     lines2.append({"type": "meta", "header": match[1], "data": match[2]})
        #     continue
        # match = re.fullmatch(r'^#(\w+):\s*(.*)$', ln) # colon separated
        # if match:
        #     lines2.append({"type": "score", "header": match[1], "data": match[2]})
        #     continue
        # lines2.append({"type": "comment", "header": None, "data": ln})
        if ln[:1] != "#":
            lines2.append({"type": "comment", "header": None, "data": ln})
        elif ":" in ln:
            parts = ln.split(":", 1)
            lines2.append({"type": "score", "header": parts[0][1:], "data": parts[1].lstrip()})
        elif " " in ln:
            parts = ln.split(" ", 1)
            lines2.append({"type": "meta", "header": parts[0][1:], "data": parts[1].lstrip()})
        else:
            lines2.append({"type": "comment", "header": None, "data": ln})
    bpm_mapping = {}
    speed_mapping = {}
    beat_table: Dict[int, float] = {}
    bpm_table = {}
    notes = []
    # num_measures = min_num_measures
    speed_cursor = None
    measure_speed_cursor = None

    for ln in lines2:
        ln_type, ln_header, ln_data = ln["type"], ln["header"], ln["data"]
        if ln_type == "meta":
            if ln_header == "REQUEST":
                test = re.fullmatch(r'"ticks_per_beat (\d+)"', ln_data)
                if test:
                    ticks_per_beat = int(test[1])
            elif ln_header == "MEASUREHS":
                measure_speed_cursor = ln['data']
            elif ln_header == "HISPEED":
                speed_cursor = ln['data']
            elif ln_header == "NOSPEED":
                speed_cursor = None

        elif ln_type == "score":
            if len(ln_header) == 5:
                if ln_header[:3] == "BPM":
                    bpm_mapping[ln_header[3:]] = float(ln_data)
                    continue
                if ln_header[:3] == "TIL":
                    data = ln_data[1:-1]
                    speed_mapping[ln_header[3:]] = list(map(parse_speed, data.split(", "))) if data else []
                    continue
            # test = re.fullmatch(r"BPM(..)", ln_header)
            # if test:
            #     bpm_mapping[test[1]] = float(ln_data)
            #     continue
            # test = re.fullmatch(r"TIL(..)", ln_header)
            # if test:
            #     data = ln_data[1:-1]
            #     speed_mapping[test[1]] = list(map(parse_speed, data.split(", "))) if len(data) else []
            #     # for entry in speed_mapping[test[1]]:
            #         # num_measures = max(num_measures, entry["measure"] + 1)
            #     continue

            measure_raw = ln_header[:3]
            if not measure_raw.isdigit() or not measure_raw.isascii():
                # unrecognized header
                continue
            assert len(ln_header) >= 5
            measure_num, lane_type, lane = int(ln_header[:3]), int(ln_header[3]), int(ln_header[4], 36)
            channel = int(ln_header[5], 36) if len(ln_header) > 5 else None
            if lane_type == 0:
                if lane == 2:
                    beat_table[measure_num] = float(ln_data)
                elif lane == 8:
                    for pos, data in process_data(ln_data):
                        bpm_table[(measure_num, pos)] = bpm_mapping[data]
                else:
                    assert False, f"Unknown lane type: {lane_type}"
            else:
                for pos, data in process_data(ln_data):
                    notes.append({
                        "measure": measure_num,
                        "tick": pos,
                        "lane_type": lane_type,
                        "lane": lane,
                        "note_type": int(data[0], 36),
                        "width": int(data[1], 36),
                        "channel": channel,
                        "speed": speed_cursor,
                    })

            # test = re.fullmatch(r"(\d\d\d)02", ln_header)
            # if test:
            #     beat_table[int(test[1])] = float(ln_data)
            #     # num_measures = max(num_measures, int(test[1]) + 1)
            #     continue
            # test = re.fullmatch(r"(\d\d\d)08", ln_header)
            # if test:
            #     for pos, data in process_data(ln_data):
            #         bpm_table[(int(test[1]), pos)] = bpm_mapping[data]
            #         # num_measures = max(num_measures, int(test[1]) + 1)
            #     continue
            # test = re.fullmatch(r"(\d\d\d)(\d)(.)(.?)", ln_header)
            # if test:
            #     for pos, data in process_data(ln_data):
            #         notes.append({
            #             "measure": int(test[1]),
            #             "tick": pos,
            #             "lane_type": int(test[2]),
            #             "lane": int(test[3], 36),
            #             "note_type": int(data[0], 36),
            #             "width": int(data[1], 36),
            #             "channel": int(test[4], 36) if test[4] else None,
            #             "speed": speed_cursor,
            #         })
                    # num_measures = max(num_measures, int(test[1]) + 1)
    # number of beats in each measure
    if 0 not in beat_table:
        beat_table[0] = 4.0 # default 4/4
    beats = build_beats_lookup(beat_table)
    max_beat_measure = len(beats) - 1
    real_bpm_table = []
    bpm_exist00 = False
    for measure, pos in bpm_table:
        obj = {
            "measure": measure,
            "tick": round(ticks_per_beat * beats[min(measure, max_beat_measure)]) * pos[0] // pos[1],
            "bpm": bpm_table[(measure, pos)]
        }
        real_bpm_table.append(obj)
        if (measure, obj["tick"]) == (0, 0):
            bpm_exist00 = True
    if not bpm_exist00:
        real_bpm_table.append({
            "measure": 0,
            "tick": 0,
            "bpm": 120
        })
    real_bpm_table.sort(key=default_sort)
    for note in notes:
        pos = note["tick"]
        note["tick"] = round(ticks_per_beat * beats[min(note["measure"], max_beat_measure)]) * pos[0] // pos[1]
    return {
        # "measures": num_measures,
        "ticks": ticks_per_beat,
        # "beats": beats,
        "beat_table": beat_table,
        "bpms": real_bpm_table,
        "notes": notes,
        "hispeed": speed_mapping,
        "measurespeed": measure_speed_cursor,
    }


def simplify_chart(chart):
    default_sort_notes = lambda x: (x["measure"], x["tick"], -x["channel"] if x["channel"] else 0)

    beats = build_beats_lookup(chart["beat_table"])
    max_beat_measure = len(beats) - 1

    get_measure = lambda x: x["measure"]
    max_measure = max([
        *map(get_measure, chart["notes"]),
        *map(get_measure, chart["bpms"]),
        *[
            get_measure(entry)
            for v in chart["hispeed"].values()
            for entry in v
        ],
        *chart["beat_table"]
    ])

    measure_tick: List[int] = [0] * (max_measure + 1)
    # index -> starting tick number
    for i in range(max_measure):
        total_ticks = chart["ticks"] * beats[min(i, max_beat_measure)]
        assert total_ticks % 1 == 0 # must be integer
        measure_tick[i + 1] = measure_tick[i] + round(total_ticks)

    real_bpm = []
    raw_bpm_events: Dict[int, dict] = {} # tick: events
    first = True
    for entry in chart["bpms"]:
        time = (entry["measure"], entry["tick"])
        if first:
            assert time == (0, 0)
            new_entry = {
                "tick": 0,
                "sec": 0,
                "bpm": entry["bpm"],
                "sec/tick": 60 / entry["bpm"] / chart["ticks"],
            }
            real_bpm.append(new_entry)
            first = False
        else:
            real_tick = measure_tick[time[0]] + time[1]
            elapsed_tick = real_tick - real_bpm[-1]["tick"]
            elapsed_time = elapsed_tick * real_bpm[-1]["sec/tick"]
            new_entry = {
                "tick": real_tick,
                "sec": real_bpm[-1]["sec"] + elapsed_time,
                "bpm": entry["bpm"],
                "sec/tick": 60 / entry["bpm"] / chart["ticks"],
            }
            real_bpm.append(new_entry)
        raw_bpm_events[new_entry["tick"]] = {
            "sec": new_entry["sec"],
            "bpm": new_entry["bpm"],
            "beats": None, # inherit
        }
    notes_1 = sorted(chart["notes"], key=default_sort_notes)

    extra_data = {
        "hispeed": [],
        # "beats": [
        #     {
        #         "measure": m + 1,
        #         "beat": sd + 1,
        #         "tick": measure_tick[m] + chart["ticks"] * sd
        #     }
        #     for m in range(chart["measures"] + 1)
        #     for sd in range(
        #         1
        #         if m == chart["measures"]
        #         else int(beats[min(m, max_beat_measure)])
        #     )
        # ],
        # "bpms": [{
        #     "sec": bpm["sec"],
        #     "bpm": bpm["bpm"]
        # } for bpm in real_bpm],
    }
    if chart['measurespeed'] is not None:
        chosenspeed = chart['hispeed'][chart['measurespeed']]
        for speed in chosenspeed:
            extra_data["hispeed"].append({
                "tick": measure_tick[speed["measure"]] + speed["tick"],
                "speed": speed['speed']
            })

    def is_path_note(notedata):
        return notedata["note_type"] != 0 and (notedata["note_type"] not in [3, 5] or "flick_type" in notedata or not notedata["ignored"])

    # merge notes
    notes_2 = []
    slide_dict = set()
    flick_dict = {}
    tap_dict = {}

    for note in notes_1:
        current_key = (note["measure"], note["tick"], note["lane"])
        if note["lane_type"] == 3: # slide notes, record their keys
            slide_dict.add(current_key)
        elif note["lane_type"] == 1: # tap notes
            if note["note_type"] in (2, 3, 5, 6, 7, 8): # 2: critical, 3: tick remove, 5: friction, 6: friction critical, 7: slide end remove, 8: slide end remove critical
                tap_dict[current_key] = note["note_type"]


    recorded_notes = set()

    for note in notes_1:
        current_key = (note["measure"], note["tick"], note["lane"])
        if note["lane_type"] == 5: # flick style, not in real notes
            # 1: flick, 2: ease in, 3: left flick, 4: right flick, 5/6: ease out
            flick_dict[current_key] = note["note_type"] # flick style
            continue
        if note["lane_type"] == 1:
            if note["note_type"] not in (1, 2, 4, 5, 6) or current_key in slide_dict:
                # 1: normal, 2: normal critical, 4: skill, 5: friction modifier (can exist separately as green), 6: friction critical modifier (can exist separately as yellow)
                # this tap note is just a slide modifier
                continue
            if current_key in recorded_notes:
                continue
            recorded_notes.add(current_key)
        notes_2.append(note)

    notes_1, notes_2 = notes_2, []
    group_first = {}
    group_path = {}
    group_wait_next = {}
    group9_path = {}
    slide_channel = {}

    # select larger channel for duplicate slide / t-wy
    # the case where duplicate slides are different: 脳漿炸裂ガール Expert
    for note in notes_1:
        current_key = (note["measure"], note["tick"], note["lane"])
        if note["lane_type"] == 3 and note["note_type"] == 1: # start slide
            slide_channel[current_key] = max(slide_channel.get(current_key, -1), note["channel"])

    for note in notes_1:
        current_key = (note["measure"], note["tick"], note["lane"])
        notedata = {
            "tick": measure_tick[note["measure"]] + note["tick"],
            "lane": note["lane"],
            "lane_type": note["lane_type"],
            "note_type": note["note_type"],
            "width": note["width"],
            "channel": note["channel"],
            "critical": tap_dict.get(current_key) in (2, 6, 8),
            "friction": tap_dict.get(current_key) in (5, 6),
        }
        if current_key in flick_dict:
            if note["lane_type"] == 1: # tap to flick
                if flick_dict[current_key] in (1, 3, 4): # flick, left flick, right flick
                    notedata["lane_type"] = 5 # flick
                    notedata["note_type"] = flick_dict[current_key]
            else:
                notedata["flick_type"] = flick_dict[current_key]
        if note["lane_type"] == 3: # slide
            if note["note_type"] == 1: # start slide
                notedata["eliminated"] = slide_channel[current_key] != note["channel"]
                notedata["ignored"] = tap_dict.get(current_key) in (7, 8)
            elif note["note_type"] > 1: # not start slide
                if note["note_type"] in (2,):
                    notedata["ignored"] = (
                        tap_dict.get(current_key) in (7, 8) and
                        notedata.get("flick_type") not in (1, 3, 4) # flicks are not ignored
                    )
                elif note["note_type"] in (3, 5):
                    notedata["ignored"] = tap_dict.get(current_key) == 3
                prev_note = group_path[note["channel"]] # should exist
                # inherit head
                assert prev_note is not None
                if prev_note["critical"]: # inherit critical
                    notedata["critical"] = True
                notedata["eliminated"] = prev_note["eliminated"] # inherit eliminated
                if is_path_note(notedata):
                    # add intervals
                    first_note = group_first[note["channel"]]
                    current_tick = max(
                        prev_note["tick"] + (-prev_note["tick"]) % (chart["ticks"] >> 1), # ceil
                        first_note["tick"] - first_note["tick"] % (chart["ticks"] >> 1) + (chart["ticks"] >> 1) # floor + 1
                    )
                    for tick in range(current_tick, notedata["tick"], chart["ticks"] >> 1): # 8th note step
                        hidden_tick_note = {
                            "tick": tick,
                            "lane": notedata["lane"], # not strictly defined
                            "lane_type": 3,
                            "note_type": 0, # specially assigned value
                            "width": notedata["width"], # not strictly defined
                            "channel": notedata["channel"],
                            "critical": notedata["critical"],
                            "friction": False, # not used
                            "eliminated": notedata["eliminated"],
                            "prev_note": prev_note,
                            "next_note": notedata,
                        }
                        notes_2.append(hidden_tick_note)
                else:
                    group_wait_next[note["channel"]].append(notedata)
                notedata["prev_note"] = prev_note
            if is_path_note(notedata):
                group_path[note["channel"]] = notedata # to-be-added note index
                if note["channel"] in group_wait_next:
                    for tmp in group_wait_next[note["channel"]]:
                        tmp["next_note"] = notedata
                group_wait_next[note["channel"]] = []
                if group_first.get(note["channel"]) is None:
                    group_first[note["channel"]] = notedata
            if notedata["note_type"] == 2: # end slide
                group_first[note["channel"]] = None
        elif note["lane_type"] == 9: # decoration slide
            if note["note_type"] == 1: # start slide
                group9_path[note["channel"]] = notedata # to-be-added note index
            elif note["note_type"] > 1: # 2: end slide, 5: middle points
                prev_note = group9_path[note["channel"]] # should exist
                # inherit head
                assert prev_note is not None
                if prev_note["critical"]: # inherit critical
                    notedata["critical"] = True
                notedata["prev_note"] = prev_note
                group9_path[note["channel"]] = notedata

        notes_2.append(notedata)
    notes_2.sort(key=lambda x: x["tick"])

    notes_1, notes_2 = notes_2, []
    for note in notes_1:
        if note["lane_type"] == 3:
            assert "eliminated" in note
            if note["eliminated"]:
                continue
            del note["eliminated"]
        notes_2.append(note)
    for index, note in enumerate(notes_2):
        note["index"] = index
    for note in notes_2:
        if "prev_note" in note:
            note["prev_index"] = note["prev_note"]["index"]
            del note["prev_note"]
        if "next_note" in note:
            note["next_index"] = note["next_note"]["index"]
            del note["next_note"]

    def tick_to_sec(lst):
        lookup_index = 0
        for obj in lst:
            real_tick = obj["tick"]
            while lookup_index + 1 < len(real_bpm) and real_bpm[lookup_index + 1]["tick"] <= real_tick:
                lookup_index += 1
            elapsed_tick = real_tick - real_bpm[lookup_index]["tick"]
            elapsed_time = elapsed_tick * real_bpm[lookup_index]["sec/tick"]
            obj["sec"] = real_bpm[lookup_index]["sec"] + elapsed_time
            del obj["tick"]

    tick_to_sec(notes_2)
    tick_to_sec(extra_data["hispeed"])
    # tick_to_sec(extra_data["beats"])

    raw_beat_events = []
    for measure, beat in chart["beat_table"].items():
        tick = measure_tick[measure]
        if beat % 1 == 0:
            beat_tuple = ( round(beat), 4 )
        else:
            frac = beat.as_integer_ratio()
            assert 16 % frac[1] == 0, f"Invalid time signature: { frac[0] } / { frac[1] * 4 }" # power of 2 and no more than 16
            beat_tuple = ( frac[0], frac[1] * 4 )
        raw_beat_events.append({
            "tick": tick,
            "tick_backup": tick, # tick gets removed in tick_to_sec
            "beats": beat_tuple,
        })
    tick_to_sec(raw_beat_events) # add sec
    for entry in raw_beat_events:
        tick = entry["tick_backup"]
        if tick in raw_bpm_events:
            raw_bpm_events[tick]["beats"] = entry["beats"]
        else:
            raw_bpm_events[tick] = {
                "sec": entry["sec"],
                "bpm": None, # inherit
                "beats": entry["beats"],
            }

    bpm_events = []
    # initialize
    bpm_cursor = 120
    beats_cursor = (4, 4)
    first = True
    for tick, entry in sorted(raw_bpm_events.items()):
        if first:
            assert tick == 0
            first = False
        if entry["bpm"] is not None:
            bpm_cursor = entry["bpm"]
        if entry["beats"] is not None:
            beats_cursor = entry["beats"]
        bpm_events.append({
            "bpm": bpm_cursor,
            "time": entry["sec"],
            "beats": beats_cursor,
        })
    extra_data["bpm_events"] = bpm_events
    return notes_2, extra_data


def get_skill_notes(notes):
    return [note for note in notes if note["lane"] == 0 and note["width"] == 1 and note["note_type"] == 4]


def get_fever_prepare_note(notes):
    tmp = [note for note in notes if note["lane"] == 15 and note["width"] == 1 and note["note_type"] == 1]
    if len(tmp):
        return tmp[0]
    return None


def get_fever_start_note(notes):
    tmp = [note for note in notes if note["lane"] == 15 and note["width"] == 1 and note["note_type"] == 2]
    if len(tmp):
        return tmp[0]
    return None