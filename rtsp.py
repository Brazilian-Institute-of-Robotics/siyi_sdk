"""
RTSP client for getting video stream from SIYI cameras, e.g. ZR10, A8 Mini
ZR10 webpage: http://en.siyi.biz/en/Gimbal%20Camera/ZR10/overview/
A8 mini page: https://shop.siyi.biz/products/siyi-a8-mini?VariantsId=10611
Author : Mohamed Abdelkader
Email: mohamedashraf123@gmail.com
Copyright 2022

Required:
- OpenCV
    (sudo apt-get install python3-opencv -y)
- imutils
    pip install imutils
- Gstreamer (https://gstreamer.freedesktop.org/documentation/installing/index.html?gi-language=c)
    (Ubuntu: sudo apt-get install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-bad1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio -y)
- Deepstream (only for Nvidia Jetson boards)
    (https://docs.nvidia.com/metropolis/deepstream/dev-guide/text/DS_Quickstart.html#jetson-setup)
"""
import cv2
import imutils
from imutils.video import VideoStream
import logging
from time import time, sleep

class SIYIRTSP:
    def __init__(self, rtsp_url="rtsp://192.168.144.25:8554/main.264", cam_name="ZR10", debug=False) -> None:
        '''
        Receives video stream from SIYI cameras

        Params
        --
        - rtsp_url [str] RTSP url
        - cam_name [str] camera name (optional)
        - debug [bool] print debug messages
        '''
        self._rtsp_url=rtsp_url
        # Desired image wiodth/height
        self._width=640
        self._height=480

        self._frame=None

        self._debug= debug # print debug messages
        if self._debug:
            d_level = logging.DEBUG
        else:
            d_level = logging.INFO
        LOG_FORMAT=' [%(levelname)s] %(asctime)s [SIYIRTSP::%(funcName)s] :\t%(message)s'
        logging.basicConfig(format=LOG_FORMAT, level=d_level)
        self._logger = logging.getLogger(self.__class__.__name__)

        # Flad to stop frame grapping loop, and close windows
        self._stopped=False

        self._show_window=False

        self._last_image_time=time()

        # timeout (seconds) before disconnecting
        # If returned frame is None for this amount of time, exit
        self._connection_timeout=2.0

        # start stream
        self.start()

    def setShowWindow(self, f):
        self._show_window=f

    def getFrame(self):
        return(self._frame)

    def start(self):
        try:
            self._logger.debug("Starting stream...")
            self._stream = VideoStream(self._rtsp_url).start()
            self._stopped=False
        except Exception as e:
            self._logger.error(" Could not start stream %s", e)
            exit(1)
        
    def close(self):
        self._logger.info("Closing stream...")
        cv2.destroyAllWindows()
        self._stream.stop()
        self._stopped=True

    def loop(self):
        self._last_image_time=time()
        while not self._stopped:
            self._logger.debug("Reading frame...")
            self._frame = self._stream.read()

            if (time()-self._last_image_time)> self._connection_timeout:
                self._logger.warning("Connection timeout. Exiting")
                self.close()
            
            if self._frame is None:
                continue

            self._last_image_time=time()

            self._frame = imutils.resize(self._frame, width=self._width, height=self._height)

            if self._show_window:
                cv2.imshow('SIYI Stream', self._frame)
                
                key = cv2.waitKey(1) & 0xFF

                if key == ord('q'):
                    self.close()
                    break


def test():
    stream = SIYIRTSP(debug=False)
    stream.setShowWindow(True)
    stream.loop()

if __name__=="__main__":
    test()