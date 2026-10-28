import pytest
from app.operations import OperationFactory
from app.exceptions import OperationError

@pytest.mark.parametrize("name,a,b,expected", [
    ("add", 2, 3, 5), ("subtract", 2, 3, -1), ("multiply", 2, 3, 6),
    ("divide", 6, 3, 2), ("power", 2, 3, 8), ("root", 27, 3, 3),
    ("modulus", 10, 3, 1), ("int_divide", -7, 2, -3),
    ("percent", 25, 200, 12.5), ("abs_diff", 5, 12, 7),
])
def test_operations(name, a, b, expected):
    assert OperationFactory.create(name).execute(a, b) == pytest.approx(expected)

@pytest.mark.parametrize("name,a,b", [("divide", 1, 0), ("modulus", 1, 0), ("int_divide", 1, 0), ("percent", 1, 0), ("root", 4, 0), ("root", -4, 2), ("power", -1, 0.5)])
def test_operation_errors(name, a, b):
    with pytest.raises(OperationError): OperationFactory.create(name).execute(a, b)

def test_unknown_operation():
    with pytest.raises(OperationError): OperationFactory.create("wat")

def test_names_contains_all_operations():
    assert len(OperationFactory.names()) == 10

def test_power_overflow_is_handled():
    with pytest.raises(OperationError):
        OperationFactory.create("power").execute(1_000_000, 1_000_000)
