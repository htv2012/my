import logging
import logging.config
import pathlib

logging.config.fileConfig(pathlib.Path(__file__).with_name('logging.ini'))


