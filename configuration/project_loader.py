# Third-party Libraries
from loguru import logger

# Custom Modules
from utils import file_utils
from configuration.constants import FILES_DIR_PATH


def init_directories() -> None:
    logger.debug('Initializing project directories, it may take a while...')

    file_utils.create_directory_if_not_exist(directory_path=FILES_DIR_PATH)

    logger.success('Project directories initialized.')


def init_files() -> None:
    logger.debug('No files need to be initialized.')
    logger.success('Project files initialized.')
