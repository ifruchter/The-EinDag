# The EinDag (MVP)

A small **aquaculture CSV-to-insights** website (runs locally via Streamlit) with:
- **Login page**
- **Drag-and-drop CSV upload**
- **Fish-themed charts** (line, pie, bar)
- **File I/O**: uploaded CSVs are saved; summary outputs are written to disk

> Demo credentials: `operator / fish` or `prof / eindag`

## Quick start (for you + your professor)

### 1) Clone or download

- Clone:
  ```bash
  git clone <YOUR_GITHUB_REPO_URL>
  cd eindag-mvp
  ```

### 2) Create a virtual environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Mac/Linux (bash/zsh):**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies
```bash
pip install -r requirements.txt
```

### 4) (Optional) Generate a 10,000+ row sample CSV
```bash
python scripts/generate_sample_data.py --rows 12000 --out data/sample_tank_readings.csv
```

### 5) Run the website
```bash
streamlit run app.py
```

Streamlit will print a local URL (usually http://localhost:8501).

---

## Where files go (rubric: file I/O)

- Uploads are saved to `data/uploads/`
- Output summaries are written to `data/outputs/`:
  - `last_summary.json`
  - `numeric_summary.csv`

---

## Rubric checklist mapping

This project intentionally includes the items listed on the assignment sheet:

- **Custom library** with **classes, functions, constants**: `eindag/`
- **Imports** from custom library and standard library: `app.py` imports `eindag`, plus `os`, `pathlib`, etc.
- **Iteration + decision making**: in `scripts/generate_sample_data.py`, `eindag/auth.py`, `eindag/analytics.py`
- **Third party libraries**: Streamlit, pandas, numpy, matplotlib (in `requirements.txt`)
- **File I/O**: upload saves CSV; outputs write JSON/CSV (see `eindag/io_utils.py`)
- **Data structure**: dataclasses + dict/list usage (see `eindag/models.py`, `eindag/auth.py`)
- **Object oriented + inheritance**: `ChartFactory` base class and subclasses in `eindag/charts.py`
- **Data size (10k+)**: generator script creates 12k rows by default

---

## How to extend later (easy MVP -> bigger product)

Common next steps:
- Replace demo login with real auth (hashed passwords, DB)
- Add multiple-upload “projects” per user
- Add domain-specific analytics (mortality events, FCR, DO/temp alarms)
- Add a proper frontend (React) while keeping the same `eindag` Python library
