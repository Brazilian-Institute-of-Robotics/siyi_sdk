"""
@file test_center_gimbal.py
@Description: This is a test script for using the SIYI SDK Python implementation to adjust zoom level
@Author: Mohamed Abdelkader
@Contact: mohamedashraf123@gmail.com
All rights reserved 2022
"""

import sys
import os
from time import sleep

current = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current)

sys.path.append(parent_directory)

import pytest

from siyi_sdk.siyi_sdk import SIYISDK
from siyi_sdk.siyi_message import MotionModeMsg

@pytest.fixture
def camera_ip(request):
    return request.config.getoption("--camera_ip")

@pytest.fixture
def camera_port(request):
    return request.config.getoption("--camera_port")

def test_absolute_zoom(camera_ip, camera_port):
    cam = SIYISDK(server_ip=camera_ip, port=camera_port)
    assert cam.connect()

    desired_zoom_level = 3.0
    cam.requestAbsoluteZoom(desired_zoom_level)
    sleep(3)

    assert cam.getCurrentZoomLevel() == desired_zoom_level
    cam.requestAbsoluteZoom(1.0)
    sleep(3)

    assert cam.getCurrentZoomLevel() == 1.0

    cam.disconnect()

def test_fpv_mode():
    cam = SIYISDK(server_ip=camera_ip, port=camera_port)

    assert cam.connect()
    assert cam.requestFPVMode()
    sleep(2)

    cam.disconnect()

def test_set_gimbal_rotation():
    cam = SIYISDK(server_ip=camera_ip, port=camera_port)
    assert cam.connect()
    YAW, PITCH = 10, -50
    cam.setGimbalRotation(YAW, PITCH)
    attitude_yaw, attitude_pitch, _ = cam.getAttitude()
    assert attitude_yaw == YAW
    assert attitude_pitch == PITCH

    cam.disconnect()

def test_lock_mode():
    cam = SIYISDK(server_ip=camera_ip, port=camera_port)

    assert cam.connect()
    assert cam.requestLockMode()
    sleep(2)
    assert cam.getMotionMode() == MotionModeMsg.LOCK

    cam.disconnect()

def test_follow_mode():
    cam = SIYISDK(server_ip=camera_ip, port=camera_port)

    assert cam.connect()
    assert cam.requestFollowMode()
    sleep(2)
    assert cam.getMotionMode() == MotionModeMsg.FOLLOW

    cam.disconnect()

def test_zoom():
    cam = SIYISDK(server_ip=camera_ip, port=camera_port)

    assert cam.connect()

    assert cam.requestZoomIn()
    sleep(1)
    assert cam.requestZoomHold()
    sleep(1)

    assert cam.requestZoomOut()
    sleep(1)
    assert cam.requestZoomHold()
    sleep(1)
    assert cam.getZoomLevel() > -1

    cam.disconnect()
