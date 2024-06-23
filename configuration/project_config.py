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
    _CONFIG_DATA: Optional[dict] = None

    def load_config(self) -> None:
        if self._CONFIG_DATA is None:
            loaded_config_data = self._load_config_yaml()
            self._CONFIG_DATA = loaded_config_data
        else:
            logger.debug("Config already loaded, no actions taken.")

    def get_host_screen_resolution(self) -> Optional[ScreenResolution]:
        screen_resolution_str: str = self._CONFIG_DATA["SETTINGS"]["HOST_SCREEN_RESOLUTION"]
        width, height = map(int, screen_resolution_str.split('x'))
        return ScreenResolution(width, height)

    def get_telegram_window_name(self) -> Optional[str]:
        window_name: str = self._CONFIG_DATA["BLUM_SETTINGS"]["TELEGRAM_WINDOW_NAME"]
        return window_name

    def get_stars_from_bomb(self) -> Optional[float]:
        stars_from_bomb: float = self._CONFIG_DATA["BLUM_SETTINGS"]["STARS_FROM_BOMB"]
        return stars_from_bomb

    @staticmethod
    def _load_config_yaml() -> dict:
        loaded_config_data = file_utils.load_yaml(file_path=CONFIG_PATH)

        if loaded_config_data:
            return loaded_config_data
        else:
            raise ConfigLoadError(f"Loaded empty config data from file at '{CONFIG_PATH}'")
