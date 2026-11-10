from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "results" / "data"
FIG_DIR = ROOT / "results" / "figures"
import json

files = [
    DATA_DIR / "time_of_measure_result.json",
    DATA_DIR / "time_of_measure_result_2.json"
]

for filename in files:
    print("\n" + "=" * 45)
    print("FILE:", filename)
    print("=" * 45)

    with open(filename, "r", encoding="utf-8") as file:
        result = json.load(file)

    analysis = result.get("data", {}).get("result", {})
    stats = analysis.get("stats_data", {})
    features = analysis.get("map_data", {}).get("features", [])

    print("Status:", result.get("message"))
    print("Analytic type:", stats.get("analytic_type"))
    print("Units:", stats.get("units"))
    print("Tiles:", len(features))
    print("UTC window:", stats.get("window_utc"))
    print("Hour counts UTC:", stats.get("hour_counts_utc"))