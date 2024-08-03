# configuration/project_config.py

# Standard Libraries
from typing import Optional, Any, List

# Third-party Libraries
from loguru import logger

# Custom Modules
from core.objects import ScreenResolution, NonClickableArea
from utils import file_utils
from configuration.constants import CONFIG_TEMPLATE_PATH, CONFIG_PATH
from configuration.exceptions import ConfigLoadError, ConfigKeyError, ConfigValueError, InitialConfigLoadError


class ProjectConfig:
    _CONFIG_DATA: Optional[dict] = None

    def load(self) -> None:
        # STEP #0: CHECK IF CONFIG FILE EXISTS
        configfile_exist = file_utils.check_if_file_exist(file_path=CONFIG_PATH)

        # STEP #1: CREATE CONFIG IF ITS MISSING
        if not configfile_exist:
            file_utils.copy_file(source_path=CONFIG_TEMPLATE_PATH, destination_path=CONFIG_PATH)
            logger.debug(f'No config file was found at "{CONFIG_PATH}", initial file created.')
            raise InitialConfigLoadError(
                f'Initial config file created. User setup required: '
                f'please go to "{CONFIG_PATH}" and configure file according to your system and needs.'
            )

        # STEP #2: LOAD THE CONFIG IF IT ALREADY EXISTS
        logger.debug(f'Config file at "{CONFIG_PATH}" already exist, loading it.')
        loaded_config_data = self._load_yaml_data()
        self._CONFIG_DATA = loaded_config_data
        logger.success('Project configuration loaded.')

    def get_host_screen_resolution(self) -> ScreenResolution:
        # STEP #0: GET HOST SCREEN RESOLUTION VALUES FROM PROJECT CONFIG
        # screen_width_str: str = self._CONFIG_DATA['HOST_SETTINGS']['HOST_SCREEN_RESOLUTION']['WIDTH']
        screen_width_str: str = self._get_key(key_path=['HOST_SETTINGS', 'HOST_SCREEN_RESOLUTION', 'WIDTH'])
        # screen_height_str: str = self._CONFIG_DATA['HOST_SETTINGS']['HOST_SCREEN_RESOLUTION']['HEIGHT']
        screen_height_str: str = self._get_key(key_path=['HOST_SETTINGS', 'HOST_SCREEN_RESOLUTION', 'HEIGHT'])

        # STEP #1: CONVERT VALUES TO INTEGER
        screen_width_int: int = self._convert_px_to_int(pixels_str=screen_width_str)
        screen_height_int: int = self._convert_px_to_int(pixels_str=screen_height_str)

        # STEP #2: CREATE HOST SCREEN RESOLUTION USING FETCHED VALUES FROM THE CONFIG
        host_screen_resolution = ScreenResolution(width=screen_width_int, height=screen_height_int)
        return host_screen_resolution

    def get_telegram_window_name(self) -> str:
        window_name: str = self._CONFIG_DATA['BLUM_SETTINGS']['TELEGRAM_WINDOW_NAME']
        return window_name

    def get_stars_from_bomb(self) -> float:
        stars_from_bomb: float = self._CONFIG_DATA['BLUM_SETTINGS']['STARS_FROM_BOMB']
        return stars_from_bomb

    def get_non_clickable_area(self) -> NonClickableArea:
        # STEP #0: GET NON CLICKABLE AREA VALUES FROM PROJECT CONFIG
        left_padding_str: str = self._CONFIG_DATA['BLUM_SETTINGS']['NON_CLICKABLE_AREA']['PADDING_LEFT']
        right_padding_str: str = self._CONFIG_DATA['BLUM_SETTINGS']['NON_CLICKABLE_AREA']['PADDING_RIGHT']
        top_padding_str: str = self._CONFIG_DATA['BLUM_SETTINGS']['NON_CLICKABLE_AREA']['PADDING_TOP']
        bottom_padding_str: str = self._CONFIG_DATA['BLUM_SETTINGS']['NON_CLICKABLE_AREA']['PADDING_BOTTOM']

        # STEP #1: CONVERT VALUES TO AN INTEGER
        left_padding_int: int = self._convert_px_to_int(pixels_str=left_padding_str)
        right_padding_int: int = self._convert_px_to_int(pixels_str=right_padding_str)
        top_padding_int: int = self._convert_px_to_int(pixels_str=top_padding_str)
        bottom_padding_int: int = self._convert_px_to_int(pixels_str=bottom_padding_str)

        # STEP #2: CREATE NON-CLICKABLE AREA USING FETCHED VALUES FROM THE CONFIG
        non_clickable_area = NonClickableArea(padding_left=left_padding_int, padding_right=right_padding_int,
                                              padding_top=top_padding_int, padding_bottom=bottom_padding_int)
        return non_clickable_area

    def _get_key(self, key_path: List[str]) -> Any:
        if self._CONFIG_DATA is None:
            raise ConfigLoadError(
                'Unable to get key from config - config data did not load. '
                'Please load the config first before accessing key values.'
            )

        if key_path is None:
            raise ConfigKeyError('Path to the key cannot be None.')

        try:
            current_level = self._CONFIG_DATA

            for key in key_path:
                if current_level is None or key not in current_level:
                    raise ConfigKeyError(
                        f'Key "{key}" not found in path "{key_path}". '
                        'Please ensure the full path is correct and the key exists.'
                    )
                current_level = current_level[key]

            if current_level is not None:
                return current_level
            else:
                raise ConfigKeyError(
                    f'Value for key "{key_path}" is None. '
                    'Please ensure the key exists and contains a valid value.'
                )

        except KeyError as e:
            raise ConfigKeyError(
                f'Key error while accessing path "{key_path}": {e}. '
                'Please check that the key exists and the path is correct.'
            )
        except TypeError as e:
            raise ConfigKeyError(
                f'Type error while accessing path "{key_path}": {e}. '
                'Ensure that the path is a list of valid keys and the configuration is correctly formatted.'
            )

    @staticmethod
    def _load_yaml_data() -> dict:
        loaded_config_data = file_utils.load_yaml(file_path=CONFIG_PATH)

        if loaded_config_data:
            return loaded_config_data
        else:
            raise ConfigLoadError(f'Loaded empty config data from file at "{CONFIG_PATH}"')

    @staticmethod
    def _convert_px_to_int(pixels_str: str) -> int:
        try:
            pixels_parts = pixels_str.split('px')

            pixels_part = pixels_parts[0].strip()
            pixels_int = int(pixels_part)

            return pixels_int
        except Exception:
            raise ConfigValueError(
                f'Error converting pixels to an integer! Check that you used valid pixels format in the config, '
                f'for example: 100px or 100 px or 100'
            )
