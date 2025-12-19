"""File I/O helpers.

Rubric:
- Must read input from a file and produce an output file.

This module saves uploaded CSVs and writes summary outputs (JSON/CSV).
"""

from __future__ import annotations

import csv
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

import pandas as pd

from .constants import OUTPUT_DIR, UPLOAD_DIR


def ensure_dirs(repo_root: str) -> None:
    Path(repo_root, UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
    Path(repo_root, OUTPUT_DIR).mkdir(parents=True, exist_ok=True)


def save_upload(repo_root: str, filename: str, bytes_data: bytes) -> str:
    """Saves uploaded bytes to data/uploads and returns the relative path."""
    ensure_dirs(repo_root)
    safe_name = filename.replace("..", "_").replace("/", "_").replace("\\", "_")
    stamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    rel_path = os.path.join(UPLOAD_DIR, f"{stamp}__{safe_name}")
    abs_path = os.path.join(repo_root, rel_path)
    with open(abs_path, "wb") as f:
        f.write(bytes_data)
    return rel_path


def read_csv_any(repo_root: str, rel_path: str) -> pd.DataFrame:
    """Read a CSV regardless of delimiter quirks."""
    abs_path = os.path.join(repo_root, rel_path)
    # pandas handles most; if it fails, try python csv sniffer
    try:
        return pd.read_csv(abs_path)
    except Exception:
        with open(abs_path, "r", newline="", encoding="utf-8") as f:
            sample = f.read(2048)
            f.seek(0)
            dialect = csv.Sniffer().sniff(sample)
            return pd.read_csv(f, sep=dialect.delimiter)


def write_json(repo_root: str, name: str, payload: Dict[str, Any]) -> str:
    ensure_dirs(repo_root)
    rel_path = os.path.join(OUTPUT_DIR, name)
    abs_path = os.path.join(repo_root, rel_path)
    with open(abs_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, default=str)
    return rel_path


def write_csv(repo_root: str, name: str, rows: List[Dict[str, Any]]) -> str:
    ensure_dirs(repo_root)
    rel_path = os.path.join(OUTPUT_DIR, name)
    abs_path = os.path.join(repo_root, rel_path)
    if not rows:
        with open(abs_path, "w", encoding="utf-8") as f:
            f.write("")
        return rel_path
    fieldnames = list(rows[0].keys())
    with open(abs_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return rel_path
