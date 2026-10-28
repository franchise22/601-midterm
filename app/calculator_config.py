"""Environment-based configuration for the calculator."""
import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv
from .exceptions import ValidationError

@dataclass(frozen=True)
class CalculatorConfig:
    log_dir: Path
    history_dir: Path
    max_history_size: int
    auto_save: bool
    precision: int
    max_input_value: float
    default_encoding: str
    log_file: Path
    history_file: Path

    @classmethod
    def from_env(cls, env_file: str | Path = ".env") -> "CalculatorConfig":
        load_dotenv(dotenv_path=env_file, override=False)
        log_dir = Path(os.getenv("CALCULATOR_LOG_DIR", "logs"))
        history_dir = Path(os.getenv("CALCULATOR_HISTORY_DIR", "history"))
        try:
            max_history = int(os.getenv("CALCULATOR_MAX_HISTORY_SIZE", "100"))
            precision = int(os.getenv("CALCULATOR_PRECISION", "10"))
            max_input = float(os.getenv("CALCULATOR_MAX_INPUT_VALUE", "1000000"))
        except ValueError as exc:
            raise ValidationError("Numeric configuration values are invalid.") from exc
        auto_raw = os.getenv("CALCULATOR_AUTO_SAVE", "true").strip().lower()
        if auto_raw not in {"true", "false", "1", "0", "yes", "no"}:
            raise ValidationError("CALCULATOR_AUTO_SAVE must be true or false.")
        auto_save = auto_raw in {"true", "1", "yes"}
        if max_history < 1 or precision < 0 or max_input <= 0:
            raise ValidationError("History size and max input must be positive; precision cannot be negative.")
        encoding = os.getenv("CALCULATOR_DEFAULT_ENCODING", "utf-8")
        log_file = Path(os.getenv("CALCULATOR_LOG_FILE", str(log_dir / "calculator.log")))
        history_file = Path(os.getenv("CALCULATOR_HISTORY_FILE", str(history_dir / "calculations.csv")))
        return cls(log_dir, history_dir, max_history, auto_save, precision, max_input, encoding, log_file, history_file)

    def ensure_directories(self) -> None:
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
