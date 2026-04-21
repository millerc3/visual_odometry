# visual_odometry

### Object Detection

Object detection using the YOLO v8 model to identify cars and other objects in the scene.

<img width="800" height="241" alt="20260420_object_detection" src="https://github.com/user-attachments/assets/0db57327-0387-4409-8ca0-1a05e7f64d2b" />

### Depth Mapping

SGBM used to calculate disparity between the two stero cameras for generating a depth map of the scene.

<img width="800" height="241" alt="20260420_depth_mapping" src="https://github.com/user-attachments/assets/9b9245f9-16b2-4dba-bc27-5da1d458563a" />


### Distance Estimation

Using the detected objects and the depth map, the distance between the camera and the identified objects can be estimated.
With the physical distance between the cameras and the focal length of the camera, the real world distance can be calculated.

<img width="796" height="240" alt="20260420_distance_estimation" src="https://github.com/user-attachments/assets/8f057f3a-c514-451d-9927-ea759b16ec8f" />

