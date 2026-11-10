
import json
from collections import Counter

with open("exceedance_result.json", "r", encoding="utf-8") as file:
    result = json.load(file)

analysis = result.get("data", {}).get("result", {})

print("EXCEEDANCE RESULT SUMMARY")
print("-------------------------")

print("Top-level result keys:", list(analysis.keys()))

# Inspect map tiles
map_data = analysis.get("map_data", {})
features = map_data.get("features", [])

values = [
    feature.get("properties", {}).get("value")
    for feature in features
]

print("\nTILE SUMMARY")
print("Total tiles:", len(features))
print("Tiles with values:", sum(v is not None for v in values))
print("Unique values:", sorted(set(v for v in values if v is not None)))

print("\nVALUE FREQUENCY")
for value, count in sorted(Counter(v for v in values if v is not None).items()):
    print(f"{value}: {count} tiles")

# Inspect statistics
stats = analysis.get("stats_data", {})

print("\nSTATISTICS")
print(json.dumps(stats, indent=4)[:5000])
