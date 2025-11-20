"""
Flag encryption/decryption utilities.

Uses Fernet (AES-128) symmetric encryption with a key derived from FLAG_MASTER_KEY.
Flags are encrypted in the database and decrypted at runtime for display.
Flag submissions are hashed and compared against stored hashes.
"""
import base64
import hashlib
import os
from functools import lru_cache
from typing import Iterable, Tuple

from cryptography.fernet import Fernet, InvalidToken

# Derive encryption key from environment variable or default seed
_SEED = os.getenv("FLAG_MASTER_KEY", "black-sunrise-zero-day")
_DEFAULT_TASK = "GLOBAL"
_KNOWN_TASKS = (
    _DEFAULT_TASK,
    "SQLI",
    "SQLI_ADV",
    "SQLI_BLIND",
    "XSS",
    "CSRF",
    "STEG",
)

def _normalize_task(task_name: str | None) -> str:
    """Normalize task names to keep derivation consistent."""
    if not task_name:
        return _DEFAULT_TASK
    normalized = task_name.strip().upper()
    return normalized or _DEFAULT_TASK


@lru_cache(maxsize=64)
def _cipher_for(task_name: str) -> Fernet:
    """Return a Fernet cipher bound to a specific task name."""
    material = f"{_SEED}:{task_name}".encode()
    key = base64.urlsafe_b64encode(hashlib.sha256(material).digest())
    return Fernet(key)


def _candidate_tasks(task_name: str | None) -> Iterable[str]:
    """Yield task names to attempt during decryption (ordered, deduped)."""
    if task_name:
        normalized = _normalize_task(task_name)
        yield normalized
        if normalized != _DEFAULT_TASK:
            yield _DEFAULT_TASK
        return

    seen = set()
    for name in _KNOWN_TASKS:
        if name not in seen:
            seen.add(name)
            yield name


def encrypt_flag(value: str, task_name: str | None = None) -> str:
    """Encrypt a plaintext flag value for storage in the database."""
    if not value:
        return ""
    cipher = _cipher_for(_normalize_task(task_name))
    token = cipher.encrypt(value.encode())
    return token.decode()


def decrypt_flag(token: str, task_name: str | None = None) -> str:
    """Decrypt an encrypted flag token back to plaintext."""
    if not token:
        return ""
    for candidate in _candidate_tasks(task_name):
        cipher = _cipher_for(candidate)
        try:
            return cipher.decrypt(token.encode()).decode()
        except InvalidToken:
            continue
    return "[corrupted-flag]"


def hash_flag(value: str) -> str:
    """Generate SHA-256 hash of a flag for submission validation."""
    return hashlib.sha256(value.encode()).hexdigest()


def split_flag_halves(value: str) -> Tuple[str, str]:
    """Split a flag into two parts where the first half ends with '_'.

    Raises ValueError if no suitable underscore boundary exists.
    """
    if not value:
        return "", ""

    underscores = [idx for idx, ch in enumerate(value) if ch == "_"]
    if not underscores:
        raise ValueError("Flag must contain underscore characters for split.")

    mid = len(value) // 2
    split_idx = None
    # Prefer underscore at/left of midpoint, otherwise fallback to first available
    for idx in underscores:
        if idx < len(value) - 1 and idx <= mid:
            split_idx = idx
    if split_idx is None:
        # Choose earliest underscore that isn't terminal
        for idx in underscores:
            if idx < len(value) - 1:
                split_idx = idx
                break
    if split_idx is None:
        raise ValueError("Unable to split flag without leaving empty tail.")

    first = value[: split_idx + 1]
    second = value[split_idx + 1 :]
    return first, second

