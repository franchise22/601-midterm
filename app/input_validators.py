"""Input validation helpers."""
import math
from .exceptions import ValidationError

def parse_number(value: str | int | float, max_value: float = 1_000_000) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValidationError(f"{value!r} is not a valid number.") from exc
    if not math.isfinite(number):
        raise ValidationError("Inputs must be finite numbers.")
    if abs(number) > max_value:
        raise ValidationError(f"Input magnitude cannot exceed {max_value}.")
    return number

def validate_operands(a: str | int | float, b: str | int | float, max_value: float = 1_000_000) -> tuple[float, float]:
    return parse_number(a, max_value), parse_number(b, max_value)
