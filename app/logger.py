import logging
import os

current_dir = os.path.abspath(__file__).rsplit("/", 1)[0]
log_file = "{}.log".format(__file__).rsplit("/", 1)[1]
log_file_path = os.path.join(current_dir, "log", log_file)
target_level = logging.DEBUG

# set logger
logger = logging.getLogger("unique")
logger.propagate = False
logger.setLevel(target_level)
# set handler
fileHandler = logging.FileHandler(log_file_path, mode="w")
fileHandler.setLevel(target_level)
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(target_level)
# set formatter
formatter = logging.Formatter(
    "[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
consoleHandler.setFormatter(formatter)
fileHandler.setFormatter(formatter)
# add handler
if logger.hasHandlers():
    logger.handlers.clear()
logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)
