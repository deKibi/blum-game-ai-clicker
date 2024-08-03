# Third-party Libraries
from loguru import logger

# Custom Modules
from configuration import project_loader
from configuration.project_logger import ProjectLogger
from configuration.project_config import ProjectConfig


def init():
    logger.info("Project initialization started.")

    # Step #1: Initialize project structure (folders & files)
    project_loader.init_project_directories()
    project_loader.init_project_files()

    # Step #2: Set up project logger
    project_logger = ProjectLogger()
    project_logger.setup_file_logger()
    project_logger.setup_console_logger()

    # Step #3: Load project config
    project_config = ProjectConfig()
    project_config.load_config_data()

    logger.success("Project initialization finished.")
