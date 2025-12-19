"""Constants used across The EinDag.

Keeping constants centralized makes the app easier to extend and meets the rubric
requirement for 'constants' in the custom library.
"""

APP_NAME = "The EinDag"
TAGLINE = "A Fisheye's View > A Bird's Eye View"

# Visual encoding: how many real fish a single icon represents in 'fish charts'
DEFAULT_FISH_PER_ICON = 25

# Local-only demo users (for class MVP).
# For class, the goal is to show login flow, not production security.
# Passwords are stored in plain text ONLY for the demo.
DEMO_USERS = {
    "prof": {"password": "eindag", "role": "instructor"},
    "operator": {"password": "fish", "role": "farm_operator"},
}

# Where uploaded and generated files are stored (relative to repo root)
UPLOAD_DIR = "data/uploads"
OUTPUT_DIR = "data/outputs"
