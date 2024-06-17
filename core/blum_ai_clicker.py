# Standard Libraries
from time import sleep

# Third-party Libraries
from pynput.mouse import Button, Controller

# Custom Modules
from core.window_capture import WindowCapture


class BlumAIClicker:
    def __init__(self):
        pass

    def start(self):
        mouse = Controller()

        print("Starting Blum AI clicker in 5 seconds...")
        sleep(5)

        window_name = "Blum1"
        cfg_file_name = "./yolov4-tiny/yolov4-tiny-custom.cfg"
        weights_file_name = "yolov4-tiny-custom_last.weights"

        wincap = WindowCapture(window_name)
        improc = ImageProcessor(wincap.get_window_size(), cfg_file_name, weights_file_name)
