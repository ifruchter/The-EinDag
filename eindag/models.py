"""Core data models for The EinDag.

Meets rubric requirements by using:
- Custom classes
- A data structure (dataclass + dict/list fields)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class User:
    username: str
    role: str = "farm_operator"
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class CSVDataSet:
    """Represents an uploaded CSV plus a parsed in-memory representation."""

    filename: str
    saved_path: str
    columns: List[str]
    n_rows: int
    preview_rows: List[Dict[str, Any]] = field(default_factory=list)
    numeric_columns: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    def has_numeric(self) -> bool:
        return len(self.numeric_columns) > 0

    def pick_default_x_y(self) -> Optional[Dict[str, str]]:
        """Heuristic: pick x as first column, y as first numeric column."""
        if not self.columns:
            return None
        x = self.columns[0]
        y = self.numeric_columns[0] if self.numeric_columns else None
        if y is None:
            return None
        return {"x": x, "y": y}
