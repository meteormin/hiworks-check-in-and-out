import logging
import logging.config
from hciao.logger.logger_adapter import LoggerAdapter
import config as cfg


class Log:
    DEFAULT_LOGGER = 'auto-checker'

    @classmethod
    def logger(cls, tag: str = '') -> LoggerAdapter:
        config = cfg.LOGGER

        logging.config.dictConfig(config)
        logger = logging.getLogger(cls.DEFAULT_LOGGER)
        logger = LoggerAdapter(tag, logger)
        return logger
