from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from ultralytics.engine.results import Results

from vo.util.typings import Image, DisparityMap
from vo.kitti.oxts import Oxts

@dataclass
class DriveStep:
    left_frame:Image
    right_frame:Image
    timestamp:datetime
    frame_ms:int = 42   # default to 24 fps
    left_tracked_results:Optional[Results] = None
    disparity_map:Optional[DisparityMap] = None
    diaprity_vis:Optional[Image] = None
    oxts:Optional[Oxts] = None