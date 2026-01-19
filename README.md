# FSM Library

A generic Finite State Machine library in Python, with a mod-three example implementation.

## Overview

This library provides a reusable implementation of **deterministic finite automata (DFA)** based on the formal 5-tuple definition:

- **Q** — Finite set of states
- **Σ** — Finite input alphabet
- **q₀** — Initial state (q₀ ∈ Q)
- **F** — Set of accepting/final states (F ⊆ Q)
- **δ** — Transition function (Q × Σ → Q)

The library is designed for extensibility and can be used to implement any finite state machine, not just the included mod-three example.

## Project Structure

```
├── src/
│   └── fsm/                    # FSM library module
│       ├── __init__.py         # Public API exports
│       ├── automaton.py        # FiniteAutomaton class
│       └── exceptions.py       # Custom exceptions
│
├── examples/
│   ├── __init__.py
│   └── mod_three.py            # Mod-three example implementation
│
├── tests/
│   ├── conftest.py             # Shared test fixtures
│   ├── test_automaton.py       # FSM library tests
│   └── test_mod_three.py       # Mod-three tests
│
├── pyproject.toml              # Project configuration
├── run_example.py              # Quick demo script
└── README.md                   # This file
```

## Setup

### Prerequisites

- Python 3.10 or higher

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd PR_assessment

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install with development dependencies
pip install -e ".[dev]"
```

## Quick Start

Run the example script to see the mod-three function in action:

```bash
python run_example.py
```

Output:
```
Mod-Three FSM Examples
========================================
mod_three('1101') = 1  (binary 1101 = 13, 13 % 3 = 1)
mod_three('1110') = 2  (binary 1110 = 14, 14 % 3 = 2)
mod_three('1111') = 0  (binary 1111 = 15, 15 % 3 = 0)
 
...
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=term-missing

# Run specific test file
pytest tests/test_mod_three.py

# Run with verbose output
pytest -v
```

## Type Checking

```bash
mypy src/ examples/
```

## Usage

### Using the FSM Library

```python
from enum import Enum
from fsm import FiniteAutomaton

# Define your states
class State(Enum):
    START = "start"
    ACCEPTING = "accepting"

# Create a finite automaton
fa = FiniteAutomaton(
    states=frozenset({State.START, State.ACCEPTING}),
    alphabet=frozenset({"a", "b"}),
    initial_state=State.START,
    accepting_states=frozenset({State.ACCEPTING}),
    transitions={
        (State.START, "a"): State.ACCEPTING,
        (State.START, "b"): State.START,
        (State.ACCEPTING, "a"): State.ACCEPTING,
        (State.ACCEPTING, "b"): State.START,
    }
)

# Process input
final_state = fa.process("aab")
print(f"Final state: {final_state}")  # State.START

# Check if input is accepted
is_accepted = fa.accepts("aa")
print(f"Accepted: {is_accepted}")  # True
```

### Using the Mod-Three Example

```python
from examples.mod_three import mod_three

# Compute remainder when binary number is divided by 3
print(mod_three("1101"))  # 1 (13 % 3 = 1)
print(mod_three("1110"))  # 2 (14 % 3 = 2)
print(mod_three("1111"))  # 0 (15 % 3 = 0)
```

## API Reference

### `FiniteAutomaton`

A generic finite automaton class.

#### Constructor Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `states` | `FrozenSet[StateT]` | The finite set of states (Q) |
| `alphabet` | `FrozenSet[SymbolT]` | The input alphabet (Σ) |
| `initial_state` | `StateT` | The initial state (q₀) |
| `accepting_states` | `FrozenSet[StateT]` | The accepting states (F) |
| `transitions` | `Mapping[tuple[StateT, SymbolT], StateT]` | The transition function (δ) |

#### Methods

| Method | Description |
|--------|-------------|
| `process(input_sequence)` | Process input and return the final state |
| `step(state, symbol)` | Perform a single state transition |
| `accepts(input_sequence)` | Check if input leads to an accepting state |

#### Properties

| Property | Description |
|----------|-------------|
| `is_complete` | Whether all state-symbol pairs have transitions |

### `mod_three(binary_input: str) -> int`

Compute the remainder when a binary number is divided by three.

#### Parameters

- `binary_input`: A string of '0' and '1' characters representing an unsigned binary integer (MSB first)

#### Returns

The remainder (0, 1, or 2)

#### Raises

- `ValueError`: If the input is empty
- `InvalidSymbolError`: If input contains non-binary characters

## Design Decisions

### Error Handling

- **Invalid symbols**: The library raises `InvalidSymbolError` when processing characters not in the alphabet. This fail-fast approach prevents silent incorrect behavior.

- **Empty input**: The `mod_three` function raises `ValueError` for empty input, as an empty string does not represent a valid binary integer per the problem specification.

### Type Safety

The library uses Python generics (`TypeVar`) to provide type-safe state and symbol handling. Using `Enum` for states is recommended for maximum type safety and readability.

### Immutability

`FiniteAutomaton` is implemented as a frozen dataclass, ensuring immutability after construction. This prevents accidental state corruption and makes the automaton safe for concurrent use.

### Validation

All validation occurs at construction time:
- Initial state must be in the states set
- Accepting states must be a subset of states
- All transitions must reference valid states and symbols

## Mod-Three FSM Specification

The mod-three FSM computes the remainder when dividing a binary number by 3:

```
States: Q = {S0, S1, S2}
Alphabet: Σ = {0, 1}
Initial State: q₀ = S0
Accepting States: F = {S0, S1, S2}

Transitions:
  δ(S0, 0) = S0    δ(S0, 1) = S1
  δ(S1, 0) = S2    δ(S1, 1) = S0
  δ(S2, 0) = S1    δ(S2, 1) = S2

Output Mapping:
  S0 → 0 (divisible by 3)
  S1 → 1 (remainder 1)
  S2 → 2 (remainder 2)
```
