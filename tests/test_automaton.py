from enum import Enum

import pytest

from fsm import (
    FiniteAutomaton,
    InvalidStateError,
    InvalidSymbolError,
    InvalidTransitionError,
)
from tests.conftest import SimpleState, ThreeState


class TestFiniteAutomatonConstruction:
    """Tests for automaton construction and validation."""

    def test_valid_construction(self, simple_automaton: FiniteAutomaton[SimpleState, str]) -> None:
        """Test that a valid automaton can be constructed."""
        assert simple_automaton.initial_state == SimpleState.A
        assert simple_automaton.states == frozenset({SimpleState.A, SimpleState.B})
        assert simple_automaton.alphabet == frozenset({"0", "1"})

    def test_invalid_initial_state_raises_error(self) -> None:
        """Test that an invalid initial state raises InvalidStateError."""

        class State(Enum):
            A = "A"
            B = "B"
            C = "C"  # Not in states set

        with pytest.raises(InvalidStateError, match="Initial state"):
            FiniteAutomaton(
                states=frozenset({State.A, State.B}),
                alphabet=frozenset({"0", "1"}),
                initial_state=State.C,  # Invalid: not in states
                accepting_states=frozenset({State.B}),
                transitions={
                    (State.A, "0"): State.A,
                    (State.A, "1"): State.B,
                    (State.B, "0"): State.A,
                    (State.B, "1"): State.B,
                },
            )

    def test_invalid_accepting_state_raises_error(self) -> None:
        """Test that an invalid accepting state raises InvalidStateError."""

        class State(Enum):
            A = "A"
            B = "B"
            C = "C"

        with pytest.raises(InvalidStateError, match="Accepting states"):
            FiniteAutomaton(
                states=frozenset({State.A, State.B}),
                alphabet=frozenset({"0", "1"}),
                initial_state=State.A,
                accepting_states=frozenset({State.C}),  # Invalid: not in states
                transitions={
                    (State.A, "0"): State.A,
                    (State.A, "1"): State.B,
                    (State.B, "0"): State.A,
                    (State.B, "1"): State.B,
                },
            )

    def test_invalid_transition_source_state_raises_error(self) -> None:
        """Test that a transition from an invalid state raises error."""

        class State(Enum):
            A = "A"
            B = "B"
            C = "C"

        with pytest.raises(InvalidTransitionError, match="source state"):
            FiniteAutomaton(
                states=frozenset({State.A, State.B}),
                alphabet=frozenset({"0", "1"}),
                initial_state=State.A,
                accepting_states=frozenset({State.B}),
                transitions={
                    (State.A, "0"): State.A,
                    (State.A, "1"): State.B,
                    (State.C, "0"): State.A,  # Invalid: C not in states
                    (State.B, "1"): State.B,
                },
            )

    def test_invalid_transition_target_state_raises_error(self) -> None:
        """Test that a transition to an invalid state raises error."""

        class State(Enum):
            A = "A"
            B = "B"
            C = "C"

        with pytest.raises(InvalidTransitionError, match="target state"):
            FiniteAutomaton(
                states=frozenset({State.A, State.B}),
                alphabet=frozenset({"0", "1"}),
                initial_state=State.A,
                accepting_states=frozenset({State.B}),
                transitions={
                    (State.A, "0"): State.C,  # Invalid: C not in states
                    (State.A, "1"): State.B,
                    (State.B, "0"): State.A,
                    (State.B, "1"): State.B,
                },
            )

    def test_invalid_transition_symbol_raises_error(self) -> None:
        """Test that a transition with invalid symbol raises error."""

        class State(Enum):
            A = "A"
            B = "B"

        with pytest.raises(InvalidTransitionError, match="symbol"):
            FiniteAutomaton(
                states=frozenset({State.A, State.B}),
                alphabet=frozenset({"0", "1"}),
                initial_state=State.A,
                accepting_states=frozenset({State.B}),
                transitions={
                    (State.A, "0"): State.A,
                    (State.A, "2"): State.B,  # Invalid: "2" not in alphabet
                    (State.B, "0"): State.A,
                    (State.B, "1"): State.B,
                },
            )

    def test_frozen_dataclass_is_immutable(self, simple_automaton: FiniteAutomaton[SimpleState, str]) -> None:
        """Test that the automaton is immutable (frozen dataclass)."""
        with pytest.raises(AttributeError):
            simple_automaton.initial_state = SimpleState.B  # type: ignore[misc]


class TestFiniteAutomatonStep:
    """Tests for single-step transitions."""

    def test_step_returns_correct_state(self, simple_automaton: FiniteAutomaton[SimpleState, str]) -> None:
        """Test that step returns the correct next state."""
        assert simple_automaton.step(SimpleState.A, "0") == SimpleState.A
        assert simple_automaton.step(SimpleState.A, "1") == SimpleState.B
        assert simple_automaton.step(SimpleState.B, "0") == SimpleState.A
        assert simple_automaton.step(SimpleState.B, "1") == SimpleState.B

    def test_step_with_invalid_state_raises_error(self, simple_automaton: FiniteAutomaton[SimpleState, str]) -> None:
        """Test that step with invalid state raises InvalidStateError."""

        class OtherState(Enum):
            X = "X"

        with pytest.raises(InvalidStateError):
            simple_automaton.step(OtherState.X, "0")  # type: ignore[arg-type]

    def test_step_with_invalid_symbol_raises_error(self, simple_automaton: FiniteAutomaton[SimpleState, str]) -> None:
        """Test that step with invalid symbol raises InvalidSymbolError."""
        with pytest.raises(InvalidSymbolError, match="'2'"):
            simple_automaton.step(SimpleState.A, "2")


