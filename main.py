"""Command-line REPL for the advanced calculator."""
from app import Calculator, CalculatorConfig, HistoryManager, AutoSaveObserver
from app.exceptions import CalculatorError
from app.logger import Logger, LoggingObserver
from app.operations import OperationFactory

HELP = """Commands:
  add|subtract|multiply|divide|power|root|modulus|int_divide|percent|abs_diff NUMBER NUMBER
  history, clear, undo, redo, save, load, help, exit
"""

def build_calculator():
    config = CalculatorConfig.from_env()
    config.ensure_directories()
    calculator = Calculator(config, HistoryManager(config.max_history_size, config.history_file, config.default_encoding))
    calculator.attach(LoggingObserver(Logger.configure(config.log_file)))
    calculator.attach(AutoSaveObserver(calculator.history, config.auto_save))
    return calculator

def run_repl(calculator=None, input_fn=input, output_fn=print):
    calculator = calculator or build_calculator()
    output_fn("Advanced Calculator — type 'help' for commands.")
    while True:
        try: line = input_fn("> ")
        except (EOFError, KeyboardInterrupt):
            output_fn("\nGoodbye!"); break
        parts = line.strip().split()
        if not parts: continue
        command = parts[0].lower()
        try:
            if command == "exit": output_fn("Goodbye!"); break
            if command == "help": output_fn(HELP); continue
            if command == "history":
                if not calculator.history.items: output_fn("History is empty.")
                for i, item in enumerate(calculator.history.items, 1): output_fn(f"{i}. {item.operation}({item.operand1}, {item.operand2}) = {item.result}")
                continue
            if command == "clear": calculator.clear(); output_fn("History cleared."); continue
            if command == "undo": output_fn("Last calculation undone." if calculator.undo() else "Nothing to undo."); continue
            if command == "redo": output_fn("Calculation redone." if calculator.redo() else "Nothing to redo."); continue
            if command == "save": output_fn(f"History saved to {calculator.history.save()}"); continue
            if command == "load": output_fn(f"Loaded {calculator.history.load()} calculation(s)."); continue
            if command not in OperationFactory.names(): output_fn("Unknown command. Type 'help' for available commands."); continue
            if len(parts) != 3: output_fn("Each operation requires exactly two numeric operands."); continue
            record = calculator.calculate(command, parts[1], parts[2])
            output_fn(f"Result: {record.result}")
        except (CalculatorError, OSError, ValueError) as exc:
            output_fn(f"Error: {exc}")

if __name__ == "__main__":
    run_repl()
