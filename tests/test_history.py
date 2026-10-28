import pandas as pd
import pytest
from app.history import HistoryManager
from app.calculation import Calculation
from app.exceptions import PersistenceError

def sample(): return Calculation.create("add", 2, 3, 5)

def test_add_limit_undo_redo_clear(tmp_path):
    h = HistoryManager(1, tmp_path / "history.csv")
    h.add(sample()); h.add(sample())
    assert len(h.items) == 1
    assert h.undo() is not None
    assert h.redo() is not None
    h.clear(); assert h.items == []
    assert h.undo() is None and h.redo() is None

def test_save_load(tmp_path):
    path = tmp_path / "sub" / "history.csv"
    h = HistoryManager(10, path); h.add(sample())
    assert h.save() == path
    other = HistoryManager(10, path)
    assert other.load() == 1
    assert other.items[0].operation == "add"
    assert other.items[0].result == 5

def test_load_missing_file(tmp_path):
    with pytest.raises(PersistenceError): HistoryManager(history_file=tmp_path / "missing.csv").load()

def test_load_bad_columns(tmp_path):
    path = tmp_path / "bad.csv"; pd.DataFrame({"wrong": [1]}).to_csv(path, index=False)
    with pytest.raises(PersistenceError): HistoryManager(history_file=path).load()

def test_load_malformed_values(tmp_path):
    path = tmp_path / "bad.csv"
    path.write_text("operation,operand1,operand2,result,timestamp\nadd,no,2,3,now\n")
    with pytest.raises(PersistenceError): HistoryManager(history_file=path).load()
