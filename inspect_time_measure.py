
import json
from collections import Counter

with open("time_of_measure_result.json", "r", encoding="utf-8") as file:
    result = json.load(file)

analysis = result["data"]["result"]

# Inspect map tiles
features = analysis["map_data"]["features"]
values = [
    feature.get("properties", {}).get("value")
    for feature in features
]

print("TIME OF MEASURE SUMMARY")
print("-----------------------")
print("Total tiles:", len(features))
print("Tiles with values:", sum(v is not None for v in values))
print("Unique values:", sorted(set(v for v in values if v is not None)))

print("\nVALUE FREQUENCY")
for value, count in Counter(values).most_common():
    print(f"{value}: {count} tiles")

# Inspect statistics
stats = analysis.get("stats_data", {})

print("\nSTATISTICS KEYS")
print(list(stats.keys()))

print("\nSTATISTICS CONTENT")
print(json.dumps(stats, indent=4)[:4000])
