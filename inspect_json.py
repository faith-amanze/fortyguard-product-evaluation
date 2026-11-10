import json

with open("heatmap_result.json", "r", encoding="utf-8") as file:
    result = json.load(file)

print("TOP-LEVEL KEYS:")
print(list(result.keys()))

print("\nCOMPLETE JSON STRUCTURE:")
print(json.dumps(result, indent=4)[:5000])