import logging

from rich.logging import RichHandler
from rich.console import Console
from rich.text import Text


console = Console()


def logger_config():
    logger = logging.getLogger("xact")
    logging.basicConfig(
        format="%(asctime)s | %(levelname)s: %(message)s",
        datefmt="%b/%d %H:%M:%S",
        level=logging.INFO,
    )
    # handler = RichHandler(rich_tracebacks=True, console=console)
    # logger.addHandler(handler)
    logger.propagate = False
    return logger


def toggle_logging(enable: bool=True):
    if enable:
        logging.disable(logging.NOTSET)
    else:
        logging.disable(logging.CRITICAL)


logger = logger_config()


def log_error(message):
    logger.error(Text(message, style="bold red"))


def log_info(message, style="bold white"):
    logger.info(Text(message, style=style))


def log_warning(message):
    logger.warning(Text(message, style="bold yellow"))
