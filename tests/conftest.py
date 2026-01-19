from enum import Enum

import pytest

from fsm import FiniteAutomaton


class SimpleState(Enum):
    """Simple two-state enum for testing."""

    A = "A"
    B = "B"


class ThreeState(Enum):
    """Three-state enum for testing (matches mod-three structure)."""

    S0 = 0
    S1 = 1
    S2 = 2


@pytest.fixture
def simple_automaton() -> FiniteAutomaton[SimpleState, str]:
    """
    A simple two-state automaton for basic testing.

    Accepts strings ending in '1'.
    """
    return FiniteAutomaton(
        states=frozenset({SimpleState.A, SimpleState.B}),
        alphabet=frozenset({"0", "1"}),
        initial_state=SimpleState.A,
        accepting_states=frozenset({SimpleState.B}),
        transitions={
            (SimpleState.A, "0"): SimpleState.A,
            (SimpleState.A, "1"): SimpleState.B,
            (SimpleState.B, "0"): SimpleState.A,
            (SimpleState.B, "1"): SimpleState.B,
        },
    )


@pytest.fixture
def mod_three_automaton() -> FiniteAutomaton[ThreeState, str]:
    """
    The mod-three automaton for testing.

    Computes remainder when binary number is divided by 3.
    """
    return FiniteAutomaton(
        states=frozenset({ThreeState.S0, ThreeState.S1, ThreeState.S2}),
        alphabet=frozenset({"0", "1"}),
        initial_state=ThreeState.S0,
        accepting_states=frozenset({ThreeState.S0, ThreeState.S1, ThreeState.S2}),
        transitions={
            (ThreeState.S0, "0"): ThreeState.S0,
            (ThreeState.S0, "1"): ThreeState.S1,
            (ThreeState.S1, "0"): ThreeState.S2,
            (ThreeState.S1, "1"): ThreeState.S0,
            (ThreeState.S2, "0"): ThreeState.S1,
            (ThreeState.S2, "1"): ThreeState.S2,
        },
    )
