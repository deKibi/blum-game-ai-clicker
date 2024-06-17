# Standard Libraries
from typing import Tuple
from time import sleep

# Third-party Libraries
from pynput.mouse import Button, Controller
import cv2 as cv

# Custom Modules
from core.window_capture import WindowCapture
from core.image_processor import ImageProcessor


mouse = Controller()


class BlumAIClicker:
    def start(self):
        print("Please, open Blum home page. Starting AI clicker in 4 seconds...")
        sleep(4)

        # test window: Paint - Blum test.png - Paint
        window_name = "Blum1"
        cfg_file_name = "./yolov4-tiny/yolov4-tiny-custom.cfg"
        weights_file_name = "yolov4-tiny-custom_last.weights"

        wincap = WindowCapture(window_name)
        image_size = wincap.get_window_size()
        improc = ImageProcessor(image_size, cfg_file_name, weights_file_name)

        # TODO: limit for protection
        iterations_limit = 250
        current_iterations = 0

        while current_iterations < iterations_limit:
            current_iterations += 1

            ss = wincap.get_screenshot()

            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                break

            coordinates = improc.proccess_image(ss)

            coordinates = [c for c in coordinates if c["class_name"] == "star"]

            if len(coordinates) == 0:
                continue

            detected_star = coordinates[0]

            # Step #1: Get coordinates and parameters of star
            star_x = detected_star['x']
            star_y = detected_star['y']
            star_width = detected_star['w']
            star_height = detected_star['h']

            # Step #2: Get center coordinates of star
            star_center_coordinates = self._find_object_center(x=star_x, y=star_y, width=star_width, height=star_height)
            star_center_x = star_center_coordinates['x']
            star_center_y = star_center_coordinates['y']

            # Step #3: Scale coordinates to screen resolution
            image_width, image_height = image_size
            scaled_center_coordinates = self._convert_coordinates(x=star_center_x, y=star_center_y,
                                                                  initial_width=image_width,
                                                                  initial_height=image_height,
                                                                  target_width=2560, target_height=1440)
            scaled_x, scaled_y = scaled_center_coordinates

            mouse.position = (scaled_x, scaled_y)
            mouse.press(Button.left)
            sleep(0.05)
            mouse.release(Button.left)

            # pass

            # # For testing purposes
            # sleep(3)
            #
            # print("[DEBUG] Point on top left corner of detected object.")
            # mouse.position = (star_x, star_y)
            # sleep(2)
            #
            # print("[DEBUG] Point on the center of detected object.")
            # mouse.position = (star_center_x, star_center_y)
            # sleep(2)
            #
            # mouse.position = (scaled_x, scaled_y)
            #
            # print("[DEBUG] Delay 4 secs...")
            # sleep(3)

        print('Finished.')

    @staticmethod
    def _find_object_center(x: int, y: int, width: int, height: int) -> dict:
        center_x = x + width / 2
        center_y = y + height / 2

        center_coordinates = {
            'x': center_x,
            'y': center_y
        }

        return center_coordinates

    @staticmethod
    def _convert_coordinates(x: int, y: int, initial_width: int, initial_height: int, target_width: int, target_height: int) -> Tuple[int, int]:
        """
        Convert coordinates from one resolution to another.

        Parameters:
        x, y: Coordinates in the initial resolution.
        initial_width, initial_height: Dimensions of the initial resolution.
        target_width, target_height: Dimensions of the target resolution.

        Returns:
        (target_x, target_y): Coordinates in the target resolution.
        """
        # Calculate scaling factors
        scale_x = target_width / initial_width
        scale_y = target_height / initial_height

        # Apply scaling to coordinates
        target_x = x * scale_x
        target_y = y * scale_y

        return int(target_x), int(target_y)
