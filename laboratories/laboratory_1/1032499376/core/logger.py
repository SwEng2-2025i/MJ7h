import logging
from pathlib import Path
from typing import Final


class EventLogger: 
    _instance: "EventLogger | None" = None
    _log_file: Final = "logs/notifications.log"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._configure()
        return cls._instance

    def _configure(self) -> None:
        Path("logs").mkdir(exist_ok=True)
        logging.basicConfig(
            filename=self._log_file,
            level=logging.INFO,
            format="%(asctime)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        self._logger = logging.getLogger("notif")

    def info(self, msg: str) -> None:
        self._logger.info(msg)

    def warning(self, msg: str) -> None:
        self._logger.warning(msg)

    def error(self, msg: str) -> None:
        self._logger.error(msg)


