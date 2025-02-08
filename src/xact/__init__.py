from xact.log.config import log_manager

log = log_manager.init(__name__)
def main() -> None:
    print("xact init")
    log.info("xact init : system")

