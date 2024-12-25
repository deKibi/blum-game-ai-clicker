# configuration/constants.py
# DO NOT CHANGE THIS FILE UNLESS YOU KNOW WHAT YOU ARE DOING

PROJECT_VERSION = '1.0.0'

# PROJECT FOLDERS
FILES_DIR_PATH = 'files'
LOGS_DIR_PATH = 'files/logs'
FILE_TEMPLATES_DIR_PATH = 'configuration/file_templates'

# PROJECT FILES
CONFIG_PATH = f'{FILES_DIR_PATH}/config.yaml'
CONFIG_TEMPLATE_PATH = f'{FILE_TEMPLATES_DIR_PATH}/config_template.yaml'
YOLO_CONFIG_PATH = './yolov4-tiny/yolov4-tiny-custom.cfg'
YOLO_WEIGHTS_PATH = './yolov4-tiny/training/yolov4-tiny-custom_last.weights'
