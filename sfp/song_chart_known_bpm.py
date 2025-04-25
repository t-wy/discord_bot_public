from common.chart_factory import BPM
from typing import *

known_bpms: Dict[int, List[Union[
    Tuple[BPM, Tuple[int, int]],
    Tuple[BPM, Tuple[int, int], bool]
]]] = {
}