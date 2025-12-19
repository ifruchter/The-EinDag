import os
from pathlib import Path
import altair as alt
from eindag.charts_interactive import ChartSpec as IChartSpec, line_chart, pie_chart_counts, bar_chart_sum_by_category

import streamlit as st
import pandas as pd

PRETTY_COLUMNS = {
    "timestamp": "Timestamp",
    "site": "Site",
    "tank_id": "Tank ID",
    "species": "Species",
    "temperature_c": "Temperature (°C)",
    "dissolved_oxygen_mg_l": "Dissolved Oxygen (mg/L)",
    "ph": "pH",
    "ammonia_mg_l": "Ammonia (mg/L)",
    "feed_kg": "Feed Amount (kg)",
    "health_score": "Health Score",
    "estimated_fish_count": "Estimated Fish Count",
}


def pretty(col: str) -> str:
    """Return a human-friendly label for a column name."""
    return PRETTY_COLUMNS.get(col, col.replace("_", " ").title())

from eindag import (
    APP_NAME,
    TAGLINE,
    AuthManager,
    save_upload,
    read_csv_any,
    describe_dataset,
    compute_basic_metrics,
    write_json,
    write_csv,
    ChartSpec,
    FishLineChart,
    FishPieChart,
    FishBarChart,
)


REPO_ROOT = str(Path(__file__).resolve().parent)


def init_state():
    st.session_state.setdefault("auth", {"logged_in": False, "user": None})
    st.session_state.setdefault("last_upload", None)


def render_header():
    st.markdown(f"# {APP_NAME}")
    st.caption(TAGLINE)


def login_view():
    render_header()
    st.markdown("### Login")
    st.info("Demo credentials: **operator / fish** or **prof / eindag**")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Log in", use_container_width=True):
        auth = AuthManager()
        result = auth.validate(username, password)
        if result.ok:
            st.session_state["auth"] = {"logged_in": True, "user": result.user}
            st.success(f"Welcome, {result.user.username}!")
            st.rerun()
        else:
            st.error(result.message)


def logout_button():
    if st.button("Log out"):
        st.session_state["auth"] = {"logged_in": False, "user": None}
        st.session_state["last_upload"] = None
        st.rerun()


def home_view():
    render_header()
    user = st.session_state["auth"]["user"]
    st.write(f"Logged in as **{user.username}** ({user.role}).")
    logout_button()

    st.markdown("---")
    st.markdown("### Upload tank CSV")
    st.caption("Drag and drop a CSV. We'll save it to disk, parse it, and generate a themed chart + output files.")

    uploaded = st.file_uploader("CSV file", type=["csv"], accept_multiple_files=False)

    if uploaded is None:
        st.markdown("#### Need sample data?")
        st.caption("Run: `python scripts/generate_sample_data.py --rows 12000 --out data/sample_tank_readings.csv`")
        return

    rel_path = save_upload(REPO_ROOT, uploaded.name, uploaded.getvalue())
    df = read_csv_any(REPO_ROOT, rel_path)

    ds = describe_dataset(df, filename=uploaded.name, saved_path=rel_path)
    st.session_state["last_upload"] = ds

    st.success(f"Saved upload to `{rel_path}`")

    st.markdown("### Quick preview")
    st.write(f"Rows: **{ds.n_rows}** | Columns: **{len(ds.columns)}**")
    st.dataframe(pd.DataFrame(ds.preview_rows), use_container_width=True)

    st.markdown("---")
    st.markdown("### Create a chart")

    chart_type = st.selectbox("Chart type", ["Fish Line", "Fish Pie (category counts)", "Fish Bar (sum by category)"])

    if chart_type == "Fish Line":
        x_col = st.selectbox("X column", ds.columns, index=0)
        y_options = ds.numeric_columns if ds.numeric_columns else ds.columns
        y_col = st.selectbox("Y column (numeric)", y_options, index=0)
        spec = IChartSpec(
            title=f"{pretty(y_col)} over {pretty(x_col)}",
            x_col=x_col,
            y_col=y_col,
        )

        chart = line_chart(df, spec)

        chart = chart.encode(
            x=alt.X(x_col, title=pretty(x_col)),
            y=alt.Y(y_col, title=pretty(y_col)),
            tooltip=[
                alt.Tooltip(x_col, title=pretty(x_col)),
                alt.Tooltip(y_col, title=pretty(y_col)),
            ],
        )

        st.altair_chart(chart, use_container_width=True)



    elif chart_type == "Fish Pie (category counts)":
        cat_col = st.selectbox("Category column", ds.columns, index=0)
        spec = IChartSpec(
        title=f"Distribution of {pretty(cat_col)}",
        category_col=cat_col,
        )

        chart = pie_chart_counts(df, spec).encode(
            color=alt.Color(f"{cat_col}:N", title=pretty(cat_col)),
            tooltip=[
                alt.Tooltip(f"{cat_col}:N", title=pretty(cat_col)),
                alt.Tooltip("count:Q", title="Count"),
            ],
        )

        st.altair_chart(chart, use_container_width=True)

    else:
        cat_col = st.selectbox("Category column", ds.columns, index=0)
        y_options = ds.numeric_columns if ds.numeric_columns else ds.columns
        y_col = st.selectbox("Numeric column to sum", y_options, index=0)
        spec = IChartSpec(
            title=f"Total {pretty(y_col)} by {pretty(cat_col)}",
            category_col=cat_col,
            y_col=y_col,
        )

        chart = bar_chart_sum_by_category(df, spec).encode(
            x=alt.X(f"{cat_col}:N", title=pretty(cat_col), sort="-y"),
            y=alt.Y(f"{y_col}:Q", title=f"Total {pretty(y_col)}"),
            tooltip=[
                alt.Tooltip(f"{cat_col}:N", title=pretty(cat_col)),
                alt.Tooltip(f"{y_col}:Q", title=f"Total {pretty(y_col)}"),
            ],
        )

        st.altair_chart(chart, use_container_width=True)

    st.markdown("---")
    st.markdown("### Output files (rubric: file I/O)")

    metrics = compute_basic_metrics(df)
    json_rel = write_json(REPO_ROOT, "last_summary.json", metrics)

    rows = []
    for col, stats in metrics.get("numeric_summary", {}).items():
        rows.append({"column": col, **stats})
    csv_rel = write_csv(REPO_ROOT, "numeric_summary.csv", rows)

    st.write("Wrote:")
    st.code(json_rel)
    st.code(csv_rel)

    json_abs = os.path.join(REPO_ROOT, json_rel)
    csv_abs = os.path.join(REPO_ROOT, csv_rel)

    with open(json_abs, "rb") as f:
        st.download_button("Download JSON summary", f, file_name="eindag_summary.json", use_container_width=True)
    with open(csv_abs, "rb") as f:
        st.download_button("Download CSV summary", f, file_name="eindag_numeric_summary.csv", use_container_width=True)


def main():
    st.set_page_config(page_title=APP_NAME, page_icon="🐟", layout="wide")
    init_state()

    if not st.session_state["auth"]["logged_in"]:
        login_view()
    else:
        home_view()


if __name__ == "__main__":
    main()
