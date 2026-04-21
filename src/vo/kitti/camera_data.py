from dataclasses import dataclass
from functools import cached_property

@dataclass
class CameraData:
    fx: float
    fy: float
    cx: float
    cy: float
    Tx: float

    @cached_property
    def baseline(self) -> float:
        return -self.Tx / self.fx