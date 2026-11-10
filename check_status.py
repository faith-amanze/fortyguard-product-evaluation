
import os
import requests
import json

# Persistence activity ID
activity_id = "31e17644-b1e9-486e-8ab0-e115c64293ec"

url = f"https://api.fortyguard.com/v1/status/{activity_id}"

api_key = os.getenv("FORTYGUARD_API_KEY")

if not api_key:
    print("ERROR: API key not configured.")
    raise SystemExit(1)

headers = {"api-key": api_key}

try:
    print("Retrieving Persistence results...")

    response = requests.get(
        url,
        headers=headers,
        timeout=60
    )

    print("HTTP Status:", response.status_code)
    response.raise_for_status()

    result = response.json()

    print("API Message:", result.get("message"))

    with open(
        "persistence_result.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(result, file, indent=4)

    print("Response saved to persistence_result.json")
    print("Analysis status:", result.get("data", {}).get("status"))

except requests.exceptions.RequestException as error:
    print("API request failed:", error)

except ValueError:
    print("Invalid JSON response.")
