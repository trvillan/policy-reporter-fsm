"""
FSM Library - A generic Finite State Machine implementation.

init file for the FSM library to provide all the public API exports.
"""

from fsm.automaton import FiniteAutomaton
from fsm.exceptions import (
    FSMError,
    InvalidStateError,
    InvalidSymbolError,
    InvalidTransitionError,
)

__all__ = [
    "FiniteAutomaton",
    "FSMError",
    "InvalidStateError",
    "InvalidSymbolError",
    "InvalidTransitionError",
]

__version__ = "0.1.0"
