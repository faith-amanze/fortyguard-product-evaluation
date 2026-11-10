
import json
from collections import Counter

with open("persistence_result.json", "r", encoding="utf-8") as file:
    response = json.load(file)

# Locate the analysis result
def find_result(obj):
    if isinstance(obj, dict):
        if "map_data" in obj and "stats_data" in obj:
            return obj
        for value in obj.values():
            found = find_result(value)
            if found:
                return found
    elif isinstance(obj, list):
        for item in obj:
            found = find_result(item)
            if found:
                return found
    return None

result = find_result(response)

if not result:
    print("Could not locate map_data and stats_data.")
    raise SystemExit(1)

map_data = result["map_data"]
stats_data = result["stats_data"]

features = map_data.get("features", [])

values = [
    feature.get("properties", {}).get("value")
    for feature in features
    if feature.get("properties", {}).get("value") is not None
]

print("\nPERSISTENCE RESULT SUMMARY")
print("--------------------------")
print("Total tiles:", len(features))
print("Tiles with values:", len(values))

print("\nVALUE FREQUENCY")
for value, count in sorted(Counter(values).items()):
    print(f"{value}: {count} tiles")

print("\nSTATISTICS")
print(json.dumps(stats_data, indent=4))

print("\nINSPECTION COMPLETE")
