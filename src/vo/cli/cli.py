import argparse
from pathlib import Path

def handle_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="OpenCV tool using KITTI dataset")
    parser.add_argument("--drive_path", "-p", type=Path, action="store", help="Path to where the desired drive to analyze is stored")

    args = parser.parse_args()
    return args