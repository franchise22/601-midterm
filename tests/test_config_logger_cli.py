import logging
import pytest
from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError
from app.logger import Logger, LoggingObserver
from app.calculation import Calculation
from app.calculator import Calculator
from main import run_repl

def test_config_defaults_and_env(tmp_path, monkeypatch):
    for key in list(__import__('os').environ):
        if key.startswith("CALCULATOR_"): monkeypatch.delenv(key, raising=False)
    config = CalculatorConfig.from_env(tmp_path / "absent.env")
    assert config.max_history_size == 100 and config.auto_save is True

def test_config_invalid(tmp_path, monkeypatch):
    monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "oops")
    with pytest.raises(ValidationError): CalculatorConfig.from_env(tmp_path / "absent.env")

def test_config_invalid_boolean(tmp_path, monkeypatch):
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "maybe")
    with pytest.raises(ValidationError): CalculatorConfig.from_env(tmp_path / "absent.env")

def test_logger_and_observer(tmp_path):
    logger = Logger.configure(tmp_path / "calc.log")
    LoggingObserver(logger).update(Calculation.create("add", 1, 2, 3))
    for handler in logger.handlers: handler.flush()
    assert "operation=add" in (tmp_path / "calc.log").read_text()

def test_cli_commands(tmp_path):
    cfg = CalculatorConfig(tmp_path / "logs", tmp_path / "history", 10, False, 2, 100, "utf-8", tmp_path / "logs/a.log", tmp_path / "history/a.csv")
    calc = Calculator(cfg)
    inputs = iter(["add 2 3", "history", "undo", "redo", "save", "load", "bad", "add 1", "help", "clear", "exit"])
    output = []
    run_repl(calc, lambda prompt: next(inputs), output.append)
    assert any("Result: 5" in x for x in output)
    assert any("Unknown command" in x for x in output)
    assert any("Goodbye" in x for x in output)

def test_cli_eof(tmp_path):
    cfg = CalculatorConfig(tmp_path / "logs", tmp_path / "history", 10, False, 2, 100, "utf-8", tmp_path / "logs/a.log", tmp_path / "history/a.csv")
    outputs=[]
    def eof(prompt): raise EOFError
    run_repl(Calculator(cfg), eof, outputs.append)
    assert any("Goodbye" in x for x in outputs)
