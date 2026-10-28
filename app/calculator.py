"""Calculator engine using Factory, Memento, and Observer patterns."""
from collections.abc import Callable
from .calculation import Calculation
from .calculator_memento import CalculatorMemento
from .calculator_config import CalculatorConfig
from .exceptions import OperationError
from .history import HistoryManager
from .input_validators import validate_operands
from .operations import OperationFactory

class AutoSaveObserver:
    def __init__(self, history: HistoryManager, enabled: bool = True): self.history, self.enabled = history, enabled
    def update(self, calculation: Calculation) -> None:
        if self.enabled: self.history.save()

class Calculator:
    def __init__(self, config: CalculatorConfig | None = None, history: HistoryManager | None = None):
        self.config = config or CalculatorConfig.from_env()
        self.config.ensure_directories()
        self.history = history or HistoryManager(self.config.max_history_size, self.config.history_file, self.config.default_encoding)
        self._observers: list[Callable[[Calculation], None] | object] = []
        self._undo_states: list[CalculatorMemento] = []
        self._redo_states: list[CalculatorMemento] = []

    def attach(self, observer) -> None:
        if observer not in self._observers: self._observers.append(observer)
    def detach(self, observer) -> None:
        if observer in self._observers: self._observers.remove(observer)
    def _notify(self, calculation: Calculation) -> None:
        for observer in tuple(self._observers): observer.update(calculation)
    def calculate(self, operation: str, a, b) -> Calculation:
        first, second = validate_operands(a, b, self.config.max_input_value)
        result = OperationFactory.create(operation).execute(first, second)
        result = round(result, self.config.precision)
        record = Calculation.create(operation.lower(), first, second, result)
        self._undo_states.append(CalculatorMemento(tuple(self.history.items)))
        self._redo_states.clear()
        self.history.add(record)
        try: self._notify(record)
        except Exception:
            # Calculation remains in history; observer failure is reported to caller/logging.
            raise
        return record
    def undo(self) -> Calculation | None:
        if not self.history.items: return None
        self._redo_states.append(CalculatorMemento(tuple(self.history.items)))
        previous = self._undo_states.pop() if self._undo_states else CalculatorMemento(tuple(self.history.items[:-1]))
        removed = self.history.undo()
        self.history._items = list(previous.history)
        return removed
    def redo(self) -> Calculation | None:
        if not self._redo_states: return None
        state = self._redo_states.pop()
        current = self.history.items
        self._undo_states.append(CalculatorMemento(tuple(current)))
        # Restore the next calculation state from the redo memento.
        self.history._items = list(state.history)
        if self.history._redo: self.history._redo.pop()
        return self.history.items[-1] if self.history.items else None
    def clear(self) -> None:
        self._undo_states.clear(); self._redo_states.clear(); self.history.clear()
