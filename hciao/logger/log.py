import json
import os
import logging
import logging.config
from hciao.logger.logger_adapter import LoggerAdapter
from hciao.definitions import PATH


class Log:
    DEFAULT_LOGGER = 'auto-checker'

    @classmethod
    def logger(cls, tag: str = '') -> LoggerAdapter:
        with open(os.path.join(PATH['config'], 'logger.json')) as f:
            config = json.load(f)
        logging.config.dictConfig(config)
        logger = logging.getLogger(cls.DEFAULT_LOGGER)
        logger = LoggerAdapter(tag, logger)
        return logger
