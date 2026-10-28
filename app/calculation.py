"""Immutable record representing a completed calculation."""
from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass(frozen=True)
class Calculation:
    operation: str
    operand1: float
    operand2: float
    result: float
    timestamp: str

    @classmethod
    def create(cls, operation: str, a: float, b: float, result: float) -> "Calculation":
        return cls(operation, a, b, result, datetime.now(timezone.utc).isoformat())
