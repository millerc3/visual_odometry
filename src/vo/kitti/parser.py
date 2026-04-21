import cv2 as cv
from datetime import datetime
from pathlib import Path
from pandas import to_datetime
from typing import Tuple

from vo.kitti.oxts import Oxts
from vo.kitti.camera_data import CameraData
from vo.util.typings import Image

def parse_oxts_file(filepath:Path) -> Oxts:
    assert filepath.is_file()

    with open(filepath) as f:
        data = f.readline()
        data = [float(d) for d in data.split()]

    return Oxts.from_list(data)

def get_oxts_data(drivepath:Path) -> list[Oxts]:
    assert drivepath.is_dir()

    oxts_dir = drivepath / "oxts/data"

    return [parse_oxts_file(f) for f in oxts_dir.iterdir()]

def get_stereo_images(drivepath:Path) -> Tuple[list[Image], list[Image]]:
    assert drivepath.is_dir()

    left_images_dir = drivepath / "image_02/data"
    right_images_dir = drivepath / "image_03/data"

    assert left_images_dir.is_dir()
    assert right_images_dir.is_dir()

    left_image_paths:list[Path] = [f for f in left_images_dir.iterdir()]
    left_image_paths.sort()
    right_image_paths:list[Path] = [f for f in right_images_dir.iterdir()]
    right_image_paths.sort()

    assert len(right_image_paths) == len(left_image_paths)

    left_images:list[Image] = [cv.imread(f) for f in left_image_paths]
    right_images:list[Image] = [cv.imread(f) for f in right_image_paths]

    return (left_images, right_images)

def get_timestamps(drivepath:Path) -> list[datetime]:
    # assume rectified cameras and only grab left
    timestamp_path = drivepath / "image_02/timestamps.txt"

    timestamps:list[datetime]
    with open(timestamp_path) as f:
        timestamps = [to_datetime(line.strip()) for line in f]
    
    return timestamps

def parse_cam_cam_calib(filepath:Path) -> CameraData:
    assert filepath.is_file()

    with open(filepath) as f:
        for line in f:
            items = line.split()
            if "P_rect_03" not in line:
                continue
            fx = float(items[1])
            fy = float(items[6])
            cx = float(items[3])
            cy = float(items[7])
            tx = float(items[4])

            return CameraData(fx, fy, cx, cy, tx)
    
    raise RuntimeError("CameraData not found in drive path!")

def get_time_per_frame(timestamps:list[datetime]) -> list[float]:
    frame_times:list[float] = list()
    for i in range(len(timestamps) - 1):
        delta = timestamps[i+1] - timestamps[i]
        frame_times.append(delta.microseconds // 1000)
    # make the last frame last as long as the second to last frame
    frame_times.append(frame_times[-1])

    return frame_times