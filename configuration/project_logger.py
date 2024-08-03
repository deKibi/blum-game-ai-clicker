# Standard Libraries
from typing import Literal
import sys
import os
from datetime import datetime

# Third-party Libraries
from loguru import logger

# Custom Modules
from configuration.constants import LOGS_DIR_PATH
from utils import file_utils


class LoggerManager:
    @staticmethod
    def setup_console_logger(level: Literal['DEBUG', 'INFO', 'WARNING']) -> None:
        logger.remove()  # reset current logger
        logger.add(sys.stderr, level=level)  # create new logger & set log level

    def setup_file_logger(self, level: Literal['DEBUG', 'INFO', 'WARNING']) -> None:
        available_log_file_path = self._get_available_log_file_path()
        file_logger_format = '[{time:DD-MM-YYYY HH:mm:ss}] [{name}:{function}/{level}]: {message}'

        logger.add(
            sink=available_log_file_path,
            level=level,
            backtrace=True,
            format=file_logger_format
        )

    def _get_available_log_file_path(self) -> str:
        # Step #1: Create a folder with today's date inside the log dir
        today_date_str = datetime.now().strftime('%Y-%m-%d')
        today_date_dir_path = f'{LOGS_DIR_PATH}/{today_date_str}'
        os.makedirs(today_date_dir_path, exist_ok=True)

        # Step #2: Scan today's directory for all *.log files
        log_file_names = file_utils.scan_folder_for_files(directory_path=today_date_dir_path, extension='.log')

        # Prepare the next available log file name
        if len(log_file_names) > 0:
            available_log_number = self._get_available_log_number(today_logs_dir_path=today_date_dir_path)
        else:
            available_log_number = 1

        available_log_file_path = f'{today_date_dir_path}/{today_date_str}-{available_log_number}.log'
        return available_log_file_path

    @staticmethod
    def _get_available_log_number(today_logs_dir_path: str) -> int:
        log_files = file_utils.scan_folder_for_files(directory_path=today_logs_dir_path, extension='.log')

        existing_log_numbers = []

        for file in log_files:
            filename = file.split('.')[0]  # log file name without an extension
            numbers = filename.split('-')  # numbers from filename
            number = int(numbers[3])
            existing_log_numbers.append(number)

        max_existing_log_number = max(existing_log_numbers)
        available_log_number = max_existing_log_number + 1

        return available_log_number

