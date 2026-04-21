import matplotlib.pyplot as plt
from math import radians, sin, cos, sqrt, atan2
import numpy as np

from vo.util.drive import Drive



def calc_disatnce(lat1:float, lon1:float, lat2:float, lon2:float) -> float:
    R = 6371000  # meters

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c

def plot_velocity(drive:Drive) -> None:
    velocity:list[float] = list()
    for i in range(1, len(drive.steps)):
        curr_oxts = drive.steps[i].oxts
        prev_oxts = drive.steps[i-1].oxts

        lat1 = prev_oxts.lat
        lon1 = prev_oxts.lon
        lat2 = curr_oxts.lat
        lon2 = curr_oxts.lon

        d = calc_disatnce(lat1, lon1, lat2, lon2)
        t = drive.steps[i].frame_ms / 1000.0
        v = d / t
        velocity.append(v)
    # copy step_1's velocity into step_0
    velocity.insert(0, velocity[0])

    velocity = np.array(velocity)
    plt.plot(velocity)
    plt.show()