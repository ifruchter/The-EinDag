import os
from pathlib import Path

import streamlit as st
import pandas as pd

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

    # Preview
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
        spec = ChartSpec(title=f"{uploaded.name} — {y_col} over {x_col}", x_col=x_col, y_col=y_col)
        fig = FishLineChart(df, spec).render()
        st.pyplot(fig, use_container_width=True)

    elif chart_type == "Fish Pie (category counts)":
        cat_col = st.selectbox("Category column", ds.columns, index=0)
        spec = ChartSpec(title=f"{uploaded.name} — Distribution of {cat_col}", category_col=cat_col)
        fig = FishPieChart(df, spec).render()
        st.pyplot(fig, use_container_width=True)

    else:
        cat_col = st.selectbox("Category column", ds.columns, index=0)
        y_options = ds.numeric_columns if ds.numeric_columns else ds.columns
        y_col = st.selectbox("Numeric column to sum", y_options, index=0)
        spec = ChartSpec(title=f"{uploaded.name} — Sum({y_col}) by {cat_col}", category_col=cat_col, y_col=y_col)
        fig = FishBarChart(df, spec).render()
        st.pyplot(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("### Output files (rubric: file I/O)")

    metrics = compute_basic_metrics(df)
    json_rel = write_json(REPO_ROOT, "last_summary.json", metrics)

    # Also write a tidy CSV of numeric summaries for convenience
    rows = []
    for col, stats in metrics.get("numeric_summary", {}).items():
        rows.append({"column": col, **stats})
    csv_rel = write_csv(REPO_ROOT, "numeric_summary.csv", rows)

    st.write("Wrote:")
    st.code(json_rel)
    st.code(csv_rel)

    # Download buttons
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
