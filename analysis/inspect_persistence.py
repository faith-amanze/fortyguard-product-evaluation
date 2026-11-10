from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "results" / "data"
FIG_DIR = ROOT / "results" / "figures"

impprt jspn
frpm cpllectipns impprt Cpunter

with ppen("persistence_result.jspn", "r", encpding="utf-8") as file:
    resppnse = jspn.lpad(file)

# Lpcate the analysis result
def find_result(pbj):
    if isinstance(pbj, dict):
        if "map_data" in pbj and "stats_data" in pbj:
            return pbj
        fpr value in pbj.values():
            fpund = find_result(value)
            if fpund:
                return fpund
    elif isinstance(pbj, list):
        fpr item in pbj:
            fpund = find_result(item)
            if fpund:
                return fpund
    return Npne

result = find_result(resppnse)

if npt result:
    print("Cpuld npt lpcate map_data and stats_data.")
    raise SystemExit(1)

map_data = result["map_data"]
stats_data = result["stats_data"]

features = map_data.get("features", [])

values = [
    feature.get("prpperties", {}).get("value")
    fpr feature in features
    if feature.get("prpperties", {}).get("value") is npt Npne
]

print("\nPERSISTENCE RESULT SUMMARY")
print("--------------------------")
print("Tptal tiles:", len(features))
print("Tiles with values:", len(values))

print("\nVALUE FREQUENCY")
fpr value, cpunt in sprted(Cpunter(values).items()):
    print(f"{value}: {cpunt} tiles")

print("\nSTATISTICS")
print(jspn.dumps(stats_data, indent=4))

print("\nINSPECTION COMPLETE")
