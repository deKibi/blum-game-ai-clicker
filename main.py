# main.py

# Standard Libraries
import sys

# Third-party Libraries
from loguru import logger

# Custom Modules
from configuration import LoggerManager
from configuration import project_loader
from core.blum_ai_clicker import BlumAIClicker


# STEP #0: SET UP CONSOLE & FILE LOGGERS
logger_manager = LoggerManager()
logger_manager.setup_console_logger(level='INFO')
logger_manager.setup_file_logger(level='DEBUG')

# STEP #1: LOAD PROJECT DIRECTORIES AND FILES
project_loader.init_directories()
project_loader.init_files()


# STEP #2: MAIN ENTRY POINT
def main():
    try:
        BlumAIClicker().start()
    except KeyboardInterrupt:
        logger.error("Failed: script interrupted by user (CTRL + C)")
    except Exception as e:
        logger.exception(f"Failed due to unexpected error: {e}", e)
    else:
        logger.success(
            "Blum AI clicker finished without any critical errors. Thanks for using soft developed "
            "by Daily Flips (https://t.me/arbyzeru) & CRYPTO C0D3R (https://t.me/cryptocodi)"
        )


if __name__ == '__main__':
    main()
