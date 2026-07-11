"""
This file is a common interface for a Chart class for creating chart images.
Implement subclasses for the note skin in different games
This is hot-reloadable now since all subclasses are unreloaded
"""

"""
MIT License

Copyright (c) 2026 t-wy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from PIL import Image, ImageDraw
from typing import *
from enum import Enum
from common.exception import CustomException

if TYPE_CHECKING:
    import numpy as np

Point = Tuple[float, float]
Color = Union[Tuple[int, int, int], Tuple[int, int, int, int]]

def pick_first_color(color: Union[Color, List[Color]]) -> Color:
    if isinstance(color, list):
        return color[0]
    return color

class BPMCalculationException(CustomException):
    """
    Cannot determine the BPM of the given chart.
    """
    def __init__(self, message=None):
        super().__init__("Cannot determine the BPM of the given chart." if message is None else message)

class Label:
    def __init__(self, time: float, lane: int, width: int = 1, speed: float = 1):
        """
        time: note time (in seconds)
        lane: lane number
        width: note span
        speed: note speed (for video only, also display a speed marker if it is not 1)
        """
        self.time = time
        self.lane = lane
        self.width = width
        self.speed = speed

class Note(Label):
    def __init__(self, time: float, lane: int, width: int=1, speed: float=1, counted: bool=True, **extra):
        """
        color: note color
        note_type: note type (extra fields)
        counted: whether the note is counted towards the total notes
        """
        super().__init__(time, lane, width, speed)
        self.counted = counted
        self.extra = extra
    
    async def draw_on(self, canvas: ImageDraw.ImageDraw, get_x: Callable[[int], float], get_y: Callable[[int], float]):
        x_left = get_x(self.lane)
        x_right = get_x(self.lane + self.width)
        y = get_y(self.time)
        color = (255, 128, 192)
        canvas.rectangle(((x_left + 1 + 6, y - 6), (x_right - 1 - 6, y + 6)), color)
        canvas.ellipse(((x_left + 1, y - 6), (x_left + 1 + 12, y + 6)), color)
        canvas.ellipse(((x_right - 1 - 12, y - 6), (x_right - 1, y + 6)), color)

    def __repr__(self):
        return f"{self.__class__.__name__}(time={self.time}, lane=({self.lane}, {self.lane + self.width - 1}), speed={self.speed}, counted={self.counted}, {', '.join(f'{k}={v}' for k, v in self.extra.items())})"

class Flick(Note):
    class Direction(Enum):
        FREE = "free"
        UP = "up"
        DOWN = "down"
        LEFT = "left"
        RIGHT = "right"
        LEFTRIGHT = "leftright"
        def mirror(self) -> 'Flick.Direction':
            if self == Flick.Direction.LEFT:
                return Flick.Direction.RIGHT
            elif self == Flick.Direction.RIGHT:
                return Flick.Direction.LEFT
            else:
                return self
    def __init__(self, time: float, lane: int, width: int=1, speed: float=1, counted: bool=True, direction: Optional[Direction] = None, **kwargs):
        super().__init__(time, lane, width, speed, counted, **kwargs)
        self.direction = direction
    
    async def draw_on(self, canvas: ImageDraw.ImageDraw, get_x: Callable[[int], float], get_y: Callable[[int], float]):
        await Note.draw_on(self, canvas, get_x, get_y)
        x_left = get_x(self.lane)
        x_right = get_x(self.lane + self.width)
        x_middle = (x_left + x_right) / 2
        y = get_y(self.time)
        color = (224, 200, 255)
        if self.direction == Flick.Direction.UP or self.direction == Flick.Direction.FREE:
            canvas.polygon([
                (x_middle - 6, y - 6),
                (x_middle + 6, y - 6),
                (x_middle, y - 18),
            ], color)
        if self.direction == Flick.Direction.DOWN or self.direction == Flick.Direction.FREE:
            canvas.polygon([
                (x_middle - 6, y + 6),
                (x_middle + 6, y + 6),
                (x_middle, y + 18),
            ], color)
        if self.direction == Flick.Direction.LEFT or self.direction == Flick.Direction.LEFTRIGHT or self.direction == Flick.Direction.FREE:
            canvas.polygon([
                (x_left, y),
                (x_left + 9, y - 12),
                (x_left + 9, y + 12),
            ], color)
        if self.direction == Flick.Direction.RIGHT or self.direction == Flick.Direction.LEFTRIGHT or self.direction == Flick.Direction.FREE:
            canvas.polygon([
                (x_right, y),
                (x_right - 9, y - 12),
                (x_right - 9, y + 12),
            ], color)

class Connector:
    """
    The connector connecting two notes (by default linearly)
    This may be known as "Note Line".
    Implement get_polygon and get_x_percentage to change the shape.
    """
    def __init__(self, note1: Label, note2: Label, color: Tuple[int, int, int]=(128, 192, 255), channel: int=1, **extra):
        """        
        channel: note channel (for layering)
        """
        self.note1 = note1
        self.note2 = note2
        self.channel = channel
        self.color = color
        self.extra = extra
    
    def get_x_range(self, y_time: float) -> Tuple[float, float]:
        """
        Derive x percentage from y percentage
        """
        from common.curve import lerp, unlerp
        y_percentage = unlerp(self.note1.time, self.note2.time, y_time)
        return lerp(self.note1.lane, self.note2.lane, y_percentage), lerp(self.note1.lane + self.note1.width, self.note2.lane + self.note2.width, y_percentage)

    async def get_polygon(self, get_x, get_y):
        """
        Implement this to change the polygon
        """
        notep, note = self.note1, self.note2
        x1, x2, y = get_x(note.lane), get_x(note.lane + note.width), get_y(note.time)
        xp1, xp2, yp = get_x(notep.lane), get_x(notep.lane + notep.width), get_y(notep.time)
        points = [
            (xp1 + 2, yp),
            (xp2 - 2, yp),
            (x2 - 2, y),
            (x1 + 2, y)
        ]
        return points
    
    async def draw_polygon(self, canvas: ImageDraw.ImageDraw, points: List[Point]):
        """
        Implement this to change the way the polygon is handled
        """
        canvas.polygon(points, self.color)
    
    async def draw_on(self, canvas: ImageDraw.ImageDraw, get_x: Callable[[int], float], get_y: Callable[[int], float]):
        """
        Implement this if it is not drawn as a polygon
        """
        points: List[Point] = await self.get_polygon(get_x, get_y)
        await self.draw_polygon(canvas, points)

class EaseInQuadConnector(Connector):
    """
    (x(t), y(t)) = (t^2, t)
    """
    def __init__(self, note1: Label, note2: Label, color: Tuple[int, int, int]=(128, 192, 255), channel: int=1, **extra):
        """        
        channel: note channel (for layering)
        """
        super().__init__(note1, note2, color, channel, **extra)
    
    def get_x_range(self, y_time: float) -> Tuple[float, float]:
        from common.curve import lerp, unlerp
        y_percentage = unlerp(self.note1.time, self.note2.time, y_time)
        x_percentage = y_percentage ** 2
        return lerp(self.note1.lane, self.note2.lane, x_percentage), lerp(self.note1.lane + self.note1.width, self.note2.lane + self.note2.width, x_percentage)
    
    async def get_polygon(self, get_x: Callable[[int], float], get_y: Callable[[int], float]) -> List[Point]:
        notep, note = self.note1, self.note2
        xn1, xn2, yn = get_x(note.lane), get_x(note.lane + note.width), get_y(note.time)
        xp1, xp2, yp = get_x(notep.lane), get_x(notep.lane + notep.width), get_y(notep.time)
        from common.curve import quadratic_bezier_to_points
        ym = (yn + yp) / 2
        return quadratic_bezier_to_points(*[
            (xp1 + 2, yp), (xp1 + 2, ym), (xn1 + 2, yn)
        ], max_distance=0.5) + quadratic_bezier_to_points(*[
            (xn2 - 2, yn), (xp2 - 2, ym), (xp2 - 2, yp)
        ], max_distance=0.5)

class EaseOutQuadConnector(Connector):
    """
    (x(t), y(t)) = (1-(1-t)^2, t)
    """
    def __init__(self, note1: Label, note2: Label, color: Tuple[int, int, int]=(128, 192, 255), channel: int=1, **extra):
        """        
        channel: note channel (for layering)
        """
        super().__init__(note1, note2, color, channel, **extra)
    
    def get_x_range(self, y_time: float) -> Tuple[float, float]:
        from common.curve import lerp, unlerp
        y_percentage = unlerp(self.note1.time, self.note2.time, y_time)
        x_percentage = 1 - (1 - y_percentage) ** 2
        return lerp(self.note1.lane, self.note2.lane, x_percentage), lerp(self.note1.lane + self.note1.width, self.note2.lane + self.note2.width, x_percentage)
    
    async def get_polygon(self, get_x: Callable[[int], float], get_y: Callable[[int], float]) -> List[Point]:
        notep, note = self.note1, self.note2
        xn1, xn2, yn = get_x(note.lane), get_x(note.lane + note.width), get_y(note.time)
        xp1, xp2, yp = get_x(notep.lane), get_x(notep.lane + notep.width), get_y(notep.time)
        from common.curve import quadratic_bezier_to_points
        ym = (yn + yp) / 2
        return quadratic_bezier_to_points(*[
            (xp1 + 2, yp), (xn1 + 2, ym), (xn1 + 2, yn)
        ], max_distance=0.5) + quadratic_bezier_to_points(*[
            (xn2 - 2, yn), (xn2 - 2, ym), (xp2 - 2, yp)
        ], max_distance=0.5)

class QuadraticBezierConnector(Connector):
    """
    A connector with quadratic bezier support 
    """

    def __init__(self, note1: Label, note2: Label, control: Label, color: Tuple[int, int, int]=(128, 192, 255), channel: int=1, **extra):
        """        
        channel: note channel (for layering)
        """
        super().__init__(note1, note2, color, channel, **extra)
        self.control = control
    
    def get_x_range(self, y_time: float) -> Tuple[float, float]:
        from common.curve import lerp, quadratic_lerp, quadratic_unlerp
        t = quadratic_unlerp(self.note1.time, self.control.time, self.note2.time, y_time)
        x0_center = self.note1.lane + self.note1.width / 2
        x1_center = self.control.lane + self.control.width / 2
        x2_center = self.note2.lane + self.note2.width / 2
        center = quadratic_lerp(x0_center, x1_center, x2_center, t)
        width = lerp(self.note1.width, self.note2.width, t)
        return center - width / 2, center + width / 2
    
    async def get_polygon(self, get_x: Callable[[int], float], get_y: Callable[[int], float]) -> List[Point]:
        notep, note = self.note1, self.note2
        xn1, xn2, yn = get_x(note.lane), get_x(note.lane + note.width), get_y(note.time)
        xp1, xp2, yp = get_x(notep.lane), get_x(notep.lane + notep.width), get_y(notep.time)
        xm, ym = get_x(self.control.lane + self.control.width / 2), get_y(self.control.time)
        y, yp = get_y(note.time), get_y(notep.time)
        from common.curve import quadratic_trapezoid_to_points
        return quadratic_trapezoid_to_points(
            p0l = (xp1 + 2, yp),
            p0r = (xp2 - 2, yp),
            p1 = (xm, ym),
            p2l = (xn1 + 2, yn),
            p2r = (xn2 - 2, yn),
            max_distance = 0.5
        )

class PolyConnector:
    """
    A connector that takes multiple labels only to create a polygon with head and tail counted as combo
    """
    def __init__(self, notes: List[Label], channel: int=1, **extra):
        """        
        channel: note channel (for layering)
        """
        self.notes = notes
        self.channel = channel
        self.extra = extra

    async def get_polygon(self, get_x: Callable[[int], float], get_y: Callable[[int], float]) -> List[Point]:
        points = [
            (get_x(note.lane) + 2, get_y(note.time))
        for note in self.notes] + [
            (get_x(note.lane + note.width) - 2, get_y(note.time))
        for note in self.notes[::-1]]
        return points
    
    async def draw_polygon(self, canvas: ImageDraw.ImageDraw, points: List[Point]):
        canvas.polygon(points, (128, 192, 255))
    
    async def draw_on(self, canvas: ImageDraw.ImageDraw, get_x: Callable[[int], float], get_y: Callable[[int], float]):
        points: List[Point] = await self.get_polygon(get_x, get_y)
        await self.draw_polygon(canvas, points)

class Tick(Note):
    """
    A tick having its own lane and width specified
    """
    def __init__(self, time: float, lane: int, width: int=1, speed: float=1, counted: bool=True, visible: bool=True, **extra):
        super().__init__(time, lane, width, speed, counted, **extra)
        self.visible = visible

    async def draw_on(self, canvas: ImageDraw.ImageDraw, get_x: Callable[[int], float], get_y: Callable[[int], float]):
        x_left = get_x(self.lane)
        x_right = get_x(self.lane + self.width)
        x_middle = (x_left + x_right) / 2
        y = get_y(self.time)
        color = (64, 192, 255) if self.visible else (168, 168, 168)
        canvas.polygon([
            (x_middle + 6, y),
            (x_middle, y + 6),
            (x_middle - 6, y),
            (x_middle, y - 6),
        ], color)

class ConnectorTick:
    """
    A tick having its lane and width derived from the connector at a given time
    """
    def __init__(self, time: float, target: Connector, counted: bool=True, visible: bool=True, **extra):
        self.time = time
        self.target = target
        self.counted = counted
        self.visible = visible
        self.extra = extra

    async def draw_on(self, canvas: ImageDraw.ImageDraw, get_x: Callable[[int], float], get_y: Callable[[int], float]):
        """
        Codes that determine the position
        """
        x_left, x_right = self.target.get_x_range(self.time)
        await self.draw_on_main(canvas, get_x(x_left), get_x(x_right), get_y(self.time))

    async def draw_on_main(self, canvas: ImageDraw.ImageDraw, x_left: float, x_right: float, y: float):
        """
        Codes that draw the tick after determining the position
        """
        # style the tick
        x_middle = (x_left + x_right) / 2
        color = (64, 192, 255) if self.visible else (168, 168, 168)
        canvas.polygon([
            (x_middle + 6, y),
            (x_middle, y + 6),
            (x_middle - 6, y),
            (x_middle, y - 6),
        ], color)

class Beat:
    def __init__(self, measure_num: int, beat_num: int, time: float):
        # measure num and beat num are 1-based
        self.measure_num = measure_num
        self.beat_num = beat_num
        self.time = time
    def __repr__(self):
        return f"Beat(time={self.time}, measure_num={self.measure_num}, beat_num={self.beat_num})"

class BPM:
    def __init__(self, bpm: float, time: float):
        self.bpm = float(bpm)
        self.time = time
    def __str__(self):
        if self.bpm.is_integer():
            return str(int(self.bpm))
        if self.bpm % 0.5 == 0:
            return f"{self.bpm:.1f}"
        return f"{self.bpm:.2f}"
    def __repr__(self):
        return f"BPM(bpm={self.bpm}, time={self.time:.4f})"

class Marker:
    def __init__(self, time: float, text: str, color: Color):
        self.time = time
        self.text = text
        self.color = color

class ScrollSpeed:
    def __init__(self, speed: float, time: float):
        self.speed = speed
        self.time = time
    def __str__(self):
        if self.speed % 1 == 0:
            return str(int(self.speed))
        if 0 < self.speed < 1:
            return "{:.3f}".format(self.speed)
        return "{:.2f}".format(self.speed)

class Region:
    def __init__(self, time1: float, time2: float, color: Color):
        if time1 > time2:
            time1, time2 = time2, time1
        self.time1 = time1
        self.time2 = time2
        self.color = color

class AutoBeat:
    def __init__(self, beat: Tuple[int, int] = (4, 4)):
        self.beat = beat

class Chart:
    def __init__(self, num_lanes: int, name: str="Untitled", difficulty: str="NORMAL", level: Union[int, str]= 1, lane_offset: int=0, duration: float=...):
        """
        name: song name
        num_lanes: number of lanes
        lane_offset: the lane number of the leftmost lane
        difficulty: the name of the difficulty (e.g. NORMAL, HARD, MASTER)
        level: representation of the Lv.
        duration: set if the duration is known or not necessarily ends right at the last note
        """
        self.name = name
        self.difficulty = difficulty
        self.level = level

        self.num_lanes = num_lanes
        self.lane_offset = lane_offset

        # objects
        self.background: List[Union[Note, Connector, PolyConnector]] = []
        self.notes: List[Note] = []
        self.labels: List[Label] = []
        """
        remember the labels to facilitate mirroring
        """
        self.ticks: List[Union[Tick, ConnectorTick]] = []
        """
        drawn on connectors
        """
        self.connectors: List[Union[Connector, PolyConnector]] = []
        self.regions: List[Region] = []

        # bpm exact?
        self.guessed_bpm: bool = False
        """
        whether the bpm is exact
        """

        # for bar mode
        self.beats: List[Beat] = []

        # for markers
        self.scroll_speeds: List[ScrollSpeed] = []
        self.bpm_changes: List[BPM] = []
        self.markers: List[Marker] = []
        
        self.duration: float = duration
        self.auto_duration: bool = duration is None

        self.finalized: bool = False
        # TODO
        self.lyrics = []
    
    def set_bpm(self, bpm: float, offset: float = 0, beat: Tuple[int, int] = (4, 4), guessed: bool=True):
        """
        offset: the time that the specified BPM starts (in second)
        """
        self.bpm_changes = [
            BPM(bpm, offset)
        ]
        self.beats = AutoBeat(beat)
        self.guessed_bpm = guessed
    
    def set_bpm_smart(self, guess_bpm=None):
        from .chart_utility import find_bpm, find_offset_and_beat
        timing_points = [*set([x.time for x in self.notes] + [x.time for x in self.ticks])] # avoid duplicates
        guessed_bpm = find_bpm(timing_points, guess_bpm=guess_bpm)
        offset, beat = find_offset_and_beat([timing_points], guessed_bpm)
        self.set_bpm(guessed_bpm, offset, beat, guessed=True)
    
    def set_bpms(self, bpms: List[Union[
        Tuple[BPM, Tuple[int, int]],
        Tuple[BPM, Tuple[int, int], bool]
    ]], end_time: Optional[float] = None, guessed: bool=False):
        """
        Set BPM According to a list of (BPM, beat[, force new bar = False]) tuples
        """
        assert len(bpms) > 0
        self.bpm_changes = [bpm for bpm, *_ in bpms]
        bar_index = 1
        beat_num = 1
        self.beats = []
        # Placeholders
        actual_offset: float = 0
        unit_duration: float = 1
        current_beat: Tuple[int, int] = (4, 4)
        epsilon = 0.002 # considering ms (=0.001s) resolution
        if end_time is None:
            end_time = max(max(self.notes, key=lambda x: x.time).time if len(self.notes) else 0, bpms[-1][0].time)
        for index, next_entry in enumerate(bpms + [
            (BPM(bpms[-1][0].bpm, end_time), bpms[-1][1])
        ]):
            if len(next_entry) == 2:
                next_bpm, next_beat = next_entry
                force_new = False
            else:
                next_bpm, next_beat, force_new = next_entry
            if index == 0:
                current_bpm = bpms[0][0].bpm
                current_offset = bpms[0][0].time
                current_beat = bpms[0][1]
            else:
                current_bpm = bpms[index - 1][0].bpm
                current_offset = bpms[index - 1][0].time
                current_beat = bpms[index - 1][1]
            # The time measure changes
            if next_beat != current_beat:
                force_new = True
            next_offset = next_bpm.time
            beat_duration = 60 / current_bpm
            unit_duration = beat_duration / (current_beat[1] / 4)
            measure_duration = current_beat[0] * unit_duration
            # handle measure 0 (i.e. Fillers before Measure 1)
            if index == 0:
                # the bar 0
                bar_index -= 1
                actual_offset = current_offset - measure_duration
            elif abs(current_offset - actual_offset) < epsilon:
                # auto snapping
                actual_offset = current_offset
            # create all beats from current offset to next offset
            while actual_offset + epsilon <= next_offset: # don't occupy next beat
                # No need to create beats before time 0
                if actual_offset >= 0:
                    self.beats.append(Beat(
                        measure_num = bar_index,
                        beat_num = beat_num,
                        time = actual_offset
                    ))
                beat_num += 1
                if actual_offset + unit_duration > next_offset + epsilon:
                    # BPM changing within beat
                    next_beat_duration = 60 / next_bpm.bpm
                    next_unit_duration = next_beat_duration / (next_beat[1] / 4)
                    partial_beat = (next_offset - actual_offset) / unit_duration
                    actual_offset = next_offset + next_unit_duration * (1 - partial_beat)
                else:
                    actual_offset += unit_duration
                # Start a new bar
                if beat_num > current_beat[0]:
                    beat_num = 1
                    bar_index += 1
            if force_new:
                # force start a new bar (esp. when encountering incomplete bars)
                if beat_num != 1:
                    beat_num = 1
                    bar_index += 1
                actual_offset = next_offset
        # handle the last measure
        # assert actual_offset + epsilon > end_time
        while True:
            # Draw the next beat right after end_time
            self.beats.append(Beat(
                measure_num = bar_index,
                beat_num = beat_num,
                time = actual_offset
            ))
            beat_num += 1
            if beat_num == 2:
                # the song has finished and the first beat of the next bar has been drawn
                # this also handles the case current_beat[0] = 1 (as long as this if is put before the "beat_num > current_beat[0]" part)
                break
            actual_offset += unit_duration
            if beat_num > current_beat[0]:
                beat_num = 1
                bar_index += 1
        self.guessed_bpm = guessed
    
    def set_channel_smart(self, foreground: bool = True, background: bool = True):
        def get_start_time(connector: Union[Connector, PolyConnector]):
            return connector.note1.time if isinstance(connector, Connector) else connector.notes[0].time
        def get_end_time(connector: Union[Connector, PolyConnector]):
            return connector.note2.time if isinstance(connector, Connector) else connector.notes[-1].time
        connectors_list = []
        if foreground:
            connectors_list.append(self.connectors)
        if background:
            connectors_list.append([obj for obj in self.background if isinstance(obj, Connector) or isinstance(obj, PolyConnector)])
        for connectors in connectors_list:
            connectors.sort(key = get_end_time)
            channel_last = []
            for connector in connectors:
                temp = 0
                while temp < len(channel_last) and get_start_time(connector) <= channel_last[temp]:
                    temp += 1
                connector.channel = temp
                if temp == len(channel_last):
                    channel_last.append(get_end_time(connector))
                else:
                    channel_last[temp] = get_end_time(connector)
    
    def finalize(self):
        if self.finalized:
            return
        if len(self.scroll_speeds) == 0:
            self.scroll_speeds.append(ScrollSpeed(1, 0))
        self.notes.sort(key=lambda x: x.time)
        if self.duration is ...:
            self.duration = self.notes[-1].time if len(self.notes) else 0
            self.auto_duration = True
        # for whole song with the same BPM and measure
        if isinstance(self.beats, AutoBeat):
            assert len(self.bpm_changes) == 1
            num, deno = self.beats.beat
            # offset: when the first bar start
            bpm, offset = self.bpm_changes[0].bpm, self.bpm_changes[0].time
            bar = -1
            beat_duration = 60 / bpm
            unit_duration = beat_duration / (deno / 4)
            measure_duration = num * unit_duration
            self.beats = []
            while True:
                time = offset + bar * measure_duration
                if time > self.duration + 0.002:
                    break
                for i in range(num):
                    actual_time = time + i * unit_duration
                    if actual_time >= 0:
                        self.beats.append(Beat(
                            measure_num = bar + 1,
                            beat_num = i + 1,
                            time = actual_time
                        ))
                    if i == 0 and actual_time > self.duration:
                        break
                bar += 1
        self.ticks.sort(key=lambda x: x.time)
        self.channels = set([x.channel for x in self.connectors])
        self.background_channels = set([x.channel for x in self.background if hasattr(x, "channel")])
        self.bpm_changes.sort(key=lambda x: x.time)
        # remove duplicate bpm
        self.bpm_changes = self.bpm_changes[:1] + [b for a, b in zip(self.bpm_changes[:-1], self.bpm_changes[1:]) if a.bpm != b.bpm]
        self.scroll_speeds.sort(key=lambda x: x.time)
        self.regions.sort(key=lambda x: x.time2)

    class LaneStyle(Enum):
        BOUNDARY = 0
        """
        The vertical lines are drawn at the left and right boundary of each lane
        """
        CENTER = 1
        """
        The vertical lines are drawn at the center of each lane
        """
    
    @property
    def note_times(self) -> List[float]:
        # get the list of counted times
        return [x.time for x in self.notes + self.ticks if x.counted]
    
    @property
    def note_count(self) -> int:
        return len(self.note_times)

    async def gen_chart(
        self,
        *,
        mirror: bool = False,
        time_marker: bool = True,
        note_marker: bool = True,
        hidden_ticks: bool = False,
        bar_mode: Optional[bool] = False,
        show_distance: bool = False,
        seconds_per_column: int = 10,
        lane_style: LaneStyle = LaneStyle.BOUNDARY,
        major_lane: int = 1,
        minor_lane: int = 1,
        progress_callback: Optional[Callable[[str, Tuple[int, int]], Coroutine[Any, Any, None]]] = None,
    ) -> Image.Image:
        """
        bar_mode: True means bar# marker, False means per-second marker, None means no horizontal lines
        major_lane: spaces between highlighted white vertical lines (1 means all vertical lines are highlighted, 0 means no vertical lines are highlighted)
        minor_lane: spaces between highlighted gray vertical lines when it's not white (1 means all vertical lines are highlighted, 0 means no vertical lines are highlighted)
        """
        if not self.finalized:
            self.finalize()
        if major_lane > 0:
            if lane_style == Chart.LaneStyle.CENTER:
                assert (self.num_lanes - 1) % major_lane == 0
            elif lane_style == Chart.LaneStyle.BOUNDARY:
                assert self.num_lanes % major_lane == 0
        if minor_lane > 0:
            assert major_lane > 0
            assert major_lane % minor_lane == 0
            if lane_style == Chart.LaneStyle.CENTER:
                assert (self.num_lanes - 1) % minor_lane == 0
            elif lane_style == Chart.LaneStyle.BOUNDARY:
                assert self.num_lanes % minor_lane == 0
        from PIL import Image, ImageFont, ImageDraw
        import common.graphics as ImageDraw
        from image_composition import alpha_composition, BlendMode
        from math import ceil
        import asyncio
        import numpy as np
        bpm_text = "???"
        if len(self.bpm_changes) > 0:
            bpms = [self.bpm_changes[0]] + [y for x, y in zip(self.bpm_changes[:-1], self.bpm_changes[1:]) if x.bpm != y.bpm]
            bpm_text = "→".join([str(x) for x in bpms])
        if self.guessed_bpm:
            bpm_text += " (Guessed)"
        time_array = np.array(self.note_times)
        title = f"{self.name}　{self.difficulty}　Lv.{self.level}　{len(time_array)} Notes　BPM={bpm_text}"
        pixels_per_second = 400 # pixel height per second
        pixels_width = 325 # width of the chart (single column)
        pixels_offsetx = 70 # offset from the left of the chart image
        pixels_col = (pixels_width - pixels_offsetx - 5) // (self.num_lanes * 2) * 2 # pixel width of each column
        assert pixels_offsetx + pixels_col * self.num_lanes < pixels_width # overflow prevention
        extra_filling = 60 # extra pixel height shown for each column
        title_height = 60 # height of the header (and footer)
        fnt = ImageFont.truetype("font/RoNOWStd-GB-Fallback.otf", 20) # font for time marker and note number marker
        fnt_tiny = ImageFont.truetype("font/RoNOWStd-GB-Fallback.otf", 12) # font for marker text
        fnt_title = ImageFont.truetype("font/RoNOWStd-GB-Fallback.otf", 40) # font for header and footer
        offset_y = title_height
        if bar_mode == True:
            if len(self.beats) == 0:
                # the bpm is never set
                raise BPMCalculationException()
            start_sec = [0]
            measures = [0] + [x.time for x in self.beats if x.beat_num == 1]
            if self.duration > measures[-1]:
                measures.append(self.duration)
            for measure1, measure2 in zip(measures[:-1], measures[1:]):
                duration = measure2 - measure1
                if duration > seconds_per_column + 1e-4: # just break it
                    while start_sec[-1] + seconds_per_column < measure2:
                        start_sec.append(start_sec[-1] + seconds_per_column)
                elif measure2 > start_sec[-1] + seconds_per_column + 1e-4:
                    start_sec.append(measure1)
            start_sec.append(measures[-1])
            duration = measures[-1]
        else:
            start_sec = [
                seconds_per_column * i
                for i in range(ceil(self.duration / seconds_per_column) + 1)
            ]
            duration = start_sec[-1] = ceil(self.duration)
        img_height = ceil(duration * pixels_per_second + extra_filling * 2)
        temp_size = (pixels_width, img_height)

        # left-aligned
        def get_x(lane):
            return pixels_offsetx + pixels_col * (lane - self.lane_offset)
        def get_y(sec):
            return img_height - extra_filling - pixels_per_second * sec
        assert get_x(self.lane_offset) == pixels_offsetx

        if mirror:
            for note in self.notes:
                note.lane = self.lane_offset * 2 + self.num_lanes - note.width - note.lane
                if isinstance(note, Flick):
                    note.direction = note.direction.mirror()
                await asyncio.sleep(0)
            for note in self.background:
                if isinstance(note, Note):
                    note.lane = self.lane_offset * 2 + self.num_lanes - note.width - note.lane
                    if isinstance(note, Flick):
                        note.direction = note.direction.mirror()
                await asyncio.sleep(0)
            for note in self.ticks:
                if isinstance(note, Tick):
                    note.lane = self.lane_offset * 2 + self.num_lanes - note.width - note.lane
                await asyncio.sleep(0)
            for note in self.labels:
                note.lane = self.lane_offset * 2 + self.num_lanes - note.width - note.lane
                await asyncio.sleep(0)
            for note in self.connectors:
                await asyncio.sleep(0)

        black = (0, 0, 0) # background
        gray = (64, 64, 64) # end marker
        white = (255, 255, 255)

        if temp_size[0] == 0 and temp_size[1] == 0:
            return None

        temp_image = Image.new('RGBA', temp_size, black)
        temp_graphics = ImageDraw.Draw(temp_image)

        pixels_offsetx2 = pixels_offsetx + pixels_col * self.num_lanes
        def add_marker(time, text, color, dashed=False):
            y_coord = get_y(time)
            if dashed:
                temp_graphics.line(((pixels_offsetx - 2, y_coord), (pixels_offsetx, y_coord)), fill=color)
                for x in range(pixels_offsetx + 8, pixels_offsetx2 + 4, 8):
                    temp_graphics.line(((x - 4, y_coord), (min(x, pixels_offsetx2), y_coord)), fill=color)
            else:
                temp_graphics.line(((pixels_offsetx - 2, y_coord), (pixels_offsetx2, y_coord)), fill=color)
            temp_graphics.line(((pixels_offsetx - 2, y_coord), (pixels_offsetx - 2, y_coord - 2)), fill=color)
            intensity = sum([c * w for c, w in zip(color, (0.2126, 0.7152, 0.0722))])
            temp_graphics.text((pixels_offsetx - 2, y_coord - 2), text, fill=color, font=fnt_tiny, anchor="rd", stroke_width=2, stroke_fill=white)
            if intensity > 0.5:
                # pad black border
                temp_graphics.text((pixels_offsetx - 2, y_coord - 2), text, fill=color, font=fnt_tiny, anchor="rd", stroke_width=1, stroke_fill=black)

        temp_image_channels: Dict[Image.Image] = {}
        temp_graphics_channels: Dict[ImageDraw.ImageDraw] = {}
        temp_image_channels[(None, None)] = Image.new('RGBA', temp_size, ((255, 255, 255, 0)))
        temp_graphics_channels[(None, None)] = ImageDraw.Draw(temp_image_channels[(None, None)])
        for c in self.channels:
            temp_image_channels[(c, True)] = Image.new('RGBA', temp_size, ((255, 255, 255, 0)))
            temp_graphics_channels[(c, True)] = ImageDraw.Draw(temp_image_channels[(c, True)])
            await asyncio.sleep(0)
        for c in self.background_channels:
            temp_image_channels[(c, False)] = Image.new('RGBA', temp_size, ((255, 255, 255, 0)))
            temp_graphics_channels[(c, False)] = ImageDraw.Draw(temp_image_channels[(c, False)])
            await asyncio.sleep(0)

        # after the end of chart
        temp_graphics.rectangle(((pixels_offsetx, 0), (pixels_offsetx2, get_y(self.duration))), gray)

        region_last = []
        for region in self.regions:
            chosen = 0
            while chosen < len(region_last) and region.time1 <= region_last[chosen]:
                chosen += 1
            x = get_x(self.lane_offset + self.num_lanes) - chosen * 8
            temp_graphics.rectangle((
                (x - 8, get_y(region.time2)),
                (x, get_y(region.time1))
            ), region.color)
            if chosen >= len(region_last):
                region_last.append(region.time2)
            else:
                region_last[chosen] = region.time2
        
        if lane_style == Chart.LaneStyle.CENTER:
            for lane in range(self.num_lanes):
                if minor_lane != 0: # major_lane != 0
                    if lane % minor_lane != 0:
                        continue
                elif major_lane != 0:
                    if lane % major_lane != 0:
                        continue
                elif lane != 0 and lane != self.num_lanes - 1: # both major_lane and minor_lane == 0
                    continue
                x = (
                    get_x(self.lane_offset + lane) +
                    get_x(self.lane_offset + lane + 1)
                ) // 2
                temp_graphics.line(
                    [(x, 0), (x, img_height)],
                    white if (
                        (major_lane > 0 and lane % major_lane == 0) or
                        lane == 0 or lane == self.num_lanes - 1
                    ) else gray,
                    1
                )
                await asyncio.sleep(0)
        elif lane_style == Chart.LaneStyle.BOUNDARY:
            for lane in range(self.num_lanes + 1):
                if minor_lane != 0: # major_lane != 0
                    if lane % minor_lane != 0:
                        continue
                elif major_lane != 0:
                    if lane % major_lane != 0:
                        continue
                elif lane != 0 and lane != self.num_lanes - 1: # both major_lane and minor_lane == 0
                    continue
                x = get_x(self.lane_offset + lane)
                temp_graphics.line(
                    [(x, 0), (x, img_height)],
                    white if (
                        (major_lane > 0 and lane % major_lane == 0) or
                        lane == 0 or lane == self.num_lanes
                    ) else gray,
                    1
                )
                await asyncio.sleep(0)

        if bar_mode == True:
            for beat in self.beats:
                time = beat.time
                bar = beat.measure_num
                if beat.beat_num == 1:
                    temp_graphics.line([(pixels_offsetx, get_y(time)), (pixels_offsetx2, get_y(time))], white, 1)
                else:
                    temp_graphics.line([(pixels_offsetx, get_y(time)), (pixels_offsetx2, get_y(time))], gray, 1)
                    continue
                if note_marker:
                    note_count = time_array[time_array <= time + 1e-4].shape[0]
                else:
                    note_count = None
                if note_marker and time_marker:
                    temp_graphics.text((pixels_offsetx - 2, get_y(time)), "#" + str(bar), font=fnt, anchor="rd")
                    temp_graphics.text((pixels_offsetx - 2, get_y(time)), "{}".format(note_count), font=fnt, anchor="ra")
                elif time_marker:
                    temp_graphics.text((pixels_offsetx - 2, get_y(time)), "#" + str(bar), font=fnt, anchor="rm")
                elif note_marker:
                    temp_graphics.text((pixels_offsetx - 2, get_y(time)), "{}".format(note_count), font=fnt, anchor="rm")
                await asyncio.sleep(0)
        elif bar_mode == False:
            for time in range(ceil(duration) + 1):
                temp_graphics.line([(pixels_offsetx, get_y(time)), (pixels_offsetx2, get_y(time))], white, 1)
                if time + 0.5 < duration:
                    temp_graphics.line([(pixels_offsetx, get_y(time + 0.5)), (pixels_offsetx2, get_y(time + 0.5))], gray, 1)
                if note_marker:
                    note_count = time_array[time_array <= time + 1e-4].shape[0]
                else:
                    note_count = None
                if note_marker and time_marker:
                    temp_graphics.text((pixels_offsetx - 2, get_y(time)), "{}:{:02}".format(time//60, time%60), font=fnt, anchor="rd")
                    temp_graphics.text((pixels_offsetx - 2, get_y(time)), "{}".format(note_count), font=fnt, anchor="ra")
                elif time_marker:
                    temp_graphics.text((pixels_offsetx - 2, get_y(time)), "{}:{:02}".format(time//60, time%60), font=fnt, anchor="rm")
                elif note_marker:
                    temp_graphics.text((pixels_offsetx - 2, get_y(time)), "{}".format(note_count), font=fnt, anchor="rm")
                await asyncio.sleep(0)
        
        # distance markers at bottom
        if show_distance and len(self.bpm_changes) > 0:
            yellow = (255, 255, 0)
            timing_points = sorted(set([x.time for x in self.notes] + [x.time for x in self.ticks if x.visible])) # avoid duplicates
            bpm_changes_index_last = 0
            bpm_changes_index_now = 0
            for a, b in zip(timing_points[:-1], timing_points[1:]):
                while bpm_changes_index_now + 1 < len(self.bpm_changes) and self.bpm_changes[bpm_changes_index_now + 1].time < b:
                    bpm_changes_index_now += 1
                if bpm_changes_index_now == bpm_changes_index_last:
                    bar_length = 4 * 60 / self.bpm_changes[bpm_changes_index_now].bpm # duration of a whole note (4 quarter notes)
                    dist = (b - a) / bar_length
                else:
                    bar_length_b = 4 * 60 / self.bpm_changes[bpm_changes_index_now].bpm
                    bar_length_a = 4 * 60 / self.bpm_changes[bpm_changes_index_last].bpm
                    change_time = self.bpm_changes[bpm_changes_index_now].time
                    dist = (b - change_time) / bar_length_b + (change_time - a) / bar_length_a
                num_ticks_test = dist * 480
                if -0.1 < round(num_ticks_test) - num_ticks_test < 0.1:
                    def gcd(a, b):
                        while b:
                            a, b = b, a % b
                        return a
                    dist_frac = (round(num_ticks_test), 480)
                    dist_frac_gcd = gcd(dist_frac[0], dist_frac[1])
                    add_marker(a, "{}/{}".format(
                        "" if dist_frac[0] == dist_frac_gcd else (dist_frac[0] // dist_frac_gcd),
                        dist_frac[1] // dist_frac_gcd
                    ), yellow, dashed=True)
                else:
                    if dist < 1:
                        # remove 0 before the decimal point
                        add_marker(a, "{:.3f}".format(dist)[1:], yellow, dashed=True)
                    else:
                        add_marker(a, "{:.3f}".format(dist), yellow, dashed=True)
                bpm_changes_index_last = bpm_changes_index_now
        
        # change in scroll speed
        lime = (0, 255, 0)
        if len(self.scroll_speeds) > 1:
            for speed in self.scroll_speeds:
                add_marker(speed.time, f"⇩×{speed}", lime)
                await asyncio.sleep(0)
        
        # change in note speed
        for note in self.notes:
            if note.speed != 1:
                speed_repr = note.speed
                if speed_repr.is_integer():
                    speed_repr = int(speed_repr)
                elif 0 < speed_repr < 1:
                    speed_repr = f"{speed_repr:.3f}"
                else:
                    speed_repr = f"{speed_repr:.2f}"
                add_marker(note.time, f"☄×{speed_repr}", lime)
                await asyncio.sleep(0)

        # change in bpm
        red = (255, 0, 0)
        if len(self.bpm_changes) > 1:
            for bpm in self.bpm_changes:
                add_marker(bpm.time, f"♩{bpm}", red)
                await asyncio.sleep(0)

        # other markers
        for marker in self.markers:
            add_marker(marker.time, marker.text, marker.color)
            await asyncio.sleep(0)

        # background connectors behind real connectors
        for obj in self.background:
            target_channel = (obj.channel, False) if hasattr(obj, "channel") else (None, None)
            await obj.draw_on(temp_graphics_channels[target_channel], get_x, get_y)
            await asyncio.sleep(0)

        for connector in self.connectors:
            await connector.draw_on(temp_graphics_channels[(connector.channel, True)], get_x, get_y)
            await asyncio.sleep(0)

        # check parallel
        previous_note: Optional[Note] = None
        for note in self.notes:
            if previous_note is not None:
                if previous_note.time == note.time:
                    x1 = get_x(previous_note.lane + 0.5)
                    x2 = get_x(note.lane + 0.5)
                    y = get_y(note.time)
                    temp_graphics.line([(x1, y), (x2, y)], white, 3)
            previous_note = note
            await asyncio.sleep(0)

        # prevent blocking
        # from basic_utility import to_async
        # alpha_composition_async = to_async(alpha_composition)
        
        # temp_image_channel = Image.new('RGBA', temp_size, ((255, 255, 255, 0)))
        # for key in temp_image_channels:
        #     if key[1] == False: # background layers
        #         temp_image_channel = await alpha_composition_async(temp_image_channel, temp_image_channels[key], BlendMode.Screen)
        #     await asyncio.sleep(0)
        # for key in temp_image_channels:
        #     if key[1] is None: # background notes
        #         temp_image_channel = await alpha_composition_async(temp_image_channel, temp_image_channels[key], BlendMode.Screen)
        #     await asyncio.sleep(0)
        # for key in temp_image_channels:
        #     if key[1] == True:
        #         temp_image_channel = await alpha_composition_async(temp_image_channel, temp_image_channels[key], BlendMode.Screen)
        #     await asyncio.sleep(0)
        # screen operation is fully commutative right?
        # temp_image_channel = Image.new('RGBA', temp_size, ((255, 255, 255, 0)))
        # for key in temp_image_channels:
        #     temp_image_channel = await alpha_composition_async(temp_image_channel, temp_image_channels[key], BlendMode.Screen)
        #     await asyncio.sleep(0)
        # screen operation is fully commutative right? (2)
        from PIL import ImageChops
        temp_image_channel = Image.new('RGBa', temp_size, ((0, 0, 0, 0)))
        for key_img in temp_image_channels.values():
            temp_image_channel = ImageChops.screen(temp_image_channel, key_img.convert("RGBa"))
            await asyncio.sleep(0)
        temp_image.alpha_composite(temp_image_channel.convert("RGBA"))

        # draw all diamonds
        for index, tick in enumerate(self.ticks):
            if hidden_ticks or tick.visible: # visible point
                await tick.draw_on(temp_graphics, get_x, get_y)
                if progress_callback is not None:
                    await progress_callback("ticks", (index, len(self.ticks)))
            await asyncio.sleep(0)

        for index, note in enumerate(self.notes[::-1]):
            await note.draw_on(temp_graphics, get_x, get_y)
            if progress_callback is not None:
                await progress_callback("notes", (index, len(self.notes)))
            await asyncio.sleep(0)
        
        # convert scroll image to chart image
        new_seconds_per_column = 0 if len(start_sec) <= 1 else max([start_sec[x + 1] - start_sec[x] for x in range(len(start_sec) - 1)])
        result_size = (max(1, len(start_sec) - 1) * pixels_width, ceil(new_seconds_per_column * pixels_per_second) + extra_filling * 2 + offset_y + title_height)
        result_image = Image.new('RGBA', result_size, black)
        result_graphics = ImageDraw.Draw(result_image)
        if temp_size[0] != 0 and temp_size[1] != 0:
            for x in range(len(start_sec) - 1):
                start_y = int(get_y(start_sec[x])) + extra_filling
                cropped_height = start_y - ceil(get_y(start_sec[x + 1])) + extra_filling
                result_image.alpha_composite(temp_image, (
                    x * pixels_width, # dest left
                    result_size[1] - title_height - cropped_height, # dest top
                ), (
                    0, start_y - cropped_height, # src left, src top
                    pixels_width, start_y # src right, src bottom
                ))
        result_graphics.rectangle(((0, 0), (result_size[0], title_height)), black)
        result_graphics.text((25, title_height >> 1), title, font=fnt_title, anchor="lm")
        result_graphics.rectangle(((0, result_size[1] - title_height), (result_size[0], result_size[1])), black)
        result_graphics.text((result_size[0] - 25, result_size[1] - (title_height >> 1)), "Coded by TWY, Generated by 社長#3716", font=fnt_title, anchor="rm")
        return result_image

    # TODO: Design the structure for creating video
    # async def gen_chart_video(
    #     ...
    # ):
    #     pass