from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from ultralytics.engine.results import Results

from typings import Image, DisparityMap

@dataclass
class DriveStep:
    left_frame:Image
    right_frame:Image
    timestamp:datetime
    frame_ms:int = 42   # default to 24 fps
    left_tracked_results:Optional[Results] = None
    disp_map:Optional[DisparityMap] = None
    disp_frame:Optional[Image] = None