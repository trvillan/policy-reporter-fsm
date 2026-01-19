import pytest

from examples.mod_three import mod_three
from fsm import InvalidSymbolError


class TestModThreeBasicValues:
    """Tests for basic mod_three functionality with known values."""

    @pytest.mark.parametrize(
        "binary,expected",
        [
            # Single digits
            ("0", 0),  # 0 % 3 = 0
            ("1", 1),  # 1 % 3 = 1
            # Two digits
            ("00", 0),  # 0 % 3 = 0
            ("01", 1),  # 1 % 3 = 1
            ("10", 2),  # 2 % 3 = 2
            ("11", 0),  # 3 % 3 = 0
            # Three digits
            ("100", 1),  # 4 % 3 = 1
            ("101", 2),  # 5 % 3 = 2
            ("110", 0),  # 6 % 3 = 0
            ("111", 1),  # 7 % 3 = 1
            # Examples from the problem statement
            ("1101", 1),  # 13 % 3 = 1
            ("1110", 2),  # 14 % 3 = 2
            ("1111", 0),  # 15 % 3 = 0
        ],
    )
    def test_known_values(self, binary: str, expected: int) -> None:
        """Test mod_three against known binary-to-remainder mappings."""
        assert mod_three(binary) == expected

    @pytest.mark.parametrize("n", range(100))
    def test_matches_modulo_operator(self, n: int) -> None:
        """Test that mod_three matches the % operator for values 0-99."""
        binary = bin(n)[2:]  # Convert to binary, strip '0b' prefix
        assert mod_three(binary) == n % 3


class TestModThreeEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_empty_string_raises_error(self) -> None:
        """Test that empty input raises ValueError."""
        with pytest.raises(ValueError, match="empty"):
            mod_three("")

    def test_leading_zeros(self) -> None:
        """Test that leading zeros don't affect the result."""
        assert mod_three("0001") == mod_three("1") == 1
        assert mod_three("00010") == mod_three("10") == 2
        assert mod_three("00011") == mod_three("11") == 0
        assert mod_three("0000") == mod_three("0") == 0

    def test_all_zeros(self) -> None:
        """Test strings of all zeros."""
        assert mod_three("0") == 0
        assert mod_three("00") == 0
        assert mod_three("000") == 0
        assert mod_three("0000000000") == 0

    def test_all_ones(self) -> None:
        """Test strings of all ones."""
        # 1 = 1, 11 = 3, 111 = 7, 1111 = 15, 11111 = 31
        assert mod_three("1") == 1  # 1 % 3 = 1
        assert mod_three("11") == 0  # 3 % 3 = 0
        assert mod_three("111") == 1  # 7 % 3 = 1
        assert mod_three("1111") == 0  # 15 % 3 = 0
        assert mod_three("11111") == 1  # 31 % 3 = 1

    def test_large_binary_number(self) -> None:
        """Test with a large binary number."""
        # 2^20 = 1048576, 1048576 % 3 = 1
        large_binary = "1" + "0" * 20
        assert mod_three(large_binary) == 1048576 % 3

    def test_very_long_input(self) -> None:
        """Test that the function handles very long inputs efficiently."""
        # Create a binary string that represents a number we can verify
        # Using pattern that we can calculate: 101010... 
        long_binary = "10" * 50  # 100 characters
        decimal_value = int(long_binary, 2)
        assert mod_three(long_binary) == decimal_value % 3


class TestModThreeInvalidInput:
    """Tests for invalid input handling."""

    def test_invalid_character_raises_error(self) -> None:
        """Test that non-binary characters raise InvalidSymbolError."""
        with pytest.raises(InvalidSymbolError):
            mod_three("102")

    def test_letter_raises_error(self) -> None:
        """Test that letters raise InvalidSymbolError."""
        with pytest.raises(InvalidSymbolError):
            mod_three("10a1")

    def test_space_raises_error(self) -> None:
        """Test that spaces raise InvalidSymbolError."""
        with pytest.raises(InvalidSymbolError):
            mod_three("10 01")

    def test_negative_sign_raises_error(self) -> None:
        """Test that negative sign raises InvalidSymbolError."""
        with pytest.raises(InvalidSymbolError):
            mod_three("-101")

    def test_decimal_point_raises_error(self) -> None:
        """Test that decimal point raises InvalidSymbolError."""
        with pytest.raises(InvalidSymbolError):
            mod_three("10.01")


class TestModThreeReturnType:
    """Tests for return type verification."""

    def test_returns_integer(self) -> None:
        """Test that mod_three returns an integer."""
        result = mod_three("1101")
        assert isinstance(result, int)

    def test_return_value_range(self) -> None:
        """Test that return values are always 0, 1, or 2."""
        for n in range(50):
            binary = bin(n)[2:]
            result = mod_three(binary)
            assert result in {0, 1, 2}
