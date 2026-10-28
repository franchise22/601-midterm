"""Calculation history and CSV persistence using pandas."""
from pathlib import Path
import pandas as pd
from .calculation import Calculation
from .exceptions import PersistenceError

COLUMNS = ["operation", "operand1", "operand2", "result", "timestamp"]

class HistoryManager:
    def __init__(self, max_size: int = 100, history_file: str | Path = "history/calculations.csv", encoding: str = "utf-8"):
        self.max_size = max_size
        self.history_file = Path(history_file)
        self.encoding = encoding
        self._items: list[Calculation] = []
        self._redo: list[Calculation] = []

    @property
    def items(self) -> list[Calculation]: return list(self._items)
    def add(self, calculation: Calculation) -> None:
        self._items.append(calculation)
        self._items = self._items[-self.max_size:]
        self._redo.clear()
    def clear(self) -> None:
        self._items.clear(); self._redo.clear()
    def undo(self) -> Calculation | None:
        if not self._items: return None
        item = self._items.pop(); self._redo.append(item); return item
    def redo(self) -> Calculation | None:
        if not self._redo: return None
        item = self._redo.pop(); self._items.append(item); self._items = self._items[-self.max_size:]; return item
    def save(self, path: str | Path | None = None) -> Path:
        destination = Path(path) if path is not None else self.history_file
        try:
            destination.parent.mkdir(parents=True, exist_ok=True)
            frame = pd.DataFrame([vars(item) for item in self._items], columns=COLUMNS)
            frame.to_csv(destination, index=False, encoding=self.encoding)
            return destination
        except (OSError, ValueError, TypeError) as exc:
            raise PersistenceError(f"Could not save history: {exc}") from exc
    def load(self, path: str | Path | None = None) -> int:
        source = Path(path) if path is not None else self.history_file
        try:
            frame = pd.read_csv(source, encoding=self.encoding)
            if not set(COLUMNS).issubset(frame.columns):
                raise PersistenceError("CSV is missing required columns.")
            loaded = []
            for row in frame[COLUMNS].to_dict(orient="records"):
                loaded.append(Calculation(str(row["operation"]), float(row["operand1"]), float(row["operand2"]), float(row["result"]), str(row["timestamp"])))
            self._items = loaded[-self.max_size:]
            self._redo.clear()
            return len(self._items)
        except PersistenceError:
            raise
        except (OSError, ValueError, TypeError, pd.errors.ParserError, UnicodeError) as exc:
            raise PersistenceError(f"Could not load history: {exc}") from exc
