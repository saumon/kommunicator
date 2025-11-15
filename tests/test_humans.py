#!/usr/bin/env python3
"""
Test script for humans configuration and alias lookup.
"""

import sys
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import get_email_by_alias
from logging_config import get_logger

logger = get_logger(__name__)


def test_alias_lookup():
    """Test the alias lookup functionality."""

    print("Testing explicit aliases:\n")
    explicit_test_cases = [
        ("john", "john.doe@example.com"),
        ("John", "john.doe@example.com"),  # Case insensitive
        ("JOHN DOE", "john.doe@example.com"),  # Case insensitive multi-word
        ("alice smith", "alice.smith@example.com"),
        ("jd", "john.doe@example.com"),
        ("bob", "bob.wilson@example.com"),
    ]

    for alias, expected_email in explicit_test_cases:
        try:
            email = get_email_by_alias(alias)
            status = "✓" if email == expected_email else "✗"
            print(f"{status} Alias '{alias}' -> {email} (expected: {expected_email})")
        except ValueError as e:
            print(f"✗ Alias '{alias}' -> Error: {e}")

    print("\nTesting auto-generated aliases (from email parts):\n")
    auto_alias_test_cases = [
        # For toto.smith@example.com =
        ("toto", "toto.smith@example.com"),
        ("smith", "toto.smith@example.com"),
        ("Toto Smith", "toto.smith@example.com"),
        # For momo.salam-ext@example.com = (ext should be filtered)
        ("momo", "momo.salam-ext@example.com"),
        ("salam", "momo.salam-ext@example.com"),
        ("Momo Salam", "momo.salam-ext@example.com"),
    ]

    for alias, expected_email in auto_alias_test_cases:
        try:
            email = get_email_by_alias(alias)
            status = "✓" if email == expected_email else "✗"
            print(f"{status} Alias '{alias}' -> {email} (expected: {expected_email})")
        except ValueError as e:
            print(f"✗ Alias '{alias}' -> Error: {e}")

    print("\nTesting duplicate handling (ambiguous aliases):\n")
    duplicate_test_cases = [
        # roger.moore@example.com = and roger.rabbit@example.com =
        # "roger" is ambiguous and should fail
        ("moore", "roger.moore@example.com"),  # Should work (unique)
        ("roger moore", "roger.moore@example.com"),  # Should work (unique)
        ("rabbit", "roger.rabbit@example.com"),  # Should work (unique)
        ("roger rabbit", "roger.rabbit@example.com"),  # Should work (unique)
    ]

    for alias, expected_email in duplicate_test_cases:
        try:
            email = get_email_by_alias(alias)
            status = "✓" if email == expected_email else "✗"
            print(f"{status} Alias '{alias}' -> {email} (expected: {expected_email})")
        except ValueError as e:
            print(f"✗ Alias '{alias}' -> Error: {e}")

    # Test ambiguous alias (should fail)
    print("\nTesting ambiguous alias (should fail):\n")
    try:
        email = get_email_by_alias("roger")
        print(f"✗ Alias 'roger' should have failed (ambiguous) but returned: {email}")
    except ValueError as e:
        print(f"✓ Alias 'roger' correctly raised error (ambiguous): {e}")

    # Test invalid aliases
    print("\nTesting invalid aliases:\n")
    invalid_aliases = ["unknown", "nonexistent"]

    for alias in invalid_aliases:
        try:
            email = get_email_by_alias(alias)
            print(f"✗ Alias '{alias}' should have failed but returned: {email}")
        except ValueError as e:
            print(f"✓ Alias '{alias}' correctly raised error: {e}")

    # Test empty alias
    print("\nTesting empty alias:\n")
    try:
        email = get_email_by_alias("")
        print(f"✗ Empty alias should have failed but returned: {email}")
    except ValueError as e:
        print(f"✓ Empty alias correctly raised error: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("Humans Configuration Test")
    print("=" * 60)
    print("\nMake sure conf/humans.conf exists and has test data from")
    print("conf/humans.conf.example\n")
    print("=" * 60 + "\n")

    test_alias_lookup()
