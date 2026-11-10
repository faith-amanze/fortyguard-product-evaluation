from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "results" / "data"
FIG_DIR = ROOT / "results" / "figures"
import json
import geopandas as gpd
import matplotlib.pyplot as plt

# Load the saved API response
with open(DATA_DIR / "heatmap_result.json", "r", encoding="utf-8") as file:
    result = json.load(file)

# Extract GeoJSON map data
map_data = result["data"]["result"]["map_data"]

# Convert GeoJSON into a GeoDataFrame
gdf = gpd.GeoDataFrame.from_features(
    map_data["features"],
    crs="EPSG:4326"
)

# Display temperature statistics
stats = result["data"]["result"]["stats_data"]["temperature_stats"]

print("\nTEMPERATURE STATISTICS")
print("----------------------")
print(f"Minimum: {stats['minimum']:.4f} °C")
print(f"Maximum: {stats['maximum']:.4f} °C")
print(f"Mean: {stats['mean']:.4f} °C")
print(f"Standard Deviation: {stats['standard_deviation']:.4f} °C")

# Create the heatmap
fig, ax = plt.subplots(figsize=(12, 9))

gdf.plot(
    column="average_temperature",
    cmap="turbo",
    legend=True,
    edgecolor="white",
    linewidth=0.1,
    ax=ax,
    legend_kwds={"label": "Temperature (°C)"}
)

ax.set_title("FortyGuard Temperature Heatmap - Colorado")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

plt.tight_layout()

# Save the map
plt.savefig(FIG_DIR / "fortyguard_heatmap.png", dpi=300)

print("\nHeatmap saved as fortyguard_heatmap.png")

plt.show()