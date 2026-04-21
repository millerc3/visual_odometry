
from dataclasses import dataclass

from dataclasses import dataclass

@dataclass(frozen=True)
class Oxts:
    # Position
    lat: float
    lon: float
    alt: float

    # Orientation (radians)
    roll: float
    pitch: float
    yaw: float

    # Velocity (global + local)
    vn: float
    ve: float
    vf: float
    vl: float
    vu: float

    # Acceleration (vehicle frame)
    ax: float
    ay: float
    az: float

    # Acceleration (surface-aligned)
    af: float
    al: float
    au: float

    # Angular rates (vehicle frame)
    wx: float
    wy: float
    wz: float

    # Angular rates (surface-aligned)
    wf: float
    wl: float
    wu: float

    # Accuracy
    pos_accuracy: float
    vel_accuracy: float

    # GPS / navigation metadata
    navstat: int
    numsats: int
    posmode: int
    velmode: int
    orimode: int

    @classmethod
    def from_list(cls, values:list[float]) -> "Oxts":
        return cls(*values)