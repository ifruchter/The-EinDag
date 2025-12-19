"""The EinDag - aquaculture CSV-to-insights MVP.

This is the project's custom library.
"""

from .constants import APP_NAME, TAGLINE, DEFAULT_FISH_PER_ICON, DEMO_USERS, UPLOAD_DIR, OUTPUT_DIR
from .models import User, CSVDataSet
from .auth import AuthManager, AuthResult
from .io_utils import ensure_dirs, save_upload, read_csv_any, write_json, write_csv
from .analytics import describe_dataset, compute_basic_metrics, bucketize_counts
from .charts import ChartFactory, ChartSpec, FishPieChart, FishLineChart, FishBarChart

__all__ = [
    "APP_NAME",
    "TAGLINE",
    "DEFAULT_FISH_PER_ICON",
    "DEMO_USERS",
    "UPLOAD_DIR",
    "OUTPUT_DIR",
    "User",
    "CSVDataSet",
    "AuthManager",
    "AuthResult",
    "ensure_dirs",
    "save_upload",
    "read_csv_any",
    "write_json",
    "write_csv",
    "describe_dataset",
    "compute_basic_metrics",
    "bucketize_counts",
    "ChartFactory",
    "ChartSpec",
    "FishPieChart",
    "FishLineChart",
    "FishBarChart",
]
