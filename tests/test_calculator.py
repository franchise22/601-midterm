from dataclasses import replace
import pytest
from app.calculator import Calculator, AutoSaveObserver
from app.calculator_config import CalculatorConfig
from app.history import HistoryManager
from app.exceptions import ValidationError
from app.input_validators import parse_number, validate_operands

@pytest.fixture
def config(tmp_path):
    return CalculatorConfig(tmp_path / "logs", tmp_path / "history", 10, False, 2, 1000, "utf-8", tmp_path / "logs/app.log", tmp_path / "history/history.csv")

def test_calculator_calculate_and_history(config):
    calc = Calculator(config)
    record = calc.calculate("add", "2", "3")
    assert record.result == 5
    assert len(calc.history.items) == 1

def test_undo_redo(config):
    calc = Calculator(config)
    first = calc.calculate("add", 2, 3)
    second = calc.calculate("multiply", 3, 4)
    assert calc.undo() == second
    assert calc.history.items == [first]
    assert calc.redo() == second
    assert calc.history.items == [first, second]

def test_undo_redo_empty_and_clear(config):
    calc = Calculator(config)
    assert calc.undo() is None
    assert calc.redo() is None
    calc.calculate("add", 1, 2)
    calc.clear()
    assert calc.history.items == []
    assert calc.undo() is None

def test_new_calculation_clears_redo(config):
    calc = Calculator(config)
    calc.calculate("add", 1, 2)
    calc.undo()
    calc.calculate("multiply", 2, 3)
    assert calc.redo() is None

def test_validation_errors(config):
    calc = Calculator(config)
    with pytest.raises(ValidationError): calc.calculate("add", "hello", 2)
    with pytest.raises(ValidationError): calc.calculate("add", 1001, 2)

def test_observers_and_detach(config, tmp_path):
    calc = Calculator(config)
    class Observer:
        def __init__(self): self.seen = []
        def update(self, record): self.seen.append(record)
    obs = Observer(); calc.attach(obs); calc.calculate("add", 1, 2)
    assert len(obs.seen) == 1
    calc.detach(obs); calc.calculate("add", 2, 3)
    assert len(obs.seen) == 1

def test_autosave_observer(config, tmp_path):
    history = HistoryManager(10, tmp_path / "x.csv")
    observer = AutoSaveObserver(history, enabled=False)
    from app.calculation import Calculation
    observer.update(Calculation.create("add", 1, 2, 3))
    assert not (tmp_path / "x.csv").exists()

def test_validators():
    assert parse_number("2.5") == 2.5
    assert validate_operands("1", 2) == (1.0, 2.0)
    for invalid in ("nope", "nan", "inf"):
        with pytest.raises(ValidationError): parse_number(invalid)
