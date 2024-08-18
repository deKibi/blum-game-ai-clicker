# core/blum_ai_clicker.py

# Standard Libraries
from typing import Tuple
import time
from math import sqrt
from time import sleep

# Third-party Libraries
from loguru import logger
from pynput.mouse import Button, Controller
import keyboard

# Custom Modules
from configuration.project_config import ProjectConfig
from core.window_capture import WindowCapture
from core.image_processor import ImageProcessor
from core.objects import NonClickableArea
from utils import console_utils
from configuration.constants import PROJECT_VERSION, YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH

mouse = Controller()


class BlumAIClicker:
    def __init__(self):
        self._project_config = ProjectConfig()

    def start(self) -> None:
        logger.info(f'Starting Blum AI clicker "v{PROJECT_VERSION}" developed by https://t.me/arbyzeru')

        # STEP #0: LOAD PROJECT CONFIG
        self._project_config.load()

        # HOST SETTINGS
        host_screen_resolution = self._project_config.get_host_screen_resolution()
        host_screen_width = host_screen_resolution.get_width()
        host_screen_height = host_screen_resolution.get_height()
        # BLUM-RELATED SETTINGS
        telegram_window_name = self._project_config.get_telegram_window_name()
        stars_from_bomb = self._project_config.get_stars_from_bomb()
        non_clickable_area = self._project_config.get_non_clickable_area()

        # STEP #1: PREPARE WINDOW CAPTURE
        window_capture = WindowCapture(telegram_window_name)
        image_size = window_capture.get_window_size()
        improc = ImageProcessor(image_size, YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH)

        # STEP #2: SET GAMES GOAL
        time.sleep(0.1)  # delay to avoid loguru and Python input() conflict
        games_to_play = console_utils.ask_how_much_games_to_play()
        games_played = 0

        logger.info(f'Games goal for this session is set to {games_to_play} games.')
        logger.info('Please, open Blum home page and focus on it. Starting AI clicker in 5 seconds...')
        sleep(5)
        logger.debug('Started playing Blum games.')

        # STEP #3: START ANALYZING IMAGES AND PRESSING THE OBJECTS
        while True:
            # STEP #1: START CAPTURING GAME IMAGE
            ss = window_capture.get_screenshot()

            # STEP #2: EMERGENCY STOP (IF NEEDED)
            if keyboard.is_pressed('q'):
                logger.warning("You manually exited the game by pressing q!")
                break

            # STEP #3: FETCH ALL OBJECTS WITH THEIR COORDINATES FROM THE GAME IMAGE
            coordinates = improc.proccess_image(ss)

            # STEP #4: GET PLAY BUTTON (IF EXIST)
            play_buttons = [c for c in coordinates if c["class_name"] in ["play_btn", "play_again_btn"]]
            if len(play_buttons) > 0:
                # Step #1: Get play button coordinates and size
                play_btn = play_buttons[0]
                play_btn_center_coordinates = self._find_object_center(play_btn['x'], play_btn['y'], play_btn['w'],
                                                                       play_btn['h'])

                # Step #2: Locate x, y for btn
                play_btn_center_x = play_btn_center_coordinates['x']
                play_btn_center_y = play_btn_center_coordinates['y']

                # Step #3: Press play btn and increase played games counter
                if games_played < games_to_play:
                    logger.info(f"Starting new game... {games_played}/{games_to_play}")

                    time.sleep(0.1)  # delay to let the interface for play again load and then click the button
                    self.click_at(x=play_btn_center_x, y=play_btn_center_y)
                    logger.debug("Play button clicked.")

                    time.sleep(2)
                    games_played += 1

                    logger.info(f"New game started. {games_played}/{games_to_play}")
                else:
                    break

            # STEP #6: FITER DETECTED OBJECTS
            stars_and_freezes = [c for c in coordinates if c["class_name"] in ["star", "freeze"]]
            bombs = [c for c in coordinates if c["class_name"] == "bomb"]

            # STEP #7: PRIORITIZE "FREEZE"
            if any(c["class_name"] == "freeze" for c in stars_and_freezes):
                filtered_objects = next(c for c in stars_and_freezes if c["class_name"] == "freeze")
            else:
                filtered_objects = stars_and_freezes[0] if stars_and_freezes else None

            # STEP #8: GET STARS FROM DETECTED OBJECTS
            if filtered_objects:
                # Step #1: Get coordinates and parameters of the detected object
                obj_x = filtered_objects['x']
                obj_y = filtered_objects['y']
                obj_width = filtered_objects['w']
                obj_height = filtered_objects['h']

                # Step #2: Get center coordinates of the detected object
                obj_center_coordinates = self._find_object_center(x=obj_x, y=obj_y, width=obj_width, height=obj_height)
                obj_center_x = obj_center_coordinates['x']
                obj_center_y = obj_center_coordinates['y']

                # Step #3: Scale coordinates to screen resolution
                image_width, image_height = image_size
                scaled_center_coordinates = self._convert_coordinates(x=obj_center_x, y=obj_center_y,
                                                                      initial_width=image_width,
                                                                      initial_height=image_height,
                                                                      target_width=host_screen_width,
                                                                      target_height=host_screen_height)
                scaled_x, scaled_y = scaled_center_coordinates

                # Check if the detected object is near a bomb
                too_close_to_bomb = False
                for bomb in bombs:
                    bomb_center_coordinates = self._find_object_center(x=bomb['x'], y=bomb['y'], width=bomb['w'],
                                                                       height=bomb['h'])

                    distance_to_bomb = self.distance(obj_center_coordinates, bomb_center_coordinates)
                    object_size = max(obj_width, obj_height)

                    # How far away the bomb should be (counting in object sizes)
                    object_size_with_correction = object_size * stars_from_bomb

                    if distance_to_bomb < object_size_with_correction:
                        too_close_to_bomb = True
                        logger.debug(
                            f"Too close to bomb! Distance to bomb: {distance_to_bomb}, "
                            f"object size: {object_size} ({obj_width}, {obj_height}), "
                            f"correction coefficient: {stars_from_bomb}, "
                            f"object size with correction: {object_size_with_correction}"
                        )
                        break

                # CHECK IF OBJECT IN NON-CLICKABLE AREA & NOT TOO CLOSE TO BOMB
                if not self._is_in_non_clickable_area(x=scaled_x, y=scaled_y, non_clickable_area=non_clickable_area,
                                                      screen_width=host_screen_width, screen_height=host_screen_height):
                    if not too_close_to_bomb:
                        self.click_at(scaled_x, scaled_y)
                else:
                    logger.debug(f'Skipped click at ({scaled_x}, {scaled_y}) - within non-clickable area.')

        logger.success(f'Finished playing Blum games. Played {games_played}/{games_to_play} games.')

    @staticmethod
    def _is_in_non_clickable_area(x: int, y: int, non_clickable_area: NonClickableArea,
                                  screen_width: int, screen_height: int) -> bool:
        """Check if the given coordinates are within the non-clickable padding area."""

        # STEP #0: GET NON-CLICKABLE AREAS
        padding_left = non_clickable_area.get_padding_left()
        padding_right = non_clickable_area.get_padding_right()
        padding_top = non_clickable_area.get_padding_top()
        padding_bottom = non_clickable_area.get_padding_bottom()

        # STEP #1: CHECK COORDINATES FOR EACH AXIS
        is_x_non_clickable_area = bool(x < padding_left or x > screen_width - padding_right)
        is_y_non_clickable_area = bool(y < padding_top or y > screen_height - padding_bottom)

        # STEP #2: CHECK IF THE OBJECT'S COORDINATES ARE IN THE CLICKABLE AREA
        if is_x_non_clickable_area or is_y_non_clickable_area:
            return True
        else:
            return False

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
    def _convert_coordinates(x: int, y: int, initial_width: int, initial_height: int, target_width: int,
                             target_height: int) -> Tuple[int, int]:
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
