#!/usr/bin/env python3
"""Simple command-line calculator."""

from __future__ import annotations

import operator
from typing import Callable

Operation = Callable[[float, float], float]

OPERATIONS: dict[str, Operation] = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "//": operator.floordiv,
    "%": operator.mod,
    "**": operator.pow,
}


def calculate(left: float, op: str, right: float) -> float:
    if op not in OPERATIONS:
        raise ValueError(f"Unsupported operator: {op}")
    if op in {"/", "//", "%"} and right == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return OPERATIONS[op](left, right)


def parse_number(raw: str) -> float:
    try:
        return float(raw.strip())
    except ValueError as exc:
        raise ValueError(f"Not a number: {raw!r}") from exc


def prompt_once() -> str | None:
    try:
        line = input("calc> ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return "quit"
    return line


def run_repl() -> None:
    print("Calculator. Operators: +  -  *  /  //  %  **")
    print("Type expressions like: 12 * 4")
    print("Commands: help, quit")

    while True:
        line = prompt_once()
        if line is None or line in {"quit", "exit", "q"}:
            break
        if not line:
            continue
        if line in {"help", "?"}:
            print("Usage: <number> <operator> <number>")
            print("Operators:", " ".join(OPERATIONS))
            continue

        parts = line.split()
        if len(parts) != 3:
            print("Expected: <number> <operator> <number>")
            continue

        left_raw, op, right_raw = parts
        try:
            result = calculate(parse_number(left_raw), op, parse_number(right_raw))
        except (ValueError, ZeroDivisionError) as exc:
            print(exc)
            continue

        if result.is_integer():
            print(int(result))
        else:
            print(result)


if __name__ == "__main__":
    run_repl()