class TestFiniteAutomatonProcess:
    """Tests for processing input sequences."""

    def test_process_empty_input_returns_initial_state(
        self, simple_automaton: FiniteAutomaton[SimpleState, str]
    ) -> None:
        """Test that processing empty input returns initial state."""
        assert simple_automaton.process("") == SimpleState.A

    def test_process_single_symbol(self, simple_automaton: FiniteAutomaton[SimpleState, str]) -> None:
        """Test processing a single symbol."""
        assert simple_automaton.process("0") == SimpleState.A
        assert simple_automaton.process("1") == SimpleState.B

    def test_process_multiple_symbols(self, simple_automaton: FiniteAutomaton[SimpleState, str]) -> None:
        """Test processing multiple symbols."""
        assert simple_automaton.process("01") == SimpleState.B
        assert simple_automaton.process("10") == SimpleState.A
        assert simple_automaton.process("11") == SimpleState.B
        assert simple_automaton.process("00") == SimpleState.A

    def test_process_long_input(self, simple_automaton: FiniteAutomaton[SimpleState, str]) -> None:
        """Test processing a longer input sequence."""
        # Ends in 1, so should be in state B
        assert simple_automaton.process("0101010101") == SimpleState.B
        # Ends in 0, so should be in state A
        assert simple_automaton.process("1010101010") == SimpleState.A

    def test_process_with_invalid_symbol_raises_error(
        self, simple_automaton: FiniteAutomaton[SimpleState, str]
    ) -> None:
        """Test that processing invalid symbol raises InvalidSymbolError."""
        with pytest.raises(InvalidSymbolError):
            simple_automaton.process("012")

    def test_process_with_list_input(self, simple_automaton: FiniteAutomaton[SimpleState, str]) -> None:
        """Test that process works with any iterable, not just strings."""
        assert simple_automaton.process(["0", "1"]) == SimpleState.B
        assert simple_automaton.process(["1", "0"]) == SimpleState.A


class TestFiniteAutomatonAccepts:
    """Tests for the accepts method."""

    def test_accepts_returns_true_for_accepting_state(
        self, simple_automaton: FiniteAutomaton[SimpleState, str]
    ) -> None:
        """Test accepts returns True when final state is accepting."""
        # SimpleState.B is the only accepting state
        assert simple_automaton.accepts("1") is True
        assert simple_automaton.accepts("01") is True
        assert simple_automaton.accepts("11") is True

    def test_accepts_returns_false_for_non_accepting_state(
        self, simple_automaton: FiniteAutomaton[SimpleState, str]
    ) -> None:
        """Test accepts returns False when final state is not accepting."""
        # SimpleState.A is not an accepting state
        assert simple_automaton.accepts("0") is False
        assert simple_automaton.accepts("10") is False

    def test_accepts_empty_input(self, simple_automaton: FiniteAutomaton[SimpleState, str]) -> None:
        """Test accepts with empty input (initial state)."""
        # Initial state A is not accepting
        assert simple_automaton.accepts("") is False


class TestFiniteAutomatonIsComplete:
    """Tests for the is_complete property."""

    def test_complete_automaton(self, simple_automaton: FiniteAutomaton[SimpleState, str]) -> None:
        """Test that a complete automaton returns True."""
        assert simple_automaton.is_complete is True

    def test_incomplete_automaton(self) -> None:
        """Test that an incomplete automaton returns False."""

        class State(Enum):
            A = "A"
            B = "B"

        fa = FiniteAutomaton(
            states=frozenset({State.A, State.B}),
            alphabet=frozenset({"0", "1"}),
            initial_state=State.A,
            accepting_states=frozenset({State.B}),
            transitions={
                # Missing (State.B, "0") and (State.B, "1")
                (State.A, "0"): State.A,
                (State.A, "1"): State.B,
            },
        )
        assert fa.is_complete is False


class TestModThreeAutomaton:
    """Tests specifically for the mod-three automaton configuration."""

    @pytest.mark.parametrize(
        "binary,expected_state",
        [
            ("0", ThreeState.S0),  # 0 % 3 = 0
            ("1", ThreeState.S1),  # 1 % 3 = 1
            ("10", ThreeState.S2),  # 2 % 3 = 2
            ("11", ThreeState.S0),  # 3 % 3 = 0
            ("100", ThreeState.S1),  # 4 % 3 = 1
            ("101", ThreeState.S2),  # 5 % 3 = 2
            ("110", ThreeState.S0),  # 6 % 3 = 0
            ("1101", ThreeState.S1),  # 13 % 3 = 1
            ("1110", ThreeState.S2),  # 14 % 3 = 2
            ("1111", ThreeState.S0),  # 15 % 3 = 0
        ],
    )
    def test_mod_three_transitions(
        self,
        mod_three_automaton: FiniteAutomaton[ThreeState, str],
        binary: str,
        expected_state: ThreeState,
    ) -> None:
        """Test that the mod-three automaton produces correct states."""
        assert mod_three_automaton.process(binary) == expected_state

    def test_mod_three_all_states_accepting(
        self, mod_three_automaton: FiniteAutomaton[ThreeState, str]
    ) -> None:
        """Test that all states are accepting in mod-three automaton."""
        assert mod_three_automaton.accepting_states == mod_three_automaton.states
