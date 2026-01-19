from dataclasses import dataclass
from typing import FrozenSet, Generic, Iterable, Mapping, TypeVar

from fsm.exceptions import (
    InvalidStateError,
    InvalidSymbolError,
    InvalidTransitionError,
)

StateT = TypeVar("StateT")
SymbolT = TypeVar("SymbolT")

@dataclass(frozen=True)
class FiniteAutomaton(Generic[StateT, SymbolT]):
    """
    A finite automaton (FA) defined by the 5-tuple 
    (states, alphabet, initial_state, accepting_states, transitions).

    Attributes:
        states: Q - The finite set of states
        alphabet: Σ - The finite input alphabet
        initial_state: q0 - The initial state (must be in Q)
        accepting_states: F - The set of accepting/final states (subset of Q)
        transitions: δ - The transition function as a mapping from (state, symbol) to state
    """

    states: FrozenSet[StateT]
    alphabet: FrozenSet[SymbolT]
    initial_state: StateT
    accepting_states: FrozenSet[StateT]
    transitions: Mapping[tuple[StateT, SymbolT], StateT]

    def __post_init__(self) -> None:
        """Validate the automaton configuration after initialization."""
        self._validate()

    def _validate(self) -> None:
        """
        Validate that the automaton configuration is consistent.

        Raises:
            InvalidStateError: If initial_state is not in states, or if
                accepting_states is not a subset of states.
            InvalidTransitionError: If any transition references invalid
                states or symbols.
        """
        # Validate initial state
        if self.initial_state not in self.states:
            raise InvalidStateError(
                f"Initial state {self.initial_state!r} is not in the set of states"
            )

        # Validate accepting states
        if not self.accepting_states.issubset(self.states):
            invalid = self.accepting_states - self.states
            raise InvalidStateError(
                f"Accepting states {invalid!r} are not in the set of states"
            )

        # Validate transitions
        for (source_state, symbol), target_state in self.transitions.items():
            if source_state not in self.states:
                raise InvalidTransitionError(
                    f"Transition source state {source_state!r} is not in the set of states"
                )
            if symbol not in self.alphabet:
                raise InvalidTransitionError(
                    f"Transition symbol {symbol!r} is not in the alphabet"
                )
            if target_state not in self.states:
                raise InvalidTransitionError(
                    f"Transition target state {target_state!r} is not in the set of states"
                )

    def step(self, state: StateT, symbol: SymbolT) -> StateT:
        """
        Perform a single state transition.

        Args:
            state: The current state
            symbol: The input symbol to process

        Returns:
            The next state after processing the symbol

        Raises:
            InvalidStateError: If the state is not in Q
            InvalidSymbolError: If the symbol is not in Σ
            InvalidTransitionError: If no transition is defined for (state, symbol)
        """
        if state not in self.states:
            raise InvalidStateError(f"State {state!r} is not in the set of states")

        if symbol not in self.alphabet:
            raise InvalidSymbolError(f"Symbol {symbol!r} is not in the alphabet")

        transition_key = (state, symbol)
        if transition_key not in self.transitions:
            raise InvalidTransitionError(
                f"No transition defined for state {state!r} with symbol {symbol!r}"
            )

        return self.transitions[transition_key]

    def process(self, input_sequence: Iterable[SymbolT]) -> StateT:
        """
        Process an input sequence and return the final state.

        Args:
            input_sequence: An iterable of symbols to process

        Returns:
            The final state after processing all input symbols

        Raises:
            InvalidSymbolError: If any symbol in the input is not in the alphabet
            InvalidTransitionError: If any transition is undefined
        """
        current_state = self.initial_state

        for symbol in input_sequence:
            current_state = self.step(current_state, symbol)

        return current_state

    def accepts(self, input_sequence: Iterable[SymbolT]) -> bool:
        """
        Check if the input sequence is accepted by the automaton.

        Args:
            input_sequence: An iterable of symbols to process

        Returns:
            True if the final state is an accepting state, False otherwise

        Raises:
            InvalidSymbolError: If any symbol in the input is not in the alphabet
            InvalidTransitionError: If any transition is undefined
        """
        final_state = self.process(input_sequence)
        return final_state in self.accepting_states

    @property
    def is_complete(self) -> bool:
        """
        Check if the transition function is complete.

        A complete automaton has a defined transition for every
        combination of state and symbol (|Q| × |Σ| transitions).

        Returns:
            True if all state-symbol pairs have defined transitions
        """
        expected_transitions = len(self.states) * len(self.alphabet)
        return len(self.transitions) == expected_transitions
