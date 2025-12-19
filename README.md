# The EinDag (MVP)

A small **aquaculture CSV-to-insights** website (runs locally via Streamlit) with:
- **Login page**
- **Drag-and-drop CSV upload**
- **charts** (line, pie, bar)
- **File I/O**: uploaded CSVs are saved; summary outputs are written to disk

## How to extend later (easy MVP -> bigger product)

Common next steps:
- Replace demo login with real auth (hashed passwords, DB)
- Add multiple-upload “projects” per user
- Add domain-specific analytics (mortality events, FCR, DO/temp alarms)
- Add a proper frontend (React) while keeping the same `eindag` Python library
