# Standard Libraries
from typing import Tuple
from time import sleep

# Third-party Libraries
from pynput.mouse import Button, Controller
import cv2 as cv

# Custom Modules
from core.window_capture import WindowCapture
from core.image_processor import ImageProcessor


class BlumAIClicker:
    def start(self):
        mouse = Controller()

        print("Please, open Blum home page. Starting AI clicker in 5 seconds...")
        sleep(3)

        window_name = "Paint - Blum test.png - Paint"
        cfg_file_name = "./yolov4-tiny/yolov4-tiny-custom.cfg"
        weights_file_name = "yolov4-tiny-custom_last.weights"

        wincap = WindowCapture(window_name)
        improc = ImageProcessor(wincap.get_window_size(), cfg_file_name, weights_file_name)

        while (True):
            ss = wincap.get_screenshot()

            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                break

            coordinates = improc.proccess_image(ss)

            coordinates = [c for c in coordinates if c["class_name"] == "star"]

            if len(coordinates) == 0:
                continue

            detected_star = coordinates[0]

            star_x = detected_star['x']
            star_y = detected_star['y']
            star_width = detected_star['w']
            star_height = detected_star['h']

            star_to_hit = self._find_object_center(x=star_x, y=star_y, width=star_width, height=star_height)
            star_center_x = star_to_hit['x']
            star_center_y = star_to_hit['y']

            # Step #1: Press on star
            mouse.position = (star_center_x, star_center_y)
            mouse.press(Button.left)
            sleep(0.1)
            mouse.release(Button.left)

            pass

        print('Finished.')

    @staticmethod
    def _find_object_center(x: int, y: int, width: int, height: int) -> dict:
        center_x = x + width // 2
        center_y = y + height // 2

        center_coordinates = {
            'x': center_x,
            'y': center_y
        }

        return center_coordinates
