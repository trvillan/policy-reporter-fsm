class FSMError(Exception):
    """Base exception for all FSM-related errors."""
    pass


class InvalidStateError(FSMError):
    """Raised when a state is not a member of Q (the set of states)."""
    pass


class InvalidSymbolError(FSMError):
    """Raised when a symbol is not a member of Σ (the alphabet)."""
    pass


class InvalidTransitionError(FSMError):
    """Raised when a transition is undefined or invalid."""
    pass
