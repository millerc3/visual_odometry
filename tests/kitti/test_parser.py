from math import isclose

from vo.util.paths import TEST_DATA
from vo.kitti.parser import parse_oxts_file, parse_cam_cam_calib

def test_cam_data_parser():
    example_file = TEST_DATA / "calib_cam_to_cam.txt"

    # P_rect_03: 7.215377e+02 0.000000e+00 6.095593e+02 -3.395242e+02 
    #            0.000000e+00 7.215377e+02 1.728540e+02  2.199936e+00 
    #            0.000000e+00 0.000000e+00 1.000000e+00  2.729905e-03

    cam_data = parse_cam_cam_calib(example_file)

    assert isclose(cam_data.fx, 7.215377e+02)
    assert isclose(cam_data.Tx, -3.395242e+02)
    assert isclose(cam_data.baseline, .470556, rel_tol=1e-5)

def test_oxts_file_parser():
    example_file = TEST_DATA / "oxts_1.txt"

    oxts = parse_oxts_file(example_file)

    # lat lon alt
    # 49.015003823272 8.4342971002335 116.43032836914
    assert isclose(oxts.lat, 49.015003823272)
    assert isclose(oxts.lon, 8.4342971002335)
    assert isclose(oxts.alt, 116.43032836914)

    # roll pitch yaw
    # 0.035752 0.00903 -2.6087069803847
    assert isclose(oxts.roll, 0.035752)
    assert isclose(oxts.pitch, 0.00903)
    assert isclose(oxts.yaw, -2.6087069803847)

    # vn ve vf vl vu
    # -6.811441479104 -11.275641809511 13.172716663769 -0.12475264293164 -0.032919903047354
    assert isclose(oxts.vn, -6.811441479104)
    assert isclose(oxts.ve, -11.275641809511)
    assert isclose(oxts.vf, 13.172716663769)
    assert isclose(oxts.vl, -0.12475264293164)
    assert isclose(oxts.vu, -0.032919903047354)

    # check the rest later
    ...