"""Arithmetic operations and Factory pattern."""
import math
from abc import ABC, abstractmethod
from .exceptions import OperationError

class Operation(ABC):
    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        """Execute an operation using two numbers."""

class Add(Operation):
    def execute(self, a, b): return a + b
class Subtract(Operation):
    def execute(self, a, b): return a - b
class Multiply(Operation):
    def execute(self, a, b): return a * b
class Divide(Operation):
    def execute(self, a, b):
        if b == 0: raise OperationError("Cannot divide by zero.")
        return a / b
class Power(Operation):
    def execute(self, a, b):
        try: result = a ** b
        except (OverflowError, ValueError, ZeroDivisionError) as exc: raise OperationError(f"Invalid power operation: {exc}") from exc
        if isinstance(result, complex):
            raise OperationError("Power result is not a finite real number.")
        try:
            finite = math.isfinite(float(result))
        except (OverflowError, ValueError):
            finite = False
        if not finite:
            raise OperationError("Power result is not a finite real number.")
        return result
class Root(Operation):
    def execute(self, a, b):
        if b == 0: raise OperationError("Root degree cannot be zero.")
        if a < 0:
            if not float(b).is_integer() or int(b) % 2 == 0: raise OperationError("A negative number requires an odd integer root degree.")
            return -((-a) ** (1 / b))
        try: result = a ** (1 / b)
        except (OverflowError, ValueError, ZeroDivisionError) as exc: raise OperationError(f"Invalid root operation: {exc}") from exc
        if not math.isfinite(float(result)): raise OperationError("Root result is not finite.")
        return result
class Modulus(Operation):
    def execute(self, a, b):
        if b == 0: raise OperationError("Cannot calculate modulus with zero divisor.")
        return a % b
class IntegerDivision(Operation):
    def execute(self, a, b):
        if b == 0: raise OperationError("Cannot divide by zero.")
        return math.trunc(a / b)  # Assignment says discard the fractional part.
class Percent(Operation):
    def execute(self, a, b):
        if b == 0: raise OperationError("Cannot calculate a percentage with a zero denominator.")
        return (a / b) * 100
class AbsoluteDifference(Operation):
    def execute(self, a, b): return abs(a - b)

class OperationFactory:
    _operations = {
        "add": Add, "subtract": Subtract, "multiply": Multiply, "divide": Divide,
        "power": Power, "root": Root, "modulus": Modulus, "int_divide": IntegerDivision,
        "percent": Percent, "abs_diff": AbsoluteDifference,
    }
    @classmethod
    def create(cls, name: str) -> Operation:
        try: return cls._operations[name.lower()]()
        except (KeyError, AttributeError) as exc: raise OperationError(f"Unknown operation: {name}") from exc
    @classmethod
    def names(cls) -> tuple[str, ...]: return tuple(cls._operations.keys())
