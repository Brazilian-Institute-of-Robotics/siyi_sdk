"""
@file test_get_gimbal_info.py
@Description: This is a test script for using the SIYI SDK Python implementation to get gimbal configuration information
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

from siyi_sdk.siyi_sdk import SIYISDK

def test():
    cam = SIYISDK(server_ip="192.168.144.25", port=37260)
    if not cam.connect():
        print("No connection ")
        exit(1)

    val = cam.requestGimbalInfo()
    sleep(1)
    if val:
        print("Recording state: ", cam.getRecordingState())
        print("Motion mode: ", cam.getMotionMode())
        print("Mounting direction: ", cam.getMountingDirection())
        print("HDR state: ", cam.getGimbalInfo().hdr_state)
        print("Video output status: ", cam.getGimbalInfo().video_output_status)

    cam.disconnect()

if __name__ == "__main__":
    test()