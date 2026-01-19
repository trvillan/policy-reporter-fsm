"""
Quick example script to demonstrate the mod_three function.

Run with: python run_example.py
"""

from examples.mod_three import mod_three
from fsm import InvalidSymbolError


def main():
    # Examples from the requirements
    # Feel free to add more test cases here
    test_cases = [
        ("1101", 13),   # 13 % 3 = 1
        ("1110", 14),   # 14 % 3 = 2
        ("1111", 15),   # 15 % 3 = 0
    ]

    # Additional edge cases
    edge_cases = [
        ("0", 0),                     # Zero
        ("1", 1),                     # One
        ("11", 3),                    # Exactly divisible by 3
        ("110", 6),                   # Another multiple of 3
        ("0001", 1),                  # Leading zeros
        ("00000000", 0),              # All zeros
        ("11111111", 255),            # All ones (8 bits)
        ("10000000000", 1024),        # Power of 2 (2^10)
        ("11111111111111111111", 1048575),  # Large number (2^20 - 1)
        ("101010101010101010101010", 11184810),  # Alternating pattern
    ]

    print("=" * 60)
    print("MOD-THREE FSM EXAMPLES")
    print("=" * 60)

    print("\n Examples from Requirements:\n")
    for binary, decimal in test_cases:
        result = mod_three(binary)
        print(f"  mod_three('{binary}') = {result}  ({decimal} % 3 = {result})")

    print("\n Edge Cases:\n")
    for binary, decimal in edge_cases:
        result = mod_three(binary)
        expected = decimal % 3
        status = "✓" if result == expected else "✗"
        print(f"  {status} mod_three('{binary[:20]}{'...' if len(binary) > 20 else ''}') = {result}  ({decimal} % 3 = {expected})")

    # Error cases - demonstrating input validation
    print("\n  Error Handling (these should raise errors):\n")
    
    error_cases = [
        ("", "Empty string"),
        ("102", "Invalid character '2'"),
        ("hello", "Letters"),
        ("10 01", "Space in input"),
        ("-101", "Negative sign"),
        ("1.01", "Decimal point"),
    ]

    for invalid_input, description in error_cases:
        try:
            mod_three(invalid_input)
            print(f"  ✗ mod_three('{invalid_input}') - Expected error but got result!")
        except (ValueError, InvalidSymbolError) as e:
            print(f"  ✓ mod_three('{invalid_input}') → {type(e).__name__}: {description}")

    print("\n" + "=" * 60)
    print("\nTry your own (in Python interactive terminal):")
    print("  $ python")
    print("  >>> from examples.mod_three import mod_three")
    print("  >>> mod_three('1010')  # 10 % 3 = 1")
    print("=" * 60)


if __name__ == "__main__":
    main()
