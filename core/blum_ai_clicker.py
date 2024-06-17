# Standard Libraries
from time import sleep

# Third-party Libraries
from pynput.mouse import Button, Controller
import cv2 as cv

# Custom Modules
from core.window_capture import WindowCapture
from core.image_processor import ImageProcessor


class BlumAIClicker:
    @staticmethod
    def start():
        mouse = Controller()

        print("Please, open Blum home page. Starting AI clicker in 5 seconds...")
        sleep(5)

        window_name = "Blum1"
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

            coordinates = [c for c in coordinates if c["class_name"] == "fruit"]

            if len(coordinates) == 0:
                continue

            star_to_hit = coordinates[0]

            # mouse.move(star_to_hit['w'], star_to_hit['h'])
            # sleep(0.05)
            # mouse.release(Button.left)

            mouse.position = (star_to_hit['x'], star_to_hit['y'])
            mouse.press(Button.left)
            sleep(0.05)
            mouse.release(Button.left)

        print('Finished.')
