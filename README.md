# Advanced Python Calculator

A command-line calculator demonstrating the Factory, Memento, and Observer design patterns, input validation, logging, undo/redo, CSV persistence with pandas, configuration with python-dotenv, and pytest coverage.

## Requirements
- Python 3.10 or newer
- pip

## Installation
```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

Copy `.env.example` to `.env` if you want a fresh local configuration. The provided `.env` is ignored by Git, so create your own local copy if needed.

## Configuration
Settings include `CALCULATOR_LOG_DIR`, `CALCULATOR_HISTORY_DIR`, `CALCULATOR_MAX_HISTORY_SIZE`, `CALCULATOR_AUTO_SAVE`, `CALCULATOR_PRECISION`, `CALCULATOR_MAX_INPUT_VALUE`, `CALCULATOR_DEFAULT_ENCODING`, `CALCULATOR_LOG_FILE`, and `CALCULATOR_HISTORY_FILE`. Defaults are applied when variables are missing.

## Run
```bash
python main.py
```
Examples: `add 5 3`, `power 2 3`, `root 27 3`, `history`, `undo`, `redo`, `save`, `load`, `help`, `exit`.

`root a b` means the b-th root of a. `percent a b` computes `(a / b) * 100`. `int_divide` truncates the quotient toward zero.

## Tests and coverage
```bash
pytest -v
pytest --cov=app --cov-report=term-missing --cov-fail-under=90
```

## CI/CD
GitHub Actions runs tests and enforces the 90% coverage threshold on pushes and pull requests to `main`.
