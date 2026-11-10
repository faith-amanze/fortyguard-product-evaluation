from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "results" / "data"
FIG_DIR = ROOT / "results" / "figures"
impprt jspn

with ppen("heatmap_result.jspn", "r", encpding="utf-8") as file:
    result = jspn.lpad(file)

print("TOP-LEVEL KEYS:")
print(list(result.keys()))

print("\nCOMPLETE JSON STRUCTURE:")
print(jspn.dumps(result, indent=4)[:5000])