# convert from chart_sonolus.c by LittleYang0531
# converted by t-wy
# used to host a sonolus server for testing official charts using the referenced engine
# Code Source:
# https://github.com/SonolusHaniwa/sonolus-sirius-engine/blob/master/convert.h#L120
# up to commit 11be3447bb33e1ebe7f3e9d4fa2b11c75cffeefd

class Note:
    def __init__(self):
        self.startTime = 0
        self.endTime = 0
        self.type = 0
        self.leftLane = 0
        self.laneLength = 0
        self.gimmickType = 0
        self.scratchLength = 0

    def __lt__(self, other):
        if self.endTime == other.endTime:
            return self.leftLane * 100 + self.laneLength < other.leftLane * 100 + other.laneLength
        return self.endTime < other.endTime

from enum import Enum, auto

class NoteType(Enum):
    HiSpeed = -1
    _None = 0
    Normal = 10
    Critical = 20
    Sound = 30
    SoundPurple = auto() # the original source swapped these two
    ScratchSound = 40
    Flick = 50
    HoldStart = 80
    CriticalHoldStart = auto()
    ScratchHoldStart = auto()
    ScratchCriticalHoldStart = auto()
    Hold = 100
    CriticalHold = auto()
    ScratchHold = 110
    ScratchCriticalHold = auto()
    HoldEighth = 900

