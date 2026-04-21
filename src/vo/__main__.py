from vo.util.drive import Drive
from vo.cli.cli import handle_args

def main():
    args = handle_args()

    drive : Drive = Drive.from_dir(args.drive_path)

    drive.watch_left(overlay_tracking=True)
    #drive.watch_disparity(overlay_tracking=True)


if __name__ == '__main__':
    main()