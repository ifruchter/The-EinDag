from __future__ import annotations

import math
import random
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .constants import DEFAULT_FISH_PER_ICON


@dataclass
class ChartSpec:
    title: str
    x_col: Optional[str] = None
    y_col: Optional[str] = None
    category_col: Optional[str] = None
    fish_per_icon: int = DEFAULT_FISH_PER_ICON


class ChartFactory(ABC):

    def __init__(self, df: pd.DataFrame, spec: ChartSpec) -> None:
        self.df = df
        self.spec = spec

    @abstractmethod
    def render(self) -> plt.Figure:
        raise NotImplementedError

    # Shared helper
    def _fish_text(self) -> str:
        return "🐟"


class FishLineChart(ChartFactory):

    def render(self) -> plt.Figure:
        x = self.df[self.spec.x_col] if self.spec.x_col else pd.RangeIndex(len(self.df))
        y = pd.to_numeric(self.df[self.spec.y_col], errors="coerce") if self.spec.y_col else None

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_title(self.spec.title)
        ax.grid(True)

        if y is None:
            ax.text(0.5, 0.5, "Pick a numeric Y column", ha="center", va="center")
            return fig

        n = len(y)
        step = max(1, n // 200)
        x_s = np.array(x)[::step]
        y_s = np.array(y)[::step]

        ax.plot(x_s, y_s)

        fish_every = max(1, len(x_s) // 25)
        for i in range(0, len(x_s), fish_every):
            ax.text(x_s[i], y_s[i], self._fish_text(), fontsize=10, ha="center", va="center")

        ax.set_xlabel(self.spec.x_col or "index")
        ax.set_ylabel(self.spec.y_col or "value")
        fig.tight_layout()
        return fig


class FishBarChart(ChartFactory):

    def render(self) -> plt.Figure:
        cat = self.spec.category_col
        y_col = self.spec.y_col

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_title(self.spec.title)
        ax.grid(axis="y")

        if not cat or not y_col:
            ax.text(0.5, 0.5, "Pick a category and numeric column", ha="center", va="center")
            return fig

        grouped = self.df.groupby(cat)[y_col].sum(numeric_only=True).sort_values(ascending=False).head(12)
        labels = list(map(str, grouped.index))
        vals = grouped.values.astype(float)

        ax.bar(labels, vals)
        ax.tick_params(axis='x', rotation=45)

        # Decorate top of each bar with fish icons proportional to bar height
        max_val = float(np.nanmax(vals)) if len(vals) else 1.0
        for i, v in enumerate(vals):
            # Decide fish count; cap for readability
            fish_count = int(round((v / max_val) * 25))
            fish_count = min(25, max(1, fish_count))
            for f in range(fish_count):
                ax.text(i, (v * (f + 1) / (fish_count + 1)), self._fish_text(), ha="center", va="center", fontsize=8)

        fig.tight_layout()
        return fig


class FishPieChart(ChartFactory):

    def render(self) -> plt.Figure:
        cat = self.spec.category_col
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_title(self.spec.title)

        if not cat:
            ax.text(0.5, 0.5, "Pick a category column", ha="center", va="center")
            return fig

        counts = self.df[cat].astype(str).value_counts().head(8)
        labels = counts.index.tolist()
        values = counts.values.astype(float)

        wedges, _ = ax.pie(values, labels=labels, startangle=90)
        ax.axis('equal')

        total = float(values.sum()) if values.sum() else 1.0

        # Place fish icons in each wedge; 1 fish = fish_per_icon individuals (visual metaphor)
        # This is not an animation, but it clearly 'incorporates' the fish theme.
        for wedge, v in zip(wedges, values):
            # fish icons proportional to slice size; cap for readability
            fish_icons = int(round((v / total) * 40))
            fish_icons = min(40, max(1, fish_icons))

            theta1, theta2 = wedge.theta1, wedge.theta2
            for _ in range(fish_icons):
                # random angle within wedge
                ang = math.radians(random.uniform(theta1, theta2))
                r = random.uniform(0.2, 0.8)
                x = r * math.cos(ang)
                y = r * math.sin(ang)
                ax.text(x, y, self._fish_text(), ha="center", va="center", fontsize=9)

        fig.tight_layout()
        return fig
