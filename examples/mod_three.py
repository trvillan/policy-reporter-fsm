"""
Mod-Three: An example implementation using the FSM library.

This module demonstrates how to use the FiniteAutomaton class to compute
the remainder when a binary number is divided by three.

The FSM is configured according to the following specification:
    Q = {S0, S1, S2}
    Σ = {0, 1}
    q0 = S0
    F = {S0, S1, S2}
    δ(S0,0) = S0; δ(S0,1) = S1
    δ(S1,0) = S2; δ(S1,1) = S0
    δ(S2,0) = S1; δ(S2,1) = S2

Example:
    >>> mod_three("1101")  # 13 in decimal
    1
    >>> mod_three("1110")  # 14 in decimal
    2
    >>> mod_three("1111")  # 15 in decimal
    0
"""


from enum import Enum

from fsm import FiniteAutomaton

class ModThreeState(Enum):
    S0 = 0
    S1 = 1
    S2 = 2


# The mod-three finite automaton configuration
_MOD_THREE_AUTOMATON: FiniteAutomaton[ModThreeState, str] = FiniteAutomaton(
    states=frozenset({ModThreeState.S0, ModThreeState.S1, ModThreeState.S2}),
    alphabet=frozenset({"0", "1"}),
    initial_state=ModThreeState.S0,
    accepting_states=frozenset({ModThreeState.S0, ModThreeState.S1, ModThreeState.S2}),
    transitions={
        # (current_state, symbol): next_state,
        (ModThreeState.S0, "0"): ModThreeState.S0,
        (ModThreeState.S0, "1"): ModThreeState.S1,
        (ModThreeState.S1, "0"): ModThreeState.S2,
        (ModThreeState.S1, "1"): ModThreeState.S0,
        (ModThreeState.S2, "0"): ModThreeState.S1,
        (ModThreeState.S2, "1"): ModThreeState.S2,
    },
)

# Mapping from final state to remainder value
_STATE_TO_REMAINDER: dict[ModThreeState, int] = {
    ModThreeState.S0: 0,
    ModThreeState.S1: 1,
    ModThreeState.S2: 2,
}


def mod_three(binary_input: str) -> int:
    """
    Compute the remainder when a binary number is divided by three.

    Args:
        binary_input: A string of '0' and '1' characters representing
            an unsigned binary integer (MSB first).

    Returns:
        The remainder when the binary number is divided by 3 (0, 1, or 2).

    Raises:
        ValueError: If the input string is empty.
        InvalidSymbolError: If the input contains characters other than '0' or '1'.
    """
    if not binary_input:
        raise ValueError("Input cannot be empty: expected a binary string")

    final_state = _MOD_THREE_AUTOMATON.process(binary_input)
    return _STATE_TO_REMAINDER[final_state]
