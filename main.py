# main.py

# Standard Libraries
import sys

# Third-party Libraries
from loguru import logger

# Custom Modules
from configuration import project_initialization
from core.blum_ai_clicker import BlumAIClicker

# Step #0: Initialize the project
project_initialization.init()

# Step #1: Create necessary class instances
blum_ai_clicker = BlumAIClicker()


# Step #2: Main Entry Point
def main():
    try:
        blum_ai_clicker.start()
    except KeyboardInterrupt:
        logger.error("Failed: script interrupted by user (CTRL + C)")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Failed due to unexpected error: {e}", e)
        sys.exit(1)
    else:
        logger.success(
            "Blum AI clicker finished without any critical errors. Thanks for using soft developed "
            "by Daily Flips (https://t.me/arbyzeru) & CRYPTO C0D3R (https://t.me/cryptocodi)"
        )


if __name__ == '__main__':
    main()
