import os
import sqlite3
import pytest
import test  # This imports the test.py file

@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    """
    Fixture to set up a fresh database before each test
    and tear it down afterward.
    """
    # 1. Setup: Create a clean database
    test.vinitdatabase()

    # 2. Yield to run the actual test function
    yield

    # 3. Teardown: Clean up the DB file after the test is done
    try:
        if os.path.exists("testing.db"):
            os.remove("testing.db")
    except PermissionError:
        print("Warning: Could not remove testing.db due to a PermissionError.")

# ---------- UNIT TESTS ----------

@pytest.mark.parametrize("password, expected_result", [
    ("ValidPass123$", True),       # Valid case
    ("short1$", False),            # Too short
    ("NoSymbol123", False),        # No symbol
    ("nouppercase1$", False),      # No uppercase
    ("NOLOWERCASE1$", False),      # No lowercase
    ("NoNumberPass$", False),      # No number
    ("A password with spaces1$", False) # Contains spaces
])
def test_password_checks(password, expected_result):
    """Tests various password formats using parameterization."""
    assert test.checkpw(password) == expected_result

def test_add_user_success():
    """Tests that a new user can be added successfully."""
    assert test.adduser("vinit", "ValidPass123$") is True

def test_add_user_duplicate():
    """Tests that adding a user with a duplicate username fails."""
    test.adduser("vinit", "ValidPass123$")  # Add user first time
    assert test.adduser("vinit", "AnotherPass456%") is False

def test_authenticate_success():
    """Tests that an existing user with the correct password can be authenticated."""
    test.adduser("vinit", "ValidPass123$")
    assert test.authenticate("vinit", "ValidPass123$") is True

def test_authenticate_wrong_password():
    """Tests that authentication fails for an existing user with the wrong password."""
    test.adduser("vinit", "ValidPass12-3$")
    assert test.authenticate("vinit", "wrongpass") is False

def test_authenticate_nonexistent_user():
    """Tests that authentication fails for a username that does not exist."""
    assert test.authenticate("ghost", "anypassword") is False

# ---------- INTEGRATION TESTS ----------

def test_signup_and_login_workflow():
    """Integration Test: A full user flow of signing up and then logging in."""
    # Step 1: Signup is successful
    assert test.adduser("vinit", "ValidPass123$") is True
    # Step 2: Login with the correct credentials is successful
    assert test.authenticate("vinit", "ValidPass123$") is True

def test_signup_duplicate_and_login_attempts():
    """Integration Test: Signup, fail to add duplicate, then test login attempts."""
    # Step 1: Initial signup is successful
    assert test.adduser("vinit", "ValidPass123$") is True
    # Step 2: Attempting to add the same user again fails
    assert test.adduser("vinit", "AnotherPass456%") is False
    # Step 3: Login with correct credentials succeeds
    assert test.authenticate("vinit", "ValidPass123$") is True
    # Step 4: Login with incorrect credentials fails
    assert test.authenticate("vinit", "WrongPassword789$") is False