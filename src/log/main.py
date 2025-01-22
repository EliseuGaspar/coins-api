import logging
from logging.handlers import TimedRotatingFileHandler
from os import makedirs, path


class Log:
    __objectID: str = "Log"

    def __init__(self) -> None:
        log_directory = path.join("src", "log", "logFile")
        if not path.exists(log_directory):
            makedirs(log_directory)

        handler = TimedRotatingFileHandler(
            path.join(log_directory, "fileLog.log"),
            when="midnight",
            interval=1,
        )

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)

        self.logger = logging.getLogger(self.__objectID)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(handler)

    def debug_message(self, msg: str) -> None:
        self.logger.debug(msg)

    def info_message(self, msg: str) -> None:
        self.logger.info(msg)

    def error_message(self, msg: str) -> None:
        self.logger.error(msg)

    def warning_message(self, msg: str) -> None:
        self.logger.warning(msg)


def configure_global_logging():
    log_directory = path.join("src", "log", "logFile")
    if not path.exists(log_directory):
        makedirs(log_directory)

    handler = TimedRotatingFileHandler(
        path.join(log_directory, "fileLog.log"),
        when="midnight",
        interval=1,
    )
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(handler)


logg = Log()
