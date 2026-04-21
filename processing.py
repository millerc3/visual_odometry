import cv2 as cv
import numpy as np
from ultralytics import YOLO
from ultralytics.engine.results import Results, Boxes

from drive_step import DriveStep
from typings import DisparityMap, Image

def compute_yolo_tracking(frames:list[Image]) -> list[Results]:
    model = YOLO("yolov8n.pt")
    results = model(frames)
    return results

def apply_yolo_boxes(frame:Image, boxes:Boxes) -> Image:
    if boxes is None:
        return frame
    ret = frame.copy()
    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cv.rectangle(ret, (x1, y1), (x2, y2), (0, 255, 0), 2)
    return ret

def apply_dist_text(frame:Image, disp_map:DisparityMap, boxes:Boxes, focal_lengh, baseline) -> Image:
    ret = frame.copy()
    h, w = disp_map.shape[:2]
    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        x1 = np.clip(x1, 0, w - 1)
        x2 = np.clip(x2, 0, w - 1)
        y1 = np.clip(y1, 0, h - 1)
        y2 = np.clip(y2, 0, h - 1)
        roi = disp_map[y1:y2, x1:x2]
        if roi.size == 0:
            continue
        disparity = np.median(roi)
        if disparity <= 0:
            continue
        dist = focal_lengh[0] * baseline / disparity
        tx = x1
        ty = (y1 + y2) // 2
        cv.putText(ret, f"{dist:.2f}m", (tx, ty), cv.FONT_HERSHEY_SIMPLEX, .6, (255, 255, 255), 2)
    return ret

def computeDepthMap(step:DriveStep) -> DisparityMap:
    window_size = 5
    min_disp = 0
    nDisFactor = 8
    num_disp = 16*nDisFactor - min_disp

    stereo = cv.StereoSGBM.create(minDisparity=min_disp,
                                  numDisparities=num_disp,
                                  blockSize=window_size,
                                  P1=8*3*window_size**2,
                                  P2=40*3*window_size**2,
                                  disp12MaxDiff=1,
                                  uniquenessRatio=15,
                                  speckleWindowSize=100,
                                  speckleRange=1,
                                  preFilterCap=63,
                                  mode=cv.STEREO_SGBM_MODE_SGBM_3WAY)
    
    left = cv.cvtColor(step.left_frame, cv.COLOR_BGR2GRAY)
    left = cv.GaussianBlur(left, (5,5), 0)
    right = cv.cvtColor(step.right_frame, cv.COLOR_BGR2GRAY)
    right = cv.GaussianBlur(right, (5,5), 0)
    disparity = stereo.compute(left, right).astype(np.float32) / 16.0
    return disparity