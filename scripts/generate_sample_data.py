from __future__ import annotations

import argparse
import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd


def generate(rows: int, seed: int | None = 7) -> pd.DataFrame:
    if seed is not None:
        random.seed(seed)

    start = datetime.utcnow() - timedelta(minutes=rows)

    sites = ["Hoboken Pilot", "Brooklyn Lab", "Jersey Shore Farm"]
    tanks = [f"T{n:03d}" for n in range(1, 31)]
    species = ["tilapia", "salmon", "shrimp", "catfish"]

    data = []
    for i in range(rows):
        ts = start + timedelta(minutes=i)
        site = random.choice(sites)
        tank = random.choice(tanks)
        sp = random.choice(species)

        if sp == "salmon":
            temp_base = 12
            do_base = 9
        elif sp == "shrimp":
            temp_base = 28
            do_base = 6
        elif sp == "catfish":
            temp_base = 24
            do_base = 5.5
        else:
            temp_base = 26
            do_base = 6.5

        temperature_c = round(temp_base + random.gauss(0, 0.8), 2)
        dissolved_oxygen_mg_l = round(do_base + random.gauss(0, 0.5), 2)
        ph = round(7.2 + random.gauss(0, 0.15), 2)
        ammonia_mg_l = round(max(0, 0.15 + random.gauss(0, 0.05)), 3)
        feed_kg = round(max(0, random.gauss(1.5, 0.4)), 2)

        health = 100
        if dissolved_oxygen_mg_l < 5:
            health -= 25
        if ammonia_mg_l > 0.25:
            health -= 20
        if temperature_c > (temp_base + 2.5) or temperature_c < (temp_base - 2.5):
            health -= 10
        if ph < 6.8 or ph > 7.8:
            health -= 10
        health = max(0, min(100, health))

        estimated_fish_count = int(800 + random.gauss(0, 30))

        data.append(
            {
                "timestamp": ts.isoformat(timespec="seconds"),
                "site": site,
                "tank_id": tank,
                "species": sp,
                "temperature_c": temperature_c,
                "dissolved_oxygen_mg_l": dissolved_oxygen_mg_l,
                "ph": ph,
                "ammonia_mg_l": ammonia_mg_l,
                "feed_kg": feed_kg,
                "health_score": health,
                "estimated_fish_count": estimated_fish_count,
            }
        )

    return pd.DataFrame(data)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=12000)
    parser.add_argument("--out", type=str, default="data/sample_tank_readings.csv")
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()

    df = generate(args.rows, seed=args.seed)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)

    print(f"Wrote {len(df):,} rows to {out_path}")


if __name__ == "__main__":
    main()
