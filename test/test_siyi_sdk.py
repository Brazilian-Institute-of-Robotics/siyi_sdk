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

from siyi_sdk import SIYISDK
from siyi_sdk.siyi_message import MotionModeMsg

def test_absolute_zoom():
    cam = SIYISDK(server_ip="192.168.144.25", port=37260)
    assert cam.connect()

    desired_zoom_level = 3.0
    cam.requestAbsoluteZoom(desired_zoom_level)
    sleep(3)
    # print(f"Zoom level: {cam.getCurrentZoomLevel()}")
    assert cam.getCurrentZoomLevel() == desired_zoom_level
    cam.requestAbsoluteZoom(1.0)
    sleep(3)
    # print(f"Zoom level: {cam.getCurrentZoomLevel()}")
    assert cam.getCurrentZoomLevel() == 1.0

    cam.disconnect()

def test_fpv_mode():
    cam = SIYISDK(server_ip="192.168.144.25", port=37260)

    assert cam.connect()
    assert cam.requestFPVMode()
    sleep(2)
    print("Current motion mode: ", cam._motionMode_msg.mode)

    cam.disconnect()

def test_set_gimbal_rotation():
    cam = SIYISDK(server_ip="192.168.144.25", port=37260)
    assert cam.connect()
    YAW, PITCH = 10, -50
    cam.setGimbalRotation(YAW, PITCH)
    attitude_yaw, attitude_pitch, _ = cam.getAttitude()
    assert attitude_yaw == YAW
    assert attitude_pitch == PITCH

    #print("Attitude (yaw,pitch,roll) eg:", cam.getAttitude())

    cam.disconnect()

def test_lock_mode():
    cam = SIYISDK(server_ip="192.168.144.25", port=37260)

    assert cam.connect()
    assert cam.requestLockMode()
    sleep(2)
    assert cam.getMotionMode() == MotionModeMsg.LOCK
    # print("Current motion mode: ", cam._motionMode_msg.mode)

    cam.disconnect()

def test_follow_mode():
    cam = SIYISDK(server_ip="192.168.144.25", port=37260)

    assert cam.connect()
    assert cam.requestFollowMode()
    sleep(2)
    assert cam.getMotionMode() == MotionModeMsg.FOLLOW
    # print("Current motion mode: ", cam._motionMode_msg.mode)

    cam.disconnect()

def test_zoom():
    cam = SIYISDK(server_ip="192.168.144.25", port=37260)

    assert cam.connect()

    assert cam.requestZoomIn()
    sleep(1)
    assert cam.requestZoomHold()
    sleep(1)
    print("Zoom level: ", cam.getZoomLevel())

    assert cam.requestZoomOut()
    sleep(1)
    assert cam.requestZoomHold()
    sleep(1)
    assert cam.getZoomLevel() > -1
    # print("Zoom level: ", cam.getZoomLevel())

    cam.disconnect()