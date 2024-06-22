# Standard Libraries
from typing import Optional
import os
import shutil

# Third-party Libraries
from loguru import logger


def create_directory_if_not_exist(directory_path: str) -> None:
    """
    Create a directory if it doesn't exist.

    :param directory_path: The path to the directory.
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        logger.debug(f"Directory '{directory_path}' has been created.")
    else:
        logger.debug(f"Directory '{directory_path}' already exists. No changes made.")


def create_file_from_template(destination_file_path: str, file_template_path: str) -> None:
    if not os.path.exists(destination_file_path):
        copy_file(source_path=file_template_path, destination_path=destination_file_path)
        logger.info(f"File at {destination_file_path} created using template at {file_template_path}.")
    else:
        logger.debug(f"File at {destination_file_path} already exists. No changes made.")


def copy_file(source_path: str, destination_path: str) -> None:
    """
    Copy a file from the source path to the destination path.

    :param source_path: The path to the source file.
    :param destination_path: The path to the destination file.
    """
    try:
        shutil.copy2(source_path, destination_path)
        logger.debug(f"File copied from {source_path} to {destination_path}")
    except FileNotFoundError:
        raise CopyFileError(f"Could not make a copy to {destination_path}, there is no source file at {source_path}.")
