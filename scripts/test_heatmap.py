
import os
import requests
import json

submit_url = "https://api.fortyguard.com/v1/heatmap"

api_key = os.getenv("FORTYGUARD_API_KEY")

if not api_key:
    print("ERROR: API key not configured.")
    raise SystemExit(1)

headers = {
    "api-key": api_key,
    "Content-Type": "application/json"
}

payload = {
    "polygon_aoi": {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-105.012833, 39.785168],
                        [-105.002833, 39.785168],
                        [-105.002833, 39.795168],
                        [-105.012833, 39.795168],
                        [-105.012833, 39.785168]
                    ]]
                }
            }
        ]
    },
    "date_time": {
        "start_date": "2024-07-15",
        "start_time": "14:00",
        "end_time": "16:00",
        "filter_type": 2
    },
    "granularity": 100,
    "analytic_type": "persistence",
    "threshold": 30,
    "direction": "above"
}

try:
    print("Submitting Persistence request...")

    response = requests.post(
        submit_url,
        headers=headers,
        json=payload,
        timeout=60
    )

    print("\n--- API RESPONSE ---")
    print("HTTP Status:", response.status_code)

    try:
        result = response.json()
        print(json.dumps(result, indent=4))

        if response.ok:
            activity_id = result.get("data", {}).get("activity_id")

            if activity_id:
                print("\nSUCCESS!")
                print("Activity ID:", activity_id)
                print("Persistence request submitted.")
            else:
                print("\nNo Activity ID returned.")
        else:
            print("\nAPI request failed.")

    except ValueError:
        print("Response was not valid JSON.")
        print("Response body:", response.text[:2000])

except requests.exceptions.RequestException as error:
    print("API request error:", error)
