from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import altair as alt
import pandas as pd


@dataclass
class ChartSpec:
    title: str
    x_col: Optional[str] = None
    y_col: Optional[str] = None
    category_col: Optional[str] = None


def line_chart(df: pd.DataFrame, spec: ChartSpec) -> alt.Chart:
    x = spec.x_col
    y = spec.y_col
    if not x or not y:
        return alt.Chart(pd.DataFrame({"msg": ["Pick X and Y"]})).mark_text().encode(text="msg")

    base = alt.Chart(df).properties(title=spec.title)

    line = base.mark_line().encode(
        x=alt.X(x, title=x),
        y=alt.Y(y, title=y),
        tooltip=[alt.Tooltip(x, title=x), alt.Tooltip(y, title=y)],
    )

    points = base.mark_point().encode(
        x=x,
        y=y,
        tooltip=[alt.Tooltip(x, title=x), alt.Tooltip(y, title=y)],
    )

    return (line + points).interactive()


def pie_chart_counts(df: pd.DataFrame, spec: ChartSpec) -> alt.Chart:
    cat = spec.category_col
    if not cat:
        return alt.Chart(pd.DataFrame({"msg": ["Pick a category column"]})).mark_text().encode(text="msg")

    counts = df[cat].astype(str).value_counts().reset_index()
    counts.columns = [cat, "count"]

    chart = alt.Chart(counts).properties(title=spec.title).mark_arc().encode(
        theta=alt.Theta("count:Q"),
        color=alt.Color(f"{cat}:N", title=cat),
        tooltip=[alt.Tooltip(f"{cat}:N", title=cat), alt.Tooltip("count:Q", title="Count")],
    )

    return chart


def bar_chart_sum_by_category(df: pd.DataFrame, spec: ChartSpec) -> alt.Chart:
    cat = spec.category_col
    y = spec.y_col
    if not cat or not y:
        return alt.Chart(pd.DataFrame({"msg": ["Pick a category and numeric column"]})).mark_text().encode(text="msg")

    tmp = df.copy()
    tmp[cat] = tmp[cat].astype(str)

    agg = tmp.groupby(cat, as_index=False)[y].sum()
    agg = agg.sort_values(y, ascending=False).head(12)

    chart = alt.Chart(agg).properties(title=spec.title).mark_bar().encode(
        x=alt.X(f"{cat}:N", sort="-y", title=cat),
        y=alt.Y(f"{y}:Q", title=y),
        tooltip=[alt.Tooltip(f"{cat}:N", title=cat), alt.Tooltip(f"{y}:Q", title=f"Sum({y})")],
    )

    return chart
