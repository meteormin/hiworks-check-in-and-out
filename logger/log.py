from logger.logger_adapter import LoggerAdapter
import json
import os
import logging
import logging.config


class Log:
    DEFAULT_LOGGER = 'auto-checker'

    @classmethod
    def logger(cls, tag: str = '') -> LoggerAdapter:
        with open(os.path.dirname(os.path.abspath(
                __file__)) + '/logger.json') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
        logger = logging.getLogger(cls.DEFAULT_LOGGER)
        logger = LoggerAdapter(tag, logger)
        return logger
