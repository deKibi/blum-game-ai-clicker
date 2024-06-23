# Third-party Libraries
from loguru import logger

# Custom Modules
from configuration import project_loader
from configuration.project_config import ProjectConfig


def init():
    logger.info("Project initialization started.")

    # Step #1: Initialize project structure (folders & files)
    project_loader.init_project_directories()
    project_loader.init_project_files()

    # Step #2: Load config
    project_config = ProjectConfig()
    project_config.load_config()

    logger.success("Project initialization finished.")
