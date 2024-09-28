# main.py

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
        logger.error('Failed: script interrupted by user (CTRL + C)')
    except Exception as e:
        logger.exception(f'Failed due to an error: {e}', e)
        logger.info(
            'Check error message above for steps to fix it. If there is no steps or you do not know what to do, '
            'contact community support via Telegram chat https://t.me/+3z98nad38M40ZGE6'
        )
    else:
        logger.success('Blum AI clicker finished without any critical errors.')
    finally:
        logger.success(
            '\n============================================\n'
            '       Script Execution Complete\n'
            '   Developed by https://t.me/cryptocodi\n'
            ' Buy auto farm - https://t.me/cryptocodi/102\n'
            '   Thank you for using Blum AI Clicker!\n'
            '============================================'
        )


if __name__ == '__main__':
    main()
