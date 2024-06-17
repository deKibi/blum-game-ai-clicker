# Standard Libraries
from typing import Tuple, Dict
from math import sqrt
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
        iterations_limit = 400
        current_iterations = 0

        while current_iterations < iterations_limit:
            current_iterations += 1

            ss = wincap.get_screenshot()

            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                break

            coordinates = improc.proccess_image(ss)

            # Filter objects
            stars_and_freezes = [c for c in coordinates if c["class_name"] in ["star", "freeze"]]
            bombs = [c for c in coordinates if c["class_name"] == "bomb"]

            # Priority to "freeze"
            if any(c["class_name"] == "freeze" for c in stars_and_freezes):
                detected_object = next(c for c in stars_and_freezes if c["class_name"] == "freeze")
            else:
                detected_object = stars_and_freezes[0] if stars_and_freezes else None

            if detected_object:
                # Step #1: Get coordinates and parameters of the detected object
                obj_x = detected_object['x']
                obj_y = detected_object['y']
                obj_width = detected_object['w']
                obj_height = detected_object['h']

                # Step #2: Get center coordinates of the detected object
                obj_center_coordinates = self._find_object_center(x=obj_x, y=obj_y, width=obj_width, height=obj_height)
                obj_center_x = obj_center_coordinates['x']
                obj_center_y = obj_center_coordinates['y']

                # Step #3: Scale coordinates to screen resolution
                image_width, image_height = image_size
                scaled_center_coordinates = self._convert_coordinates(x=obj_center_x, y=obj_center_y,
                                                                initial_width=image_width,
                                                                initial_height=image_height,
                                                                target_width=2560, target_height=1440)
                scaled_x, scaled_y = scaled_center_coordinates

                # Check if the detected object is near a bomb
                too_close_to_bomb = False
                for bomb in bombs:
                    bomb_center_coordinates = self._find_object_center(x=bomb['x'], y=bomb['y'], width=bomb['w'],
                                                                 height=bomb['h'])
                    if self.distance(obj_center_coordinates, bomb_center_coordinates) < max(obj_width, obj_height):
                        too_close_to_bomb = True
                        break

                # Click only if it's not too close to a bomb
                if not too_close_to_bomb:
                    self.click_at(scaled_x, scaled_y)

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

    @staticmethod
    def distance(coord1: dict, coord2: dict) -> float:
        """Calculate the Euclidean distance between two coordinates."""
        distance = sqrt((coord1['x'] - coord2['x']) ** 2 + (coord1['y'] - coord2['y']) ** 2)
        return distance

    @staticmethod
    def click_at(x: int, y: int) -> None:
        """Move the mouse to the specified coordinates and click."""
        mouse.position = (x, y)
        mouse.press(Button.left)
        sleep(0.05)
        mouse.release(Button.left)
