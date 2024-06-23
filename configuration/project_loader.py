# Third-party Libraries
from loguru import logger

# Custom Modules
from utils import file_utils
from configuration.constants import FILES_DIR_PATH, CONFIG_PATH, CONFIG_TEMPLATE_PATH


def init_project_directories() -> None:
    logger.debug("Initializing project directories, it may take a while...")

    file_utils.create_directory_if_not_exist(directory_path=FILES_DIR_PATH)

    logger.success("Project directories initialized.")


def init_project_files() -> None:
    logger.debug("Initializing project files, it may take a while...")

    file_utils.create_file_from_template_if_not_exist(destination_file_path=CONFIG_PATH,
                                                      file_template_path=CONFIG_TEMPLATE_PATH)

    logger.success("Project structure initialized.")
