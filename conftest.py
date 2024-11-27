def pytest_addoption(parser):
    parser.addoption("--camera_ip", action="store", default="127.0.0.1",
                     help="Camera IP")
    parser.addoption("--camera_port", action="store", default="5000",
                     help="Camera Port")

