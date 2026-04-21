import argparse
from pathlib import Path


from drive import Drive

def handle_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="OpenCV tool using KITTI dataset")
    parser.add_argument("--drive_path", "-p", type=Path, action="store", help="Path to where the desired drive to analyze is stored")

    args = parser.parse_args()
    return args

def main():
    args = handle_args()

    drive : Drive = Drive.from_dir(args.drive_path)

    drive.watch_left(overlay_tracking=True)
    #drive.watch_disparity(overlay_tracking=True)


if __name__ == '__main__':
    main()