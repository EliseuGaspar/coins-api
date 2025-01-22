import logging
from logging.handlers import TimedRotatingFileHandler
from os import makedirs, path


class Log:
    """
    A wrapper for the logging module that ensures consistent configuration and usage.
    """

    def __init__(self, logger_name: str = "ApplicationLog") -> None:
        log_directory = path.join("src", "log", "logFile")
        if not path.exists(log_directory):
            makedirs(log_directory)

        handler = TimedRotatingFileHandler(
            path.join(log_directory, "fileLog.log"),
            when="midnight",
            interval=1,
            backupCount=7,  # Keep logs for 7 days
        )

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)

        self.logger = logging.getLogger(logger_name)
        if not self.logger.hasHandlers():  # Prevent duplicate handlers
            self.logger.setLevel(logging.DEBUG)
            self.logger.addHandler(handler)

    def debug_message(self, msg: str) -> None:
        """Logs a debug message."""
        self.logger.debug(msg)

    def info_message(self, msg: str) -> None:
        """Logs an info message."""
        self.logger.info(msg)

    def error_message(self, msg: str) -> None:
        """Logs an error message."""
        self.logger.error(msg)

    def warning_message(self, msg: str) -> None:
        """Logs a warning message."""
        self.logger.warning(msg)


def configure_global_logging():
    """
    Configures global logging for the application.
    """
    log_directory = path.join("src", "log", "logFile")
    if not path.exists(log_directory):
        makedirs(log_directory)

    handler = TimedRotatingFileHandler(
        path.join(log_directory, "fileLog.log"),
        when="midnight",
        interval=1,
        backupCount=7,  # Keep logs for 7 days
    )
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    if not root_logger.hasHandlers():  # Prevent duplicate handlers
        root_logger.setLevel(logging.DEBUG)
        root_logger.addHandler(handler)


# Example usage:
logg = Log("MyAppLogger")
