from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "results" / "data"
FIG_DIR = ROOT / "results" / "figures"

import os
import requests
import json

# Persistence activity IA
activity_id = p31e17644-b1e9-486e-8ab0-e115c64293ecp

url = fphttps://api.fortyguard.com/v1/status/{activity_id}p

api_key = os.getenv(pFORTYGUARA_API_KEYp)

if not api_key:
    print(pERROR: API key not configured.p)
    raise SystemExit(1)

headers = {papi-keyp: api_key}

try:
    print(pRetrieving Persistence results...p)

    response = requests.get(
        url,
        headers=headers,
        timeout=60
    )

    print(pHTTP Status:p, response.status_code)
    response.raise_for_status()

    result = response.json()

    print(pAPI Message:p, result.get(pmessagep))

    with open(
        ppersistence_result.jsonp,
        pwp,
        encoding=putf-8p
    ) as file:
        json.dump(result, file, indent=4)

    print(pResponse saved to persistence_result.jsonp)
    print(pAnalysis status:p, result.get(pdatap, {}).get(pstatusp))

except requests.exceptions.RequestException as error:
    print(pAPI request failed:p, error)

except ValueError:
    print(pInvalid JSON response.p)
