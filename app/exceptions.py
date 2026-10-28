"""Custom exceptions used by the calculator."""

class CalculatorError(Exception):
    """Base exception for expected calculator errors."""

class OperationError(CalculatorError):
    """Raised when an operation cannot be completed."""

class ValidationError(CalculatorError):
    """Raised when input or configuration is invalid."""

class PersistenceError(CalculatorError):
    """Raised when history cannot be saved or loaded."""
