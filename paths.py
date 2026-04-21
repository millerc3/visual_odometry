from pathlib import Path


LEFT_CAM_DIRNAME = "image_02"
RIGHT_CAM_DIRNAME = "image_03"

def get_image_paths(drive_path: Path, left:bool) -> list[Path]:
    assert drive_path
    assert drive_path.is_dir()

    cam_dirname = LEFT_CAM_DIRNAME if left else RIGHT_CAM_DIRNAME
    images_dir = drive_path / cam_dirname / "data"

    ret: list[Path] = [f for f in images_dir.iterdir()]
    ret.sort()

    return ret
