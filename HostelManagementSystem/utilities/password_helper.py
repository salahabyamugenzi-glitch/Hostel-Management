"""Password hashing and verification helpers."""

import hashlib
import hmac
import os


_ALGORITHM = "pbkdf2_sha256"
_ITERATIONS = 310_000


def hash_password(password: str) -> str:
    """Return a salted, one-way password representation."""
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, _ITERATIONS)
    return f"{_ALGORITHM}${_ITERATIONS}${salt.hex()}${digest.hex()}"


def verify_password(password: str, stored_password: str) -> bool:
    """Verify hashed passwords and support legacy plaintext records."""
    if not stored_password.startswith(f"{_ALGORITHM}$"):
        return hmac.compare_digest(password, stored_password)

    try:
        algorithm, iterations, salt_hex, digest_hex = stored_password.split("$", 3)
        if algorithm != _ALGORITHM:
            return False
        expected = bytes.fromhex(digest_hex)
        actual = hashlib.pbkdf2_hmac(
            "sha256", password.encode(), bytes.fromhex(salt_hex), int(iterations)
        )
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False
