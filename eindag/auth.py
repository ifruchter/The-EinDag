"""Simple authentication for the MVP.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .constants import DEMO_USERS
from .models import User


@dataclass
class AuthResult:
    ok: bool
    user: Optional[User] = None
    message: str = ""


class AuthManager:
    """Validates credentials against a local in-code user store."""

    def __init__(self) -> None:
        # Data structure (dict) + iteration used in validate()
        self._users = DEMO_USERS

    def validate(self, username: str, password: str) -> AuthResult:
        username = (username or "").strip()
        password = password or ""

        # Decision making
        if not username:
            return AuthResult(False, None, "Please enter a username.")

        # Iteration example (not necessary, but shows you can loop over store)
        for stored_username, meta in self._users.items():
            if stored_username == username:
                if meta.get("password") == password:
                    return AuthResult(True, User(username=username, role=meta.get("role", "farm_operator")), "")
                return AuthResult(False, None, "Incorrect password.")

        return AuthResult(False, None, "Unknown user.")
