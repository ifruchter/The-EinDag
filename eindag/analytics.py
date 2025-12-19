"""Lightweight analytics for CSV uploads.

This is intentionally simple so it can be built on later.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd

from .models import CSVDataSet


def describe_dataset(df: pd.DataFrame, filename: str, saved_path: str, preview_n: int = 10) -> CSVDataSet:
    columns = [str(c) for c in df.columns]
    n_rows = int(len(df))

    # Identify numeric columns
    numeric_cols: List[str] = []
    for c in df.columns:
        # decision: treat ints/floats as numeric
        if pd.api.types.is_numeric_dtype(df[c]):
            numeric_cols.append(str(c))

    preview = df.head(preview_n).fillna("").to_dict(orient="records")

    return CSVDataSet(
        filename=filename,
        saved_path=saved_path,
        columns=columns,
        n_rows=n_rows,
        preview_rows=preview,
        numeric_columns=numeric_cols,
        errors=[],
    )


def compute_basic_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """Return a JSON-serializable summary (and write it to disk elsewhere)."""
    summary: Dict[str, Any] = {
        "rows": int(len(df)),
        "columns": [str(c) for c in df.columns],
        "numeric_summary": {},
    }

    for c in df.columns:
        if pd.api.types.is_numeric_dtype(df[c]):
            s = pd.to_numeric(df[c], errors="coerce")
            summary["numeric_summary"][str(c)] = {
                "min": float(np.nanmin(s)) if np.isfinite(np.nanmin(s)) else None,
                "max": float(np.nanmax(s)) if np.isfinite(np.nanmax(s)) else None,
                "mean": float(np.nanmean(s)) if np.isfinite(np.nanmean(s)) else None,
                "median": float(np.nanmedian(s)) if np.isfinite(np.nanmedian(s)) else None,
                "std": float(np.nanstd(s)) if np.isfinite(np.nanstd(s)) else None,
            }

    return summary


def bucketize_counts(series: pd.Series, max_buckets: int = 8) -> List[Dict[str, Any]]:
    """Turn a column into top-k category counts for a pie/bar chart."""
    s = series.astype(str).fillna("")
    counts = s.value_counts().head(max_buckets)
    rows: List[Dict[str, Any]] = []
    for k, v in counts.items():
        rows.append({"category": str(k), "count": int(v)})
    return rows
