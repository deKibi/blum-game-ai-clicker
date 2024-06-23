# Standard Libraries
from typing import Optional

# Third-party Libraries
from loguru import logger

# Custom Modules
from utils import file_utils
from configuration.constants import CONFIG_PATH
from configuration.exceptions import ConfigLoadError


class Config:
    _CONFIG_DATA: Optional[dict] = None

    def load_config(self) -> None:
        if self._CONFIG_DATA is None:
            loaded_config_data = self._load_config_yaml()
            self._CONFIG_DATA = loaded_config_data
        else:
            logger.debug("Config already loaded, no actions taken.")

    @staticmethod
    def _load_config_yaml() -> dict:
        loaded_config_data = file_utils.load_yaml(file_path=CONFIG_PATH)

        if loaded_config_data:
            return loaded_config_data
        else:
            raise ConfigLoadError(f"Loaded empty config data from file at '{CONFIG_PATH}'")
