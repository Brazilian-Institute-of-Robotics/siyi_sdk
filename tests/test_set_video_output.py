"""
@file test_set_video_output.py
@Description: This is a test script for using the SIYI SDK Python implementation to configure video output
@Author: Claudia Ramos
@Contact: claudia.ramos@fieb.org.br
All rights reserved 2025
"""

import sys
import os
from time import sleep

current = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current)

sys.path.append(parent_directory)

from siyi_sdk.siyi_sdk import SIYISDK

ENABLE_HDMI = 6
ENABLE_CVBS = 7
DISABLE_BOTH = 8

def test():
    cam = SIYISDK(server_ip="192.168.144.25", port=37260)

    if not cam.connect():
        print("No connection ")
        exit(1)

    cam.configureVideoOutput(DISABLE_BOTH)
    sleep(2)

    cam.disconnect()

if __name__ == "__main__":
    test()
