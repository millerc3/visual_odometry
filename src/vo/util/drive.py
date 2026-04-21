from pathlib import Path
import cv2 as cv
from datetime import datetime
from typing import Tuple
import pandas as pd
import numpy as np

from vo.util.drive_step import DriveStep
from vo.util.processing import compute_yolo_tracking, computeDepthMap, apply_yolo_boxes, apply_dist_text



class Drive:
    def __init__(self, cam_baseline:float, focal_length:Tuple[float], steps:list[DriveStep]|None=None):
        self.cam_baseline:float = cam_baseline
        self.cam_focal_length:Tuple[float] = focal_length
        self.steps:list[DriveStep] = list()
        if steps:
            self.steps = steps

    def compute_disparty(self) -> None:
        depth_maps = [computeDepthMap(s) for s in self.steps]
        for i, dm in enumerate(depth_maps):
            disp = dm.copy()
            disp = cv.normalize(disp, None, 0, 255, cv.NORM_MINMAX)
            disp = disp.astype(np.uint8)
            self.steps[i].disp_frame = disp
            self.steps[i].disp_map = depth_maps[i]

    def track_left(self) -> None:
        print("Computing YOLO Tracking")
        left_results = compute_yolo_tracking([s.left_frame for s in self.steps])
        for i, s in enumerate(self.steps):
            s.left_tracked_results = left_results[i]

    
    def watch_video(self, frame_getter, overlay_tracking):
        show_video = True
        while show_video:
            for s in self.steps:
                f = frame_getter(s).copy()
                if (s.left_tracked_results is None):
                    self.track_left()

                if overlay_tracking:
                    f = apply_yolo_boxes(f, s.left_tracked_results.boxes)
                    f = apply_dist_text(f, s.disp_map, s.left_tracked_results.boxes, self.cam_focal_length, self.cam_baseline)

                cv.imshow("Drive", f)

                k = cv.waitKey(s.frame_ms*2)
                if k == ord("q"):
                    cv.destroyAllWindows()
                    show_video = False
                    break

    def watch_left(self, overlay_tracking=False):
        if overlay_tracking and self.steps[0].disp_map is None:
            self.compute_disparty()
        if overlay_tracking and self.steps[0].left_tracked_results is None:
            self.track_left()
        self.watch_video(lambda s: s.left_frame, overlay_tracking)
    
    def watch_disparity(self, overlay_tracking=False):
        if self.steps[0].disp_frame is None:
            self.compute_disparty()
        if overlay_tracking and self.steps[0].left_tracked_results is None:
            self.track_left()

        self.watch_video(lambda s: s.disp_frame, overlay_tracking)

    @classmethod
    def from_dir(cls, data_dir:Path):
        assert data_dir
        assert data_dir.is_dir()

        left_images_dir = data_dir / "image_02/data"
        right_images_dir = data_dir / "image_03/data"
        timestamp_file = data_dir / "image_02" / "timestamps.txt"
        cam_calib_file = data_dir / "calib_cam_to_cam.txt"

        assert left_images_dir.is_dir()
        assert right_images_dir.is_dir()
        assert timestamp_file.is_file()
        assert cam_calib_file.is_file()

        timestamps:list[datetime]
        with open(timestamp_file) as f:
            timestamps = [pd.to_datetime(line.strip()) for line in f]

        left_image_paths:list[Path] = [f for f in left_images_dir.iterdir()]
        left_image_paths.sort()
        right_image_paths:list[Path] = [f for f in right_images_dir.iterdir()]
        right_image_paths.sort()
        
        assert len(timestamps) == len(left_image_paths) == len(right_image_paths), "frame counts not matching"

        steps:list[DriveStep] = list()
        for i in range(len(timestamps)):
            step = DriveStep(cv.imread(left_image_paths[i]),
                             cv.imread(right_image_paths[i]),
                             timestamps[i])
            steps.append(step)
        
        for i in range(len(steps)):
            if i == (len(steps) - 1):
                delay = steps[i-1].frame_ms
            else:
                delta = steps[i+1].timestamp - steps[i].timestamp
                delay = delta.microseconds / 1000
            steps[i].frame_ms = int(delay)

        with open(cam_calib_file) as f:
            fx = fy = tx = 0.0
            for line in f:
                items = line.split()
                if "P_rect_03" in items[0]:
                    fx = float(items[1])
                    fy = float(items[6])
                    tx = float(items[4])
               
            baseline = -tx / fx
        print("Camera baseline: %f" % baseline)
        print("Camera fx: %f" % fx)
        print("Camera tx: %f" % tx)
        return cls(baseline, (fx, fy), steps)


