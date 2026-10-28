"""Memento object for storing calculator history state."""
from dataclasses import dataclass
from .calculation import Calculation

@dataclass(frozen=True)
class CalculatorMemento:
    history: tuple[Calculation, ...]
