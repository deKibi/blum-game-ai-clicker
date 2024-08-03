# configuration/constants.py
# DO NOT CHANGE THIS FILE UNLESS YOU KNOW WHAT YOU ARE DOING

PROJECT_VERSION = '0.5.2-beta'

# PROJECT FOLDERS
FILES_DIR_PATH = 'files'
LOGS_DIR_PATH = 'files/logs'
FILE_TEMPLATES_DIR_PATH = 'configuration/file_templates'

# PROJECT FILES
CONFIG_PATH = f'{FILES_DIR_PATH}/config.yaml'
CONFIG_TEMPLATE_PATH = f'{FILE_TEMPLATES_DIR_PATH}/config_template.yaml'
YOLO_CONFIG_PATH = './yolov4-tiny/yolov4-tiny-custom.cfg'
# Default weights: core/weights/default/yolov4-tiny-custom_last.weights
# Event #1: core/weights/event1/yolov4-tiny-custom_last.weights
YOLO_WEIGHTS_PATH = 'core/weights/default/yolov4-tiny-custom_last.weights'
