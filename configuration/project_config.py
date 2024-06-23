# Standard Libraries
from typing import Optional, Any

# Third-party Libraries
from loguru import logger

# Custom Modules
from utils import file_utils
from configuration.constants import CONFIG_PATH
from configuration.exceptions import ConfigLoadError
from core.objects.screen_resolution import ScreenResolution


class ProjectConfig:
    def __init__(self):
        self._config_data = self.load_config()

    def load_config(self) -> dict:
        loaded_config_data = self._load_config_yaml()
        return loaded_config_data

    def get_host_screen_resolution(self) -> ScreenResolution:
        screen_resolution_str: str = self._config_data["SETTINGS"]["HOST_SCREEN_RESOLUTION"]
        width, height = map(int, screen_resolution_str.split('x'))
        return ScreenResolution(width, height)

    def get_telegram_window_name(self) -> str:
        window_name: str = self._config_data["BLUM_SETTINGS"]["TELEGRAM_WINDOW_NAME"]
        return window_name

    def get_stars_from_bomb(self) -> float:
        stars_from_bomb: float = self._config_data["BLUM_SETTINGS"]["STARS_FROM_BOMB"]
        return stars_from_bomb

    @staticmethod
    def _load_config_yaml() -> dict:
        loaded_config_data = file_utils.load_yaml(file_path=CONFIG_PATH)

        if loaded_config_data:
            return loaded_config_data
        else:
            raise ConfigLoadError(f"Loaded empty config data from file at '{CONFIG_PATH}'")
