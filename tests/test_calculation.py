from app.calculation import Calculation

def test_calculation_create():
    c = Calculation.create("add", 1, 2, 3)
    assert (c.operation, c.operand1, c.operand2, c.result) == ("add", 1, 2, 3)
    assert "T" in c.timestamp
