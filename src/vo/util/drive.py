from pathlib import Path
import cv2 as cv
from datetime import datetime
from typing import Tuple
import numpy as np

from vo.util.drive_step import DriveStep
from vo.util.processing import compute_yolo_tracking, computeDepthMap, apply_yolo_boxes, apply_dist_text
from vo.kitti import parser as kitti_parser

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

                k = cv.waitKey(s.frame_ms)
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

        timestamps:list[datetime] = kitti_parser.get_timestamps(data_dir)
        left_images, right_images = kitti_parser.get_stereo_images(data_dir)
        frame_times = kitti_parser.get_time_per_frame(timestamps)
        oxts_data = kitti_parser.get_oxts_data(data_dir)

        steps:list[DriveStep] = list()
        for i in range(len(timestamps)):
            step = DriveStep(left_images[i],
                             right_images[i],
                             timestamps[i],
                             frame_ms=frame_times[i],
                             oxts=oxts_data[i])
            steps.append(step)

        cam_calib_file = data_dir / "calib_cam_to_cam.txt"
        assert cam_calib_file.is_file()
        cam_data = kitti_parser.parse_cam_cam_calib(cam_calib_file)

        return cls(cam_data.baseline, (cam_data.fx, cam_data.fy), steps)