def fromSirius(text: str, chartOffset: float, bgmOffset: float = 0) -> str:
    def add_log(*args):
        logging.info(" ".join(map(str, args)))
    from typing import Dict, List
    import json, logging
    # 谱面读取
    lines = text.split("\n")
    notes = []
    speed = 1

    for line in lines:
        x = Note()
        components = line.split(",")

        if len(components) < 7:
            break

        x.startTime = float(components[0]) + chartOffset
        x.endTime = float(components[1])
        if x.endTime != -1:
            x.endTime += chartOffset

        x.type = NoteType(int(components[2]))
        x.leftLane = int(components[3])
        x.laneLength = int(components[4])

        s = components[5]
        x.scratchLength = int(components[6])

        if s == "JumpScratch":
            x.gimmickType = 1 # "JumpScratch"
        elif s == "OneDirection":
            x.gimmickType = 2 # "OneDirection"
        elif all(c in "0123456789" for c in s):
            x.gimmickType = int(s)
        else:
            x.gimmickType = 0

        notes.append(x)

    notes.sort(key=lambda note: (note.startTime, note.type.value))
    add_log("[INFO] Total Note Number:", len(notes))

    # 开始转换
    res = []
    single = {}
    holdEnd: List[Note] = []
    SyncLineLeft: Dict[float, int] = {}
    SyncLineRight: Dict[float, int] = {}

    def addSyncLine(beat, leftLane, laneLength):
        if beat not in SyncLineLeft:
            SyncLineLeft[beat] = leftLane
        else:
            SyncLineLeft[beat] = min(SyncLineLeft[beat], leftLane)

        if beat not in SyncLineRight:
            SyncLineRight[beat] = leftLane + laneLength - 1
        else:
            SyncLineRight[beat] = max(SyncLineRight[beat], leftLane + laneLength - 1)

    res.append({
        "archetype": "Sirius Initialization",
        "data": []
    })
    res.append({
        "archetype": "Sirius Input Manager",
        "data": []
    })
    res.append({
        "archetype": "Sirius Stage",
        "data": []
    })
    res.append({
        "archetype": "#BPM_CHANGE",
        "data": [
            {"name": "#BEAT", "value": 0},
            {"name": "#BPM", "value": 60}
        ]
    })

    lastEighthTime = [[0 for _ in range(13)] for _ in range(13)]
    total = 0

    for i, note in enumerate(notes):
        # 提前处理 Sirius HoldEnd;
        while len(holdEnd) and holdEnd[0].endTime <= note.startTime:
            x = holdEnd.pop(0)
            single = {"data": []}
            if x.type == NoteType.Hold or x.type == NoteType.CriticalHold:
                single["archetype"] = "Sirius Hold End"
                single["data"].append({"name": "beat", "value": x.endTime})
                single["data"].append({"name": "stBeat", "value": x.startTime})
                single["data"].append({"name": "lane", "value": x.leftLane})
                single["data"].append({"name": "laneLength", "value": x.laneLength})
                total += 1
            else:
                single["archetype"] = "Sirius Scratch Hold End"
                single["data"].append({"name": "beat", "value": x.endTime})
                single["data"].append({"name": "stBeat", "value": x.startTime})
                single["data"].append({"name": "lane", "value": x.leftLane})
                single["data"].append({"name": "laneLength", "value": x.laneLength})
                single["data"].append({"name": "scratchLength", "value": x.scratchLength})
                total += 1
            res.append(single.copy())
            addSyncLine(x.endTime, x.leftLane, x.laneLength)
        # 处理当前 Note
        x = note
        single = {"data": []}
        if x.type == NoteType.Normal:
            single["archetype"] = "Sirius Normal Note"
            single["data"].append({"name": "beat", "value": x.startTime})
            single["data"].append({"name": "lane", "value": x.leftLane})
            single["data"].append({"name": "laneLength", "value": x.laneLength})
            addSyncLine(x.startTime, x.leftLane, x.laneLength)
            total += 1
        elif x.type == NoteType.Critical:
            single["archetype"] = "Sirius Critical Note"
            single["data"].append({"name": "beat", "value": x.startTime})
            single["data"].append({"name": "lane", "value": x.leftLane})
            single["data"].append({"name": "laneLength", "value": x.laneLength})
            addSyncLine(x.startTime, x.leftLane, x.laneLength)
            total += 1
        elif x.type == NoteType.Flick:
            single["archetype"] = "Sirius Flick Note"
            single["data"].append({"name": "beat", "value": x.startTime})
            single["data"].append({"name": "lane", "value": x.leftLane})
            single["data"].append({"name": "laneLength", "value": x.laneLength})
            single["data"].append({"name": "scratchLength", "value": x.scratchLength})
            addSyncLine(x.startTime, x.leftLane, x.laneLength)
            total += 1
        elif x.type == NoteType.HoldStart:
            single["archetype"] = "Sirius Hold Start"
            single["data"].append({"name": "beat", "value": x.startTime})
            single["data"].append({"name": "lane", "value": x.leftLane})
            single["data"].append({"name": "laneLength", "value": x.laneLength})
            addSyncLine(x.startTime, x.leftLane, x.laneLength)
            total += 1
        elif x.type == NoteType.CriticalHoldStart:
            single["archetype"] = "Sirius Critical Hold Start"
            single["data"].append({"name": "beat", "value": x.startTime})
            single["data"].append({"name": "lane", "value": x.leftLane})
            single["data"].append({"name": "laneLength", "value": x.laneLength})
            addSyncLine(x.startTime, x.leftLane, x.laneLength)
            total += 1
        elif x.type == NoteType.ScratchHoldStart:
            single["archetype"] = "Sirius Scratch Hold Start"
            single["data"].append({"name": "beat", "value": x.startTime})
            single["data"].append({"name": "lane", "value": x.leftLane})
            single["data"].append({"name": "laneLength", "value": x.laneLength})
            addSyncLine(x.startTime, x.leftLane, x.laneLength)
            total += 1
        elif x.type == NoteType.ScratchCriticalHoldStart:
            single["archetype"] = "Sirius Critical Scratch Hold Start"
            single["data"].append({"name": "beat", "value": x.startTime})
            single["data"].append({"name": "lane", "value": x.leftLane})
            single["data"].append({"name": "laneLength", "value": x.laneLength})
            addSyncLine(x.startTime, x.leftLane, x.laneLength)
            total += 1
        elif x.type in [NoteType.Hold, NoteType.CriticalHold, NoteType.ScratchHold, NoteType.ScratchCriticalHold]:
            holdEnd.append(x)
        elif x.type in [NoteType.Sound, NoteType.SoundPurple]:
            lastEighthTime[x.leftLane][x.leftLane + x.laneLength - 1] = x.startTime
            single["archetype"] = "Sirius Sound"
            single["data"].append({"name": "beat", "value": x.startTime})
            single["data"].append({"name": "lane", "value": x.leftLane})
            single["data"].append({"name": "laneLength", "value": x.laneLength})
            single["data"].append({"name": "holdType", "value": NoteType.Hold.value if x.type == NoteType.Sound else NoteType.ScratchHold.value})
            total += 1
        elif x.type == NoteType.ScratchSound:
            lastEighthTime[x.leftLane][x.leftLane + x.laneLength - 1] = x.startTime
            single["archetype"] = "Sirius Scratch Hold End"
            single["data"].append({"name": "beat", "value": x.startTime})
            single["data"].append({"name": "stBeat", "value": x.startTime})
            single["data"].append({"name": "lane", "value": x.leftLane})
            single["data"].append({"name": "laneLength", "value": x.laneLength})
            single["data"].append({"name": "scratchLength", "value": 0})
            addSyncLine(x.startTime, x.leftLane, x.laneLength)
            total += 1
        elif x.type == NoteType.HoldEighth:
            if lastEighthTime[x.leftLane][x.leftLane + x.laneLength - 1] == x.startTime:
                continue
            single["archetype"] = "Sirius Hold Eighth"
            single["data"].append({"name": "beat", "value": x.startTime})
            single["data"].append({"name": "lane", "value": x.leftLane})
            single["data"].append({"name": "laneLength", "value": x.laneLength})
            single["data"].append({"name": "holdType", "value": 0})
            total += 1
        elif x.type == NoteType._None:
            single["archetype"] = "Sirius Split Line"
            single["data"].append({"name": "beat", "value": x.startTime})
            single["data"].append({"name": "endBeat", "value": x.endTime})
            single["data"].append({"name": "split", "value": x.gimmickType % 10})
            single["data"].append({"name": "color", "value": x.scratchLength})
        elif x.type == NoteType.HiSpeed:
            single["archetype"] = "#TIMESCALE_CHANGE"
            single["data"].append({"name": "#BEAT", "value": x.startTime})
            single["data"].append({"name": "#TIMESCALE", "value": x.endTime - chartOffset})

        if "archetype" in single:
            res.append(single)
        else:
            add_log(single)

        if int(10 * (i + 1) / len(notes)) != int(10 * i / len(notes)):
            add_log("[INFO]", 100 * (i + 1) / len(notes), "% Notes Solved.")

    while holdEnd:
        x = holdEnd.pop(0)
        single = {"data": []}
        if x.type == NoteType.Hold or x.type == NoteType.CriticalHold:
            single["archetype"] = "Sirius Hold End"
            single["data"].append({"name": "beat", "value": x.endTime})
            single["data"].append({"name": "stBeat", "value": x.startTime})
            single["data"].append({"name": "lane", "value": x.leftLane})
            single["data"].append({"name": "laneLength", "value": x.laneLength})
            total += 1
        else:
            single["archetype"] = "Sirius Scratch Hold End"
            single["data"].append({"name": "beat", "value": x.endTime})
            single["data"].append({"name": "stBeat", "value": x.startTime})
            single["data"].append({"name": "lane", "value": x.leftLane})
            single["data"].append({"name": "laneLength", "value": x.laneLength})
            single["data"].append({"name": "scratchLength", "value": x.scratchLength})
            total += 1

        res.append(single)
        addSyncLine(x.endTime, x.leftLane, x.laneLength)

    add_log("[INFO] Total Note Number:", total)
    add_log("[INFO] Solving Sync Line...")

    for beat, left in SyncLineLeft.items():
        single = {"data": []}
        single["archetype"] = "Sirius Sync Line"
        single["data"].append({"name": "beat", "value": beat})
        single["data"].append({"name": "left", "value": left})
        single["data"].append({"name": "right", "value": SyncLineRight[beat]})
        res.append(single.copy())

    add_log("[INFO] Sync Line Solved.")

    data = {
        "formatVersion": 5,
        "bgmOffset": bgmOffset,
        "entities": res
    }

    return json.dumps(data, separators=(',', ':'))

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    text = """
<insert test chart>
""".strip()
    chartOffset = 0.5
    bgmOffset = 0
    result = fromSirius(text, chartOffset, bgmOffset)
    # print(result)