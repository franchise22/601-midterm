"""Logging observer and logger configuration."""
import logging
from pathlib import Path
from .calculation import Calculation

class Logger:
    @staticmethod
    def configure(log_file: str | Path) -> logging.Logger:
        path = Path(log_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        logger = logging.getLogger("advanced_calculator")
        logger.setLevel(logging.INFO)
        logger.propagate = False
        target = str(path.resolve())
        if not any(isinstance(h, logging.FileHandler) and getattr(h, "baseFilename", None) == target for h in logger.handlers):
            handler = logging.FileHandler(path, encoding="utf-8")
            handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
            logger.addHandler(handler)
        return logger

class LoggingObserver:
    def __init__(self, logger: logging.Logger): self.logger = logger
    def update(self, calculation: Calculation) -> None:
        self.logger.info("operation=%s operand1=%s operand2=%s result=%s", calculation.operation, calculation.operand1, calculation.operand2, calculation.result)
