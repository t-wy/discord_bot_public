from typing import *

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