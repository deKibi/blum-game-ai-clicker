# Third-party Libraries
import sys

from loguru import logger

# Custom Modules
from configuration import project_initialization
from core.blum_ai_clicker import BlumAIClicker


def main():
    # Create necessary class instances
    blum_ai_clicker = BlumAIClicker()

    try:
        # Step #1: Initialize project
        project_initialization.init()

        # Step #2: Start the clicker
        blum_ai_clicker.start()
    except KeyboardInterrupt:
        logger.error("Failed: script interrupted by user (CTRL + C)")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Failed due to unexpected error: {e}", e)
        sys.exit(1)
    else:
        logger.success("Blum AI clicker finished without any critical errors.")


if __name__ == '__main__':
    main()
