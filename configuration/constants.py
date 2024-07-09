# configuration/constants.py

PROJECT_VERSION = "0.4.1"  # DO NOT CHANGE

# Project Folders
FILES_DIR_PATH = "files"
LOGS_DIR_PATH = "logs"
FILE_TEMPLATES_DIR_PATH = "configuration/file_templates"

# Project Config
CONFIG_PATH = f"{FILES_DIR_PATH}/config.yaml"
CONFIG_TEMPLATE_PATH = f"{FILE_TEMPLATES_DIR_PATH}/config_template.yaml"

# AI
YOLO_CONFIG_PATH = "./yolov4-tiny/yolov4-tiny-custom.cfg"

# Default weights: core/weights/default/yolov4-tiny-custom_last.weights
# Event: core/weights/event1/yolov4-tiny-custom_last.weights
YOLO_WEIGHTS_PATH = "core/weights/default/yolov4-tiny-custom_last.weights"
