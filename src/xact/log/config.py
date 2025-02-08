
import logging

import logging.config


__all__ = [
"log_manager",
]




import logging
from typing import Dict, Iterable, List, Literal


class LogManager:
    """
    A class to manage logger instances with dynamic runtime configuration.
    """

    def __init__(self,        
        format: str = None,
        formatter:logging.Formatter=None,
        datefmt: str | None = None,
        level: Literal["info", "debug", "warning", "error", "critical",10,50] = logging.DEBUG,
        handlers: Iterable[logging.Handler] | None = None,):
        self.loggers = {}

        self.format = format
        self.formatter= formatter
        self.datefmt=datefmt
        self.level=level
        self.handlers = handlers
        self.levels = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }
    

    def init(self, name, level=logging.INFO, formatter=None):
        """
        Creates a logger with a basic configuration.

        Args:
            name (str): Name of the logger.
            level (int): Logging level (default: logging.INFO).
            formatter (logging.Formatter, optional): Custom formatter. Default is a basic formatter.

        Returns:
            logging.Logger: Configured logger instance.
        """
        if name in self.loggers:
            return self.loggers[name]

        # Create a new logger
        logger = logging.getLogger(name)
      
        self.config(format=self.format,formatter=self.formatter,datefmt=self.datefmt,level=self.level, handlers=self.handlers,loggers={name:logger})

        # Store the logger for future reference
        self.loggers[name] = logger
        return logger

    def config(
            self,
        format: str = None,
        formatter:logging.Formatter=None,
        datefmt: str | None = None,
        level:Literal[10,50]=logging.INFO,
        handlers: Iterable[logging.Handler] | None = None,
        loggers:Dict[str,logging.Logger]=None
    ):
        loggers = loggers or self.loggers
        for logger_name, logger in loggers.items():
            if handlers:
                logger.propagate = False
                logger.handlers.clear()
                for handler in handlers:
                    logger.addHandler(handler)
            if level:
                logger.setLevel(level)
            if format or formatter :
                _formatter = None
                if format:
                    _formatter= logging.Formatter(format,datefmt)
                elif formatter:
                    _formatter = formatter
                else:
                    _formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s: %(message)s",datefmt)
                for handler in logger.handlers:
                    handler.setFormatter(  _formatter)
       

    def remove_handler(self, handler_type):
        """
        Removes all handlers of a specific type from all loggers managed by LogManager.

        Args:
            handler_type (type): The type of handler to remove (e.g., logging.StreamHandler).
        """
        for logger_name, logger in self.loggers.items():
            logger.handlers = [
                h for h in logger.handlers if not isinstance(h, handler_type)
            ]

    def ext_enable(self, enable: bool = True):
        """
        Enable or disable logs for external libraries.

        Args:
            enable (bool): Whether to enable or disable library logs.
        """
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO if enable else logging.CRITICAL)

    def enable(self, enable: bool = True):
        """
        Enable or disable logs for the current logger.

        Args:
            enable (bool): Whether to enable this logger's logs.
        """
        for logger in self.loggers.values():
            logger.disabled = not enable

    def setup_custom_level(self, level:str, level_num:int):
        """
        Creates a custom logging level.

        Args:
            level (str): Name of the custom logging level.
            level_num (int): Numeric value for the custom logging level.
        """
        level = level.upper()
        if not hasattr(logging, level):
            logging.addLevelName(level_num, level)

            def custom_level_method(self, message, *args, **kwargs):
                if self.isEnabledFor(level_num):
                    self._log(level_num, message, args, **kwargs)

            setattr(logging.Logger, level.lower(), custom_level_method)
            self.levels[level.upper()]=level_num


# Example usage

    @classmethod
    def get_manager(cls):

        class CenteredFormatter(logging.Formatter):
            def format(self, record):
                # Center the 'name' field within a width of 20 characters
                record.name = f"{record.name:^20}"
                return super().format(record)

        # Define the custom format
        formatter = CenteredFormatter(
            fmt="%(asctime)-15s | %(name)s  | %(levelname)-8s | %(message)s",
            datefmt="%b/%d %H:%M:%S",
        )

        log_manager = cls(
            formatter=formatter,
            level=logging.DEBUG,
            handlers=[
                logging.FileHandler("stream.log"),  # Stream logs to a file
                logging.StreamHandler(),  # Also stream to the console
            ],
        )

        return log_manager 







log_manager: LogManager = LogManager.get_manager()
log_manager.setup_custom_level("xact_stream",25)

log = log_manager.init(__name__)

log_xst = log_manager.init("xact-stream")


log.info("log initilized")
log.xact_stream("log streaming initilized")